# Standard library imports
import argparse
import json
import os
import re
import ssl
import sys
import hashlib
import xml.etree.ElementTree as Et
from datetime import datetime, timezone

# Third-party imports
import requests
import yaml
from bs4 import BeautifulSoup, NavigableString

# Local library specific imports
current_dir = os.getcwd()
sys.path.insert(0, current_dir)
import certifi
import process_uma


# Load the feed structure template
with open("feed_structure_template_v1.yaml", "r") as file:
    feed_structure = yaml.safe_load(file)


def load_configurations(config_file_path):
    """
    Load configurations from the given configuration file used in main.
    :param config_file_path:
    :return:
    """
    with open(config_file_path, "r") as file:
        return json.load(file)


def process_os_version(os_type, os_version, name_info):
    """
    Process the OS version information from the given name_info. This is a rather odd helper, but needed to scrape
    CVE info as well as rapid response info.
    :param os_type:
    :param os_version:
    :param name_info:
    :return:
    """

    print(f"Processing data - {os_type}: {os_version}, Searching in: {name_info} ")

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
    """
    Fetch the latest version information for the given OS type and version name. Source: Apple's gdmf API.
    :param os_type:
    :param os_version_name:
    :return: The latest version information if found, otherwise None.
    """
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
        v
        for v in data.get("AssetSets", {}).get(os_versions_key, [])
        if v.get("ProductVersion", "").startswith(
            os_version_name.split(" ")[-1] if os_type == "macOS" else os_version_name
        )
    ]

    if os_type == "iOS":
        filtered_versions = [
            v
            for v in filtered_versions
            if "SupportedDevices" in v
            and any(
                device.startswith("iPad") or device.startswith("iPhone")
                for device in v["SupportedDevices"]
            )
        ]

    if filtered_versions:
        latest_version = max(
            filtered_versions,
            key=lambda x: datetime.strptime(x["PostingDate"], "%Y-%m-%d"),
        )
        return {
            "ProductVersion": latest_version.get("ProductVersion"),
            "Build": latest_version.get("Build"),
            "ReleaseDate": latest_version.get("PostingDate"),
            "ExpirationDate": latest_version.get("ExpirationDate", ""),
            "SupportedDevices": latest_version.get("SupportedDevices", []),
        }

    print(f"No versions matched the criteria for {os_type} {os_version_name}.")
    return None


def fetch_security_releases(os_type, os_version):
    """
    Fetch security releases for the given OS type and version, source HT201222 page.
    :param os_type:
    :param os_version:
    :return:
    """
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
                if (
                    os_version_info and os_version in os_version_info
                ):  # Filter based on the targeted OS version
                    link = cells[0].find("a", href=True)
                    if link:
                        link_info = link["href"]
                        cves_exploitation_status = fetch_cves(link_info)
                    else:
                        link_info = None
                        cves_exploitation_status = {}

                    # Use regex to extract ProductVersion from the name_info
                    version_match = re.search(r"\d+(\.\d+)*", name_info)
                    product_version = (
                        version_match.group() if version_match else "Unknown"
                    )

                    print(
                        f"Processing security release {product_version}, source {name_info}"
                    )

                    # Handling the case when the page indicates no published CVE entries
                    if (
                        link_info
                        and "no published CVE entries"
                        in fetch_content(link_info).lower()
                    ):
                        cves_exploitation_status = {}

                    date = cells[-1].get_text(strip=True)
                    release_dates.append(date)

                    # Extract actively exploited CVEs if any
                    actively_exploited_cves = [
                        cve
                        for cve, exploited in cves_exploitation_status.items()
                        if exploited
                    ]

                    security_releases.append(
                        {
                            "UpdateName": os_version_info,
                            "ProductVersion": product_version,
                            "ReleaseDate": date,
                            "SecurityInfo": (
                                link_info
                                if link_info
                                else "This update has no published CVE entries."
                            ),
                            "CVEs": cves_exploitation_status,
                            "ActivelyExploitedCVEs": actively_exploited_cves,
                            "UniqueCVEsCount": len(cves_exploitation_status),
                        }
                    )

        # Calculate days since previous release
        days_since_previous_release = calculate_days_since_previous_release(
            release_dates
        )

        for release in security_releases:
            release_date = release["ReleaseDate"]
            if release_date in days_since_previous_release:
                release["DaysSincePreviousRelease"] = days_since_previous_release[
                    release_date
                ]
            else:
                release["DaysSincePreviousRelease"] = 0

        return security_releases
    else:
        print("Failed to retrieve security releases.")
        return []


