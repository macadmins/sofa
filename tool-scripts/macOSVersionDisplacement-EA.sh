#!/bin/zsh --no-rcs
# shellcheck shell=bash

# Return the displacement between the installed major macOS version and
# latest major macOS version.
#
# This is commonly referred to as "n-x" where "n" is the current major
# version as released by Apple and "x" is displacement, or how far
# behind (or ahead, if running a beta release), a given computer's 
# installed version is.
#
# E.g if the latest major version is 15 and a computer has 13 installed,
# the displacement is 2 (or n-2). 15-2 is 13.
#
# Apple will not release software updates for macOS versions with a
# displacement greater than 2 (n-2) and many software vendors will also 
# cease support.
#
# To use in a Smart Groups to scope computers that have a displacement
# greater than n-2:
#
#   macOS Version Displacement - greater than - 2
#

# Get current system OS
system_version=$( /usr/bin/sw_vers -productVersion )
# system_version=14.1  # UNCOMMENT TO TEST OLDER VERSIONS
system_os=$( /usr/bin/cut -d. -f1 <<< "$system_version" )
echo "System Major Version: $system_os"

if [[ $system_os -ge 12 ]]; then
    # use plistlib
    os_compatibility="current"
else
    # use python 2.7
    os_compatibility="legacy"
    python_path="/usr/bin/python"
fi


# URL to the online JSON data
online_json_url="https://sofafeed.macadmins.io/v1/macos_data_feed.json"
user_agent="SOFA-Jamf-EA-macOSVersionDisplacement/1.0"

# Local store
json_cache_dir="/private/var/tmp/sofa"
json_cache="$json_cache_dir/macos_data_feed.json"
etag_cache="$json_cache_dir/macos_data_feed_etag.txt"
etag_cache_temp="$json_cache_dir/macos_data_feed_etag_temp.txt"

# Ensure local cache folder exists
/bin/mkdir -p "$json_cache_dir"

# Check local vs online using etag (only available on macOS 12+)
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
elif [[ "$os_compatibility" == "legacy" ]]; then
    echo "OS not compatible with e-tags, proceeding to download SOFA json file"
    /usr/bin/curl --compressed --location --max-time 3 --silent --header "User-Agent: $user_agent" "$online_json_url" --output "$json_cache"
else
    echo "No e-tag or SOFA json file cached, proceeding to download SOFA json file"
    /usr/bin/curl --compressed --location --max-time 3 --silent --header "User-Agent: $user_agent" "$online_json_url" --etag-save "$etag_cache" --output "$json_cache"
fi

# Get OSVersions.Latest.ProductVersion
if [[ "$os_compatibility" == "current" ]]; then
    os_version=$( /usr/bin/plutil -extract "OSVersions.0.Latest.ProductVersion" raw "$json_cache" | /usr/bin/head -n 1 | /usr/bin/grep -v "<stdin>" )
else
    os_version=$( "$python_path" -c 'import sys, json; print json.load(sys.stdin)["OSVersions"][0]["Latest"]["ProductVersion"]' < "$json_cache" | /usr/bin/head -n 1 )
fi
latest_os=$( /usr/bin/cut -d. -f1 <<< "$os_version"  )
echo "Latest Major Version: $latest_os"

# Verify integer received from SOFA and output the result
if [[ "$((latest_os-latest_os))" == 0 ]]; then
    echo "<result>$((latest_os-system_os))</result>"
else
    echo "<result></result>"
fi
