#!/bin/zsh --no-rcs
# shellcheck shell=bash

# A Jamf Pro Extension Attribute script to check if the local system has any unpatched CVEs
# by Graham Pugh

# The result string shows the total number of unpatched CVEs on the system 
# plus the number of unpatched, actively exploited CVEs
#
# To use in Smart Groups:
#   To check only for Active Exploits:
#   macOS CVE Check - matches regex - ActiveExploits:[1-9]
#
#   To check for any CVEs:
#   macOS CVE Check - matches regex - CVEs:[1-9]
#
# Note that this uses plutil so is only compatible with macOS 12+

# autoload is-at-least module for version comparisons
autoload is-at-least

# URL to the online JSON data
online_json_url="https://sofa.macadmins.io/v1/macos_data_feed.json"
json_data=$(/usr/bin/curl -L -m 3 -s "$online_json_url")
if [[ ! "$json_data" ]]; then
    echo "<result>Could not obtain data</result>"
    exit
fi

# 1. Get model (DeviceID)
device_info=$(/usr/sbin/ioreg -c IOPlatformExpertDevice -d 2)
model=$(/usr/bin/grep \"model\" <<< "$device_info" | /usr/bin/awk -F '<"|">' '{ print $2 }')
echo "Model Identifier: $model"

# 2. Get current system OS
system_version=$( /usr/bin/sw_vers -productVersion )
# system_version=14.1  # UNCOMMENT TO TEST OLDER VERSIONS
system_os=$(cut -d. -f1 <<< "$system_version")
echo "System Version: $system_version"

# exit if less than macOS 12
if ! is-at-least 12 "$system_os"; then
    echo
    echo "<result>Unsupported macOS</result>"
    exit
fi

echo
# 3. idenfity latest compatible major OS
latest_compatible_os=$(/usr/bin/plutil -extract "Models.$model.SupportedOS.0" raw -expect string - - <<< "$json_data" | /usr/bin/head -n 1 | cut -d' ' -f2)
echo "Latest Compatible macOS: $latest_compatible_os"

# 4. Get OSVersions.Latest.ProductVersion
for i in {0..3}; do
    os_version=$(/usr/bin/plutil -extract "OSVersions.$i.OSVersion" raw - - <<< "$json_data" | /usr/bin/head -n 1 | grep -v "<stdin>" | cut -d' ' -f2)
    if [[ $os_version ]]; then
        if [[ "$os_version" == "$latest_compatible_os" ]]; then
            product_version=$(/usr/bin/plutil -extract "OSVersions.$i.Latest.ProductVersion" raw - - <<< "$json_data" | /usr/bin/head -n 1)
            echo "Latest Compatible macOS Version: $product_version"
        fi
        if [[ "$os_version" == "$system_os" ]]; then
            os_position=$i
        fi
    fi
done

# set counts
cves=0
exploits=0

# 5. Compare system with latest compatible
if ! is-at-least "$product_version" "$system_version"; then
    echo
    # work through each previous version counting the CVEs
    for j in {0..20}; do
        product_version=$(/usr/bin/plutil -extract "OSVersions.$os_position.SecurityReleases.$j.ProductVersion" raw - - <<< "$json_data" 2>/dev/null | grep -v "<stdin>")

        if [[ "$product_version" == "$system_version" ]]; then
            break
        fi

        if [[ $product_version ]]; then
            cves_in_version=$(/usr/bin/plutil -extract "OSVersions.$os_position.SecurityReleases.$j.UniqueCVEsCount" raw - - <<< "$json_data" 2>/dev/null | grep -v "<stdin>")
            echo "CVEs in macOS Version $product_version: $cves_in_version"
            cves=$((cves + cves_in_version))

            exploits_in_version=$(/usr/bin/plutil -extract "OSVersions.$os_position.SecurityReleases.$j.ActivelyExploitedCVEs" raw - - <<< "$json_data" 2>/dev/null | grep -v "<stdin>")
            echo "Actively exploited CVEs in macOS Version $product_version: $exploits_in_version"
            exploits=$((exploits + exploits_in_version))
        else
            break
        fi
    done
fi

echo
echo "<result>CVEs:$cves ActiveExploits:$exploits</result>"
