'''
Intern Coding Challenge:
Log Parsing and Testing
---
log_parse.py
---
Read log file
Parse test cases
Check packet events
Calculate DOS times
Save to file
---
Created on Feb 17, 2021
---
@author: Adrian Camaj
'''

import json
from datetime import datetime

#_START_BUFFER_VARS_#
# list of nested records [[record 1], [record 2], [record 3], etc...]
nest_list = []
# non-duplicate formatted list of nested records
formatted_list = []
#_END_BUFFER_VARS_#

# list of item identifiers.. (0,1,2,3,4,5,6,7,8)
item_identifiers = ['Date_Time', 'na', 'Interface', 'Num', 'etc', 'Type', 'Sig', 'Packets', 'Parameters']
# list of dictionary records [{record 1}, {record 2}, {record 3}, etc...]
log_records = []
# comments and verdicts
other_info = []
# failed case ID #'s
failed_cases = []

#list of dictionary records for failed case times
failed_cases_start_times = []  # e.g. [{'ID':'1', 'start':'2021-02-09 13:11:11'}]
failed_cases_end_times = [] # e.g. [{'ID':'1', 'end':'2021-02-09 13:12:12'}]

# string for final output
dos_log = ""

# boolean if data is loaded
#data_loaded = False

def merge_lists(input_list):
    """ Merge 2 lists into a dictionary """
    # merge 2 lists into a dictionary
    # function merge_lists return dict
    # item_identifiers --> presaved or nest_list[0]
    # values --> nest_list[1:] or input_list
    clean_dict = {}
    counter = 0
    #item_identifiers = clean_nest_list[0]
    index = len(item_identifiers)
    
    if (index == len(input_list)):
        while (counter < index):
            k = item_identifiers[counter]
            v = input_list[counter]
            clean_dict.update({k:v})
            counter += 1
    else:
        other_info.append(input_list)

    return(clean_dict) # return clean_dict
    
    
def format_list(input_list):
    """ Formats nested lists and returns list of dictionaries """
    # format lists into dictionaries
    # function store_data return log
    temp_dict = {} # buffer
    for each_list in input_list:
        temp_dict = merge_lists(each_list)
        log_records.append(temp_dict)
    #print(log_records)
    return(log_records)
    
    
def write_json(path_loc, the_data):
    """ Write JSON file and export database """
    # reformat and write into JSON
    with open(path_loc, "w") as json_obj:
        json.dump(the_data, json_obj)      
        
        
def load_parse(file_path):
    """ Load all data, parse it, and store into list """
    # read file, parse, strip & clean
    # then store into nested list

    try:
        with open(file_path) as file:   # open file
            raw_data = file.readlines() # store lines
            for line in raw_data:   # loop through line by line
                clean_data = line.split('\t') # clean data    (invisible tab between packets e.g. 'D4 B1 2B')
                clean_data = [item.strip() for item in clean_data]   # list comprehension
                ###print(clean_data)
                nest_list.append(clean_data)    # store clean data to nested list
            #print(nest_list)  
        
        global formatted_list   # must declare global           
        formatted_list = format_list(nest_list) # format nested list
        #print(formatted_list)
            
        # write parsed log to file
        write_json('parse_log.json', formatted_list)
            
        # other info includes any data without all item_identifiers information (basically comments)
        global other_info   # must declare global
        other_info = [ x for x in other_info if x != [''] ]   # clean data 
        # run the loop for failed cases
        for each_item in other_info:
            #print(each_item)
            for string in each_item:    # check for failed cases
                if (string.lower().startswith('test case')):
                    string = string.split(' ',5)
                    if (string[4].lower() == 'failed'):
                        #print(string[2]) #failed case IDs
                        failed_cases.append(string[2])  # store the failed case ID #'s
        #print(failed_cases)
        
        # write case verdicts to file
        write_json('case_verdicts.json', other_info)
        #print(other_info)
    except:
        # display error
        print("The file doesn't exist")


def find_failed_case_start_times():    
    """ Stores the failed case start times """ 
    count = 0
    global failed_cases_start_times # must declare global
    while (count < len(failed_cases)):
        ID = failed_cases[count]    # update the failed case Number/ID every loop
        for each_dict in formatted_list:
            #print(each_dict)
            if (each_dict): # checks if data is valid
                #print(each_dict)
                if( each_dict['Num'] == ID and each_dict['Parameters'].split('|')[0].lower().startswith('can_fd_raw_frame_invalid_frame') ):
                    start_time = each_dict['Date_Time'] # find the right event and store the date/time
                    failed_cases_start_times.append({'Num':ID, 'Date_Time':start_time}) # store it in a dict/list
                    count += 1
    #print(failed_cases_start_times)


def find_failed_case_end_times():
    """ Stores the failed case end times """ 
    Id_list = []    # keep track of case IDs
    count = 0
    global failed_cases_end_times # must declare global
    while (count < len(failed_cases)):
        ID = failed_cases[count]  # update the failed case Number/ID every loop
        for each_dict in formatted_list:
            if (each_dict): # checks if data is valid
                if( each_dict['Num'] == ID ): # find the right event
                    if (each_dict['Parameters'].split('|')[1].lower().strip() == 'response'):
                        end_time = each_dict['Date_Time'] # store the Date & Time of that particular record (end of failed test case)
                        if ( ID in Id_list ): # check whether Failed case Number/ID already exists 
                            failed_cases_end_times[-1]['Date_Time'] = end_time  # then override it
                        else:   # if it doesnt exist create a new one
                            Id_list.append(ID) # keep track of failed case Number/IDs (Buffer) for next loop
                            failed_cases_end_times.append({'Num':ID, 'Date_Time':end_time}) 
                            count += 1
                        #print(Id_list)
    #print(failed_cases_end_times)
                            
                            
def calculate_dos_times():
    """ Finds the difference between start & end times from the failed cases """
    count = 0
    global dos_log # must declare global
    # loop each failed case
    for each_failed_case in failed_cases:
        end_time = datetime.strptime(failed_cases_end_times[count]['Date_Time'], "%Y-%m-%d %H:%M:%S.%f")   # reformat date/time 
        start_time = datetime.strptime(failed_cases_start_times[count]['Date_Time'], "%Y-%m-%d %H:%M:%S.%f")   # reformat date/time
        dos_time = end_time - start_time  # subtract the times from the end and start of each failed test case
        count += 1
        dos_log += ("Test case #" + each_failed_case + " - DoS time is: " + str(dos_time) +"\n")
        print("Test case #" + each_failed_case + " - DoS time is: " + str(dos_time))
        #print(dos_time)
    
def print_to_file(file_loc):
    """ Saves the Dos Times to a file of your choosing """
    with open(file_loc, "w") as file_output:
        file_output.write(dos_log)