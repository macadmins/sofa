import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup


def fetch_latest_macos_version_info(macos_version_major):
    url = "https://gdmf.apple.com/v2/pmv"
    response = requests.get(url, verify=False)
    data = response.json()

    macos_versions = data.get("AssetSets", {}).get("macOS", [])
    filtered_versions = [
        v
        for v in macos_versions
        if v.get("ProductVersion", "").startswith(macos_version_major)
    ]

    if filtered_versions:
        latest_macos_version = sorted(
            filtered_versions,
            key=lambda x: datetime.strptime(x["PostingDate"], "%Y-%m-%d"),
            reverse=True,
        )[0]

        return {
            "ProductVersion": latest_macos_version.get("ProductVersion"),
            "Build": latest_macos_version.get("Build"),
            "ReleaseDate": latest_macos_version.get("PostingDate"),
            "ExpirationDate": latest_macos_version.get("ExpirationDate"),
        }
    else:
        return None


def get_major_version(macos_full_version):
    # Example input: "macOS Ventura 13"
    # Expected output: "13"
    match = re.search(r"\d+$", macos_full_version)
    return match.group(0) if match else None


def process_os_version(macos_version, name_info):
    # Split the macOS version into name and number for dynamic regex construction
    if " " in macos_version:
        version_name, version_number = macos_version.rsplit(" ", 1)
        version_regex = rf"{version_name} {version_number}.*?(\d+\.\d+(\.\d+)*)?"
    else:
        version_regex = rf"{macos_version}.*?(\d+\.\d+(\.\d+)*)?"

    version_match = re.search(version_regex, name_info)

    if version_match:
        # Construct regex pattern for OSVersion stripping
        perfect_pattern = r"(Rapid Security Response)?macOS\s+\w+\s*\d+(?:\.\d+)*(?:\.\d+)*(?:\s*(?:\(.\))?.*?)?"
        # Applying regex pattern specifically for OSVersion field
        os_version = re.search(perfect_pattern, name_info).group()
        return os_version
    else:
        return None

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


def fetch_security_releases(macos_version):
    # Uncomment the following line to hardcode the macOS version for debugging
    # macos_version = "macOS Sonoma"
    # macos_version = "macOS Ventura"
    # macos_version = "macOS Monterey"

    url = "https://support.apple.com/en-us/HT201222"
    response = requests.get(url)
    security_releases = []

    # Debugging print to show which macOS version is being searched for
    print(f"Fetching security releases for: {macos_version}")

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "lxml")
        rows = soup.find_all("tr")

        release_dates = []

        for row in rows:
            cells = row.find_all("td")
            if cells:
                name_info = cells[0].get_text(strip=True)
                # print(f"Debug: Found name info: {name_info}")  # Debug output

                os_version = process_os_version(macos_version, name_info)
                if os_version:
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

                    security_releases.append(
                        {
                            "OSVersion": os_version,
                            "ReleaseDate": date,
                            "SecurityInfo": link_info,
                            "CVEs": cves,
                            "UniqueCVEsCount": unique_cves_count,
                        }
                    )

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
            version_info["ReleaseDate"] = post_date_match.group(1)

    return version_info


def write_data_to_json(data, filename):
    # Format dates to ISO 8601 standard with timezone
    data["lastCheck"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat() + "Z"
    
    if "LatestMacOS" in data and "ReleaseDate" in data["LatestMacOS"]:
        data["LatestMacOS"]["ReleaseDate"] = format_iso_date(data["LatestMacOS"]["ReleaseDate"])
        
    for release in data.get("SecurityReleases", []):
        release["ReleaseDate"] = format_iso_date(release["ReleaseDate"])

    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)


def format_iso_date(date_str):
    # Try parsing with different formats
    # See https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python
    formats = ["%Y-%m-%d", "%d %b %Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).replace(microsecond=0).isoformat() + "Z"
        except ValueError:
            pass
    # If none of the formats match, return the original string
    return date_str


def read_and_validate_json(filename):
    """Reads and validates the JSON file's content."""
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            # Some validation checks
            required_keys = [
                "OSVersion",
                "LatestMacOS",
                "SecurityReleases",
                "XProtectPlistConfigData",
                "XProtectPayloads",
            ]
            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                print(f"Validation error: Missing keys {missing_keys} in {filename}")
            else:
                print(f"Validation passed for {filename}.")
                # Optionally, print the JSON content, extra visibility during docker run
                print(json.dumps(data, indent=4))
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Fetch catalog content once, as it's common for all macOS versions to be gathered - last checked 2024-02-22
    catalog_url = "https://swscan.apple.com/content/catalogs/others/index-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog"
    catalog_content = fetch_content(catalog_url)

    plist_url = re.search(
        r"https.*XProtectPlistConfigData.*?\.pkm", catalog_content
    ).group(0)
    payloads_url = re.search(r"https.*XProtectPayloads.*?\.pkm", catalog_content).group(
        0
    )

    plist_info = extract_xprotect_versions_and_post_date(catalog_content, plist_url)
    payloads_info = extract_xprotect_versions_and_post_date(
        catalog_content, payloads_url
    )

    # Process each macOS version as specified in the environment variable
    macos_versions = [
        version.strip() for version in os.getenv("MACOS_VERSIONS", "").split(",")
    ]

    for macos_version in macos_versions:
        macos_full_version = f"macOS {macos_version}"
        major_version = get_major_version(macos_full_version)

        # Fetch the latest macOS version information and security releases for each specified version
        latest_macos_info = fetch_latest_macos_version_info(major_version)
        security_releases = fetch_security_releases(macos_full_version)

        # Assemble data for the current macOS version, incorporating the fetched XProtect data
        data_for_version = {
            "OSVersion": macos_full_version,
            "LatestMacOS": latest_macos_info,
            "XProtectPayloads": payloads_info,
            "XProtectPlistConfigData": plist_info,
            "SecurityReleases": security_releases,
        }

        filename = f"muf_data_{macos_version.replace(' ', '_').lower()}.json"
        write_data_to_json(data_for_version, filename)
        print(f"Data for {macos_version} has been written to {filename}")

        # Validate the data written to the JSON file
        read_and_validate_json(filename)


if __name__ == "__main__":
    main()
