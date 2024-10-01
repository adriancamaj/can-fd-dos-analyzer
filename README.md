# CAN-FD DoS Analyzer

This repository contains a Python tool designed to parse automotive Controller Area Network with Flexible Data-Rate (CAN-FD) log files. It identifies failed test cases, calculates Denial of Service (DoS) times based on message timestamps, and outputs the results for further analysis.

## Features

- Parses CAN-FD log files with potential inconsistencies or tester comments.
- Identifies failed test cases automatically.
- Calculates DoS times for each failed test case.
- Outputs results to a file for persistent record-keeping.

## Requirements

- Python 3.x
- No external libraries required (uses standard Python libraries like `json` and `datetime`).

## Usage

1. **Clone the repository:**
 ```
 git clone https://github.com/adriancamaj/can-fd-dos-analyzer.git
 ```

2. **Navigate to the project directory:**
 ```
 cd can-fd-dos-analyzer
 ```

3. **Place your log file in the project directory:**
 Ensure your log file is named `inputFile.log` or update the `file_path` variable in `main.py` accordingly.

4. **Run the script:**
 ```
 python main.py
 ```

5. **View the results:**
 The DoS times for failed test cases will be output to `dosFile.log` in the project directory.

## Example Output
```
Test case #5 - DoS time is: 0:00:55.357000
```
- **`dosFile.log`**: The **output file** containing DoS times for failed test cases.
- ~~_`parse_log.json`: Intermediate JSON file containing parsed log records._~~
- ~~_`case_verdicts.json`: Intermediate JSON file containing case verdicts and comments._~~
  
## Project Structure
- **`main.py`**: The **main script** that orchestrates the parsing and analysis.
- **`log_parse.py`**: **Contains functions** for parsing the log file, identifying failed test cases, calculating DoS times, and outputting results.
- **`inputFile.log`**: The **log file** to be parsed (not included; user must provide).
 
## How It Works
1. **Parsing the Log File:**
   - Reads the log file line by line.
   - Cleans and splits each line into identifiable components.
   - Stores the data in a list of dictionaries for easy access.

2. **Identifying Failed Test Cases:**
   - Scans for test cases marked as "Failed".
   - Extracts the case numbers of failed tests.

3. **Calculating DoS Times:**
   - For each failed test case, finds the start time (when the problematic message was sent) and the end time (when the response was received).
   - Calculates the DoS time by subtracting the start time from the end time.
   - Compiles the results into a readable format.
  
4. **Outputting Results:**
   - Writes the DoS times for all failed test cases to `dosFile.log`.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request to discuss improvements, bug fixes, or new features.

## License
This project is open-source. You are free to use, modify, and distribute it as per the terms specified in the LICENSE file.

## Disclaimer
This tool is intended for use in automotive testing environments and assumes that the log files are structured in a specific format. Ensure that your log files match the expected format or adjust the parsing logic accordingly.

----
Feel free to reach out if you have any questions or need assistance using this tool.