def fetch_cves(url):
    """
    Fetch CVEs from the given URL, source HT201222 page.
    :param url:
    :return:
    """
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

    return (
        cves_info if cves_info else None
    )  # Return None if no CVEs were found/processed


def find_cves_in_text(text):
    """
    Find all CVEs in the given text sourced from the HT201222 page.
    :param text:
    :return:
    """
    cve_matches = re.findall(r"\bCVE-\d{4,}-\d{4,}\b", text)
    return cve_matches


def is_exploited(text):
    """
    Check in source HT201222 page if the text indicates that the CVE has been actively exploited.
    :param text:
    :return:
    """
    pattern = re.compile(
        r"Impact:.*Apple is aware.*may have been .*exploited", re.DOTALL
    )
    return bool(pattern.search(text))


def calculate_days_since_previous_release(release_dates):
    """
    Calculate the days between each release date and the previous one.
    :param release_dates:
    :return:
    """
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
    """
    Parse a date string with flexible formats. Sanity to data scraped from the web resources.
    :param date_str:
    :return:
    """
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
    """
    Optionally print the security releases for the given OS type. Not used in the main function, helpful for debugging.
    :param releases:
    :param os_type:
    :return:
    """
    print(f"Security releases for {os_type}:")
    for release in releases:
        print(f"OS Version: {release['OSVersion']}")
        print(f"Release Date: {release['ReleaseDate']}")
        print(f"Days Since Previous Release: {release['DaysSincePreviousRelease']}")
        print(f"Security Info: {release['SecurityInfo']}")
        if release["CVEs"]:
            print(f"Unique CVEs Count: {release['UniqueCVEsCount']}")
            print("CVEs:")
            for cve in release["CVEs"]:
                print(f" - {cve}")
        else:
            print("No CVE entries.")
        print("--------------------------------------------------")


def fetch_content(url):
    """
    Fetch content from the given URL, checking for errors.
    :param url:
    :return:
    """
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        raise Exception(f"Error fetching data from {url}: HTTP {response.status_code}")


def extract_xprotect_versions_and_post_date(catalog_content, pkm_url):
    """
    Extract XProtect versions and post date from the catalog content.
    :param catalog_content:
    :param pkm_url:
    :return:
    """
    pkm_content = fetch_content(pkm_url)
    version_info = {}

    if pkm_content:
        root = Et.fromstring(pkm_content)
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
            version_info["ReleaseDate"] = format_iso_date(
                release_date
            )  # Assumes format_iso_date is implemented

    return version_info


def add_compatible_machines(current_macos_full_version):
    """
    Add compatible machines for the given macOS version, this is only processed for macOS.
    :param current_macos_full_version:
    :return:
    """
    # Extract only the base name of the macOS version, ensure it's lowercase for filename construction
    # Assuming current_macos_full_version is something like "Ventura 13"
    current_macos_name = current_macos_full_version.split(" ")[
        0
    ].lower()  # This will get "ventura" from "Ventura 13"

    # Dynamically construct the filename based on the macOS name
    filename = f"model_identifier_{current_macos_name}.json"

    # Attempt to open and read the dynamically determined JSON file
    try:
        with open(filename, "r") as file:
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


def load_and_tag_model_data(filenames):
    """
    Load model data from given JSON files, tag them with the corresponding OS version,
    and merge into a structured format.

    :param filenames: A list of tuples containing the path to the JSON files and the OS version they represent.
    :return: A dictionary mapping each model to its details including supported OS versions.
    """
    model_info = {}

    for file_path, os_version in filenames:
        with open(file_path, "r") as f:
            data = json.load(f)
            for model in data:
                for identifier, name in model["Identifiers"].items():
                    formatted_os_version = " ".join(os_version.split()[1:]).strip()
                    if identifier not in model_info:
                        model_info[identifier] = {
                            "MarketingName": name,
                            "SupportedOS": [formatted_os_version],
                            "OSVersions": [int(formatted_os_version.split()[-1])],
                        }
                    else:
                        if (
                            formatted_os_version
                            not in model_info[identifier]["SupportedOS"]
                        ):
                            model_info[identifier]["SupportedOS"].append(
                                formatted_os_version
                            )
                            model_info[identifier]["OSVersions"].append(
                                int(formatted_os_version.split()[-1])
                            )
    return model_info


