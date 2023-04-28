import sys

# Check that the correct number of arguments were provided
if len(sys.argv) != 3:
    print("Usage: python script.py <python_file> <data_file>")
    sys.exit(1)

# Get the filenames from the command line arguments
python_file = sys.argv[1]
data_file = sys.argv[2]

# Open the data file and read the contents
with open(data_file, 'r') as f:
    params = [line.strip() for line in f]

# Import the Python file as a module
module = __import__(python_file)

# Call the main function of the Python file with the parameters from the data file
module.main(*params)
