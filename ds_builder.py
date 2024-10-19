'''
File: ds_builder.py
Author: Samuel Bush
Date: 10/15/2024
Description: This is a top level file with a GUI for users to run the dataset builder and web scraping scripts
             This is the second full version of the builder
'''

import pandas as pd
import os
import json
import time
import sys
import glob
from repo_clone_method import repo_scraper

#----Global Vars----#
log_file = ""

#----Functions List----#

def filetodf(readFolder, readFile, dataframeName="dataframe.csv", max_length=20000):
    '''
    This function is designed to parse an inputted file every `max_length` characters
    and append it to a designated `dataframeName` csv file.
    '''
    if readFolder == "":
        filePath = readFile
    elif readFolder[-1] != "\\":
        filePath = readFolder + "\\" + readFile
    else:
        filePath = readFolder + readFile
    outFileName = dataframeName

    # open read file
    fd = open(filePath, encoding='utf-8', errors="ignore")
    # read text
    text = fd.readlines()
    text = "".join(text)
    # divide text every 20k characters
    parts = len(text) // (max_length) + (1 if len(text) % max_length > 0 else 0)
    
    for part in range(parts):
        start_index = part * max_length
        end_index = start_index + max_length

        newStructure = {'text' : [text[start_index:end_index]]}
        loading(part + 1, parts)

        tempdf = pd.DataFrame(newStructure)
        if os.path.exists(outFileName):
            tempdf.to_csv("temp_df.csv", index=False)
            chunk_size = 1000
            for chunk in pd.read_csv('temp_df.csv', chunksize=chunk_size):
                chunk.to_csv(outFileName, mode='a', header=False, index=False)
        else:
            tempdf.to_csv(outFileName, index=False)

    print(f"\nUpdated {outFileName} with file {readFile}.\n\n")
    deletedf("temp_df.csv", False)
    return

def deletedf(dfName="dataframe.csv", print_=True):
    '''
    This function deletes the designated dataframe in `dfName`.
    '''
    open(dfName, "w")
    os.remove(dfName)
    if print_:
        print("\nDataframe cleared...")
    return

def parseJSON(nameJSON, dfName="dataframe.csv"):
    '''
    This function parses the `dfName` dataframe csv into the
    `nameJSON` json file for the final dataset.
    '''
    # read dataframe
    df_code = pd.read_csv(dfName)
    # open output .json (this is the code from Shailja)
    print("Making JSON...")
    total_rows = len(df_code['text'].values)
    index = 0
    with open(nameJSON,'a') as f:
        for row in df_code['text'].values:
            #print("Adding row...")
            # adds dictionary
            dic={"text":str(row)}
            ob=json.dumps(dic)
            f.write(ob)
            f.write('\n')
            loading(index+1, total_rows)
            index += 1
            
    f.close()
    print(f"\n\nJSON Complete : written to {os.path.dirname(f'{nameJSON}.json')+nameJSON}...")
    # clear dataframe after use
    deleteit = input("Would you like to delete the old dataframe now?\n.\n.\n.\n(Y/N) >> ")
    if deleteit == "Y" or deleteit == "y":
        deletedf(dfName)
    return

def loading(current, total, length=30):
    '''
    This function is a random loading animation function so you can see
    the scraper and builder are just slow not broken.
    '''
    progress = current / total
    bar_length = int(length * progress)
    bar = "[" + "#" * bar_length + "-" * (length - bar_length) + "]"
    # Display the progress bar with percentage
    sys.stdout.write(f"\r{bar} {int(progress * 100)}%")
    sys.stdout.flush()

def builderInitLog():
    '''
    This function will create a new log file for every time the script is run within the ./ds_builder_logs directory
    '''
    global log_file
    logName = "builder_log_run_"
    os.makedirs("ds_builder_logs", exist_ok=True)
    logNum = 0
    while os.path.exists(os.path.join("ds_builder_logs", f'{logName}{logNum}.txt')):
        logNum += 1
    log_file = os.path.join("ds_builder_logs", f'{logName}{logNum}.txt')
    logfd = open(log_file, 'a')
    logfd.close()

def builderWriteLog(in_string):
    '''
    This helper function writes whatever string is inputted into the log file
    '''
    logfd = open(log_file, 'a')
    entry = f'\n{time.time()} -- {in_string}\n-'
    logfd.write(entry)
    logfd.close()

def printHome():
    print("\n.\n.\n.\n**************\n**** HOME ****\n**************\n\nWelcome to the dataset builder 2.0")

def printDfHome():
    print("\n.\n.\n.\n***************************\n**** DATAFRAME MANAGER ****\n***************************\n\nWelcome to the dataframe manager")

