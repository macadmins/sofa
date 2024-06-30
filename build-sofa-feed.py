# Standard library imports
import argparse
import glob
import json
import os
import plistlib
import re
import ssl
import sys
import hashlib
import xml.etree.ElementTree as Et
from datetime import datetime, timezone
from urllib.request import urlopen

# Third-party imports
import requests
import yaml
from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup, NavigableString

# Local library specific imports
current_dir = os.getcwd()
sys.path.insert(0, current_dir)
import certifi
import process_uma
import process_ipsw


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

def fetch_gdmf_data():
    """
    Fetch the latest GDMF data, update the cache, and return the data.
    :return: The GDMF data.
    """
    cache_file_path = "cache/gdmf_cached.json"
    log_file_path = "cache/gdmf_log.json"
    max_log_entries = 10

    # Check if the cache file exists, is valid JSON, and output its content
    cached_data, cached_etag = check_cache_file(cache_file_path)
    if cached_data and cached_data != {}:
        print("Validated local cached GDMF data.")
    else:
        cached_data = None

    # Fetch live data if cache is not available or invalid
    url = "https://gdmf.apple.com/v2/pmv"
    try:
        response = requests.get(url, verify=False)  # Not recommended, but used here for simplicity
        response.raise_for_status()  # This will raise an HTTPError if the response was an error
        data = response.json()
        if data and data != {}:  # Only update the cache if the data is not empty
            live_etag = compute_hash(data)
            if live_etag != cached_etag:
                update_cache(cache_file_path, data, live_etag)
                print("Using live gathered GDMF data and updating cache.")
            else:
                print("Live gathered GDMF data is identical to cached data. No update needed.")
            write_gdmf_log(log_file_path, response.status_code, data, max_log_entries)
            return data
        else:
            print("Live GDMF data is empty or invalid. Using cached data if available.")
            if cached_data:
                write_gdmf_log(log_file_path, response.status_code if 'response' in locals() else 'N/A', cached_data, max_log_entries)
                return cached_data
            else:
                write_gdmf_log(log_file_path, response.status_code if 'response' in locals() else 'N/A', {}, max_log_entries)
                return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        # If fetching live data fails, use the cached data if available
        if cached_data:
            print("Using cached GDMF data due to live fetch failure.")
            write_gdmf_log(log_file_path, response.status_code if 'response' in locals() else 'N/A', cached_data, max_log_entries)
            return cached_data
        print("No valid GDMF data available.")
        write_gdmf_log(log_file_path, 'N/A', {}, max_log_entries)
        return None




def check_cache_file(cache_file_path):
    """
    Check if the cache file exists and is valid JSON.
    :param cache_file_path: Path to the cache file.
    :return: The cached data and etag if valid, otherwise None.
    """
    if os.path.exists(cache_file_path):
        try:
            with open(cache_file_path, "r") as cache_file:
                cache_content = json.load(cache_file)
                if "etag" in cache_content and "data" in cache_content:
                    print("Cache file", cache_file_path, "is valid JSON.")
                    print("Cache content:", cache_content["data"])
                    if cache_content["data"] == {}:
                        print("Cache content is empty.")
                    return cache_content["data"], cache_content["etag"]
                else:
                    print("Cache file structure is invalid.")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Failed to read cache file: {e}")
    else:
        print(f"Cache file {cache_file_path} does not exist.")
    return None, None


def update_cache(cache_file_path, data, etag):
    """
    Update the cache file with the provided data and etag.
    :param cache_file_path: Path to the cache file.
    :param data: Data to be written to the cache.
    :param etag: Etag value to be included.
    """
    try:
        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)
        cache_data = {
            "etag": etag,
            "data": data
        }
        with open(cache_file_path, "w") as cache_file:
            json.dump(cache_data, cache_file, indent=4)
        print(f"Cache updated successfully at {cache_file_path}.")
    except Exception as e:
        print(f"Failed to update cache: {e}")


