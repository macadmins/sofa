#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
POC: Scrape Apple "Identify your <Mac>" support pages into a minimized
dataset, then diff against the curated SOFA source-of-truth at
data/models/sources/macos_devices.json.

Stdlib only — designed to be ported to Rust (`reqwest` + `regex`) later.

Pages currently covered:
    https://support.apple.com/en-ca/108052   MacBook Pro
    https://support.apple.com/en-ca/108054   iMac

Run:
    ./scripts/scrape_apple_models.py
    ./scripts/scrape_apple_models.py --diff-only
    ./scripts/scrape_apple_models.py --url https://support.apple.com/en-ca/102869   # MacBook Air
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from dataclasses import asdict, dataclass, field
from html import unescape
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCES_FILE = REPO_ROOT / "data" / "models" / "sources" / "macos_devices.json"
OUT_DIR = REPO_ROOT / "data" / "models" / "scraped"

# (url, family) — family is what we attribute scraped models to.
# These are the canonical "Identify your <Mac>" support pages. The legacy
# HT* URLs (HT201300, HT201634, HT201862, HT201894, HT213073, HT202888) all
# redirect to these numeric URLs.
DEFAULT_PAGES: list[tuple[str, str]] = [
    ("https://support.apple.com/en-ca/108052", "MacBook Pro"),
    ("https://support.apple.com/en-ca/102869", "MacBook Air"),
    ("https://support.apple.com/en-ca/103257", "MacBook"),
    ("https://support.apple.com/en-ca/108054", "iMac"),
    ("https://support.apple.com/en-ca/102852", "Mac mini"),
    ("https://support.apple.com/en-ca/102231", "Mac Studio"),
    ("https://support.apple.com/en-ca/102887", "Mac Pro"),
]

# Identifiers in SOFA that are expected NOT to appear on Apple's hardware
# identification pages. These are not bugs.
VIRTUAL_ID_RE = re.compile(r"^(VMM-|VirtualMac\d+,\d+$|VMA2)")

# Apple identifiers that SOFA *intentionally* does not track even though they
# fall within the BigSur+ scope. SOFA tracks only the latest MacBook (12-inch)
# model (MacBook10,1, 2017); the 2015/2016 predecessors are out of scope.
INTENTIONAL_DROPS = {
    "MacBook8,1",
    "MacBook9,1",
}
# IPSW catalog file is consulted to recognize pre-announcement leaks where
# Apple has shipped a build for a device but hasn't updated the support page.
IPSW_FILE = REPO_ROOT / "data" / "resources" / "ipsw.json"

USER_AGENT = "Mozilla/5.0 (compatible; sofa-scrape-poc/0.1; +https://github.com/macadmins/sofa)"


# A model "block" on Apple's pages is an <h2> or <h3 class="gb-header">
# followed by <p class="gb-paragraph">[<b>]Field:[</b>] value</p> rows.
# Two markup variants exist:
#   1. Newer pages (108052/108054/etc.): <h2> per model, fields in <b>...</b>
#   2. 12-inch MacBook page (103257): <h3> per year, fields without <b>,
#      marketing name embedded in a "Tech Specs:" anchor
SECTION_SPLIT_RE = re.compile(r'<h[23]\s+class="gb-header"[^>]*>(.*?)</h[23]>', re.IGNORECASE | re.DOTALL)
# Field regex tolerates both `<b>Label:</b> value` and bare `Label: value`,
# and allows the value to contain inline tags (anchors, images).
FIELD_RE = re.compile(
    r'<p\s+class="gb-paragraph"[^>]*>\s*(?:<b>\s*)?([A-Za-z][A-Za-z\s]{2,40}?)\s*:\s*(?:</b>)?\s*(.*?)\s*</p>',
    re.IGNORECASE | re.DOTALL,
)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")
# A section header that is *just* a year means the marketing name lives in the
# body (e.g., 12-inch MacBook page, where each year-section has one model).
YEAR_ONLY_HEADER_RE = re.compile(r"^\s*(?:19|20)\d{2}\s*$")


@dataclass
class Model:
    model_identifier: str
    # Apple sometimes lists the same identifier under multiple <h2> sections
    # (e.g. iMac15,1 = both "Mid 2015" and "Late 2014"; MacBookPro15,2 = 2018
    # and 2019). We keep ALL marketing names plus a canonical primary.
    marketing_name: str
    aliases: list[str] = field(default_factory=list)
    family: str = ""
    year: str | None = None
    chip: str | None = None
    part_numbers: list[str] = field(default_factory=list)
    newest_compatible_os: str | None = None
    source_url: str = ""


