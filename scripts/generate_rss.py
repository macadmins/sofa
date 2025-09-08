#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# ///
"""
Modern RSS feed generator for SOFA
Generates RSS feed from Apple security releases data, XProtect updates, and beta releases
"""

import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Optional
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import argparse
import sys


def load_json_file(filepath: Path) -> Optional[Dict]:
    """Load and parse JSON file"""
    if not filepath.exists():
        print(f"Warning: {filepath} not found")
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing {filepath}: {e}")
        return None


def load_security_releases(data_dir: str = "data/resources") -> List[Dict]:
    """Load Apple security releases data from multiple sources"""
    releases = []
    
    # First, load from bulletin_data.json which has better dates
    bulletin_file = Path(data_dir) / "bulletin_data.json"
    bulletin_data = load_json_file(bulletin_file)
    
    if bulletin_data and "recent_releases" in bulletin_data:
        # Convert bulletin format to our format
        for release in bulletin_data["recent_releases"]:
            releases.append({
                "name": release.get("name", ""),
                "version": release.get("version", ""),
                "date": release.get("release_date", ""),  # bulletin has proper dates!
                "url": release.get("url", ""),
                "platform": release.get("platform", ""),
                "type": "os",
                # Note: CVE data will be merged from apple_security_releases.json below
            })
    
    # Then load from apple_security_releases.json for comprehensive list
    releases_file = Path(data_dir) / "apple_security_releases.json"
    releases_data = load_json_file(releases_file)
    
    if releases_data:
        # Handle the structure with "releases" key
        if isinstance(releases_data, dict) and "releases" in releases_data:
            apple_releases = releases_data["releases"]
        elif isinstance(releases_data, list):
            apple_releases = releases_data
        else:
            apple_releases = []
        
        # Create a dict for merging CVE data into existing releases
        existing_releases = {(r.get("name", ""), r.get("version", "")): r for r in releases}
        
        # Process releases from apple_security_releases
        for release in apple_releases:
            key = (release.get("name", ""), release.get("version", ""))
            
            if key in existing_releases:
                # Merge CVE data into existing release (which has good date from bulletin)
                existing_releases[key]["cves"] = release.get("cves", {})
                if not existing_releases[key].get("url") and release.get("url"):
                    existing_releases[key]["url"] = release.get("url")
            else:
                # Add new release not in bulletin data
                release_date = release.get("date") or release.get("release_date")
                if not release_date or release_date == "null":
                    release_date = None
                    
                new_release = {
                    "name": release.get("name", ""),
                    "version": release.get("version", ""),
                    "date": release_date,
                    "url": release.get("url", ""),
                    "cves": release.get("cves", {}),
                    "type": "os"
                }
                releases.append(new_release)
                existing_releases[key] = new_release

    return releases


def load_kev_catalog(data_dir: str = "data/resources") -> Set[str]:
    """Load CISA KEV catalog to identify exploited CVEs"""
    kev_file = Path(data_dir) / "kev_catalog.json"
    data = load_json_file(kev_file)

    if not data or "vulnerabilities" not in data:
        return set()

    return {vuln["cveID"] for vuln in data["vulnerabilities"] if "cveID" in vuln}


def load_xprotect_updates(data_dir: str = "data/resources") -> List[Dict]:
    """Load XProtect update information

    Note: XProtect components update independently. Each component
    (Config, Remediator, Gatekeeper, MRT, Plugin Service) may have
    different update frequencies and dates.
    """
    xprotect_file = Path(data_dir) / "xprotect.json"
    data = load_json_file(xprotect_file)

    if not data:
        return []

    updates = []
    release_date = data.get("release_date", "")

    # Component mapping with descriptions
    components = {
        "config_version": {
            "name": "XProtect Configuration Data",
            "desc": "Malware signature definitions",
            "key": "com.apple.XProtect",
        },
        "remediator_version": {
            "name": "XProtect Remediator",
            "desc": "Malware removal tool",
            "key": "com.apple.XProtectFramework.XProtect",
        },
        "gatekeeper_version": {
            "name": "Gatekeeper Configuration",
            "desc": "App notarization and security checks",
            "key": "com.apple.security.gke",
        },
        "mrt_version": {
            "name": "Malware Removal Tool (MRT)",
            "desc": "Built-in malware removal",
            "key": "com.apple.MRT",
        },
        "plugin_service_version": {
            "name": "XProtect Plugin Service",
            "desc": "Browser plugin security",
            "key": "com.apple.XprotectFramework.PluginService",
        },
    }

    # Track previous versions to detect which actually changed
    # In a real implementation, this would compare against previous xprotect.json
    component_offset = 0  # Minutes offset for each component
    
    for version_key, info in components.items():
        version = data.get(version_key)
        if version:
            # Version exists in xprotect_entries for verification
            # data.get("xprotect_entries", {}).get(info["key"])

            # Add small time offset for each component to spread them chronologically
            component_date = release_date
            if release_date and component_offset > 0:
                try:
                    # Parse the release_date and add offset
                    base_dt = datetime.fromisoformat(release_date.replace('Z', '+00:00'))
                    offset_dt = base_dt + timedelta(minutes=component_offset)
                    component_date = offset_dt.isoformat().replace('+00:00', 'Z')
                except:
                    # If parsing fails, use original date
                    component_date = release_date

            updates.append(
                {
                    "name": info["name"],
                    "version": version,
                    "date": component_date,
                    "type": f"xprotect_{version_key.replace('_version', '')}",
                    "description": f"{info['desc']} updated to version {version}",
                    "url": "https://support.apple.com/en-us/100100",  # Apple security page
                }
            )
            
            component_offset += 5  # Add 5 minutes between each component

    return updates


