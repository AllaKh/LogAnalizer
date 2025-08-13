import re
import glob
import os

# Path to log files (adjust this to your actual log folder)
log_dir = r"I:\Python Projects\Prepare to Redis\venv\venv\log_convert\logs\*.txt"

# Regular expression to extract DeviceID, Test, and Result
pattern = re.compile(r"DeviceID:(\d+)\s+Test:(\d+)\s+Result:(\w+)", re.IGNORECASE)

# List to store parsed results
results = []

# List all found files for debugging
files = glob.glob(log_dir)
if not files:
    print(f"❌ No files found at path: {log_dir}")
else:
    print(f"Found {len(files)} file(s): {files}")

# Read all log files and search for matching lines
for file_path in files:
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = pattern.search(line)
            if match:
                device_id, test_id, result = match.groups()
                results.append([device_id, test_id, result])

# If no matching lines were found, stop execution
if not results:
    print("❌ No matching lines found in logs.")
else:
    # Table column headers
    headers = ["DeviceID", "Test", "Result"]

    # Calculate max width for each column (to align table output)
    col_widths = [
        max(len(headers[0]), max(len(str(row[0])) for row in results)),
        max(len(headers[1]), max(len(str(row[1])) for row in results)),
        max(len(headers[2]), max(len(str(row[2])) for row in results))
    ]

    # Print table header
    print(f"{headers[0]:<{col_widths[0]}} | {headers[1]:<{col_widths[1]}} | {headers[2]:<{col_widths[2]}}")
    print("-" * (sum(col_widths) + 6))

    # Print each row in the table
    for record in results:
        print(f"{record[0]:<{col_widths[0]}} | {record[1]:<{col_widths[1]}} | {record[2]:<{col_widths[2]}}")
