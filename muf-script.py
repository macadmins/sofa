import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup


# Temporarily set the environment variable for this script
# os.environ['OS_VERSIONS'] = "Sonoma 14, Monterey 12, Ventura 13, iOS 17, iOS 16"

def parse_os_versions_from_env():
    os_versions_str = os.getenv("OS_VERSIONS", "")
    os_versions_list = os_versions_str.split(", ")
    os_versions = []

    for version in os_versions_list:
        parts = version.split(" ")
        if len(parts) == 3:  # macOS with a major version number, e.g., "Sonoma 14"
            os_type = "macOS"
            os_name = parts[0]
            major_version = parts[1]
        elif len(parts) == 2:  # macOS without a specified major version or iOS
            if "iOS" in parts[0]:
                os_type = "iOS"
                os_name = parts[1]
                major_version = None  # iOS does not use a sub-version in this context
            else:
                os_type = "macOS"
                os_name = parts[0]
                major_version = parts[1]
        os_versions.append((os_type, os_name, major_version))

    return os_versions


def process_os_version(os_type, os_version, name_info):
    # Dynamically adjust the regex pattern based on the OS type
    if os_type == "macOS":
        version_regex_pattern = rf"{os_type}\s+{os_version}.*?(\d+\.\d+(\.\d+)*)?"
    elif os_type == "iOS":
        version_regex_pattern = rf"{os_type}\s*{os_version}.*?(\d+)"
    else:
        # Handle other OS types or return None if OS type is unsupported
        return None

    version_match = re.search(version_regex_pattern, name_info)

    if version_match:
        # For macOS, we might still need the full pattern including the OS name, version, and potential minor updates
        if os_type == "macOS":
            perfect_pattern = r"(Rapid Security Response)?macOS\s+\w+\s*\d+(?:\.\d+)*(?:\.\d+)*(?:\s*(?:\(.\))?.*?)?"
            os_version_full = re.search(perfect_pattern, name_info).group()
        elif os_type == "iOS":
            # For iOS, the original match may already suffice, or you might want to refine this based on actual page content
            os_version_full = version_match.group(0)
        else:
            os_version_full = None

        return os_version_full
    else:
        return None


def fetch_latest_os_version_info(os_type, os_version_name):
    print(f"Fetching latest:{os_type}:{os_version_name}")
    url = "https://gdmf.apple.com/v2/pmv"
    response = requests.get(url, verify=False)  # Note: Adjust SSL verification as per your setup
    if not response.ok:
        print(f"Failed to fetch data from {url}. HTTP status code: {response.status_code}")
        return None

    data = response.json()
    os_versions_key = "macOS" if os_type == "macOS" else "iOS"
    os_versions = data.get("AssetSets", {}).get(os_versions_key, [])
    os_version_major_str = os_version_name.split(' ')[-1] if os_type == "macOS" else os_version_name

    # Filter versions for the specific major version string
    filtered_versions = [v for v in os_versions if v.get("ProductVersion", "").startswith(os_version_major_str)]

    # For iOS, further filter to ensure only those with SupportedDevices for iPad and iPhone are considered
    if os_type == "iOS":
        filtered_versions = [v for v in filtered_versions if "SupportedDevices" in v and any(device.startswith("iPad") or device.startswith("iPhone") for device in v["SupportedDevices"])]

    # Sort and pick the latest version by PostingDate
    if filtered_versions:
        latest_os_version = sorted(filtered_versions, key=lambda x: datetime.strptime(x["PostingDate"], "%Y-%m-%d"), reverse=True)[0]
        result = {
            "ProductVersion": latest_os_version.get("ProductVersion"),
            "Build": latest_os_version.get("Build"),
            "ReleaseDate": format_iso_date(latest_os_version.get("PostingDate")),
            "ExpirationDate": format_iso_date(latest_os_version.get("ExpirationDate")),
            "SupportedDevices": latest_os_version.get("SupportedDevices", [])  # Ensure SupportedDevices is always included, even if empty
        }
        return result

    print(f"No versions matched the criteria for {os_type} {os_version_name}.")
    return None


def fetch_security_releases(os_type, os_version):
    url = "https://support.apple.com/en-us/HT201222"
    response = requests.get(url)
    security_releases = []

    print(f"Fetching security releases for: {os_type} {os_version}")

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "lxml")
        rows = soup.find_all("tr")

        release_dates = []

        for row in rows:
            cells = row.find_all("td")
            if cells:
                name_info = cells[0].get_text(strip=True)

                # Adjust process_os_version to handle different OS types
                os_version_info = process_os_version(os_type, os_version, name_info)
                if os_version_info:
                    link = cells[0].find("a", href=True)
                    if link:
                        link_info = link["href"]
                        cves = fetch_cves(link_info)
                        unique_cves_count = len(set(cves))
                    else:
                        link_info = "This update has no published CVE entries."
                        cves = []
                        unique_cves_count = 0
                    date = cells[-1].get_text(strip=True)
                    release_dates.append(date)

                    security_releases.append(
                        {
                            "OSVersion": os_version_info,
                            "ReleaseDate": date,
                            "SecurityInfo": link_info,
                            "CVEs": cves,
                            "UniqueCVEsCount": unique_cves_count,
                        }
                    )

        # Assume calculate_days_since_previous_release function exists
        days_since_previous_release = calculate_days_since_previous_release(release_dates)

        for release in security_releases:
            release["DaysSincePreviousRelease"] = days_since_previous_release.get(release["ReleaseDate"], 0)

        return security_releases
    else:
        print("Failed to retrieve security releases.")
        return []


