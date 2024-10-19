import pandas as pd
import os
import json
import time
import sys
import glob

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

with open("C:\\Users\\samue\\OneDrive\\Documents\\Verilog-LLMCAD\\LLM-Verilog-CAD\\datarun1\\datarun1_info.txt", 'r', encoding='utf-8', errors='ignore') as fd:
    total_size  = 0
    # Check if the line contains "Size (KB)"
    for line in fd:
        if "Size (KB)" in line:
            # Extract the size value
            # Assuming the format is "Size (KB): <value>"
            size_str = line.split(":")[1].strip()
            size_kb = int(size_str)  # Convert the size to an integer
            # Add the size to the counter
            total_size += size_kb
    print(f"Total size of repos (KB): {total_size}")
