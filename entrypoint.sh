#!/bin/sh

# Run the main script that generates JSON
mkdir v1

# Check if OS_TYPE is set
if [ -z "$OS_TYPE" ]; then
    echo "Error: OS_TYPE environment variable is not set."
    exit 1
fi

echo "Starting: $OS_TYPE environment variable is set."
# Assuming OS_TYPE is set to "macOS" or "iOS" before this script runs
python build-sofa-feed.py $OS_TYPE


sleep 5

# Run our script for CSV time-series update
if [ -f macos_data_feed.json ]; then 
    echo "Processing: $OS_TYPE, upadte time-series.csv file."
    # Run script to generate time-series.csv only if the file exists
    python sofa-time-series.py --json macos_data_feed.json --csv time-series.csv; 
fi

