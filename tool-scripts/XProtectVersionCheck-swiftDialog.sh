#!/bin/bash

# Paths to the local XProtect Info.plists
local_bundle_info="/Library/Apple/System/Library/CoreServices/XProtect.bundle/Contents/Info.plist"
local_app_info="/Library/Apple/System/Library/CoreServices/XProtect.app/Contents/Info.plist"

# swiftDialog path
swiftDialog_command="/usr/local/bin/dialog" # Path to swiftDialog installation

# URL to the online JSON data
online_json_url="https://sofa.macadmins.io/v1/macos_data_feed.json"
json_data=$(/usr/bin/curl -L -m 3 -s "$online_json_url")
if [[ ! "$json_data" ]]; then
    title="XProtect Version Check"
    icon="SF=network.slash"
    message="WARNING: could not verify latest XProtect version."
    "$swiftDialog_command" --title "$title" --icon "$icon" --message "$message" --info &
    exit
fi

# Extract the local and online (latest) versions of XProtect using CFBundleShortVersionString
local_bundle_version=$(/usr/bin/plutil -extract CFBundleShortVersionString raw "$local_bundle_info")
echo "Local XProtect Version: $local_bundle_version"

latest_bundle_version=$(/usr/bin/plutil -extract "XProtectPlistConfigData.com\\.apple\\.XProtect" raw - - <<< "$json_data" | /usr/bin/head -n 1)
echo "Online XProtect Version: $latest_bundle_version"

local_app_version=$(/usr/bin/plutil -extract CFBundleShortVersionString raw "$local_app_info")
echo "Local XProtect Remediator Version: $local_app_version"

latest_app_version=$(/usr/bin/plutil -extract "XProtectPayloads.com\\.apple\\.XProtectFramework\\.XProtect" raw - - <<< "$json_data" | /usr/bin/head -n 1)
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
