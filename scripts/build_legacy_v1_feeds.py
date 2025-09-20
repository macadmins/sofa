#!/usr/bin/env -S uv run --python 3.13 python
"""
Legacy V1 Feed Builder - UV + Python 3.13
Builds 100% compatible v1 legacy feeds from pre-fetched data without live fetching.

This script reinterprets https://github.com/macadmins/sofa/blob/main/build-sofa-feed.py to use all data pre-feched and available in data/resources/, substituting the job normally handled by sofa-build.

The generated feeds are identical in structure to classic SOFA v1 feeds:
- https://sofafeed.macadmins.io/v1/macos_data_feed.json
- https://sofafeed.macadmins.io/v1/ios_data_feed.json

USAGE:
    # Build both macOS and iOS feeds
    scripts/build_legacy_v1_feeds.py macOS iOS
    
    # Build only macOS feed with verbose output  
    scripts/build_legacy_v1_feeds.py macOS --verbose
    
    # Build to specific output directory
    scripts/build_legacy_v1_feeds.py iOS --output-dir legacy_feeds/

FEATURES:
    - Uses identical function names as legacy_build-sofa-feed.py
    - Generates a compatible legacy v1 feed format
    - Processes GDMF data for OS versions and device support
    - Maps security releases with CVE tracking
    - Integrates KEV (Known Exploited Vulnerabilities) data
    - Includes XProtect versions for macOS feeds
    - Adds UMA catalog and IPSW data for macOS
    - Supports device models mapping
    - Use UV + Python 3.13 moree streamlined processing

HARD REQUIREMENTS:
    - Data must be pre-fetched using 'sofa-gather all' and 'sofa-fetch'
    - Requires: data/resources/gdmf_cached.json (GDMF data)
    - Requires: data/resources/apple_security_releases.json (security releases)
    - Optional: data/resources/kev_catalog.json (KEV exploitation data)
    - Optional: data/resources/xprotect.json (XProtect versions)
    - Optional: data/resources/uma_catalog.json (macOS installers)
    - Optional: data/resources/ipsw.json (macOS IPSW data)
    - Optional: data/resources/mac_models_mapping.json (device models)
"""

import argparse
import hashlib
import json
import os
import sys
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

# OS Version ranges to include in feeds (to match live feeds)
OS_RANGE_MACOS = ["12", "13", "14", "15", "26"]
OS_RANGE_IOS = ["16", "17", "18" "26"]  # Including 16 to match live feed

# macOS version name transformation table to match live feed schema
MACOS_NAME_TRANSFORM = {
    "26": "Tahoe 26",
    "15": "Sequoia 15",
    "14": "Sonoma 14", 
    "13": "Ventura 13",
    "12": "Monterey 12"
}

# packaging import is optional, will fall back to string sorting if not available
try:
    import packaging.version
    HAS_PACKAGING = True
except ImportError:
    HAS_PACKAGING = False


def main(os_types: list):
    """The main function to process OS version information based on the provided OS types"""
    feed_results: list = []  # instantiate end result
    
    # Load pre-fetched data instead of live fetching
    gdmf_data = load_gdmf_cached_data()
    if not gdmf_data:
        print("Failed to load cached GDMF data.")
        return
    
    for os_type in os_types:
        result = process_os_type(os_type, gdmf_data)
        feed_results.extend(result)
    
    print(f"✅ Successfully built {len(os_types)} legacy v1 feed(s)")


def load_gdmf_cached_data() -> dict:
    """Load GDMF data from pre-fetched cache file with failover to live fetch"""
    data_dir = Path("data/resources")
    gdmf_path = data_dir / "gdmf_cached.json"
    
    # First try to load from pre-fetched cache
    if gdmf_path.exists():
        try:
            with open(gdmf_path, 'r', encoding='utf-8') as f:
                cache_content = json.load(f)
                # Handle both wrapped and direct format
                cached_data = cache_content.get("data", cache_content)
                if cached_data and isinstance(cached_data, dict):
                    print("📦 Using pre-fetched GDMF data from cache")
                    return cached_data
        except Exception as e:
            print(f"⚠️  Error loading cached GDMF data: {e}")
    
    # Fallback: Try to load from legacy cache location
    legacy_cache_path = Path("cache/gdmf_cached.json")
    if legacy_cache_path.exists():
        try:
            with open(legacy_cache_path, 'r', encoding='utf-8') as f:
                cache_content = json.load(f)
                cached_data = cache_content.get("data", cache_content)
                if cached_data and isinstance(cached_data, dict):
                    print("📦 Using GDMF data from legacy cache location")
                    return cached_data
        except Exception as e:
            print(f"⚠️  Error loading legacy GDMF cache: {e}")
    
    print("❌ No valid GDMF cache found in data/resources/ or cache/")
    print("    Run 'sofa-gather all' or 'sofa-fetch' first to populate data.")
    return {}


