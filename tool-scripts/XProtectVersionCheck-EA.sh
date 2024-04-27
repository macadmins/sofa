#!/bin/zsh
# shellcheck shell=bash

## based on Graham Pugh's version https://github.com/grahampugh/osx-scripts/blob/main/check-xprotect-version/XProtectVersionCheck-EA.sh
#
# Note that this uses plutil so is only compatible with macOS 12+

# URL to the online JSON data
online_json_url="https://sofa.macadmins.io/v1/macos_data_feed.json"
json_data=$(/usr/bin/curl -L -m 3 -s "$online_json_url")
if [[ ! "$json_data" ]]; then
    echo "<result>Could not obtain data</result>"
    exit
fi

# Extract the online version of XProtect configuration data
onlineXProtectVersion=$(/usr/bin/plutil -extract "XProtectPlistConfigData.com\\.apple\\.XProtect" raw - - <<< "$json_data" | /usr/bin/head -n 1)
echo "Online XProtect Version: $onlineXProtectVersion"

# Extract the local installed version of XProtect configuration data
localXProtectVersion=$(/usr/bin/plutil -extract CFBundleShortVersionString raw /Library/Apple/System/Library/CoreServices/XProtect.bundle/Contents/Info.plist)
echo "Local XProtect Version: $localXProtectVersion"

# Extract the online version of XProtect.app
onlineXProtectAppVersion=$(/usr/bin/plutil -extract "XProtectPayloads.com\\.apple\\.XProtectFramework\\.XProtect" raw - - <<< "$json_data" | /usr/bin/head -n 1)
echo "Online XProtect.app Version: $onlineXProtectAppVersion"

# Extract the local installed version of XProtect.app
localXProtectAppVersion=$(/usr/bin/plutil -extract CFBundleShortVersionString raw /Library/Apple/System/Library/CoreServices/XProtect.app/Contents/Info.plist)
echo "Local XProtect.app Version: $localXProtectAppVersion"

# Compare the online version with the installed version for both XProtect and XProtect.app
if [[ "$onlineXProtectVersion" == "$localXProtectVersion" ]] && [[ "$onlineXProtectAppVersion" == "$localXProtectAppVersion" ]]; then
    echo "<result>Pass</result>"
else
    echo "<result>Fail</result>"
fi