def clean(text: str) -> str:
    """Strip tags, unescape entities, collapse whitespace."""
    return WS_RE.sub(" ", unescape(TAG_RE.sub("", text))).strip()


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_page(html: str, url: str, family: str) -> list[Model]:
    """Walk section → fields blocks. Each section may yield 1+ Model rows
    because Apple sometimes lists multiple identifiers on a single
    'Model Identifier:' row (e.g. 'Mac17,7, Mac17,9')."""
    models: list[Model] = []
    parts = SECTION_SPLIT_RE.split(html)
    # parts = [pre, header_1, body_1, header_2, body_2, ...]
    for i in range(1, len(parts), 2):
        section_header = clean(parts[i])
        body = parts[i + 1] if i + 1 < len(parts) else ""
        if not section_header:
            continue

        fields = {clean(k).lower(): clean(v) for k, v in FIELD_RE.findall(body)}
        ident_raw = fields.get("model identifier")
        if not ident_raw:
            continue  # header without identifier (intro, footer, "List of …")

        # Marketing name: section header normally; if the header is a bare
        # year, fall back to the "Tech Specs" anchor text.
        if YEAR_ONLY_HEADER_RE.match(section_header):
            marketing_name = fields.get("tech specs") or section_header
        else:
            marketing_name = section_header

        # Identifiers always look like `<Letters><digits>,<digits>`, e.g.
        # `Mac17,7` or `MacBookPro18,1`. Don't split on commas — IDs contain
        # commas. Match them whole.
        identifiers = re.findall(r"\b[A-Za-z]+\d+,\d+\b", ident_raw)
        if not identifiers:
            continue

        year_match = YEAR_RE.search(marketing_name)
        chip = fields.get("chip") or _chip_from_name(marketing_name)
        parts_list = [p.strip() for p in (fields.get("part numbers") or "").split(",") if p.strip()]
        newest_os = fields.get("newest compatible operating system")

        for ident in identifiers:
            models.append(Model(
                model_identifier=ident,
                marketing_name=marketing_name,
                family=family,
                year=year_match.group(0) if year_match else None,
                chip=chip,
                part_numbers=parts_list,
                newest_compatible_os=newest_os,
                source_url=url,
            ))
    return models


def _dedup_aggregating_aliases(models: list[Model]) -> list[Model]:
    """When Apple lists one identifier under multiple <h2> sections, keep the
    newest-year occurrence as `marketing_name` and stash the rest in `aliases`.
    Without this, the first or last parsed name silently wins."""
    by_id: dict[str, list[Model]] = {}
    for m in models:
        by_id.setdefault(m.model_identifier, []).append(m)
    out: list[Model] = []
    for ident, group in by_id.items():
        if len(group) == 1:
            out.append(group[0])
            continue
        # Sort newest year first; entries without a year sink to the bottom.
        group.sort(key=lambda m: int(m.year) if m.year else 0, reverse=True)
        primary = group[0]
        primary.aliases = [m.marketing_name for m in group[1:]]
        # Union part_numbers across all sections.
        seen_parts = set(primary.part_numbers)
        for m in group[1:]:
            for p in m.part_numbers:
                if p not in seen_parts:
                    primary.part_numbers.append(p)
                    seen_parts.add(p)
        out.append(primary)
    return out


def _chip_from_name(name: str) -> str | None:
    """Extract chip from marketing name like 'MacBook Pro (14-inch, M5)' or
    'MacBook Pro (16-inch, M5 Pro or M5 Max)'. Apple's older Intel pages don't
    surface chip in a parseable way; return None and let comparison handle it."""
    m = re.search(r"\b(M\d(?:\s+(?:Pro|Max|Ultra))?)\b", name)
    return m.group(1) if m else None


