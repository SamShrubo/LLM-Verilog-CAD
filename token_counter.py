import matplotlib.pyplot as plt
import sys
from huggingface_hub import login
from datasets import load_dataset
import csv
import numpy as np
import pandas as pd
import os
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

def fullfiletodf(readData, dataframeName="dataframe", max_size_gb=1):
    '''
    This function is designed to parse an inputted file entirely
    and append it to a designated `dataframeName` csv file.
    '''

    tempdf = pd.DataFrame({'text' : [readData]})

    file_part = 0
    # while os.path.exists(f"{dataframeName}_part{file_part}.csv"):
    #     file_part += 1
    outFileName = f"{dataframeName}_part{file_part}.csv"

    while True:
        if os.path.exists(outFileName) and os.path.getsize(outFileName) >= (max_size_gb * 1024 ** 3):
            file_part += 1
            outFileName = f"{dataframeName}_part{file_part}.csv"
        else:
            tempdf.to_csv(outFileName, mode='a', header=not os.path.exists(outFileName), index=False)
            break

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

uin = input("Would you like to refill copyright.csv with new data? (Y/N)>>  ")

def loading(current, total, length=100):
    '''
    This function is a random loading animation function so you can see
    the scraper and builder are just slow not broken.
    '''
    progress = current / total
    bar_length = int(length * progress)
    remainder = (progress * length) - bar_length

    partial_block_chars = [' ', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']
    partial_block = partial_block_chars[int(remainder * 8)]
    bar = "[" + "█" * bar_length + partial_block + "-" * (length - bar_length - 1) + "]"
    # Display the progress bar with percentage
    sys.stdout.write(f"\r{bar} {progress * 100:.2f}% | [{current}/{total}] Files")
    sys.stdout.flush()

def tokenCount(row):
    tokens = tokenizer.encode(row["text"], truncation=False, add_special_tokens=False)
    return len(tokens)

row_lengths = []
if uin.lower() == 'y':
    # fd = open("API_KEY/huggingface.txt", 'r')
    login()

    # Load the dataset with streaming enabled
    dataset = load_dataset('shailja/Verilog_GitHub', split='train', streaming=True)
    # Collect row lengths
    
    # Open a CSV file to save lengths
    with open('verigen_row_tokens.csv', mode='w', newline='', encoding='utf-8', errors="ignore") as filed:
        writer = csv.writer(filed)
        writer.writerow(["row_index", "row_data"])  # Header for CSV
        data = enumerate(dataset)
        length = 224846
        for i, row in data:
            
            writer.writerow([i, tokenCount(row)])
            loading(i, length)
            
                
    print("\nRow lengths saved to row_lengths.csv")