def fetch_cves(url):
    response = requests.get(url)
    cves = set()
    if response.ok:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        # Look for specific keywords related to CVEs
        cve_keywords = ["CVE", "Common Vulnerabilities and Exposures"]
        for keyword in cve_keywords:
            # Search for the keyword in the page content
            keyword_elements = soup.find_all(string=re.compile(keyword))
            for element in keyword_elements:
                # Check if the keyword is associated with CVEs
                if is_cve_related(element):
                    # Extract CVEs from the element's text
                    cves.update(find_cves_in_text(element))

    # Convert set to a list , then sort it
    sorted_cves = sorted(list(cves), reverse=True)  # Sort in reverse order, to have latest first
    return sorted_cves


def is_cve_related(element):
    # Check if the element is likely associated with CVEs
    # When websites change and we fail here, we may check if the element in more depth to see if contains a CVE record
    return True


def find_cves_in_text(text):
    cve_matches = re.findall(r"\bCVE-\d{4,}-\d{4,}\b", text)
    return cve_matches


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


def write_data_to_json(data, filename):
    # Ensure the 'lastCheck' timestamp is added
    data["lastCheck"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat() + "Z"

    # Format the release date in 'LatestVersionInfo'
    if "LatestVersionInfo" in data and data["LatestVersionInfo"] is not None:
        data["LatestVersionInfo"]["ReleaseDate"] = format_iso_date(data["LatestVersionInfo"]["ReleaseDate"])
        if "ExpirationDate" in data["LatestVersionInfo"]:  # Optional: Check if ExpirationDate exists
            data["LatestVersionInfo"]["ExpirationDate"] = format_iso_date(data["LatestVersionInfo"]["ExpirationDate"])

    # Format the release dates in 'SecurityReleases'
    for release in data.get("SecurityReleases", []):
        release["ReleaseDate"] = format_iso_date(release["ReleaseDate"])

    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

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
                "OSVersion",
                "LatestOS",  # Generic key for latest OS version info
                "SecurityReleases",
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


def main():
    os_versions = parse_os_versions_from_env()
    print(f"OS versions: {os_versions}")

    for os_type, name, version in os_versions:
        if os_type == "macOS" and version is not None:
            os_version_name = f"{name} {version}"
        else:
            os_version_name = name  # For iOS, use the name directly, as version is None

        latest_version_info = fetch_latest_os_version_info(os_type, os_version_name)
        print(latest_version_info)

        if latest_version_info:
            latest_version_info["ReleaseDate"] = format_iso_date(latest_version_info["ReleaseDate"])
            if "ExpirationDate" in latest_version_info:
                latest_version_info["ExpirationDate"] = format_iso_date(latest_version_info["ExpirationDate"])

        latest_version_key = "LatestOS" if os_type == "macOS" else "LatestOS"
        security_releases = fetch_security_releases(os_type, os_version_name)

        # Filter and add compatible machines for the current macOS version
        compatible_machines = add_compatible_machines(os_version_name)

        combined_data = {
            "lastCheck": datetime.now(timezone.utc).replace(microsecond=0).isoformat() + "Z",
            "OSVersion": f"{os_type} {os_version_name}",
            latest_version_key: latest_version_info,
            "SecurityReleases": security_releases,
        }

        if os_type == "macOS":

            compatible_machines = add_compatible_machines(os_version_name)
            combined_data["SupportedModels"] = compatible_machines

            catalog_url = "https://swscan.apple.com/content/catalogs/others/index-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog"
            catalog_content = fetch_content(catalog_url)

            # Extract URLs for XProtect data
            plist_url = re.search(r"https.*XProtectPlistConfigData.*?\.pkm", catalog_content).group(0)
            payloads_url = re.search(r"https.*XProtectPayloads.*?\.pkm", catalog_content).group(0)

            # Fetch and process XProtect data
            plist_info = extract_xprotect_versions_and_post_date(catalog_content, plist_url)
            payloads_info = extract_xprotect_versions_and_post_date(catalog_content, payloads_url)

            # Format ReleaseDate in ISO format
            if "ReleaseDate" in plist_info:
                plist_info["ReleaseDate"] = format_iso_date(plist_info["ReleaseDate"])
            if "ReleaseDate" in payloads_info:
                payloads_info["ReleaseDate"] = format_iso_date(payloads_info["ReleaseDate"])

            # Incorporate XProtect data into combined_data
            combined_data.update({
                "XProtectPayloads": payloads_info,
                "XProtectPlistConfigData": plist_info,
            })

        filename = f"{os_type.lower()}_{os_version_name.lower().replace(' ', '_')}.json"
        write_data_to_json(combined_data, filename)

         # Validate the data written to the JSON file
        read_and_validate_json(filename)

if __name__ == "__main__":
    main()