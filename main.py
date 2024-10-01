'''
Intern Coding Challenge:
Log Parsing and Testing
---
main.py
---
Created on Feb 14, 2021
@author: Adrian Camaj
'''

# import functions
from log_parse import * 
# filename of log
file_path = 'inputFile.log' # input
dos_log = 'dosFile.log' # output

# run functions #
load_parse(file_path)   # read log file & parse
# sort packet events
find_failed_case_start_times()  # load failed start times & sort by id
find_failed_case_end_times()    # load failed end times & sort by id
# calculate dos times
calculate_dos_times()   # subtract start and end times
# save dos log to file
print_to_file(dos_log) # dosFile.log

