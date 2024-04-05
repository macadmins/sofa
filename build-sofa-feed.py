import json
import yaml
import os
import argparse
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from collections import defaultdict

import requests
from bs4 import BeautifulSoup, NavigableString


# Load the feed structure template
with open('feed_structure_template_v1.yaml', 'r') as file:
    feed_structure = yaml.safe_load(file)


def load_configurations(config_file_path):
    with open(config_file_path, 'r') as file:
        return json.load(file)
    

def parse_ios_versions_from_config():
    os_versions_str = "iOS 15, iPadOS 15"  # Sample data, replace with your actual data
    os_versions_list = os_versions_str.split(", ")
    os_versions = []

    for version in os_versions_list:
        parts = version.split(" ")
        if len(parts) == 2:  # iOS or iPadOS
            os_type = "iOS" if parts[0] == "iOS" else "iPadOS"
            os_name = parts[1]
            major_version = None  # iOS does not use a sub-version in this context
            os_versions.append((os_type, os_name, major_version))

    return os_versions


def process_os_version(os_type, os_version, name_info):
	rapid_response_prefix = "Rapid Security Response"
	
	# Update pattern to capture macOS, iOS, iPadOS, including "Rapid Security Response"
	pattern = rf"({rapid_response_prefix})?\s*"
	pattern += r"(macOS\s+\w+\s*\d+(?:\.\d+)*(?:\.\d+)*(?:\s*\([a-z]\))?)?\s*"
	pattern += r"((iOS|iPadOS)\s+(\d+(?:\.\d+)?(?:\.\d+)?)(?:\s*\([a-z]\))?)?"
	pattern += r"(\s+and\s+)?"
	pattern += r"((iOS|iPadOS)\s+(\d+(?:\.\d+)?(?:\.\d+)?)(?:\s*\([a-z]\))?)?"
	
	match = re.search(pattern, name_info, re.IGNORECASE)
	
	if match:
		rapid_response = match.group(1) or ""
		macos_part = match.group(2) or ""
		first_os_part = match.group(3) or ""
		second_os_connector = match.group(6) or ""
		second_os_part = match.group(7) or ""
		
		# Ensure proper spacing after "Rapid Security Response" if it's present
		version_str = f"{rapid_response} " if rapid_response else ""
		
		# Concatenating OS parts with appropriate spacing
		if macos_part:
			version_str += f"{macos_part} "
			
		if first_os_part:
			version_str += f"{first_os_part} "
			
		if second_os_connector and second_os_part:
			version_str += f"and {second_os_part}"
			
		return version_str.strip()
	
	return None


def fetch_latest_os_version_info(os_type, os_version_name):
    print(f"Fetching latest: {os_type} {os_version_name}")
    url = "https://gdmf.apple.com/v2/pmv"

    try:
        response = requests.get(url, verify=False)  # Not recommended, but 
        response.raise_for_status()  # This will raise an HTTPError if the response was an error
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    data = response.json()
    os_versions_key = "macOS" if os_type == "macOS" else "iOS"
    filtered_versions = [
        v for v in data.get("AssetSets", {}).get(os_versions_key, [])
        if v.get("ProductVersion", "").startswith(os_version_name.split(' ')[-1] if os_type == "macOS" else os_version_name)
    ]

    if os_type == "iOS":
        filtered_versions = [
            v for v in filtered_versions if "SupportedDevices" in v and any(
                device.startswith("iPad") or device.startswith("iPhone") for device in v["SupportedDevices"]
            )
        ]

    if filtered_versions:
        latest_version = max(filtered_versions, key=lambda x: datetime.strptime(x["PostingDate"], "%Y-%m-%d"))
        return {
            "ProductVersion": latest_version.get("ProductVersion"),
            "Build": latest_version.get("Build"),
            "ReleaseDate": latest_version.get("PostingDate"),
            "ExpirationDate": latest_version.get("ExpirationDate", ""),
            "SupportedDevices": latest_version.get("SupportedDevices", [])
        }

    print(f"No versions matched the criteria for {os_type} {os_version_name}.")
    return None


