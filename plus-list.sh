#!/bin/bash

sum=0

# Print the input arguments
echo "Input arguments: $@"

# Loop through all the arguments and add them up
for arg in "$@"
do
    sum=$((sum + arg))
done

# Print the result
echo "Sum: $sum"

# Return the sum as the exit code
exit $sum