def write_minimized(models: list[Model], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {
            "source": "scrape:support.apple.com",
            "model_count": len(models),
        },
        "models": {m.model_identifier: asdict(m) for m in models},
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


SOFA_SYNTHETIC_SUFFIX_RE = re.compile(r"-(?:Rack)$")


def diff_against_sources(scraped: list[Model]) -> dict:
    """Compare scraped Apple data against curated SOFA sources file.

    Splits findings into actionable buckets:
    - only_in_apple_by_year: dict[year -> list[id]] (recent gaps = real bugs)
    - only_in_sofa: identifiers SOFA tracks that Apple's pages don't list
                    (excluding known SOFA conventions like '-Rack' suffix)
    - real_mismatches: year or screen-size disagree (real bugs)
    - granularity_mismatches: SOFA distinguishes chip variants Apple groups
                              under one h2 (mostly fine; informational)
    """
    if not SOURCES_FILE.exists():
        return {"error": f"sources file not found: {SOURCES_FILE}"}

    curated = json.loads(SOURCES_FILE.read_text())["devices"]
    scraped_by_id = {m.model_identifier: m for m in scraped}

    # Map SOFA's synthetic '-Rack' IDs back to their bare Apple identifier.
    def _strip_synthetic(ident: str) -> str:
        return SOFA_SYNTHETIC_SUFFIX_RE.sub("", ident)

    curated_to_apple = {ident: _strip_synthetic(ident) for ident in curated}
    apple_ids_covered = {curated_to_apple[i] for i in curated}

    only_apple = sorted(set(scraped_by_id) - apple_ids_covered - INTENTIONAL_DROPS)
    intentionally_dropped = sorted(set(scraped_by_id) & INTENTIONAL_DROPS)
    only_sofa_all = sorted(i for i, apple_i in curated_to_apple.items() if apple_i not in scraped_by_id)

    # Classify "SOFA-only" identifiers into expected / pre-release / unexplained.
    ipsw_ids = _load_ipsw_identifiers()
    only_sofa_virtual: list[str] = []
    only_sofa_pre_release: list[str] = []
    only_sofa = []
    for ident in only_sofa_all:
        if VIRTUAL_ID_RE.match(ident):
            only_sofa_virtual.append(ident)
        elif _strip_synthetic(ident) in ipsw_ids:
            only_sofa_pre_release.append(ident)
        else:
            only_sofa.append(ident)

    # Bucket "only_in_apple" by year — gaps post-2014 are real, pre-2014 is
    # legacy noise (SOFA tracks BigSur+).
    only_apple_by_year: dict[str, list[str]] = {}
    for ident in only_apple:
        m = scraped_by_id[ident]
        bucket = m.year or "unknown"
        only_apple_by_year.setdefault(bucket, []).append(ident)

    # Marketing-name comparison: real (year/inch) vs granularity (chip variant).
    real: list[dict] = []
    granularity: list[dict] = []
    year_re = re.compile(r"\b(?:19|20)\d{2}\b")
    inch_re = re.compile(r"\b\d{2}-inch\b")
    for ident, m in scraped_by_id.items():
        if ident not in curated:
            continue
        sofa_name = curated[ident].get("marketingName", "")
        candidates = [m.marketing_name, *m.aliases]
        # If SOFA's name normalizes-equals any apple variant, no mismatch.
        if any(_normalize_name(sofa_name) == _normalize_name(c) for c in candidates):
            continue

        sofa_year = (year_re.search(sofa_name) or [None])[0] if year_re.search(sofa_name) else None
        sofa_inch = (inch_re.search(sofa_name) or [None])[0] if inch_re.search(sofa_name) else None
        # Compare against ALL apple variants — disagreement only counts if
        # SOFA's year/inch matches none of them.
        apple_years = {y for c in candidates for y in year_re.findall(c)}
        apple_inches = {i for c in candidates for i in inch_re.findall(c)}

        record = {"id": ident, "apple": " | ".join(candidates), "sofa": sofa_name}
        if sofa_year and apple_years and sofa_year not in apple_years:
            record["kind"] = "year"
            real.append(record)
        elif sofa_inch and apple_inches and sofa_inch not in apple_inches:
            record["kind"] = "inch"
            real.append(record)
        else:
            granularity.append(record)

    return {
        "scraped_count": len(scraped_by_id),
        "curated_count": len(curated),
        "only_in_apple": only_apple,
        "only_in_apple_by_year": only_apple_by_year,
        "intentionally_dropped": intentionally_dropped,
        "only_in_sofa": only_sofa,
        "only_in_sofa_virtual": only_sofa_virtual,
        "only_in_sofa_pre_release": only_sofa_pre_release,
        "real_mismatches": real,
        "granularity_mismatches": granularity,
    }


def _load_ipsw_identifiers() -> set[str]:
    """Identifiers Apple has shipped IPSW builds for. Used to flag SOFA-only
    devices that are pre-announcement (Apple hasn't updated support pages yet)."""
    if not IPSW_FILE.exists():
        return set()
    try:
        data = json.loads(IPSW_FILE.read_text())
    except json.JSONDecodeError:
        return set()
    out: set[str] = set()
    # ipsw.json shape varies; walk it defensively for any "identifier" key.
    def walk(obj):
        if isinstance(obj, dict):
            ident = obj.get("identifier")
            if isinstance(ident, str):
                out.add(ident)
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)
    walk(data)
    return out