def fetch_security_releases(os_type, os_version):
    url = "https://support.apple.com/en-us/HT201222"
    response = requests.get(url)
    security_releases = []

    if response.ok:
        html_content = response.text
        soup = BeautifulSoup(html_content, "lxml")
        rows = soup.find_all("tr")

        release_dates = []

        for row in rows:
            cells = row.find_all("td")
            if cells:
                name_info = cells[0].get_text(strip=True)
                os_version_info = process_os_version(os_type, os_version, name_info)
                # Ensure os_version_info matches the targeted version before proceeding
                if os_version_info and os_version in os_version_info:  # Filter based on the targeted OS version
                    link = cells[0].find("a", href=True)
                    if link:
                        link_info = link["href"]
                        cves_exploitation_status = fetch_cves(link_info)
                    else:
                        link_info = None
                        cves_exploitation_status = {}

                    # Use regex to extract ProductVersion from the name_info
                    version_match = re.search(r'\d+(\.\d+)*', name_info)
                    product_version = version_match.group() if version_match else "Unknown"
                    
                    print(f"Processing security release {product_version}, source {name_info}")

                    # Handling the case when the page indicates no published CVE entries
                    if link_info and "no published CVE entries" in fetch_content(link_info).lower():
                        cves_exploitation_status = {}

                    date = cells[-1].get_text(strip=True)
                    release_dates.append(date)

                    # Extract actively exploited CVEs if any
                    actively_exploited_cves = [cve for cve, exploited in cves_exploitation_status.items() if exploited]

                    security_releases.append({
                        "UpdateName": os_version_info,
                        "ProductVersion": product_version,
                        "ReleaseDate": date,
                        "SecurityInfo": link_info if link_info else "This update has no published CVE entries.",
                        "CVEs": cves_exploitation_status,
                        "ActivelyExploitedCVEs": actively_exploited_cves,
                        "UniqueCVEsCount": len(cves_exploitation_status),
                    })

        # Calculate days since previous release
        days_since_previous_release = calculate_days_since_previous_release(release_dates)

        for release in security_releases:
            release_date = release["ReleaseDate"]
            if release_date in days_since_previous_release:
                release["DaysSincePreviousRelease"] = days_since_previous_release[release_date]
            else:
                release["DaysSincePreviousRelease"] = 0

        return security_releases
    else:
        print("Failed to retrieve security releases.")
        return []

def fetch_cves(url):
    response = requests.get(url)
    if not response.ok:
        return None  # Indicate failure to fetch or process CVEs

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    if "no published CVE entries" in html_content:  # Simplistic check; refine as needed
        return {}  # Explicitly indicate no CVEs without error

    cves_info = {}
    text_blocks = []
    processed_cves = set()

    for child in soup.recursiveChildGenerator():
        if isinstance(child, NavigableString) and child.strip():
            text_blocks.append(child.strip())
            cve_ids = find_cves_in_text(child)
            for cve_id in cve_ids:
                if cve_id not in processed_cves:
                    cves_info[cve_id] = is_exploited(" ".join(text_blocks))
                    processed_cves.add(cve_id)
            if len(text_blocks) > 5:  # Maintain recent context
                text_blocks.pop(0)

    return cves_info if cves_info else None  # Return None if no CVEs were found/processed


def is_cve_related(element):
    # Check if the element is likely associated with CVEs
    # When websites change and we fail here, we may check if the element in more depth to see if contains a CVE record
    return True

def find_cves_in_text(text):
    cve_matches = re.findall(r"\bCVE-\d{4,}-\d{4,}\b", text)
    return cve_matches

def is_exploited(text):
    pattern = re.compile(r"Impact:.*Apple is aware.*may have been .*exploited", re.DOTALL)
    return bool(pattern.search(text))

