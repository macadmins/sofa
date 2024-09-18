#!/bin/bash

# Paths to the local XProtect Info.plists
local_bundle_info="/Library/Apple/System/Library/CoreServices/XProtect.bundle/Contents/Info.plist"
local_app_info="/Library/Apple/System/Library/CoreServices/XProtect.app/Contents/Info.plist"

# swiftDialog path
swiftDialog_command="/usr/local/bin/dialog" # Path to swiftDialog installation

# URL to the online JSON data
online_json_url="https://sofafeed.macadmins.io/v1/macos_data_feed.json"
user_agent="SOFA-dialog-XProtectVersionCheck/1.1"

# local store
json_cache_dir="/private/var/tmp/sofa"
json_cache="$json_cache_dir/macos_data_feed.json"
etag_cache="$json_cache_dir/macos_data_feed_etag.txt"
etag_cache_temp="$json_cache_dir/macos_data_feed_etag_temp.txt"

# ensure local cache folder exists
/bin/mkdir -p "$json_cache_dir"

# check local vs online using etag (only available on macOS 12+)
if [[ -f "$etag_cache" && -f "$json_cache" ]]; then
    etag_old=$(/bin/cat "$etag_cache")
    /usr/bin/curl --compressed --silent --etag-compare "$etag_cache" --etag-save "$etag_cache_temp" --header "User-Agent: $user_agent" "$online_json_url" --output "$json_cache"
    etag_temp=$(/bin/cat "$etag_cache_temp")
    if [[ "$etag_old" == "$etag_temp" || $etag_temp == "" ]]; then
        echo "Cached ETag matched online ETag - cached json file is up to date"
        /bin/rm "$etag_cache_temp"
    else
        echo "Cached ETag did not match online ETag, so downloaded new SOFA json file"
        /bin/mv "$etag_cache_temp" "$etag_cache"
    fi
else
    echo "No e-tag or SOFA json file cached, proceeding to download SOFA json file"
    /usr/bin/curl --compressed --location --max-time 3 --silent --header "User-Agent: $user_agent" "$online_json_url" --etag-save "$etag_cache" --output "$json_cache"
fi

echo

if [[ ! "$json_cache" ]]; then
    title="XProtect Version Check"
    icon="SF=network.slash"
    message="WARNING: could not verify latest XProtect version."
    "$swiftDialog_command" --title "$title" --icon "$icon" --message "$message" --info &
    exit
fi

# Extract the local and online (latest) versions of XProtect using CFBundleShortVersionString
local_bundle_version=$(/usr/bin/plutil -extract CFBundleShortVersionString raw "$local_bundle_info")
echo "Local XProtect Version: $local_bundle_version"

latest_bundle_version=$(/usr/bin/plutil -extract "XProtectPlistConfigData.com\\.apple\\.XProtect" raw "$json_cache" | /usr/bin/head -n 1)
echo "Online XProtect Version: $latest_bundle_version"

local_app_version=$(/usr/bin/plutil -extract CFBundleShortVersionString raw "$local_app_info")
echo "Local XProtect Remediator Version: $local_app_version"

latest_app_version=$(/usr/bin/plutil -extract "XProtectPayloads.com\\.apple\\.XProtectFramework\\.XProtect" raw "$json_cache" | /usr/bin/head -n 1)
echo "Online XProtect Version: $latest_app_version"

# Compare the versions
message="XProtect version: $local_bundle_version (latest $latest_bundle_version)\n\nXProtect Remediator Version: $local_app_version (latest $latest_app_version)"

if [[ "$local_bundle_version" == "$latest_bundle_version" ]] && [[ "$local_app_version" == "$latest_app_version" ]]; then
    title="XProtect versions are up-to-date"
    icon="SF=lock.laptopcomputer"
else
    title="WARNING: XProtect version mismatch"
    icon="SF=lock.open.laptopcomputer"
    message+="\n\nPLEASE CHECK FOR UPDATES"
fi

# Display the message using swiftDialog
"$swiftDialog_command" --title "$title" --icon "$icon" --message "$message" --info &
