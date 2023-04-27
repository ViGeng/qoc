#!/bin/bash

# Get today's date in seconds since epoch
today=$(date +%s)
echo "Today is $today"

# Get the target date in seconds since epoch from the first argument
target=$(date -d "$1" +%s)
echo "Target day is $target"

# Calculate the difference in seconds
diff=$((target - today))

# Calculate the number of days
days=$((diff / 86400))

# Print the result
echo "There are $days days until $1"