def fetch_cisa_feed_live():
    feed_url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    try:
        response = requests.get(feed_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        feed_data = response.json()
        indexed_feed = {item['cveID']: item for item in feed_data['vulnerabilities']}
        return indexed_feed
    except requests.RequestException as e:
        print(f"Failed to fetch the CISA feed. Error: {e}")
        return None

#  WIP/TO DO - Implement the function to fetch CVEs from the CISA feed later 
def enhance_cve_with_cisa_details(cves_info, cisa_feed):
    """
    Enhance CVEs with dates from the CISA known exploited vulnerabilities feed.

    :param cves_info: Dictionary with CVEs as keys and exploitation status as values.
    :param cisa_feed: Dictionary indexed by CVE IDs containing CISA feed data.
    """
    for cve_id, details in cves_info.items():
        # Find this CVE in the CISA feed
        cisa_entry = cisa_feed.get(cve_id)
        if cisa_entry:
            # Add "DateAdded" and "DueDate" to the CVE details
            details['DateAdded'] = cisa_entry.get('dateAdded')
            details['DueDate'] = cisa_entry.get('dueDate')
    
    return cves_info



def calculate_days_since_previous_release(release_dates):
    days_between_releases = {}
    for i in range(len(release_dates) - 1):
        try:
            next_release_date = parse_flexible_date(release_dates[i])
            current_release_date = parse_flexible_date(release_dates[i + 1])
            days_difference = abs((next_release_date - current_release_date).days)
            days_between_releases[release_dates[i]] = days_difference
        except ValueError as e:
            print(f"Error parsing date: {e}")
    return days_between_releases


def parse_flexible_date(date_str):
    # Check for different formats
    formats = ["%Y-%m-%d", "%d %b %Y"]
    # Try to parse the date string with each format
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    # If parsing fails for all formats, raise an error
    raise ValueError(f"Date format not recognized: {date_str}")


def print_security_releases(releases, os_type):
    print(f"Security releases for {os_type}:")
    for release in releases:
        print(f"OS Version: {release['OSVersion']}")
        print(f"Release Date: {release['ReleaseDate']}")
        print(f"Days Since Previous Release: {release['DaysSincePreviousRelease']}")
        print(f"Security Info: {release['SecurityInfo']}")
        if release['CVEs']:
            print(f"Unique CVEs Count: {release['UniqueCVEsCount']}")
            print("CVEs:")
            for cve in release['CVEs']:
                print(f" - {cve}")
        else:
            print("No CVE entries.")
        print("--------------------------------------------------")


def fetch_content(url):
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        raise Exception(f"Error fetching data from {url}: HTTP {response.status_code}")


def extract_xprotect_versions_and_post_date(catalog_content, pkm_url):
    pkm_content = fetch_content(pkm_url)
    version_info = {}

    if pkm_content:
        root = ET.fromstring(pkm_content)
        for bundle in root.findall(".//bundle"):
            id_attr = bundle.get("id")
            version = bundle.get("CFBundleShortVersionString")
            if "XProtect" in id_attr or "PluginService" in id_attr:
                version_info[id_attr] = version

        post_date_regex = rf"<string>{re.escape(pkm_url)}</string>.*?<date>(.*?)</date>"
        post_date_match = re.search(post_date_regex, catalog_content, re.DOTALL)
        if post_date_match:
            # Ensure the release date is formatted in ISO 8601 format
            release_date = post_date_match.group(1)
            version_info["ReleaseDate"] = format_iso_date(release_date)  # Assumes format_iso_date is implemented

    return version_info


def add_compatible_machines(current_macos_full_version):
    # Extract only the base name of the macOS version, ensure it's lowercase for filename construction
    # Assuming current_macos_full_version is something like "Ventura 13"
    current_macos_name = current_macos_full_version.split(" ")[0].lower()  # This will get "ventura" from "Ventura 13"

    # Dynamically construct the filename based on the macOS name
    filename = f"model_identifier_{current_macos_name}.json"

    # Attempt to open and read the dynamically determined JSON file
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []

    compatible_machines = []
    for entry in data:
        model = entry["Model"]
        url = entry["URL"]
        identifiers = entry["Identifiers"]
        compatible_machines.append({
            "Model": model,
            "URL": url,
            "Identifiers": identifiers
        })

    return compatible_machines


def load_and_tag_model_data(filenames):
    """
    Load model data from given JSON files, tag them with the corresponding OS version, 
    and merge into a structured format..
    
    :param filenames: A list of tuples containing the path to the JSON files and the OS version they represent.
    :return: A dictionary mapping each model to its details including supported OS versions.
    """
    model_info = {}

    for file_path, os_version in filenames:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for model in data:
                for identifier, name in model["Identifiers"].items():
                    if identifier not in model_info:
                        model_info[identifier] = {
                            "MarketingName": name,
                            "SupportedOS": [os_version],
                            "OSVersions": [int(os_version.split()[-1])]
                        }
                    else:
                        model_info[identifier]["SupportedOS"].append(os_version)
                        model_info[identifier]["OSVersions"].append(int(os_version.split()[-1]))
                        # Ensure the marketing name is consistent; if not, log a warning or handle discrepancies
    return model_info



def write_data_to_json(feed_structure, filename):
    """
    Writes the populated feed structure to a JSON file.
    :param feed_structure: The fully populated feed structure.
    :param filename: The name of the file to which the JSON data should be written.
    """
    for os_version in feed_structure['OSVersions']:
        # Assuming 'LatestOS' is correctly structured and needs no iteration
        if 'LatestOS' in os_version:
            os_version['LatestOS']['ReleaseDate'] = format_iso_date(os_version['LatestOS'].get('ReleaseDate', ''))
            if "ExpirationDate" in os_version['LatestOS']:
                os_version['LatestOS']['ExpirationDate'] = format_iso_date(os_version['LatestOS'].get('ExpirationDate', ''))

        # Verify SecurityReleases is a list and then format dates within each release
        if 'SecurityReleases' in os_version and isinstance(os_version['SecurityReleases'], list):
            for release in os_version['SecurityReleases']:
                release['ReleaseDate'] = format_iso_date(release.get('ReleaseDate', ''))

    # Write the structured data to a JSON file
    with open(filename, "w") as json_file:
        json.dump(feed_structure, json_file, indent=4, ensure_ascii=False)


def format_iso_date(date_str):
    formats = ["%Y-%m-%d", "%d %b %Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).replace(microsecond=0).isoformat() + "Z"
        except ValueError:
            pass
    return date_str


def read_and_validate_json(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)

            # Adjusted required keys for a more generic approach
            required_keys = [
                "OSVersions",
                #"LatestOS",  # Generic key for latest OS version info
                #"SecurityReleases",
            ]
            # Additional keys like "XProtectPlistConfigData" and "XProtectPayloads" may not be relevant for all OS types

            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                print(f"Validation error: Missing keys {missing_keys} in {filename}")
            else:
                print(f"Validation passed for {filename}.")
                print(json.dumps(data, indent=4))
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main(os_type):
    # Load configurations from config.json
    config = load_configurations('config.json')

    # Filter software releases for the specified osType
    software_releases = [release for release in config["softwareReleases"] if release["osType"] == os_type]

    print(f"Software releases for {os_type}: {software_releases}")

    # Initialize the feed structure with placeholders
    feed_structure = {
        "lastCheck": datetime.now(timezone.utc).replace(microsecond=0).isoformat() + "Z",
        "OSVersions": []  # To be populated later
    }

    if os_type == "macOS":
        # Fetch and process XProtect data
        catalog_url = "https://swscan.apple.com/content/catalogs/others/index-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog"
        catalog_content = fetch_content(catalog_url)

        plist_url = re.search(r"https.*XProtectPlistConfigData.*?\.pkm", catalog_content).group(0)
        payloads_url = re.search(r"https.*XProtectPayloads.*?\.pkm", catalog_content).group(0)

        plist_info = extract_xprotect_versions_and_post_date(catalog_content, plist_url)
        payloads_info = extract_xprotect_versions_and_post_date(catalog_content, payloads_url)

        # Update feed_structure with the XProtect data
        feed_structure["XProtectPayloads"] = payloads_info
        feed_structure["XProtectPlistConfigData"] = plist_info

        # Example usage of the load_model_data function
        model_files = [
            ("model_identifier_sonoma.json", "macOS Sonoma 14"),
            ("model_identifier_ventura.json", "macOS Ventura 13"),
            ("model_identifier_monterey.json", "macOS Monterey 12")
        ]
        models_info = load_and_tag_model_data(model_files)

        # Add the aggregated models data to the feed structure.
        feed_structure["Models"] = models_info

    elif os_type == "iOS":
        # Initialize os_versions dynamically for iOS
        os_versions = [("iOS", release["name"], None) for release in software_releases]
        print(f"OS versions for {os_type}: {os_versions}")

        # Skip fetching XProtect and "Models" data for iOS
        print(f"Skipping fetching XProtect and 'Models' data for {os_type}.")
    else:
        print("Invalid OS type specified.")

    # Fetch latest OS version information only once for each OS type
    latest_versions = {}
    for release in software_releases:
        os_version_name = release["name"]
        latest_version_info = fetch_latest_os_version_info(os_type, os_version_name)
        if latest_version_info:
            latest_versions[os_version_name] = latest_version_info

    # Fetch and process OS version information
    print("Fetching OS version information...")
    for release in software_releases:
        os_version_name = release["name"]
        latest_version_info = latest_versions.get(os_version_name)
        if latest_version_info:
            # Format dates
            latest_version_info["ReleaseDate"] = format_iso_date(latest_version_info["ReleaseDate"])
            if "ExpirationDate" in latest_version_info:
                latest_version_info["ExpirationDate"] = format_iso_date(latest_version_info["ExpirationDate"])

            if os_type == "macOS":
                # Fetch compatible machines for the macOS version
                compatible_machines = add_compatible_machines(os_version_name)

                # Add the macOS version information along with compatible machines to the feed structure
                feed_structure["OSVersions"].append({
                    "OSVersion": os_version_name,
                    "Latest": latest_version_info,
                    "SecurityReleases": fetch_security_releases(os_type, os_version_name),
                    "SupportedModels": compatible_machines  # Add compatible machines here
                })
            elif os_type == "iOS":
                # For iOS, append without compatible machines
                feed_structure["OSVersions"].append({
                    "OSVersion": os_version_name,
                    "LatestOS": latest_version_info,
                    "SecurityReleases": fetch_security_releases(os_type, os_version_name)
                    # Note: 'SupportedModels' is not included for iOS
                })      
    
    # Determine the filename dynamically based on the os_type argument
    filename = f"{os_type.lower()}_data_feed.json"

    # Finally, write the structured data to a JSON file
    write_data_to_json(feed_structure, filename)

    # Optionally, validate the generated JSON file
    read_and_validate_json(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process OS version information.')
    parser.add_argument('osType', type=str, help='The type of OS to process (macOS or iOS)')

    args = parser.parse_args()

    main(args.osType)