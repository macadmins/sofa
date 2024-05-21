#!/bin/zsh --no-rcs
# shellcheck shell=bash

# Check if the model does support the latest version of macOS using SOFA
# by Balz Aschwanden
#
# adobted from the following script by Graham Pugh
# https://github.com/macadmins/sofa/blob/main/tool-scripts/macOSVersionCheck-EA.sh

# Note that this uses plutil so is only compatible with macOS 12+
#
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
    if /usr/bin/curl --etag-compare "$etag_cache" "$online_json_url"; then
        echo "Cached e-tag matches online e-tag - local cached file is up to date"
    else
        echo "Cached e-tag does not match online e-tag, proceeding to download"
        /usr/bin/curl -L -m 3 -s "$online_json_url" --etag-save "$etag_cache" -o "$json_cache"
    fi
else
    echo "No e-tag cached, proceeding to download"
    /usr/bin/curl -L -m 3 -s "$online_json_url" --etag-save "$etag_cache" -o "$json_cache"
fi

echo

if [[ ! "$json_cache" ]]; then
    echo "<result>Could not obtain data</result>"
    exit
fi

# 1. Get model (DeviceID)
model=$(/usr/sbin/sysctl -n hw.model)
echo "Model Identifier: $model"

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