def _normalize_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def print_diff(diff: dict) -> None:
    if "error" in diff:
        print(f"⚠️  {diff['error']}")
        return

    print(f"\n=== Diff: scrape ({diff['scraped_count']}) vs curated sources ({diff['curated_count']}) ===")

    # Real mismatches first — these are the actionable bugs.
    real = diff["real_mismatches"]
    print(f"\n• REAL mismatches (year or screen-size disagree):     {len(real)}")
    for r in real:
        print(f"    ! [{r['kind']:4s}] {r['id']}")
        print(f"        apple: {r['apple']}")
        print(f"        sofa : {r['sofa']}")

    # SOFA has it, Apple doesn't.
    print(f"\n• In SOFA, NOT on any Apple page (UNEXPLAINED):       {len(diff['only_in_sofa'])}")
    for i in diff["only_in_sofa"]:
        print(f"    - {i}")
    if diff["only_in_sofa_pre_release"]:
        print(f"\n• In SOFA + IPSW catalog but not yet on support page: {len(diff['only_in_sofa_pre_release'])}")
        print(f"  (Apple has shipped builds for these but the customer-facing")
        print(f"   page lags — SOFA correctly tracks them ahead of marketing)")
        for i in diff["only_in_sofa_pre_release"]:
            print(f"    ⏳ {i}")
    if diff["only_in_sofa_virtual"]:
        print(f"\n• Virtual machine identifiers (expected SOFA-only):   {len(diff['only_in_sofa_virtual'])}")
        for i in diff["only_in_sofa_virtual"]:
            print(f"    💻 {i}")

    # Apple has it, SOFA doesn't — bucket by year to separate real gaps from
    # legacy noise (SOFA is a BigSur+ dataset).
    by_year = diff["only_in_apple_by_year"]
    print(f"\n• Only on Apple page (missing from SOFA):             {len(diff['only_in_apple'])}")
    for year in sorted(by_year, reverse=True):
        ids = by_year[year]
        if year >= "2015":
            print(f"    [{year}] ({len(ids)})")
            for i in ids:
                print(f"        + {i}")
        else:
            print(f"    [{year}] {len(ids)} legacy ids (pre-BigSur era)")

    # Granularity-only mismatches — informational.
    gran = diff["granularity_mismatches"]
    print(f"\n• Granularity-only mismatches (SOFA more specific):   {len(gran)}")
    print(f"  (Apple groups chip variants under one <h2>; SOFA tracks them per-id)")

    if diff["intentionally_dropped"]:
        print(f"\n• Intentionally not tracked by SOFA:                  {len(diff['intentionally_dropped'])}")
        for i in diff["intentionally_dropped"]:
            print(f"    ⊘ {i}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--url", action="append", help="Override URLs (repeatable). Family is inferred from page title h1.")
    ap.add_argument("--diff-only", action="store_true", help="Skip writing JSON; just print the diff.")
    ap.add_argument("--out", type=Path, default=OUT_DIR / "apple_support_models.json")
    args = ap.parse_args(argv)

    pages = DEFAULT_PAGES if not args.url else [(u, _family_from_url(u)) for u in args.url]

    all_models: list[Model] = []
    for url, family in pages:
        print(f"→ fetching {url} ({family}) …", file=sys.stderr)
        html = fetch(url)
        models = parse_page(html, url, family)
        print(f"  parsed {len(models)} model rows", file=sys.stderr)
        all_models.extend(models)
    all_models = _dedup_aggregating_aliases(all_models)
    print(f"  → {len(all_models)} unique identifiers after dedup", file=sys.stderr)

    if not args.diff_only:
        write_minimized(all_models, args.out)
        print(f"✓ wrote {len(all_models)} models to {args.out.relative_to(REPO_ROOT)}", file=sys.stderr)

    diff = diff_against_sources(all_models)
    print_diff(diff)
    return 0


def _family_from_url(url: str) -> str:
    # Best-effort; user can rename later. Used only as a label in the output.
    return "Unknown"


if __name__ == "__main__":
    sys.exit(main())