def write_gdmf_log(log_file_path, status_code, data, max_log_entries):
    """
    Update the GDMF log file with the latest request details.
    :param log_file_path: Path to the log file.
    :param status_code: HTTP status code of the request.
    :param data: Data to be logged.
    :param max_log_entries: Maximum number of log entries to keep.
    """
    current_time = datetime.now(timezone.utc).replace(microsecond=0).isoformat() + "Z"
    new_etag = compute_hash(data)
    log_entry = {
        "timestamp": current_time,
        "new_etag": new_etag,
        "status": f"success ({status_code})" if status_code in {200, 201, 202, 301} else f"failed ({status_code})",
        "previous_etag": ""
    }

    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as file:
            try:
                log_data = json.load(file)
            except json.JSONDecodeError:
                log_data = {"latest_etag": {}, "log": []}
    else:
        log_data = {"latest_etag": {}, "log": []}

    if log_data["log"]:
        log_entry["previous_etag"] = log_data["log"][0]["new_etag"]

    log_data["latest_etag"] = {
        "LastCheck": current_time,
        "UpdateHash": new_etag
    }
    log_data["log"].insert(0, log_entry)
    log_data["log"] = sorted(log_data["log"], key=lambda x: x["timestamp"], reverse=True)[:max_log_entries]  # Sort and keep only the latest entries

    with open(log_file_path, "w") as file:
        json.dump(log_data, file, indent=4)



