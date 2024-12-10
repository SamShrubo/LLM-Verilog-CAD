import os
from huggingface_hub import login
from datasets import load_dataset
import csv
import matplotlib.pyplot as plt
import sys

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

login()

# Load the dataset with streaming enabled
dataset = load_dataset('SamShrubo/F24-Verilog-Generation', split='train', streaming=True)

row_lengths = []

fd = open('row_lengths.csv', mode='w', newline='')
writer = csv.writer(fd)
writer.writerow(["row_index", "row_length"])

# Loop through each row and evaluate the length
for i, row in enumerate(dataset):
    row_length = len(str(row))  # Convert row to string and get its length
    if row_length < 2500000:
        row_lengths.append(row_length)
        writer.writerow([i, row_length])
    loading(i, 1000)

    # Optionally, break after a certain number of rows if you just want a sample
fd.close()

# Plot the histogram
plt.hist(row_lengths, bins=25)  # Adjust bins as needed
plt.xlabel('Row Length')
plt.ylabel('Frequency')
plt.title('Histogram of Row Lengths')
plt.show()