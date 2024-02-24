#!/bin/bash

# Paths to the local XProtect Info.plists
localPlistBundle="/Library/Apple/System/Library/CoreServices/XProtect.bundle/Contents/Info.plist"
localPlistApp="/Library/Apple/System/Library/CoreServices/XProtect.app/Contents/Info.plist"

# URL to the online JSON data
onlineJsonUrl="https://headmin.github.io/xprotect-scan/xprotect_data.json"

# Extract the local versions of XProtect using CFBundleShortVersionString
localVersionBundle=$(defaults read "${localPlistBundle%.plist}" CFBundleShortVersionString)
localVersionApp=$(defaults read "${localPlistApp%.plist}" CFBundleShortVersionString)

# Download the online JSON and extract the XProtect versions
onlineVersionBundle=$(curl -s "$onlineJsonUrl" | grep -o '"com.apple.XProtect": "[^"]*' | awk -F': "' '{print $2}')
onlineVersionApp=$(curl -s "$onlineJsonUrl" | grep -o '"com.apple.XProtectFramework.XProtect": "[^"]*' | awk -F': "' '{print $2}')

# Compare the versions
if [[ "$localVersionBundle" == "$onlineVersionBundle" ]] && [[ "$localVersionApp" == "$onlineVersionApp" ]]; then
    message="XProtect versions are up-to-date. Local bundle version: $localVersionBundle, Online bundle version: $onlineVersionBundle; Local app version: $localVersionApp, Online app version: $onlineVersionApp"
else
    message="XProtect version mismatch. Check for updates."
fi

# Display the message using swiftDialog
swiftDialogCommand="/usr/local/bin/dialog" # Path to swiftDialog installation
"$swiftDialogCommand" --message "$message" --info