def write_data_to_json(feed_structure, filename):
    """
    Writes the populated feed structure to a JSON file.
    :param feed_structure: The fully populated feed structure.
    :param filename: The name of the file to which the JSON data should be written.
    """
    for os_version in feed_structure["OSVersions"]:
        # Assuming 'Latest' is correctly structured and needs no iteration
        if "Latest" in os_version:
            os_version["Latest"]["ReleaseDate"] = format_iso_date(
                os_version["Latest"].get("ReleaseDate", "")
            )
            if "ExpirationDate" in os_version["Latest"]:
                os_version["Latest"]["ExpirationDate"] = format_iso_date(
                    os_version["Latest"].get("ExpirationDate", "")
                )

        # Verify SecurityReleases is a list and then format dates within each release
        if "SecurityReleases" in os_version and isinstance(
            os_version["SecurityReleases"], list
        ):
            for release in os_version["SecurityReleases"]:
                release["ReleaseDate"] = format_iso_date(release.get("ReleaseDate", ""))

    # Write the structured data to a JSON file
    with open(filename, "w") as json_file:
        json.dump(feed_structure, json_file, indent=4, ensure_ascii=False)


def format_iso_date(date_str):
    """
    Format the date string to ISO 8601 format.
    :param date_str:
    :return:
    """
    formats = ["%Y-%m-%d", "%d %b %Y"]
    for fmt in formats:
        try:
            return (
                datetime.strptime(date_str, fmt).replace(microsecond=0).isoformat()
                + "Z"
            )
        except ValueError:
            pass
    return date_str


def compute_hash(data):
    """
    Compute a SHA-256 hash of the given data.

    :param data: The data to hash, typically a dictionary.
    :return: A hexadecimal string representing the hash of the data.
    """
    json_str = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(json_str).hexdigest()


def write_timestamp_and_hash(os_type, hash_value, filename="timestamp.json"):
    """
    Update the timestamp and hash value for a specific OS type in a JSON file. This function constructs
    a current timestamp and a hash over the full JSON data, and then updates or creates a JSON file 
    with timestamp and hash information for a specified OS type ('macOS' or 'iOS').

    If the file already exists, it reads the existing data and updates it.

    The structure of the maintained timestamp.json looks like:
    {
        "macOS": {
            "LastCheck": "timestamp",
            "UpdateHash": "hash_value"
        },
        "iOS": {
            "LastCheck": "timestamp",
            "UpdateHash": "hash_value"
        }
    }

    :param os_type: The OS type for which to update the timestamp and hash ('macOS' or 'iOS').
    :param hash_value: The hash value computed from the data, represented as a string.
    :param filename: The filename or path to the JSON file where the timestamp and hash
                    should be stored. Defaults to 'timestamp.json', but can be overridden
                    by an environment variable 'TIMESTAMP_FILE_PATH' if 'filename' is None.
    """

    if filename is None:
        # Default to current directory or when run in docker we can specify custom default path
        filename = os.getenv("TIMESTAMP_FILE_PATH", "timestamp.json")

    # Construct the current timestamp
    last_check = datetime.now(timezone.utc).replace(microsecond=0).isoformat() + "Z"

    # Default structure for the timestamp file
    timestamp_data = {"macOS": {}, "iOS": {}}

    # Check if the file already exists and read the existing data
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                timestamp_data = json.load(file)
        except json.JSONDecodeError:
            # If JSON decoding fails, keep the default structure
            pass

    # Update the specific OS section
    timestamp_data[os_type] = {"LastCheck": last_check, "UpdateHash": hash_value}

    # Write the updated data back to the file
    with open(filename, "w") as file:
        json.dump(timestamp_data, file, indent=4)