def load_beta_releases(data_dir: str = "data/resources") -> List[Dict]:
    """Load Apple beta releases"""
    beta_file = Path(data_dir) / "apple_beta_feed.json"
    data = load_json_file(beta_file)

    if not data or "items" not in data:
        return []

    releases = []
    for item in data["items"]:
        if "title" in item and "released" in item:  # Fixed: use "released" not "pubDate"
            # Use the provided title and version
            title = item["title"]
            version = item.get("version", "Beta")
            platform = item.get("platform", "Unknown")
            build = item.get("build", "")
            
            # Create meaningful description
            description = f"{platform} {version}"
            if build:
                description += f" ({build})"
            description += " beta release"

            releases.append(
                {
                    "name": title,
                    "version": version,
                    "date": item["released"],  # Fixed: use "released" field
                    "url": item.get("release_notes_url", item.get("downloads_url", "")),
                    "type": "beta",
                    "description": description,
                    "platform": platform,
                    "build": build
                }
            )

    return releases


def extract_cves(release: Dict, data_dir: str = "data/resources") -> Dict[str, bool]:
    """Extract CVEs from a release and identify exploited ones"""
    cves = {}
    kev_catalog = load_kev_catalog(data_dir)

    # Handle various CVE data formats
    if "cves" in release:
        cve_data = release["cves"]
        if isinstance(cve_data, list):
            for cve_id in cve_data:
                if isinstance(cve_id, str) and cve_id.startswith("CVE-"):
                    cves[cve_id] = cve_id in kev_catalog
        elif isinstance(cve_data, dict):
            for cve_id, cve_info in cve_data.items():
                if cve_id.startswith("CVE-"):
                    # Check if marked as exploited in the data itself
                    is_exploited = False
                    if isinstance(cve_info, dict):
                        context = cve_info.get("cve_context", {})
                        is_exploited = context.get("kev", False) or context.get(
                            "exploited", False
                        )
                    cves[cve_id] = is_exploited or (cve_id in kev_catalog)

    return cves


