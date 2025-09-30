#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rich>=13.7.0",
#     "typer>=0.9.0",
# ]
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
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel

console = Console()
app = typer.Typer(help="Modern RSS feed generator for SOFA")

# Configurable SOFA FQDN - can be set via environment variable
import os
SOFA_FQDN = os.getenv("SOFA_FQDN", os.getenv("SOFA_BASE_URL", "https://sofa.macadmins.io"))


def load_json_file(filepath: Path) -> Optional[Dict]:
    """Load and parse JSON file with Rich output"""
    if not filepath.exists():
        console.print(f"⚠️ Warning: {filepath} not found", style="yellow")
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        console.print(f"❌ Error parsing {filepath}: {e}", style="red")
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

    # Component maping with descriptions
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

    # Create a single consolidated XProtect update entry
    component_details = []
    for version_key, info in components.items():
        version = data.get(version_key)
        if version:
            # Extract component name for cleaner display
            name = info['name'].replace('XProtect ', '').replace(' Data', '')
            component_details.append(f"{name} ({version})")
    
    if component_details:
        # Single XProtect entry with all component versions
        updates.append({
            "name": "XProtect Security Framework",
            "version": f"Bundle Update",
            "date": release_date,
            "type": "xprotect",
            "description": f"XProtect Security Framework updated: {', '.join(component_details)}",
            "url": "https://support.apple.com/en-us/100100",
        })

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
        # Return None for missing dates instead of fallback - let caller decide
        return None

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

    # Return None for unparseable dates - let caller decide whether to include item
    return None


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

    # Filter to only include relevant platforms
    relevant_platforms = [
        "macOS", "iOS", "iPadOS", "visionOS", "tvOS", "watchOS", "Safari", "Xcode",
        "XProtect", "beta"  # Include XProtect and beta releases
    ]
    
    # Check if product name contains any relevant platform
    is_relevant = False
    product_lower = product_name.lower()
    
    # Special handling for beta releases
    if release_type == "beta" or "beta" in product_lower:
        is_relevant = True
    # Special handling for XProtect
    elif release_type.startswith("xprotect") or "xprotect" in product_lower:
        is_relevant = True
    else:
        # Check for platform names in product name
        for platform in relevant_platforms:
            if platform.lower() in product_lower:
                is_relevant = True
                break
    
    if not is_relevant:
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

    # Use Apple's official URLs as primary links for RSS compatibility
    link = SubElement(item, "link")
    
    # Prioritize Apple's official URLs to avoid RSS reader loading issues
    apple_url = release.get("url", "")
    if apple_url and apple_url.startswith("https://support.apple.com"):
        link.text = apple_url
    elif apple_url and apple_url.startswith("https://developer.apple.com"):
        link.text = apple_url  # For beta releases
    else:
        # Only use SOFA URLs when no Apple URL available
        link.text = SOFA_FQDN

    # Helper function for SOFA page mapping (for descriptions only)
    def get_sofa_page_link(product_name: str, version: str, release_type: str) -> str:
        """Generate SOFA page links for description text"""
        product_lower = product_name.lower()
        
        if "macos" in product_lower or "mac os" in product_lower:
            if "sequoia" in product_lower or "15." in version:
                return f"{SOFA_FQDN}/macos/sequoia"
            elif "sonoma" in product_lower or "14." in version:
                return f"{SOFA_FQDN}/macos/sonoma"
            elif "ventura" in product_lower or "13." in version:
                return f"{SOFA_FQDN}/macos/ventura"
            else:
                return f"{SOFA_FQDN}/macos/sequoia"
        elif "ios" in product_lower and "ipad" not in product_lower:
            return f"{SOFA_FQDN}/ios/ios18" if "18." in version else f"{SOFA_FQDN}/ios/ios17"
        elif "ipados" in product_lower or "ipad" in product_lower:
            return f"{SOFA_FQDN}/ios/ios18" if "18." in version else f"{SOFA_FQDN}/ios/ios17"
        elif "safari" in product_lower:
            return f"{SOFA_FQDN}/safari/safari18"
        elif "tvos" in product_lower:
            return f"{SOFA_FQDN}/tvos/tvos18" if "18." in version else f"{SOFA_FQDN}/tvos/tvos17"
        elif "watchos" in product_lower:
            return f"{SOFA_FQDN}/watchos/watchos11"
        elif "visionos" in product_lower:
            return f"{SOFA_FQDN}/visionos/visionos2"
        elif "xcode" in product_lower or release_type == "beta":
            return f"{SOFA_FQDN}/beta-releases"
        elif "xprotect" in product_lower or release_type.startswith("xprotect"):
            return f"{SOFA_FQDN}/macos/sequoia"
        else:
            return f"{SOFA_FQDN}/"

    # Description - varies by type
    description = SubElement(item, "description")
    desc_parts = []

    if release_type.startswith("xprotect"):
        # Enhanced XProtect update description
        desc_parts.append(release.get("description", f"{product_name} updated"))
        desc_parts.append("Malware protection and security definitions updated")
        desc_parts.append(f'Track all XProtect components on SOFA: <a href=f"{SOFA_FQDN}/macos/sequoia">{SOFA_FQDN}/macos/sequoia</a>')

    elif release_type == "beta":
        # Rich beta release description
        build_info = release.get("build", "")
        platform = release.get("platform", product_name.split()[0] if product_name else "Unknown")
        release_notes = release.get("release_notes_url", "")
        
        desc_parts.append(f"Developer Beta Release for {platform}")
        desc_parts.append(f"New features and improvements preview")
        
        if build_info:
            desc_parts.append(f"Build Number: {build_info}")
        
        if release_notes:
            desc_parts.append(f"Release Notes: Available")
        
        # Add beta-specific guidance
        desc_parts.append("Bug Reporting: Use Feedback Assistant app")
        desc_parts.append("Access: Requires Apple Developer Program or Beta Software Program")
        
        # Add SOFA link for more details
        sofa_link = get_sofa_page_link(product_name, version, release_type)
        desc_parts.append(f'More Details: <a href="{sofa_link}">{sofa_link}</a>')

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
        
        # Add Apple security bulletin link if available
        apple_security_url = release.get("url", "")
        if apple_security_url and apple_security_url.startswith("https://support.apple.com"):
            desc_parts.append(f'Apple Security Bulletin: <a href="{apple_security_url}">{apple_security_url}</a>')
        
        # Add SOFA link for more details
        if unique_cve_count > 0 or exploited_count > 0:
            sofa_link = get_sofa_page_link(product_name, version, release_type)
            desc_parts.append(f'Security Details: <a href="{sofa_link}">{sofa_link}</a>')

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

    # Publication date - skip items without valid dates
    formatted_date = format_release_date(date)
    if not formatted_date:
        # Log skipped items for data quality monitoring
        console.print(f"⚠️ Skipping '{product_name} {version}' - invalid release date: '{date}'", style="yellow")
        return None
        
    pub_date = SubElement(item, "pubDate")
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
    link.text = SOFA_FQDN

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
    image_url.text = f"{SOFA_FQDN}/images/custom_logo.png"
    image_title = SubElement(image, "title")
    image_title.text = "SOFA"
    image_link = SubElement(image, "link")
    image_link.text = SOFA_FQDN

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