def read_and_validate_json(filename):
    """
    Read and validate the JSON file. Print verbose output.
    :param filename:
    :return:
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)

            # Adjusted required keys for a more generic approach
            required_keys = [
                "OSVersions",
                # "Latest",  # Generic key for latest OS version info
                # "SecurityReleases",
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
    """
    The main function to process OS version information based on the provided OS type.

    Parameters:
    - os_type (str): The type of OS to process (e.g., "macOS", "iOS").
    """

    # Load configurations from config.json
    config = load_configurations("config.json")

    # Filter software releases for the specified osType
    software_releases = [
        release
        for release in config["softwareReleases"]
        if release["osType"] == os_type
    ]

    print(f"Software releases for {os_type}: {software_releases}")

    # Initialize the feed structure with placeholders
    feed_structure = {
        "OSVersions": [],  # To be populated later
    }

    if os_type == "macOS":
        # Fetch and process XProtect data
        catalog_url = "https://swscan.apple.com/content/catalogs/others/index-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog"
        catalog_content = fetch_content(catalog_url)

        plist_url = re.search(
            r"https.*XProtectPlistConfigData.*?\.pkm", catalog_content
        ).group(0)
        payloads_url = re.search(
            r"https.*XProtectPayloads.*?\.pkm", catalog_content
        ).group(0)

        plist_info = extract_xprotect_versions_and_post_date(catalog_content, plist_url)
        payloads_info = extract_xprotect_versions_and_post_date(
            catalog_content, payloads_url
        )

        # Update feed_structure with the XProtect data
        feed_structure["XProtectPayloads"] = payloads_info
        feed_structure["XProtectPlistConfigData"] = plist_info

        # Example usage of the load_model_data function
        model_files = [
            ("model_identifier_sonoma.json", "macOS Sonoma 14"),
            ("model_identifier_ventura.json", "macOS Ventura 13"),
            ("model_identifier_monterey.json", "macOS Monterey 12"),
        ]
        models_info = load_and_tag_model_data(model_files)

        # Add the aggregated models data to the feed structure.
        feed_structure["Models"] = models_info
        # UMA parsing
        unrefined_products = process_uma.initial_uma_parse(catalog_content.encode())
        print(f"Extracted {len(unrefined_products)} potential UMA packages")
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.load_verify_locations(cafile=certifi.where())
        filtered_dict = {}
        for slug, prod_dict in unrefined_products.items():
            title, build, version = process_uma.get_metadata(
                ctx, prod_dict.get("dist_url")
            )
            if title:
                filtered_dict[slug] = {
                    "title": title,
                    "version": version,
                    "build": build,
                    "apple_slug": slug,
                    "url": prod_dict.get("URL"),
                }
        latest, rest = process_uma.sort_installers(filtered_dict)
        uma_list = {"LatestUMA": latest, "AllPreviousUMA": rest}
        feed_structure["InstallationApps"] = uma_list

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
            latest_version_info["ReleaseDate"] = format_iso_date(
                latest_version_info["ReleaseDate"]
            )
            if "ExpirationDate" in latest_version_info:
                latest_version_info["ExpirationDate"] = format_iso_date(
                    latest_version_info["ExpirationDate"]
                )

            if os_type == "macOS":
                # Fetch compatible machines for the macOS version
                compatible_machines = add_compatible_machines(os_version_name)

                # Add the macOS version information along with compatible machines to the feed structure
                feed_structure["OSVersions"].append(
                    {
                        "OSVersion": os_version_name,
                        "Latest": latest_version_info,
                        "SecurityReleases": fetch_security_releases(
                            os_type, os_version_name
                        ),
                        "SupportedModels": compatible_machines,  # Add compatible machines here
                    }
                )
            elif os_type == "iOS":
                # For iOS, append without compatible machines
                feed_structure["OSVersions"].append(
                    {
                        "OSVersion": os_version_name,
                        "Latest": latest_version_info,
                        "SecurityReleases": fetch_security_releases(
                            os_type, os_version_name
                        ),
                        # Note: 'SupportedModels' is not included for iOS
                    }
                )

    # Compute hash of the feed_structure
    hash_value = compute_hash(feed_structure)

    # Add the hash at the top of the feed_structure
    feed_structure = {
        "UpdateHash": hash_value,  # Insert hash first
        **feed_structure,  # Unpack other content after the hash
    }

    # Determine the filename dynamically based on the os_type argument
    filename = f"{os_type.lower()}_data_feed.json"

    # Finally, write the structured data to a JSON file
    write_data_to_json(feed_structure, filename)

    # Write the timestamp and hash to a JSON file per OS type
    write_timestamp_and_hash(os_type, hash_value)

    # Optionally, validate the generated JSON file
    read_and_validate_json(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process OS version information.")
    parser.add_argument(
        "osType", type=str, help="The type of OS to process (macOS or iOS)"
    )

    args = parser.parse_args()

    main(args.osType)
