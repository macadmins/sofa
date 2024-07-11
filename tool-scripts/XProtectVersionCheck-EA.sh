#!/bin/zsh --no-rcs
# shellcheck shell=bash

## based on Graham Pugh's version https://github.com/grahampugh/osx-scripts/blob/main/check-xprotect-version/XProtectVersionCheck-EA.sh
#
# To use in a Smart Groups to scope computers that are not up to date:
#   XProtect Version Check - is - Fail
#
# Note that this uses plutil so is only compatible with macOS 12+

# autoload is-at-least module for version comparisons
autoload is-at-least

# URL to the online JSON data
online_json_url="https://sofa.macadmins.io/v1/macos_data_feed.json"
user_agent="SOFA-Jamf-EA-XProtectVersionCheck/1.0"

# local store
json_cache_dir="/private/tmp/sofa"
json_cache="$json_cache_dir/macos_data_feed.json"
etag_cache="$json_cache_dir/macos_data_feed_etag.txt"

# ensure local cache folder exists
/bin/mkdir -p "$json_cache_dir"

# check local vs online using etag
if [[ -f "$etag_cache" && -f "$json_cache" ]]; then
    if /usr/bin/curl --silent --etag-compare "$etag_cache" --header "User-Agent: $user_agent" "$online_json_url" --output /dev/null; then
        echo "Cached e-tag matches online e-tag - cached json file is up to date"
    else
        echo "Cached e-tag does not match online e-tag, proceeding to download SOFA json file"
        /usr/bin/curl --location --max-time 3 --silent --header "User-Agent: $user_agent" "$online_json_url" --etag-save "$etag_cache" --output "$json_cache"
    fi
else
    echo "No e-tag cached, proceeding to download SOFA json file"
    /usr/bin/curl --location --max-time 3 --silent --header "User-Agent: $user_agent" "$online_json_url" --etag-save "$etag_cache" --output "$json_cache"
fi

echo

if [[ ! -f "$json_cache" ]]; then
    echo "<result>Could not obtain data</result>"
    exit
elif ! plutil -extract "UpdateHash" raw "$json_cache" > /dev/null; then
    echo "<result>Could not obtain data</result>"
    exit
fi

# 1. Get model (DeviceID)
model=$(/usr/sbin/sysctl -n hw.model)
echo "Model Identifier: $model"

# 2. Get current system OS
system_version=$( /usr/bin/sw_vers -productVersion )
system_os=$(cut -d. -f1 <<< "$system_version")
echo "System Version: $system_version"

# exit if less than macOS 12
if ! is-at-least 12 "$system_os"; then
    echo "<result>Unsupported macOS</result>"
    exit
fi

echo

# Extract the online version of XProtect configuration data
onlineXProtectVersion=$(/usr/bin/plutil -extract "XProtectPlistConfigData.com\\.apple\\.XProtect" raw "$json_cache" | /usr/bin/head -n 1)
echo "Online XProtect Version: $onlineXProtectVersion"

# Extract the local installed version of XProtect configuration data
localXProtectVersion=$(/usr/bin/plutil -extract CFBundleShortVersionString raw /Library/Apple/System/Library/CoreServices/XProtect.bundle/Contents/Info.plist)
echo "Local XProtect Version: $localXProtectVersion"

# Extract the online version of XProtect.app
onlineXProtectAppVersion=$(/usr/bin/plutil -extract "XProtectPayloads.com\\.apple\\.XProtectFramework\\.XProtect" raw "$json_cache" | /usr/bin/head -n 1)
echo "Online XProtect.app Version: $onlineXProtectAppVersion"

# Extract the local installed version of XProtect.app
localXProtectAppVersion=$(/usr/bin/plutil -extract CFBundleShortVersionString raw /Library/Apple/System/Library/CoreServices/XProtect.app/Contents/Info.plist)
echo "Local XProtect.app Version: $localXProtectAppVersion"

echo

# Compare the online version with the installed version for both XProtect and XProtect.app
if [[ "$onlineXProtectVersion" == "$localXProtectVersion" ]] && [[ "$onlineXProtectAppVersion" == "$localXProtectAppVersion" ]]; then
    echo "<result>Pass</result>"
else
    echo "<result>Fail</result>"
fi