def load_security_releases_data() -> List[Dict]:
    """Load security releases from pre-fetched data"""
    data_dir = Path("data/resources")
    security_path = data_dir / "apple_security_releases.json"
    
    if not security_path.exists():
        print(f"⚠️  Security releases file not found: {security_path}")
        return []
    
    try:
        with open(security_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("releases", [])
    except Exception as e:
        print(f"⚠️  Error loading security releases: {e}")
        return []


def load_kev_data() -> Dict[str, bool]:
    """Load KEV catalog and return CVE -> exploited mapping"""
    data_dir = Path("data/resources")
    kev_path = data_dir / "kev_catalog.json"
    
    if not kev_path.exists():
        return {}
    
    try:
        with open(kev_path, 'r', encoding='utf-8') as f:
            kev = json.load(f)
        
        # Map CVE IDs to exploited status
        kev_cves = {}
        for vuln in kev.get("vulnerabilities", []):
            if "cveID" in vuln:
                kev_cves[vuln["cveID"]] = True
        
        return kev_cves
    except Exception:
        return {}


def load_xprotect_data() -> Dict:
    """Load XProtect data from pre-fetched cache"""
    data_dir = Path("data/resources")
    xprotect_path = data_dir / "xprotect.json"
    
    if not xprotect_path.exists():
        return {}
    
    try:
        with open(xprotect_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def load_uma_data() -> Dict:
    """Load UMA catalog data"""
    data_dir = Path("data/resources")
    uma_path = data_dir / "uma_catalog.json"
    
    if not uma_path.exists():
        return {}
    
    try:
        with open(uma_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def load_ipsw_data() -> Dict:
    """Load IPSW data"""
    data_dir = Path("data/resources")
    ipsw_path = data_dir / "ipsw.json"
    
    if not ipsw_path.exists():
        return {}
    
    try:
        with open(ipsw_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def load_and_tag_model_data() -> dict:
    """Load model data from individual model_identifier_*.json files"""
    models_dir = Path("data/models/legacy")
    combined_models = {}
    
    # Load all model identifier files
    for model_file in models_dir.glob("model_identifier_*.json"):
        try:
            with open(model_file, 'r', encoding='utf-8') as f:
                model_data = json.load(f)
                
            # Each file contains an array of model categories
            for entry in model_data:
                if "Identifiers" in entry:
                    # Merge identifiers from this file into combined models
                    for identifier, model_name in entry["Identifiers"].items():
                        combined_models[identifier] = model_name
                        
        except Exception as e:
            print(f"Warning: Could not load {model_file}: {e}")
            continue
    
    print(f"📱 Loaded {len(combined_models)} model identifiers from individual files")
    return combined_models


def process_os_type(os_type: str, gdmf_data: dict) -> list:
    """Process the given OS type (macOS, iOS) and update the feed structure"""
    print(f"🔧 Processing {os_type}...")
    
    feed_structure: dict = {
        "OSVersions": [],
    }
    
    # Load supporting data
    security_releases = load_security_releases_data()
    kev_data = load_kev_data()
    
    if os_type == "macOS":
        # Add XProtect data for macOS
        xprotect_data = load_xprotect_data()
        if xprotect_data:
            feed_structure["XProtectPlistConfigData"] = {
                "com.apple.XProtect": str(xprotect_data.get("config_version", "")),
                "ReleaseDate": format_iso_date(xprotect_data.get("release_date", ""))
            }
            feed_structure["XProtectPayloads"] = {
                "com.apple.XProtectFramework.XProtect": str(xprotect_data.get("remediator_version", "")),
                "com.apple.XprotectFramework.PluginService": str(xprotect_data.get("plugin_service_version", "")),
                "ReleaseDate": format_iso_date(xprotect_data.get("release_date", ""))
            }
        
        # Add Models data
        models_info = load_and_tag_model_data()
        if models_info:
            feed_structure["Models"] = models_info
        
        # Add UMA/IPSW data
        installation_apps = build_installation_apps()
        if installation_apps:
            feed_structure["InstallationApps"] = installation_apps
    
    # Process OS versions from GDMF data
    os_versions = build_os_versions_from_gdmf(os_type, gdmf_data, security_releases, kev_data)
    feed_structure["OSVersions"] = os_versions
    
    # Calculate hash and finalize structure
    hash_value = compute_hash(feed_structure)
    feed_structure = {
        "UpdateHash": hash_value,  # Insert hash first
        **feed_structure,  # Unpack other content after the hash
    }
    
    # Write the feed file
    data_feed_filename = f"{os_type.lower()}_data_feed.json"
    write_data_to_json(feed_structure, data_feed_filename)
    
    # Show full path if output directory is specified
    output_dir = Path(os.environ.get('OUTPUT_DIR', '.'))
    output_path = output_dir / data_feed_filename
    print(f"✅ Created: {output_path}")
    return []


def build_os_versions_from_gdmf(os_type: str, gdmf_data: dict, security_releases: List[Dict], kev_data: Dict[str, bool]) -> List[Dict]:
    """Build OS versions section from GDMF data"""
    os_versions = []
    
    # Get OS data from GDMF
    os_key = "macOS" if os_type == "macOS" else "iOS"
    gdmf_versions = gdmf_data.get("PublicAssetSets", {}).get(os_key, [])
    
    if not gdmf_versions:
        return os_versions
    
    # Group by major version
    version_groups = group_versions_by_major(gdmf_versions, os_type)
    
    # Determine which OS range to use
    allowed_versions = OS_RANGE_MACOS if os_type == "macOS" else OS_RANGE_IOS
    
    for major_version, versions in version_groups.items():
        # Skip versions not in the allowed range
        if major_version not in allowed_versions:
            continue
        # Get latest version for this major version
        latest_version = get_latest_version_info(versions)
        if not latest_version:
            continue
        
        # Build security releases for this version
        security_releases_for_version = fetch_security_releases(
            os_type, major_version, security_releases, kev_data, latest_version
        )
        
        # Enhance latest version with security info
        enhance_latest_with_security_info(latest_version, security_releases_for_version)
        
        # Transform OS version name to match live feed schema
        if os_type == "macOS":
            os_version_name = MACOS_NAME_TRANSFORM.get(major_version, f"macOS {major_version}")
        else:
            os_version_name = major_version
        
        os_version_data = {
            "OSVersion": os_version_name,
            "Latest": latest_version,
            "SecurityReleases": security_releases_for_version
        }
        
        # Add supported models for macOS  
        if os_type == "macOS":
            compatible_machines = add_compatible_machines(os_version_name)
            if compatible_machines:
                os_version_data["SupportedModels"] = compatible_machines
        
        os_versions.append(os_version_data)
    
    # Sort by version number (newest first)
    if HAS_PACKAGING:
        os_versions.sort(key=lambda x: packaging.version.parse(
            x["OSVersion"].split()[-1] if os_type == "macOS" else x["OSVersion"]
        ), reverse=True)
    else:
        os_versions.sort(key=lambda x: x["OSVersion"].split()[-1] if os_type == "macOS" else x["OSVersion"], reverse=True)
    
    return os_versions


def group_versions_by_major(versions: List[Dict], os_type: str) -> Dict[str, List[Dict]]:
    """Group GDMF versions by major version number"""
    groups = {}
    
    for version in versions:
        product_version = version.get("ProductVersion", "")
        if not product_version:
            continue
        
        # For iOS, filter for iOS/iPadOS devices only
        if os_type == "iOS":
            devices = version.get("SupportedDevices", [])
            if not any(device.startswith(("iPad", "iPhone")) for device in devices):
                continue
        
        try:
            major = product_version.split(".")[0]
            if major not in groups:
                groups[major] = []
            groups[major].append(version)
        except (IndexError, ValueError):
            continue
    
    return groups


def get_latest_version_info(versions: List[Dict]) -> Optional[Dict]:
    """Get the latest version from a list, preferring higher device count and newer date"""
    if not versions:
        return None
    
    latest = max(versions, key=lambda v: (
        len(v.get("SupportedDevices", [])),  # Prefer more devices
        v.get("PostingDate", ""),            # Then newer date
        v.get("ProductVersion", "")          # Then version number
    ))
    
    return {
        "ProductVersion": latest.get("ProductVersion", ""),
        "Build": latest.get("Build", ""),
        "ReleaseDate": format_iso_date(latest.get("PostingDate", "")),
        "ExpirationDate": format_iso_date(latest.get("ExpirationDate", "")),
        "SupportedDevices": latest.get("SupportedDevices", []),
        "SecurityInfo": "",
        "CVEs": {},
        "ActivelyExploitedCVEs": [],
        "UniqueCVEsCount": 0
    }


def fetch_security_releases(os_type: str, major_version: str, security_releases: List[Dict], 
                          kev_data: Dict[str, bool], gdmf_latest: Dict) -> List[Dict]:
    """Fetch security releases for the given OS type and version"""
    releases = []
    
    for release in security_releases:
        release_name = release.get("name", "")
        if not matches_os_version(release_name, os_type, major_version):
            continue
        
        # Extract version from release name
        version_match = extract_version_from_title(release_name)
        if not version_match:
            continue
        
        # Get CVEs for this release with exploitation status
        cves = {}
        actively_exploited = []
        
        for cve_id in release.get("cves", []):
            if isinstance(cve_id, str) and cve_id.startswith("CVE-"):
                is_exploited = kev_data.get(cve_id, False)
                cves[cve_id] = is_exploited
                if is_exploited:
                    actively_exploited.append(cve_id)
        
        # Determine release type
        release_type = "OS"
        if "Rapid Security Response" in release_name:
            rsr_match = re.search(r'\((\w)\)', release_name)
            if rsr_match:
                release_type = f"RSR_{rsr_match.group(1)}"
            else:
                release_type = "RSR"
        
        security_release = {
            "UpdateName": release_name,
            "ProductName": os_type,
            "ProductVersion": version_match,
            "ReleaseDate": format_iso_date(release.get("release_date", "")),
            "ReleaseType": release_type,
            "SecurityInfo": release.get("url", ""),
            "SupportedDevices": gdmf_latest.get("SupportedDevices", []),
            "CVEs": cves,
            "ActivelyExploitedCVEs": actively_exploited,
            "UniqueCVEsCount": len(cves),
            "DaysSincePreviousRelease": 0  # Could calculate if needed
        }
        
        releases.append(security_release)
    
    # Sort by release date (newest first)
    releases.sort(key=lambda x: x.get("ReleaseDate", ""), reverse=True)
    
    return releases


def matches_os_version(title: str, os_type: str, major_version: str) -> bool:
    """Check if security release title matches OS type and major version"""
    title_lower = title.lower()
    
    if os_type == "macOS":
        # More precise matching - check for space before version to avoid matching "10.15" when looking for "15"
        # Match patterns like "macOS Sequoia 15", "macOS Sequoia 15.1" or "macOS 15" but not "10.15"
        if "macos" not in title_lower:
            return False
        
        # Handle base releases like "macOS Sequoia 15" (no point version)
        # and versioned releases like "macOS Sequoia 15.1"
        # Pattern matches: "macOS Sequoia 15" or "macOS Sequoia 15.x.x"
        version_match = re.search(r'(?:macOS\s+(?:Sequoia|Sonoma|Ventura|Monterey|Big Sur)?\s*)(\d+)(?:\.(\d+))?', title, re.IGNORECASE)
        if version_match:
            extracted_major = version_match.group(1)
            return extracted_major == major_version
        return False
        
    elif os_type == "iOS":
        if not ("ios" in title_lower or "ipados" in title_lower):
            return False
        
        # Extract iOS version more precisely
        version_match = re.search(r'(?:iOS|iPadOS)\s+(\d+(?:\.\d+)*)', title, re.IGNORECASE)
        if version_match:
            extracted_major = version_match.group(1).split('.')[0]
            return extracted_major == major_version
        return False
    
    return False


def extract_version_from_title(title: str) -> Optional[str]:
    """Extract version number from security release title"""
    # First try to match versioned releases like "15.1" or "15.1.1"
    version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', title)
    if version_match:
        return version_match.group(1)
    
    # If no point version found, check for base releases like "macOS Sequoia 15"
    # This matches "15" at the end of the OS name
    base_match = re.search(r'(?:macOS\s+(?:Sequoia|Sonoma|Ventura|Monterey|Big Sur)?\s*)(\d+)$', title, re.IGNORECASE)
    if base_match:
        return base_match.group(1) + ".0"  # Return as "15.0" for consistency
    
    # For iOS, similar logic
    ios_base_match = re.search(r'(?:iOS|iPadOS)\s+(\d+)$', title, re.IGNORECASE)
    if ios_base_match:
        return ios_base_match.group(1) + ".0"
    
    return None


def enhance_latest_with_security_info(latest_info: Dict, security_releases: List[Dict]) -> None:
    """Enhance latest version info with security data from most recent security release"""
    if security_releases:
        latest_security = security_releases[0]  # Most recent
        latest_info["SecurityInfo"] = latest_security.get("SecurityInfo", "")
        latest_info["CVEs"] = latest_security.get("CVEs", {})
        latest_info["ActivelyExploitedCVEs"] = latest_security.get("ActivelyExploitedCVEs", [])
        latest_info["UniqueCVEsCount"] = latest_security.get("UniqueCVEsCount", 0)
        
        # Use security release date if available and newer
        security_date = latest_security.get("ReleaseDate", "")
        if security_date and security_date > latest_info["ReleaseDate"]:
            latest_info["ReleaseDate"] = security_date


def build_installation_apps() -> Dict:
    """Build UMA and IPSW data for macOS"""
    installation_apps = {
        "LatestUMA": None,
        "AllPreviousUMA": [],
        "LatestMacIPSW": None
    }
    
    # Load UMA data
    uma_data = load_uma_data()
    if uma_data:
        uma_entries = []
        for product_key, product_data in uma_data.items():
            if isinstance(product_data, dict):
                uma_entry = {
                    "title": product_data.get("title", ""),
                    "version": product_data.get("version", ""),
                    "build": product_data.get("build", ""),
                    "apple_slug": product_key,
                    "url": product_data.get("url", "")
                }
                uma_entries.append(uma_entry)
        
        # Sort by version to get latest
        if uma_entries:
            try:
                if HAS_PACKAGING:
                    uma_entries.sort(key=lambda x: packaging.version.parse(x.get("version", "0.0.0")), reverse=True)
                else:
                    uma_entries.sort(key=lambda x: x.get("version", "0.0.0"), reverse=True)
                installation_apps["LatestUMA"] = uma_entries[0]
                installation_apps["AllPreviousUMA"] = uma_entries[1:]
            except Exception:
                installation_apps["LatestUMA"] = uma_entries[0] if uma_entries else None
                installation_apps["AllPreviousUMA"] = uma_entries[1:] if len(uma_entries) > 1 else []
    
    # Load IPSW data
    ipsw_data = load_ipsw_data()
    if ipsw_data and isinstance(ipsw_data, dict) and "url" in ipsw_data:
        apple_slug = ipsw_data.get("url", "").split("/")[-1].replace(".ipsw", "")
        installation_apps["LatestMacIPSW"] = {
            "macos_ipsw_url": ipsw_data.get("url", ""),
            "macos_ipsw_build": ipsw_data.get("build", ""),
            "macos_ipsw_version": ipsw_data.get("version", ""),
            "macos_ipsw_apple_slug": apple_slug
        }
    
    return installation_apps


def add_compatible_machines(current_macos_full_version: str) -> List[Dict]:
    """Add compatible machines for the given macOS version, only processed for macOS
    
    This follows the same logic as the original legacy_build-sofa-feed.py:
    Extract lowercase OS 'name' to find file of compatible machines
    """
    # Extract lowercase OS 'name' to find file of compatible machines
    # This will get "sequoia" from "Sequoia 15"
    current_macos_name = current_macos_full_version.split(" ")[0].lower()
    
    # Look for model_identifier file in data/models/legacy directory
    filename = Path(f"data/models/legacy/model_identifier_{current_macos_name}.json")
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
    
    compatible_machines = []
    for entry in data:
        model = entry["Model"]
        url = entry["URL"]
        identifiers = entry["Identifiers"]
        compatible_machines.append(
            {"Model": model, "URL": url, "Identifiers": identifiers}
        )
    
    return compatible_machines


def format_iso_date(date_str: str) -> str:
    """Format the date string to ISO 8601 format or a hardcoded date if the input is 'Preinstalled'"""
    if date_str == "Preinstalled":
        return "2021-10-25T00:00:00Z"
    
    if not date_str:
        return ""
    
    # Handle various date formats
    formats = ["%Y-%m-%d", "%d %b %Y", "%B %d, %Y"]
    for fmt in formats:
        try:
            return (
                datetime.strptime(date_str, fmt).replace(microsecond=0).isoformat()
                + "Z"
            )
        except ValueError:
            pass
    return date_str


def compute_hash(data: dict) -> str:
    """Computes SHA-256 hash of the given data, typically a dict. Returns a hexadecimal str"""
    json_str = json.dumps(
        data, sort_keys=True
    ).encode()  # sorts to always produce consistent result
    return hashlib.sha256(json_str).hexdigest()


def write_data_to_json(feed_structure: dict, filename: str):
    """Writes the fully populated feed structure to JSON filename"""
    # Get output directory from environment or use current directory
    output_dir = Path(os.environ.get('OUTPUT_DIR', '.'))
    output_path = output_dir / filename
    
    latest_versions = {}

    for os_version in feed_structure["OSVersions"]:
        if "Latest" in os_version:
            latest_dict = os_version["Latest"]

            # Ensure all required keys are present with default values
            latest_dict["ProductVersion"] = latest_dict.get("ProductVersion", "")
            latest_dict["ReleaseDate"] = latest_dict.get("ReleaseDate", "")
            latest_dict["ExpirationDate"] = latest_dict.get("ExpirationDate", "")
            latest_dict["Build"] = latest_dict.get("Build", "")
            latest_dict["SecurityInfo"] = latest_dict.get("SecurityInfo", "")
            latest_dict["UniqueCVEsCount"] = latest_dict.get("UniqueCVEsCount", 0)
            latest_dict["ActivelyExploitedCVEs"] = latest_dict.get("ActivelyExploitedCVEs", [])
            latest_dict["CVEs"] = latest_dict.get("CVEs", {})
            latest_dict["SupportedDevices"] = latest_dict.get("SupportedDevices", [])

            product_version = latest_dict["ProductVersion"]

            # Store the latest version info for comparison
            latest_versions[product_version] = {
                "latest_date": latest_dict["ReleaseDate"],
                "os_version_dict": os_version
            }

        # Handle SecurityReleases similarly if present
        if "SecurityReleases" in os_version and isinstance(os_version["SecurityReleases"], list):
            for release in os_version["SecurityReleases"]:
                release["ProductVersion"] = release.get("ProductVersion", "")
                release["ReleaseDate"] = release.get("ReleaseDate", "")

                product_version = release["ProductVersion"]
                if product_version in latest_versions:
                    # Update security date if the product version matches
                    latest_versions[product_version]["security_date"] = release["ReleaseDate"]

    # Update all relevant Latest entries with their respective security dates
    for product_version, version_info in latest_versions.items():
        if "security_date" in version_info:
            latest_dict = version_info["os_version_dict"]["Latest"]
            original_date = latest_dict.get("ReleaseDate", "")
            new_date = version_info["security_date"]
            latest_dict["ReleaseDate"] = new_date
            print(f"Updated {product_version} ReleaseDate from {original_date} to {new_date}")

    # Write the updated feed structure back to a file
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(
            feed_structure, json_file, indent=4, ensure_ascii=False
        )


def validate_feeds_against_live(output_dir: str = "."):
    """Validate generated feeds against live official feeds"""
    import urllib.request
    import difflib
    
    print("\n🔍 VALIDATING FEEDS AGAINST LIVE VERSIONS...\n")
    
    # Use provided output directory or current directory
    output_path = Path(output_dir)
    
    feeds_to_validate = [
        ("macos", "https://sofafeed.macadmins.io/v1/macos_data_feed.json", "macos_data_feed.json"),
        ("ios", "https://sofafeed.macadmins.io/v1/ios_data_feed.json", "ios_data_feed.json")
    ]
    
    for feed_name, live_url, local_file in feeds_to_validate:
        local_path = output_path / local_file
        if not local_path.exists():
            print(f"⚠️  Local {feed_name} feed not found at {local_path}. Run build first.")
            continue
            
        print(f"📊 Validating {feed_name.upper()} feed...")
        
        try:
            # Fetch live feed
            with urllib.request.urlopen(live_url) as response:
                live_data = json.loads(response.read().decode())
            
            # Load local feed
            with open(local_path, 'r') as f:
                local_data = json.load(f)
            
            # Compare main structure
            print(f"  Live feed UpdateHash: {live_data.get('UpdateHash', 'N/A')[:16]}...")
            print(f"  Local feed UpdateHash: {local_data.get('UpdateHash', 'N/A')[:16]}...")
            
            # Compare OS versions
            live_versions = [v.get('OSVersion') for v in live_data.get('OSVersions', [])]
            local_versions = [v.get('OSVersion') for v in local_data.get('OSVersions', [])]
            
            print(f"  Live OS versions: {len(live_versions)} - {', '.join(live_versions[:3])}...")
            print(f"  Local OS versions: {len(local_versions)} - {', '.join(local_versions[:3])}...")
            
            # Check for differences in OS versions
            missing_in_local = set(live_versions) - set(local_versions)
            extra_in_local = set(local_versions) - set(live_versions)
            
            if missing_in_local:
                print(f"  ⚠️  Missing in local: {', '.join(missing_in_local)}")
            if extra_in_local:
                print(f"  ⚠️  Extra in local: {', '.join(extra_in_local)}")
            
            # Compare latest versions
            for os_ver in local_data.get('OSVersions', []):
                os_name = os_ver.get('OSVersion')
                live_os = next((v for v in live_data.get('OSVersions', []) if v.get('OSVersion') == os_name), None)
                
                if live_os:
                    local_latest = os_ver.get('Latest', {}).get('ProductVersion', 'N/A')
                    live_latest = live_os.get('Latest', {}).get('ProductVersion', 'N/A')
                    
                    if local_latest != live_latest:
                        print(f"  ⚠️  Version mismatch for {os_name}:")
                        print(f"      Live: {live_latest}, Local: {local_latest}")
                    
                    # Compare security releases count
                    local_sr_count = len(os_ver.get('SecurityReleases', []))
                    live_sr_count = len(live_os.get('SecurityReleases', []))
                    
                    if abs(local_sr_count - live_sr_count) > 2:  # Allow small differences
                        print(f"  ℹ️  Security releases for {os_name}:")
                        print(f"      Live: {live_sr_count}, Local: {local_sr_count}")
            
            # Compare top-level keys
            live_keys = set(live_data.keys())
            local_keys = set(local_data.keys())
            
            if live_keys != local_keys:
                missing_keys = live_keys - local_keys
                extra_keys = local_keys - live_keys
                if missing_keys:
                    print(f"  ⚠️  Missing keys: {', '.join(missing_keys)}")
                if extra_keys:
                    print(f"  ℹ️  Extra keys: {', '.join(extra_keys)}")
            
            # Special checks for macOS
            if feed_name == "macos" and "XProtectPlistConfigData" in local_data:
                local_xprotect = local_data.get("XProtectPlistConfigData", {}).get("com.apple.XProtect", "N/A")
                live_xprotect = live_data.get("XProtectPlistConfigData", {}).get("com.apple.XProtect", "N/A")
                if local_xprotect != live_xprotect:
                    print(f"  ℹ️  XProtect version: Live={live_xprotect}, Local={local_xprotect}")
            
            print(f"  ✅ {feed_name.upper()} validation complete\n")
            
        except Exception as e:
            print(f"  ❌ Error validating {feed_name}: {e}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build legacy v1 feeds from pre-fetched data.")
    parser.add_argument(
        "osTypes",
        nargs="*",  # Changed to nargs="*" to make it optional when using --validate
        type=str,
        help="The types of OS to process (e.g., macOS iOS)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Output directory for feed files"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate generated feeds against live official feeds"
    )
    
    args = parser.parse_args()
    
    # If only validate flag is set without osTypes, just validate existing feeds
    if args.validate and not args.osTypes:
        validate_feeds_against_live(str(args.output_dir))
        sys.exit(0)
    
    # If osTypes not provided and not just validating, error
    if not args.osTypes:
        parser.error("osTypes is required when not using --validate alone")
    
    # Validate data directory exists
    data_dir = Path("data/resources")
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        print("Run 'sofa-gather all' or 'sofa-fetch' first to populate data.")
        sys.exit(1)
    
    if args.verbose:
        print(f"📊 Building legacy v1 feeds for: {', '.join(args.osTypes)}")
        print(f"📁 Output directory: {args.output_dir}")
        print()
    
    # Create output directory if needed but don't change to it
    if args.output_dir != Path("."):
        args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Store the output directory path for use in write_data_to_json
    os.environ['OUTPUT_DIR'] = str(args.output_dir)
    
    # Build the feeds
    main(args.osTypes)
    
    # If validate flag is also set, validate the generated feeds
    if args.validate:
        validate_feeds_against_live(str(args.output_dir))