def format_release_date(date_str: str) -> str:
    """Format date string to RFC 822 format for RSS"""
    if not date_str or date_str == "null":
        # Use a reasonable default for missing dates (7 days ago)
        dt = datetime.now() - timedelta(days=7)
        return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

    # Try parsing different date formats
    formats = [
        "%Y-%m-%d",
        "%d %b %Y",
        "%B %d, %Y",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%a, %d %b %Y %H:%M:%S %z",  # Already in RFC 822
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            # Return RFC 822 format for RSS
            return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
        except (ValueError, TypeError):
            continue

    # If already in correct format, return as-is
    if isinstance(date_str, str) and date_str.startswith(
        ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
    ):
        return date_str

    # Default to 7 days ago if can't parse
    dt = datetime.now() - timedelta(days=7)
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def create_feed_item(
    release: Dict, seen_items: Set[str], previous_releases: Dict[str, datetime] = None, data_dir: str = "data/resources"
) -> Optional[Element]:
    """Create an RSS item element for a release"""
    # Create unique identifier
    product_name = (release.get("name") or "").strip()
    version = (release.get("version") or "").strip()
    date = (release.get("date") or "").strip()
    release_type = release.get("type", "os")  # os, xprotect, beta

    if not product_name or not version:
        return None

    # Generate unique ID for deduplication
    item_id = f"{product_name}_{version}_{date}"
    item_hash = hashlib.md5(item_id.encode()).hexdigest()

    if item_hash in seen_items:
        return None
    seen_items.add(item_hash)

    # Create item element
    item = Element("item")

    # Title - format based on type
    title = SubElement(item, "title")
    if release_type.startswith("xprotect"):
        title.text = f"{product_name} {version}"
    elif release_type == "beta":
        title.text = product_name  # Beta titles usually complete
    else:
        # Check if version is already in product name
        if version in product_name:
            title.text = product_name
        else:
            title.text = f"{product_name} {version}"

    # Link - use SecurityInfo URL if available, otherwise SOFA homepage
    link = SubElement(item, "link")
    security_url = (release.get("url") or "").strip()
    if security_url and security_url.startswith("https://"):
        link.text = security_url
    else:
        link.text = "https://sofa.macadmins.io/"

    # Description - varies by type
    description = SubElement(item, "description")
    desc_parts = []

    if release_type.startswith("xprotect"):
        # XProtect update description
        desc_parts.append(release.get("description", f"{product_name} updated"))

    elif release_type == "beta":
        # Beta release description
        desc_parts.append(release.get("description", "Beta release"))

    else:
        # Security release description with CVE info
        # Extract and count CVEs
        cves = extract_cves(release, data_dir)
        unique_cve_count = len(cves)
        exploited_count = sum(1 for is_exploited in cves.values() if is_exploited)

        if unique_cve_count > 0:
            desc_parts.append(f"Vulnerabilities Addressed: {unique_cve_count}")
        else:
            desc_parts.append("Vulnerabilities Addressed: 0")

        desc_parts.append(f"Exploited CVE(s): {exploited_count}")

        # Calculate days since previous release for same OS
        if previous_releases and date:
            try:
                current_date = datetime.strptime(date, "%Y-%m-%d")
                os_type = product_name.split()[0]  # Get OS type (macOS, iOS, etc.)

                if os_type in previous_releases:
                    days_diff = (current_date - previous_releases[os_type]).days
                    if days_diff > 0:
                        desc_parts.append(f"Days to Prev. Release: {days_diff}")
            except (ValueError, KeyError):
                pass

    description.text = "<br>".join(desc_parts) if desc_parts else "Update"

    # GUID - make unique based on type
    guid = SubElement(item, "guid")
    guid.set("isPermaLink", "false")

    if release_type.startswith("xprotect"):
        guid.text = f"XProtect_{release_type.replace('xprotect_', '')}_{version}"
    elif release_type == "beta":
        guid.text = f"Beta_{product_name.replace(' ', '_')}_{version}"
    else:
        # OS update GUID
        product_type = product_name.split()[0] if product_name else "Unknown"
        guid.text = f"{product_type}_OS_{version}"

    # Publication date
    pub_date = SubElement(item, "pubDate")
    formatted_date = format_release_date(date)
    if formatted_date:
        pub_date.text = formatted_date

    return item


def write_data_to_rss(all_releases: List[Dict], output_file: Path, data_dir: str = "data/resources") -> None:
    """Write RSS feed from combined releases data (matching legacy function name)"""
    # Create root RSS element
    rss = Element("rss")
    rss.set("version", "2.0")

    # Create channel
    channel = SubElement(rss, "channel")

    # Channel metadata
    title = SubElement(channel, "title")
    title.text = "SOFA - RSS Update Feed"

    link = SubElement(channel, "link")
    link.text = "https://sofa.macadmins.io/"

    description = SubElement(channel, "description")
    description.text = "Simple Organized Feed for Apple Software Updates - Security releases and updates"

    language = SubElement(channel, "language")
    language.text = "en-us"

    # Generator
    generator = SubElement(channel, "generator")
    generator.text = "SOFA RSS Generator 2.0"

    # Build date
    last_build = SubElement(channel, "lastBuildDate")
    last_build.text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    # Logo/image
    image = SubElement(channel, "image")
    image_url = SubElement(image, "url")
    image_url.text = "https://sofa.macadmins.io/images/custom_logo.png"
    image_title = SubElement(image, "title")
    image_title.text = "SOFA"
    image_link = SubElement(image, "link")
    image_link.text = "https://sofa.macadmins.io/"

    # Sort releases by date (newest first), handling different date formats
    def get_sortable_date(release):
        date_str = release.get("date", "")
        if not date_str:
            return datetime.min

        # Try parsing common formats
        for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ"]:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return datetime.min

    sorted_releases = sorted(all_releases, key=get_sortable_date, reverse=True)

    # Track seen items for deduplication
    seen_items: Set[str] = set()

    # Track previous release dates by OS type for calculating days
    previous_releases: Dict[str, datetime] = {}

    # Add items to feed
    items_added = 0
    for release in sorted_releases:
        item = create_feed_item(release, seen_items, previous_releases, data_dir)
        if item is not None:
            channel.append(item)
            items_added += 1

            # Update previous release tracking for OS updates
            if release.get("type", "os") == "os":
                name = release.get("name", "")
                date_str = release.get("date", "")
                if name and date_str:
                    try:
                        os_type = name.split()[0]
                        release_date = datetime.strptime(date_str, "%Y-%m-%d")
                        if (
                            os_type not in previous_releases
                            or release_date < previous_releases[os_type]
                        ):
                            previous_releases[os_type] = release_date
                    except (ValueError, KeyError):
                        pass

    # Pretty print XML
    xml_str = tostring(rss, encoding="unicode")
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ", encoding="UTF-8")

    # Write to file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "wb") as f:
        f.write(pretty_xml)

    print(f"✅ RSS feed generated: {output_file}")
    print(f"   - Total items: {items_added}")
    print(
        f"   - Security updates: {sum(1 for r in sorted_releases if r.get('type', 'os') == 'os')}"
    )
    print(
        f"   - XProtect updates: {sum(1 for r in sorted_releases if 'xprotect' in r.get('type', ''))}"
    )
    print(
        f"   - Beta releases: {sum(1 for r in sorted_releases if r.get('type') == 'beta')}"
    )
    print(f"   - Duplicates removed: {len(sorted_releases) - items_added}")


def calculate_days_between_releases(releases: List[Dict]) -> None:
    """Calculate days between consecutive releases for each OS type"""
    # Group by OS type
    os_groups = {}
    for release in releases:
        name = release.get("name", "")
        if not name:
            continue

        # Extract OS type (first word typically)
        os_type = name.split()[0]
        if os_type not in os_groups:
            os_groups[os_type] = []
        os_groups[os_type].append(release)

    # Calculate days for each OS type
    for os_type, os_releases in os_groups.items():
        # Sort by date (handle None values)
        sorted_releases = sorted(
            os_releases, key=lambda x: x.get("date") or "", reverse=True
        )

        # Calculate days between releases
        for i in range(len(sorted_releases) - 1):
            current_date = sorted_releases[i].get("date", "")
            prev_date = sorted_releases[i + 1].get("date", "")

            if current_date and prev_date:
                try:
                    current = datetime.strptime(current_date, "%Y-%m-%d")
                    previous = datetime.strptime(prev_date, "%Y-%m-%d")
                    days_diff = (current - previous).days
                    sorted_releases[i]["days_since_previous"] = days_diff
                except ValueError:
                    pass


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Generate RSS feed for Apple security releases, XProtect, and beta updates"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="rss_feed.xml",
        help="Output RSS file path (default: rss_feed.xml)",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data/resources",
        help="Data directory containing JSON files (default: ../data/resources)",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--include-xprotect",
        action="store_true",
        default=True,
        help="Include XProtect updates in feed (default: True)",
    )
    parser.add_argument(
        "--include-beta",
        action="store_true",
        default=False,
        help="Include beta releases in feed (default: False)",
    )

    args = parser.parse_args()

    all_releases = []

    # Load security releases
    if args.verbose:
        print("Loading Apple security releases...")

    releases = load_security_releases(args.data_dir)
    if releases:
        all_releases.extend(releases)
        if args.verbose:
            print(f"  ✓ Loaded {len(releases)} security releases")
    else:
        print("  ⚠️  No security releases found")

    # Load XProtect updates
    if args.include_xprotect:
        if args.verbose:
            print("Loading XProtect updates...")
        xprotect = load_xprotect_updates(args.data_dir)
        if xprotect:
            all_releases.extend(xprotect)
            if args.verbose:
                print(f"  ✓ Loaded {len(xprotect)} XProtect components")
        else:
            if args.verbose:
                print("  ⚠️  No XProtect data found")

    # Load beta releases
    if args.include_beta:
        if args.verbose:
            print("Loading beta releases...")
        betas = load_beta_releases(args.data_dir)
        if betas:
            all_releases.extend(betas)
            if args.verbose:
                print(f"  ✓ Loaded {len(betas)} beta releases")
        else:
            if args.verbose:
                print("  ⚠️  No beta releases found")

    if not all_releases:
        print("❌ No data found to generate RSS feed", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"\nTotal items to process: {len(all_releases)}")

    # Calculate days between releases for OS updates
    os_releases = [r for r in all_releases if r.get("type", "os") == "os"]
    if os_releases:
        calculate_days_between_releases(os_releases)

    # Generate RSS feed
    output_path = Path(args.output)
    write_data_to_rss(all_releases, output_path, args.data_dir)

    # Also generate at the standard location for web serving
    standard_path = Path("v1/rss_feed.xml")
    if output_path != standard_path:
        write_data_to_rss(all_releases, standard_path, args.data_dir)
        print(f"✅ Also generated at: {standard_path}")


if __name__ == "__main__":
    main()