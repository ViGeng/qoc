#!/bin/bash

# Get today's date in seconds since epoch
today=$(date +%s)

# Get the target date in seconds since epoch
target=$(date -j -f "%Y-%m-%d" "$1" "+%s")

# Calculate the difference in seconds
diff=$((target - today))

# Calculate the number of days
days=$((diff / 86400))

# Print the result
echo "There are $days days until $1"