import matplotlib.pyplot as plt
import sys
from huggingface_hub import login
from datasets import load_dataset
import csv
import numpy as np

uin = input("Would you like to refill row_lengths.csv with new data? (Y/N)>>  ")

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

row_lengths = []

if uin.lower() == 'y':
    login()

    # Load the dataset with streaming enabled
    dataset = load_dataset('shailja/Verilog_Github', split='train', streaming=True)
    # Collect row lengths
    

    # Open a CSV file to save lengths
    with open('row_lengths_verigen.csv', mode='w', newline='') as filed:
        writer = csv.writer(filed)
        writer.writerow(["row_index", "row_length"])  # Header for CSV
        data = enumerate(dataset)
        length = 227847
        for i, row in data:
            row_length = len(str(row))  # Calculate row length
            row_lengths.append(row_length)  # Append to list for histogram
            writer.writerow([i, row_length])  # Write to CSV file
            loading(i, length)
            
    print("\nRow lengths saved to row_lengths.csv")
else:
    # fill row lengths from csv
    with open('row_lengths_verigen.csv', mode='r', newline='') as filed:
        reader = csv.DictReader(filed)
        for row in reader:
            row_lengths.append(int(row["row_length"]))

# Define logarithmic bins
min_val = min(row_lengths)
max_val = max(row_lengths)
num_bins = 20
log_bins = np.logspace(np.log10(min_val), np.log10(max_val), num=num_bins)

# Create the histogram with logarithmic bins
counts, bin_edges, _ = plt.hist(row_lengths, bins=log_bins)

# Label each bin with the range it covers (for large datasets, show every few bins to avoid clutter)
bin_labels = [f"{int(bin_edges[i]):,} - {int(bin_edges[i+1]):,}" for i in range(len(bin_edges) - 1)]
plt.xticks(bin_edges[::5], labels=bin_labels[::5], rotation=45, ha='right')  # Show every 5th bin label

# Set log scale for x-axis
plt.xscale('log')

# Set labels and title
plt.xlabel('Row Length Range (Log Scale)')
plt.ylabel('Frequency')
plt.title('Histogram of Row Lengths with Logarithmic Binning')

plt.show()