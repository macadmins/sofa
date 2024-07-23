#!/bin/zsh --no-rcs
# shellcheck shell=bash

# Check if the local system matches the latest available compatible version using SOFA
# by Graham Pugh
#
# To use in a Smart Groups to scope computers that are not up to date:
#   macOS Version Check - is - Fail
#
# Note that this uses plutil so is only compatible with macOS 12+

# autoload is-at-least module for version comparisons
autoload is-at-least

# URL to the online JSON data
online_json_url="https://sofafeed.macadmins.io/v1/macos_data_feed.json"
user_agent="SOFA-Jamf-EA-macOSVersionCheck/1.0"

# local store
json_cache_dir="/private/tmp/sofa"
json_cache="$json_cache_dir/macos_data_feed.json"
etag_cache="$json_cache_dir/macos_data_feed_etag.txt"

# ensure local cache folder exists
/bin/mkdir -p "$json_cache_dir"

# check local vs online using etag
if [[ -f "$etag_cache" && -f "$json_cache" ]]; then
    echo "e-tag stored, will download only if e-tag doesn't match"
    etag_old=$(/bin/cat "$etag_cache")
    /usr/bin/curl --compressed --silent --etag-compare "$etag_cache" --etag-save "$etag_cache" --header "User-Agent: $user_agent" "$online_json_url" --output "$json_cache"
    etag_new=$(/bin/cat "$etag_cache")
    if [[ "$etag_old" == "$etag_new" ]]; then
        echo "Cached ETag matched online ETag - cached json file is up to date"
    else
        echo "Cached ETag did not match online ETag, so downloaded new SOFA json file"
    fi
else
    echo "No e-tag cached, proceeding to download SOFA json file"
    /usr/bin/curl --compressed --location --max-time 3 --silent --header "User-Agent: $user_agent" "$online_json_url" --etag-save "$etag_cache" --output "$json_cache"
fi

echo

# 1. Get model (DeviceID)
model=$(/usr/sbin/sysctl -n hw.model)
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

echo

# exit if less than macOS 12
if ! is-at-least 12 "$system_os"; then
    echo "<result>Unsupported macOS</result>"
    exit
fi

# 3. idenfity latest compatible major OS
latest_compatible_os=$(/usr/bin/plutil -extract "Models.$model.SupportedOS.0" raw -expect string "$json_cache" | /usr/bin/head -n 1)
echo "Latest Compatible macOS: $latest_compatible_os"

# 4. Get OSVersions.Latest.ProductVersion
for i in {0..3}; do
    os_version=$(/usr/bin/plutil -extract "OSVersions.$i.OSVersion" raw "$json_cache" | /usr/bin/head -n 1 | grep -v "<stdin>")
    if [[ $os_version ]]; then
        if [[ "$os_version" == "$latest_compatible_os" ]]; then
            product_version=$(/usr/bin/plutil -extract "OSVersions.$i.Latest.ProductVersion" raw "$json_cache" | /usr/bin/head -n 1)
            echo "Latest Compatible macOS Version: $product_version"
        fi
    fi
done

echo

# 5. Compare system with latest compatible
if is-at-least "$product_version" "$system_version"; then
    echo "<result>Pass</result>"
else
    echo "<result>Fail</result>"
fi
