#!/bin/sh

# Create the directory if it doesn't exist
mkdir -p v1

# Check if at least one argument is provided
if [ "$#" -eq 0 ]; then
    echo "Error: No OS types provided."
    exit 1
fi

# Loop through all OS types provided as arguments
for OS_TYPE in "$@"; do
    echo "Starting: $OS_TYPE"

    # Run the main script that generates JSON
    python build-sofa-feed.py "$OS_TYPE"

    # Wait for a moment to ensure files are written
    sleep 5

    # Run the script for CSV time-series update if the data feed file exists
    if [ "$OS_TYPE" = "macOS" ] && [ -f "macos_data_feed.json" ]; then 
        echo "Processing: $OS_TYPE, update time-series.csv file."
        python sofa-time-series.py --json macos_data_feed.json --csv time-series.csv
    elif [ "$OS_TYPE" = "iOS" ] && [ -f "ios_data_feed.json" ]; then 
        echo "Processing: $OS_TYPE"
    fi
done
