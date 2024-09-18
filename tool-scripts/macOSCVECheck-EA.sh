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
online_json_url="https://sofafeed.macadmins.io/v1/macos_data_feed.json"
user_agent="SOFA-Jamf-EA-macOSCVECheck/1.1"

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

if [[ ! -f "$json_cache" ]]; then
    echo "<result>Could not obtain data</result>"
    exit
elif ! plutil -extract "UpdateHash" raw "$json_cache" > /dev/null; then
    echo "<result>Could not obtain data</result>"
    exit
fi

# 1. Get model (DeviceID)
model=$(/usr/sbin/sysctl -n hw.model)
if [[ -z "$model" ]]; then
    echo "<result>Could not obtain model</result>"
    exit
fi
echo "Model Identifier: $model"

# check that the model is virtual or is in the feed at all
if [[ $model == "VirtualMac"* ]]; then
    # if virtual, we need to arbitrarily choose a model that supports all current OSes. Plucked for an M1 Mac mini
    model="Macmini9,1"
elif ! grep -q "$model" "$json_cache"; then
    echo "<result>Unsupported Hardware</result>"
    exit
fi

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
latest_compatible_os=$(/usr/bin/plutil -extract "Models.$model.SupportedOS.0" raw -expect string "$json_cache" | /usr/bin/head -n 1 | cut -d' ' -f2)
echo "Latest Compatible macOS: $latest_compatible_os"

# 4. Get OSVersions.Latest.ProductVersion
for i in {0..3}; do
    os_version=$(/usr/bin/plutil -extract "OSVersions.$i.OSVersion" raw "$json_cache" | /usr/bin/head -n 1 | grep -v "<stdin>" | cut -d' ' -f2)
    if [[ $os_version ]]; then
        if [[ "$os_version" == "$latest_compatible_os" ]]; then
            product_version=$(/usr/bin/plutil -extract "OSVersions.$i.Latest.ProductVersion" raw "$json_cache" | /usr/bin/head -n 1)
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
        product_version=$(/usr/bin/plutil -extract "OSVersions.$os_position.SecurityReleases.$j.ProductVersion" raw "$json_cache" 2>/dev/null | grep -v "<stdin>")

        if [[ "$product_version" == "$system_version" ]]; then
            break
        fi

        if [[ $product_version ]]; then
            cves_in_version=$(/usr/bin/plutil -extract "OSVersions.$os_position.SecurityReleases.$j.UniqueCVEsCount" raw "$json_cache" 2>/dev/null | grep -v "<stdin>")
            echo "CVEs in macOS Version $product_version: $cves_in_version"
            cves=$((cves + cves_in_version))

            exploits_in_version=$(/usr/bin/plutil -extract "OSVersions.$os_position.SecurityReleases.$j.ActivelyExploitedCVEs" raw "$json_cache" 2>/dev/null | grep -v "<stdin>")
            echo "Actively exploited CVEs in macOS Version $product_version: $exploits_in_version"
            exploits=$((exploits + exploits_in_version))
        else
            break
        fi
    done
fi

echo
echo "<result>CVEs:$cves ActiveExploits:$exploits</result>"
