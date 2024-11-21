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

def loading(current, total, to_large, length=50):
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
    sys.stdout.write(f"\r{bar} {int(progress * 100)}% | [{current}/{total}] Files | Identified {to_large} Files Greater Than 2048 Tokens")
    sys.stdout.flush()

def tokenCheck(row):
    tokens = tokenizer.encode(row["text"], truncation=False, add_special_tokens=False)
    return (len(tokens) > 2048)

row_lengths = []
if uin.lower() == 'y':
    
    fd = open("API_KEY/huggingface.txt", 'r')
    login()

    # Load the dataset with streaming enabled
    dataset = load_dataset('SamShrubo/F24-FFH-Verilog', split='train', streaming=True)
    # Collect row lengths
    
    # Open a CSV file to save lengths
    with open('tokened.csv', mode='w', newline='', encoding='utf-8', errors="ignore") as filed:
        writer = csv.writer(filed)
        writer.writerow(["row_index", "row_data"])  # Header for CSV
        data = enumerate(dataset)
        length = 224846
        count_copyrighted = 0
        for i, row in data:
            row_data = row['text']
            if tokenCheck(row):
                count_copyrighted += 1
                writer.writerow([count_copyrighted, row_data])
            else:
                fullfiletodf(row_data, "tokened_set")
            loading(i, length, count_copyrighted)
            
            
            
    print("\nRow lengths saved to row_lengths.csv")

# # Define logarithmic bins
# min_val = min(row_lengths)
# max_val = max(row_lengths)
# num_bins = 20
# log_bins = np.logspace(np.log10(min_val), np.log10(max_val), num=num_bins)

# # Create the histogram with logarithmic bins
# counts, bin_edges, _ = plt.hist(row_lengths, bins=log_bins)

# # Label each bin with the range it covers (for large datasets, show every few bins to avoid clutter)
# bin_labels = [f"{int(bin_edges[i]):,} - {int(bin_edges[i+1]):,}" for i in range(len(bin_edges) - 1)]
# plt.xticks(bin_edges[::5], labels=bin_labels[::5], rotation=45, ha='right')  # Show every 5th bin label

# # Set log scale for x-axis
# plt.xscale('log')

# # Set labels and title
# plt.xlabel('Row Length Range (Log Scale)')
# plt.ylabel('Frequency')
# plt.title('Histogram of Row Lengths with Logarithmic Binning')

# plt.show()