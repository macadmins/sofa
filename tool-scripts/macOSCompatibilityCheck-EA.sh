#!/bin/zsh --no-rcs
# shellcheck shell=bash

# Check if the model does support the latest version of macOS using SOFA
# by Balz Aschwanden
#
# adopted from the following script by Graham Pugh
# https://github.com/macadmins/sofa/blob/main/tool-scripts/macOSVersionCheck-EA.sh

# Note that this uses plutil so is only compatible with macOS 12+

# Use code inspired by the following post to exit if macOS < 12
# https://scriptingosx.com/2020/10/dealing-with-xpath-changes-in-big-sur/
if [[ $(sw_vers -buildVersion) < "21H" ]]; then
    echo "<result>This EA only supports macOS 12+</result>"
    exit
fi

# URL to the online JSON data
online_json_url="https://sofa.macadmins.io/v1/macos_data_feed.json"

# local store
json_cache_dir="/private/tmp/sofa"
json_cache="$json_cache_dir/macos_data_feed.json"
etag_cache="$json_cache_dir/macos_data_feed_etag.txt"

# ensure local cache folder exists
/bin/mkdir -p "$json_cache_dir"

# check local vs online using etag
if [[ -f "$etag_cache" && -f "$json_cache" ]]; then
    if /usr/bin/curl --silent --etag-compare "$etag_cache" "$online_json_url" --output /dev/null; then
        echo "Cached e-tag matches online e-tag - cached json file is up to date"
    else
        echo "Cached e-tag does not match online e-tag, proceeding to download SOFA json file"
        /usr/bin/curl --location --max-time 3 --silent "$online_json_url" --etag-save "$etag_cache" --output "$json_cache"
    fi
else
    echo "No e-tag cached, proceeding to download SOFA json file"
    /usr/bin/curl --location --max-time 3 --silent "$online_json_url" --etag-save "$etag_cache" --output "$json_cache"
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

# check that the model is virtual or is in the feed at all
if [[ $model == "VirtualMac"* ]]; then
    # if virtual, we need to arbitrarily choose a model that supports all current OSes. Plucked for an M1 Mac mini
    model="Macmini9,1"
elif ! grep -q "$model" "$json_cache"; then
    echo "<result>Unsupported Hardware</result>"
    exit
fi

# 2. identify the latest major OS
latest_os=$(/usr/bin/plutil -extract "OSVersions.0.OSVersion" raw -expect string "$json_cache" | /usr/bin/head -n 1)
echo "Latest macOS: $latest_os"

# 3. idenfity latest compatible major OS
latest_compatible_os=$(/usr/bin/plutil -extract "Models.$model.SupportedOS.0" raw -expect string "$json_cache" | /usr/bin/head -n 1)
echo "Latest Compatible macOS: $latest_compatible_os"

# 5. Compare latest with compatible
if [[ "$latest_os" == "$latest_compatible_os" ]];then
    echo "<result>Pass</result>"
else
    echo "<result>Fail</result>"
fi
