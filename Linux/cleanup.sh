#!/bin/bash

# Check arguments
if [ $# -ne 2 ]; then
echo "Usage: $0 <directory_path> <days>"
exit 1
fi

directory=$1
days=$2
log_file="/home/acts/deleted_files.log"

# Create log file if not exists
touch "$log_file"

# Find and delete files older than given days
find "$directory" -type f -mtime +"$days" -print -exec rm -f {} \; | while read file
do
echo "$(date) - Deleted: $file" >> "$log_file"
done

echo "Cleanup completed."
