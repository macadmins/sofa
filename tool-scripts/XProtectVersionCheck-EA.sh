#!/bin/zsh
# shellcheck shell=bash

## based on Graham Pugh's version https://github.com/grahampugh/osx-scripts/blob/main/check-xprotect-version/XProtectVersionCheck-EA.sh

# URL to the online JSON data
onlineJsonUrl="https://macadmins.github.io/sofa/v1/macos_data_feed.json"

# Extract the online version of XProtect configuration data
onlineXProtectVersion=$(curl -s "$onlineJsonUrl" | grep -o '"com.apple.XProtect": "[^"]*' | awk -F': "' '{print $2}')
echo "Online XProtect Version: $onlineXProtectVersion"

# Extract the online version of XProtect.app
onlineXProtectAppVersion=$(curl -s "$onlineJsonUrl" | grep -o '"com.apple.XProtectFramework.XProtect": "[^"]*' | awk -F': "' '{print $2}')
echo "Online XProtect.app Version: $onlineXProtectAppVersion"

# Extract the local installed version of XProtect configuration data
localXProtectVersion=$(defaults read /Library/Apple/System/Library/CoreServices/XProtect.bundle/Contents/Info.plist CFBundleShortVersionString)
echo "Local XProtect Version: $localXProtectVersion"

# Extract the local installed version of XProtect.app
localXProtectAppVersion=$(defaults read /Library/Apple/System/Library/CoreServices/XProtect.app/Contents/Info.plist CFBundleShortVersionString)
echo "Local XProtect.app Version: $localXProtectAppVersion"

# Compare the online version with the installed version for both XProtect and XProtect.app
if [[ "$onlineXProtectVersion" == "$localXProtectVersion" ]] && [[ "$onlineXProtectAppVersion" == "$localXProtectAppVersion" ]]; then
    echo "<result>Pass</result>"
else
    echo "<result>Fail</result>"
fi