def printDsHome():
    print("\n.\n.\n.\n*************************\n**** DATASET MANAGER ****\n*************************\n\nWelcome to the dataset manager")

def printSpHome():
    print("\n.\n.\n.\n*************************\n**** SCRAPER MANAGER ****\n*************************\n\nWelcome to the GitHub Scraper manager")

def runDfManager():
    '''
    This function contains all current dataframe management tools supported by the ds builder and can be run independently
    '''
    while True:
        printDfHome()
        uinDf = input("What would you like to do?\nCommands:\nnf : read specific file into a target dataframe\nraf : read all files within a specified directory into a target dataframe\nm : merge two dataframes\nc : delete a target dataframe\nh : return to home\n.\n.\n.\n>> ")
        if uinDf.lower() == 'nf':
            target_df   = input("What is your target dataframe name/path (relative to the current directory)?\n.\n.\n.\n(ex. .\\dataframe.csv)>> ")
            target_file = input("What is your target file name/path (relative to the current directory)?\n.\n.\n.\n(ex. .\\data.v)>> ")
            try:
                start_time = time.time()
                filetodf("", target_file, target_df)
                end_time = time.time()
                log_entry = f'Completed parsing file: {os.path.relpath(target_file)} into target dataframe: {os.path.relpath(target_df)} in {end_time - start_time} seconds'
                print(log_entry)
                builderWriteLog(log_entry)
            except:
                print("Invalid Argument: Target input")
                continue
        elif uinDf.lower() == 'raf':
            print("Instructions:\n- You will first enter the target dataframe and directory in which your files are stored\n- Next you must specify the file types you are wishing to add into your target dataframe")
            print("WARN: This functionality will recursively read files through any subdirectories within your target data directory\n.\n")
            target_df    = input("What is your target dataframe name/path (relative to the current directory)?\n.\n.\n.\n(ex. .\\dataframe.csv)>> ")
            target_dir   = input("What is your target data directory path (relative to the current directory)?\n.\n.\n.\n(ex. .\\all_my_files_here)>> ")
            target_types = input("Enter however many file types you want to target separated by spaces,\nto read all files regardless of type just press <enter> without typing\n.\n.\n.\n(ex. '*.txt *.v *.csv')>> ")
            try:
                if not target_types.strip():
                    target_types = '*'
                start_time = time.time()
                type_list = target_types.split(" ")
                file_count = 0
                for ftype in type_list:
                    for ifile in glob.glob(os.path.join(target_dir, '**', f'{ftype}'), recursive=True):
                        print(f"Reading {ifile} into dataframe...")
                        filetodf("", ifile, target_df)
                        file_count += 1
                end_time = time.time()
                log_entry = f'Completed parsing {file_count} files within: {os.path.relpath(target_dir)} into target dataframe: {os.path.relpath(target_df)} in {end_time - start_time} seconds'
                print(log_entry)
                builderWriteLog(log_entry)
            except:
                print("Invalid Argument: Target input")
                continue
        elif uinDf.lower() == 'm':
            print()
        elif uinDf.lower() == 'c':
            target_df = input("What is the name/path of the dataframe to delete?\n.\n.\n.\n(ex. .\\dataframe.csv)>> ")
            try:
                start_time = time.time()
                deletedf(target_df)
                end_time = time.time()
                log_entry = f'Successfully deleted {os.path.relpath(target_df)} in {end_time - start_time} seconds'
                print(log_entry)
                builderWriteLog(log_entry)
            except:
                print("Invalid Argument: File name")
                continue
        elif uinDf.lower() == 'h':
            return
        else:
            print("Invalid input...")
            continue 

def runDsManager():
    '''
    This function contains current dataset management tools supported by the ds builder and can be run independently
    '''
    while True:
        printDsHome()
        uinDs = input("What would you like to do?\nCommands:\nac : append to or create dataset from dataframe\nstats : get metrics from an existing dataset\nh : return to home\n.\n.\n.\n>> ")
        if uinDs.lower() == 'ac':
            dfName = input("Instructions\n- You will first select a path to the dataframe you wish to build from\n- Then you will select the name/path of the destination dataset (can be an existing dataset or a new one)\n.\n.\n.\nWhat is the name/path to your dataframe (relative to the current directory)?\n(ex. .\\df_here\\dataframe.csv)>> ")
            JSONname = input("What is/will be the name/path your JSON dataset?\n.\n.\n.\n(ex. .\\New_Dataset.json)>> ")
            try:
                start_time = time.time()
                parseJSON(JSONname, dfName)
                end_time = time.time()
                log_entry = f"Completed parsing dataframe: {os.path.relpath(dfName)} into dataset: {os.path.relpath(JSONname)} in {end_time - start_time} seconds"
                print(log_entry)
                builderWriteLog(log_entry)
            except:
                print("Invalid Argument: File name")
                continue
        elif uinDs.lower() == 'stats':
            dsPath = input("WIP enter to continue")
            # this will eventually gather meaningful metrics on an input dataset
        elif uinDs.lower() == 'h':
            return
        else:
            print("Invalid input...")
            continue