def fetch_latest_os_version_info(os_type, os_version_name, gdmf_data):
    """
    Fetch the latest version information for the given OS type and version name using provided GDMF data.
    :param os_type: The OS type (e.g., "macOS" or "iOS").
    :param os_version_name: The OS version name.
    :param gdmf_data: The GDMF data fetched from the API or cache.
    :return: The latest version information if found, otherwise None.
    """
    print(f"Fetching latest: {os_type} {os_version_name}")

    os_versions_key = "macOS" if os_type == "macOS" else "iOS"
    filtered_versions = [
        v
        for v in gdmf_data.get("PublicAssetSets", {}).get(os_versions_key, [])
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



def fetch_security_releases(os_type, os_version, gdmf_data):
    """
    Fetch security releases for the given OS type and version, source HT201222 page.
    :param os_type:
    :param os_version:
    :param gdmf_data: The GDMF data fetched from the API or cache.
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

                    os_info = fetch_latest_os_version_info(os_type, product_version, gdmf_data)
                    if not os_info:
                        os_info = {}

                    # Handle RSR releases by grabbing letter in ()
                    rsr_release = None
                    if "Rapid Security Response" in os_version_info:
                        rsr_release = re.search(r"\((\w)\)", os_version_info).group(1)

                    security_releases.append(
                        {
                            "UpdateName": os_version_info,
                            "ProductName": os_type,
                            "ProductVersion": product_version,
                            "ReleaseDate": date,
                            "ReleaseType": (
                                f"RSR_{rsr_release}"
                                if rsr_release
                                else "OS"
                            ),
                            "SecurityInfo": (
                                link_info
                                if link_info
                                else "This update has no published CVE entries."
                            ),
                            "SupportedDevices": os_info.get("SupportedDevices", []),
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


def load_rss_data_cache():
    """
    Load RSS data from cache files and return combined data.
    :return combined_data: Combined list of data from all cache files.
    """
    rss_cache_dir = "cache"
    combined_data = []

    cache_files = glob.glob(os.path.join(rss_cache_dir, "*_rss_data.json"))

    for cache_file in cache_files:
        try:
            with open(cache_file, "r") as file:
                data = json.load(file)
                combined_data.extend(data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading cache file - {cache_file}: {e}")

    return combined_data


def write_os_data_to_cache(product_name, data):
    """
    Write updated OS data to the cache.
    :param product_name: The name of the product (operating system) for which the data is being cached.
    :param data: The data to write to the cache.
    """
    rss_cache_dir = "cache"
    os_rss_cache = os.path.join(rss_cache_dir, f"{product_name}_rss_data.json")

    data = sort_data(data, "ReleaseDate")

    try:
        os.makedirs(rss_cache_dir, exist_ok=True)
        with open(os_rss_cache, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error writing to cache file {os_rss_cache}: {e}")


def sort_data(data, sort_by):
    """
    Sort data coming in when needed.
    :param data: Data to be sorted.
    :param sort_by: Key to be sorted by.
    :return sorted_data: Sorted data.
    """
    sorted_data = data
    if data:
        sorted_data = sorted(data, key=lambda x: x[sort_by])

    return sorted_data


def diff_rss_data(feed_results, rss_cache):
    """
    Diff feed results, update cache files for each OS type, and returns a combined list of updated data.
    :param feed_results: Generated feed results.
    :param rss_cache: Combined list of existing OS data from the cache.
    :return data: Combined list of updated data from both OS type and XProtect caches.
    """
    try:
        new_entries = []

        # Get unique product names from feed_results
        product_names = set(entry["ProductName"] for entry in feed_results)

        for product_name in product_names:
            # Filter existing data for the current ProductName
            existing_os_data = [
                item for item in rss_cache if item.get("ProductName") == product_name
            ]

            # Extract unique identifiers for existing data
            existing_os_items = {
                f"{item['ReleaseType']}_{item['ProductVersion']}"
                for item in existing_os_data
                if "ReleaseType" in item
            }
            existing_os_items.update(
                {
                    item["ProductVersion"]
                    for item in existing_os_data
                    if "ReleaseType" not in item
                }
            )

            # Extract new entries
            new_os_entries = [
                entry
                for entry in feed_results
                if entry["ProductName"] == product_name
                and f"{entry['ReleaseType']}_{entry['ProductVersion']}"
                not in existing_os_items
            ]

            # Update cache files if there are new entries
            if new_os_entries:
                updated_data = existing_os_data + new_os_entries
                write_os_data_to_cache(product_name, updated_data)
                new_entries.extend(new_os_entries)
                print(f"RSS: Cache updated for {product_name}")
            else:
                print(f"No updates found for {product_name}")

        # Merge cache and new data entries
        merged_data = rss_cache + new_entries

        # Remove any duplicate entries
        data = remove_dict_duplicates(merged_data)

        # Sort data before return
        data = sort_data(data, "ReleaseDate")

        return data
    except Exception as e:
        print(f"Error diffing RSS data with cache: {e}")
        return data


def create_rss_json_data(feed_structure):
    """
    Pull Security Releases for all OSVersions.
    :param feed_structure: The fully populated feed structure.
    :return feed_list: Sorted list of entries.
    """
    try:
        feed_list = []

        # For each OS Version, retrieve SecurityReleases and add to
        # the end of the populated list
        for os_version in feed_structure["OSVersions"]:
            security_releases = os_version.get("SecurityReleases", [])
            feed_list.extend(security_releases)

        # Handle XProtect data separately and create entries
        # that will eventually be added to cache. They should
        # mimic what other entries look like.
        if "XProtectPlistConfigData" in feed_structure:
            config_data = feed_structure["XProtectPlistConfigData"]
            config_data_version = config_data.get("com.apple.XProtect", "")
            config_date = config_data.get("ReleaseDate", "")

            feed_list.extend(
                [
                    {
                        "UpdateName": f"XProtect Plist Config {config_data_version}",
                        "ProductName": "XProtect",
                        "ProductVersion": config_data_version,
                        "ReleaseType": "Config",
                        "ReleaseDate": config_date,
                    }
                ]
            )

        if "XProtectPayloads" in feed_structure:
            payload_data = feed_structure.get("XProtectPayloads", {})
            remediator_version = payload_data.get(
                "com.apple.XProtectFramework.XProtect", ""
            )
            plugin_service = payload_data.get(
                "com.apple.XprotectFramework.PluginService", ""
            )
            payload_date = payload_data.get("ReleaseDate", "")

            feed_list.extend(
                [
                    {
                        "UpdateName": f"XProtect Remediator {remediator_version}",
                        "ProductName": "XProtect",
                        "ProductVersion": remediator_version,
                        "ReleaseType": "Remediator",
                        "ReleaseDate": payload_date,
                    },
                    {
                        "UpdateName": f"XProtect Plug-in Service {plugin_service}",
                        "ProductName": "XProtect",
                        "ProductVersion": plugin_service,
                        "ReleaseType": "Plug-in",
                        "ReleaseDate": payload_date,
                    },
                ]
            )

        return feed_list
    except Exception as e:
        print(f"Error creating RSS JSON data: {e}")
        return []


def write_data_to_rss(sorted_feed, filename):
    """
    Write the sorted feed to a RSS feed.
    :param sorted_feed: Sorted list from diff_rss_data function.
    :param filename: The name of the file to which the RSS feed should be written.
    """
    # Escape if empty list
    if not sorted_feed:
        print("No entries to write. sorted_feed is empty.")
        return

    try:
        # Set the primary feed information
        feed_gen = FeedGenerator()
        feed_gen.id("https://sofa.macadmins.io")
        feed_gen.title("SOFA - RSS Update Feed")
        feed_gen.description(
            "This feed includes updates on OS versions and security info."
        )
        feed_gen.author({"name": "Mac Admins"})
        feed_gen.link(href="https://sofa.macadmins.io", rel="alternate")
        feed_gen.logo("https://sofa.macadmins.io/images/custom_logo.png")
        feed_gen.subtitle("Simple Organized Feed for Apple Software Updates")
        feed_gen.link(href=f"https://sofa.macadmins.io/v1/{filename}", rel="self")
        feed_gen.language("en")

        # For each item in the sorted list, create a new entry in RSS Feed
        for release in sorted_feed:
            feed_entry = feed_gen.add_entry()
            feed_entry.id(
                f"{release['ProductName']}_{release['ReleaseType']}_{release['ProductVersion']}"
            )
            feed_entry.title(release["UpdateName"])
            feed_entry.link(link={"href": "https://sofa.macadmins.io/"})

            description = ""

            if "UniqueCVEsCount" in release:
                description += (
                    f"Vulnerabilities Addressed: {release['UniqueCVEsCount']}<br>"
                )

            if "CVEs" in release:
                exploited = sum(value is True for value in release["CVEs"].values())
                description += f"Exploited CVE(s): {exploited}<br>"

            if "DaysSincePreviousRelease" in release:
                description += (
                    f"Days to Prev. Release: {release['DaysSincePreviousRelease']}"
                )

            feed_entry.description(description)
            publication_date = release["ReleaseDate"]
            feed_entry.published(publication_date)

        feed_gen.rss_file(filename, pretty=True)
    except Exception as e:
        print(f"Error writing RSS feed: {e}")


def remove_dict_duplicates(data):
    """
    Remove duplicate dictionaries from a list.
    :param data: A list of dictionaries to be deduplicated.
    :return unique_list: A list of dictionaries with duplicates removed.
    """
    new_set = set()
    unique_list = []
    for item in data:
        # Serialize the dictionary into a JSON string
        item_tuple = item
        if isinstance(item, (list, dict)):
            item_tuple = json.dumps(item, sort_keys=True)

        if item_tuple not in new_set:
            new_set.add(item_tuple)
            unique_list.append(item)

    return unique_list


def format_iso_date(date_str):
    """
    Format the date string to ISO 8601 format.
    :param date_str: Date string to be formatted
    :return: ISO 8601 formatted date string or a hardcoded date if the input is "Preinstalled"
    """
    if date_str == "Preinstalled":
        # Return October 25th, 2021 in ISO 8601 format
        return "2021-10-25T00:00:00Z"

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


def compute_hash(data):
    """
    Compute a SHA-256 hash of the given data.

    :param data: The data to hash, typically a dictionary.
    :return: A hexadecimal string representing the hash of the data.
    """
    json_str = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(json_str).hexdigest()


def write_timestamp_and_hash(os_type, hash_value, filename=None):
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


def process_os_type(os_type, config, gdmf_data):
    """
    Called in main function, process the given OS type (macOS, iOS) and update the feed structure.

    :param os_type: The OS type to process.
    :param config: The configuration data loaded from the config.json file.
    :param gdmf_data: The GDMF data fetched from the API or cache.
    """
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
        # ipsw (latest/'most prevalent' in mesu only as of v1) parsing
        mesu_url: str = (
            "https://mesu.apple.com/assets/macos/com_apple_macOSIPSW/com_apple_macOSIPSW.xml"  # noqa: E501 pylint: disable=line-too-long
        )
        try:
            with urlopen(mesu_url, context=ctx) as response:
                mesu_cat = response.read()
        except (Exception, OSError) as erroir:  # pylint: disable=broad-exception-caught
            print(f"Error fetching mesu assets, {erroir}")
            raise
        mesu_catalog: dict = plistlib.loads(mesu_cat)
        restore_datas = process_ipsw.extract_ipsw_raw(mesu_catalog)
        prevalent_url, prevalent_build, prevalent_version = (
            process_ipsw.process_ipsw_data(restore_datas)
        )
        apple_slug = process_ipsw.process_slug(prevalent_url)
        print(f"Extracted IPSW\n{prevalent_url}")
        feed_structure["InstallationApps"]["LatestMacIPSW"] = {
            "macos_ipsw_url": prevalent_url,
            "macos_ipsw_build": prevalent_build,
            "macos_ipsw_version": prevalent_version,
            "macos_ipsw_apple_slug": apple_slug,
        }

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
        latest_version_info = fetch_latest_os_version_info(os_type, os_version_name, gdmf_data)
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
                latest_security_info = fetch_security_releases(
                    os_type, latest_version_info["ProductVersion"], gdmf_data
                )
                if latest_security_info:
                    latest_version_info["SecurityInfo"] = latest_security_info[0][
                        "SecurityInfo"
                    ]
                    latest_version_info["CVEs"] = latest_security_info[0]["CVEs"]
                    latest_version_info["ActivelyExploitedCVEs"] = latest_security_info[
                        0
                    ]["ActivelyExploitedCVEs"]
                    latest_version_info["UniqueCVEsCount"] = latest_security_info[0][
                        "UniqueCVEsCount"
                    ]

                # Fetch compatible machines for the macOS version
                compatible_machines = add_compatible_machines(os_version_name)

                # Add the macOS version information along with compatible machines to the feed structure
                feed_structure["OSVersions"].append(
                    {
                        "OSVersion": os_version_name,
                        "Latest": latest_version_info,
                        "SecurityReleases": fetch_security_releases(
                            os_type, os_version_name, gdmf_data
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
                            os_type, os_version_name, gdmf_data
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
    data_feed_filename = f"{os_type.lower()}_data_feed.json"

    # Finally, write the structured data to a JSON file
    write_data_to_json(feed_structure, data_feed_filename)

    # Data for RSS feed and create separate XProtect entries
    data_feed = create_rss_json_data(feed_structure)

    # Write the timestamp and hash to a JSON file per OS type
    write_timestamp_and_hash(os_type, hash_value)

    # Optionally, validate the generated JSON file
    read_and_validate_json(data_feed_filename)

    # Return data for use for feeds
    return data_feed



def main(os_types):
    """
    The main function to process OS version information based on the provided OS types.

    Parameters:
    - os_types (list of str): The types of OS to process (e.g., ["macOS", "iOS"]).
    """
    feed_results = []

    # Load configurations from config.json
    config = load_configurations("config.json")

    # Fetch GDMF data once and use it across all OS types
    gdmf_data = fetch_gdmf_data()

    if gdmf_data is None:
        print("Failed to fetch GDMF data and no valid cached data available.")
        return

    # Load all OS RSS data from cache
    rss_cache = load_rss_data_cache()

    # Process per os_type
    for os_type in os_types:
        result = process_os_type(os_type, config, gdmf_data)
        feed_results.extend(result)

    # Write out feed from data returned in dictionary
    # to RSS XML file
    rss_data = diff_rss_data(feed_results, rss_cache)
    write_data_to_rss(rss_data, "rss_feed.xml")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process OS version information.")
    parser.add_argument(
        "osTypes",
        nargs="+",
        type=str,
        help="The types of OS to process (e.g., macOS iOS)",
    )

    args = parser.parse_args()

    main(args.osTypes)
