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

echo

# exit if less than macOS 12
if ! is-at-least 12 "$system_os"; then
    echo "<result>Unsupported macOS</result>"
    exit
fi

# 3. idenfity latest compatible major OS
latest_compatible_os=$(/usr/bin/plutil -extract "Models.$model.SupportedOS.0" raw -expect string - - <<< "$json_data" | /usr/bin/head -n 1)
echo "Latest Compatible macOS: $latest_compatible_os"

# 4. Get OSVersions.Latest.ProductVersion
for i in {0..3}; do
    os_version=$(/usr/bin/plutil -extract "OSVersions.$i.OSVersion" raw - - <<< "$json_data" | /usr/bin/head -n 1 | grep -v "<stdin>")
    if [[ $os_version ]]; then
        if [[ "$os_version" == "$latest_compatible_os" ]]; then
            product_version=$(/usr/bin/plutil -extract "OSVersions.$i.Latest.ProductVersion" raw - - <<< "$json_data" | /usr/bin/head -n 1)
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