def runSpManager():
    '''
    This function handles running the webscrapers within the dataset builder
    '''
    while True:
        printSpHome()
        uinSp = input("What would you like to do?\nCommands:\nrs : scrape for verilog repos\nrc : scrape for verilog code\nmd : manage scraped file banks\nh : return to home\n.\n.\n.\n>> ")
        if uinSp.lower() == 'rs':
            try:
                start_time = time.time()
                log_entry = f'Began Scraping script at: {start_time}'
                builderWriteLog(log_entry)
                repo_scraper.runScraper()
                log_entry = f'Finished scraping script at: {time.time()} - total runtime: {time.time() - start_time} seconds'
            except:
                print("Error: Scraper has crashed unexpectedly")
        elif uinSp.lower() == 'rc':
            print("WIP")
        elif uinSp.lower() == 'md':
            target_dir = input("What is your target unfiltered data directory path (relative to the current directory)?\n.\n.\n.\n(ex. .\\all_my_files_here)>> ")
            filter_dir = input("What path would you like to send your files to (relative to the current directory)\n.\n.\n.\n(ex. .\\filtered_files\\)>> ")
            target_types = input("Enter however many file types you want to filter for separated by spaces\n.\n.\n.\n(ex. '*.txt *.v *.csv')>> ")
            if filter_dir[-1] != '\\':
                filter_dir += '\\'
            if not os.path.exists(filter_dir):
                os.makedirs(filter_dir)
            # try:
            start_time = time.time()
            type_list  = target_types.split(" ")
            file_count = 0
            total_size = 0
            for ftype in type_list:
                for ifile in glob.glob(os.path.join(target_dir, '**', f'{ftype}'), recursive=True):
                    # dest_fname = str(file_count) + os.path.basename(dest_fname)
                    # print(dest_fname)
                    destination_file = os.path.join(filter_dir, f'{file_count}-{os.path.basename(ifile)}')
                    with open(ifile, 'r') as src:
                        with open(destination_file, 'w') as dst:
                            # Read from source and write to destination in chunks
                            print(f"Reading {ifile} into {destination_file}")
                            for line in src:
                                dst.write(line)
                    total_size += os.path.getsize(destination_file)
                    file_count += 1
            end_time = time.time()
            # log_entry = f'Completed filtering {file_count} in  seconds'
            # print(log_entry)
            print('yes')
            # builderWriteLog(log_entry)
            # except:
            #     print("Invalid Argument: File Name")
        elif uinSp.lower() == 'h':
            return
        else:
            print("Invalid Input")
            continue

#----Builder Script top level----#
def runBuilder():
    '''
    This is a top level function to run all functions within the builder
    '''
    builderInitLog()
    while True:
        printHome()
        uin = input("What would you like to do?\nmdf : manage dataframes\nmsp : manager scrapers\nmds : manage datasets\nhelp : info about this script\nq : quit builder\n.\n.\n.\n>> ")
        if uin.lower() == "mdf":
            runDfManager()
        elif uin.lower() == "msp":
            runSpManager()
        elif uin.lower() == "mds":
            runDsManager()
        elif uin.lower() == "help":
            print("This is the Dataset Builder v2.0 created by Samuel Bush (contact: samuelkbush@gmail.com)")
            print("This builder serves three main purposes:\n    - Create/Update a pandas dataframe for loading files for the dataset\n    - Read a specified dataframe into a .json dataset\n    - Run GitHub scraping scripts to get data for the sets & clean data\n")
            print("NOTE: The dataframe builder can and will make its own dataframes unless given one which already exists\n    - If you are using a dataframe not made by the builder it must be in a .csv format with one column named 'text'")
            print("NOTE: When adding to a dataframe if you enter a dataframe which already has data, the new data will be appended to it")
            print("NOTE: When parsing into JSON, if you enter a JSON which already has data, the new data will be appended to it")
            input("Press enter to leave help menu>> \n")
        elif uin.lower() == "q":
            print()
        else:
            print("Invalid input...")
            continue

#import & standalone handling
def main():
    print("Opening Builder Script")
    runBuilder()

if __name__ == "__main__":
    main()