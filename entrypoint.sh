#!/bin/sh
# Run the main script that generates JSON
python muf-script.py --versions "$MACOS_VERSIONS"

sleep 5
# Run our script for CSV time-series update
python muf-time-series.py --json muf_data_sonoma_14.json --csv time-series.csv