def main(
    output: str = typer.Option("v1/rss_feed.xml", "--output", help="Output RSS file path"),
    data_dir: str = typer.Option("data/resources", "--data-dir", help="Data directory containing JSON files"),
    verbose: bool = typer.Option(True, "--verbose/--quiet", help="Enable verbose output"),
    include_xprotect: bool = typer.Option(True, "--include-xprotect/--no-xprotect", help="Include XProtect updates in feed"),
    include_beta: bool = typer.Option(False, "--include-beta/--no-beta", help="Include beta releases in feed")
):
    """Generate optimized RSS feed for Apple security releases, XProtect, and beta updates"""
    
    console.print(Panel.fit(
        "[bold blue]SOFA RSS Generator[/bold blue]\n"
        "[dim]Creating filtered RSS feed for Apple platforms[/dim]",
        border_style="blue"
    ))

    all_releases = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Load security releases
        task1 = progress.add_task("Loading Apple security releases...", total=1)
        releases = load_security_releases(data_dir)
        if releases:
            all_releases.extend(releases)
            progress.advance(task1)
            if verbose:
                console.print(f"✓ Loaded [cyan]{len(releases)}[/cyan] security releases")
        else:
            progress.advance(task1)
            console.print("⚠️ No security releases found", style="yellow")

        # Load XProtect updates
        if include_xprotect:
            task2 = progress.add_task("Loading XProtect updates...", total=1)
            xprotect = load_xprotect_updates(data_dir)
            if xprotect:
                all_releases.extend(xprotect)
                progress.advance(task2)
                if verbose:
                    console.print(f"✓ Loaded [cyan]{len(xprotect)}[/cyan] XProtect components")
            else:
                progress.advance(task2)
                if verbose:
                    console.print("⚠️ No XProtect data found", style="yellow")

        # Load beta releases
        if include_beta:
            task3 = progress.add_task("Loading beta releases...", total=1)
            betas = load_beta_releases(data_dir)
            if betas:
                all_releases.extend(betas)
                progress.advance(task3)
                if verbose:
                    console.print(f"✓ Loaded [cyan]{len(betas)}[/cyan] beta releases")
            else:
                progress.advance(task3)
                if verbose:
                    console.print("⚠️ No beta releases found", style="yellow")

    if not all_releases:
        console.print("❌ No data found to generate RSS feed", style="red")
        raise typer.Exit(1)

    if verbose:
        console.print(f"\n📊 Total items to process: [cyan]{len(all_releases)}[/cyan]")

    # Calculate days between releases for OS updates
    os_releases = [r for r in all_releases if r.get("type", "os") == "os"]
    if os_releases:
        calculate_days_between_releases(os_releases)

    # Generate RSS feed
    output_path = Path(output)
    
    with console.status(f"[bold green]Generating RSS feed..."):
        write_data_to_rss(all_releases, output_path, data_dir)

    # Generate summary table
    table = Table(title="RSS Generation Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="green")
    
    if output_path.exists():
        size = output_path.stat().st_size
        
        # Count actual items in generated RSS
        try:
            with open(output_path, 'r') as f:
                content = f.read()
                actual_items = content.count('<item>')
            
            duplicates_removed = len(all_releases) - actual_items
            
            table.add_row("Total Items", str(actual_items))
            table.add_row("Security Updates", str(len(releases)))
            if include_xprotect and 'xprotect' in locals():
                table.add_row("XProtect Updates", str(len(xprotect)))
            if include_beta and 'betas' in locals():
                table.add_row("Beta Releases", str(len(betas)))
            table.add_row("Duplicates Removed", str(duplicates_removed))
            table.add_row("File Size", f"{size:,} bytes")
            
        except Exception as e:
            table.add_row("File Size", f"{size:,} bytes")
            console.print(f"⚠️ Error reading output: {e}", style="yellow")
    
    console.print(table)
    console.print(f"✅ [bold green]RSS feed generated:[/bold green] {output_path}")

if __name__ == "__main__":
    typer.run(main)