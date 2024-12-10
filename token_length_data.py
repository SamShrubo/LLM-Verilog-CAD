import numpy as np
import matplotlib.pyplot as plt
import csv

array1 = []
with open('row_tokens.csv', mode='r', newline='') as filed:
    reader = csv.DictReader(filed)
    for row in reader:
        array1.append(int(row["row_data"]))
    over_2048 = 0
    our_count = len(array1)
    our_tot = 0
    over_2048_size = 0
    less_than_100_tokens = 0
    less_than_100_tokens_size = 0
    for item in array1:
        our_tot += item
        if item > 2048:
            over_2048 += 1
            over_2048_size += item
        if item < 200:
            less_than_100_tokens += 1
            less_than_100_tokens_size += item
    verigen_avg = our_tot / our_count
    print("-------Our Dataset--------")
    print(f"Max Token Count in FreeSet: {max(array1)}")
    print(f"Min Token Count in FreeSet: {min(array1)}")
    print(f"Avg Token Count in FreeSet: {verigen_avg}")
    print(f"Total tokens in dataset: {our_tot}")
    print(f"Number of entries Greater than 2048: {over_2048}")
    print(f"Number of entries Less than 2048: {our_count - over_2048}")
    print(f"Percentage greater than 2048: {(over_2048 / (our_count)) * 100:.2f}%")
    print(f"Actual token size of entries over 2048: {over_2048_size}")
    print(f"- Total remaining usable tokens: {our_tot - over_2048_size}")
    print(f"Percentage of token size of entries greater than 2048: {(over_2048_size / (our_tot)) * 100:.2f}%")
    print(f"\nNumber of entries Less than 200 tokens: {less_than_100_tokens}")
    print(f"Actual token size of entries less than 200 tokens: {less_than_100_tokens_size}")

array2 = []
with open('verigen_row_tokens.csv', mode='r', newline='') as filed:
    reader = csv.DictReader(filed)
    for row in reader:
        array2.append(int(row["row_data"]))
    over_2048 = 0
    verigen_count = len(array2)
    verigen_tot = 0
    over_2048_size = 0
    less_than_100_tokens = 0
    less_than_100_tokens_size = 0
    for item in array2:
        verigen_tot += item
        if item > 2048:
            over_2048 += 1
            over_2048_size += item
        if item < 200:
            less_than_100_tokens += 1
            less_than_100_tokens_size += item

        
    verigen_avg = verigen_tot / verigen_count
    print("\n\n-------Verigen Dataset--------")
    print(f"Max Token Count in VeriGen: {max(array2)}")
    print(f"Min Token Count in VeriGen: {min(array2)}")
    print(f"Avg Token Count in VeriGen: {verigen_avg}")
    print(f"Total tokens in dataset: {verigen_tot}")
    print(f"Number of entries Greater than 2048: {over_2048}")
    print(f"Number of entries Less than 2048: {verigen_count - over_2048}")
    print(f"Percentage greater than 2048: {(over_2048 / (verigen_count)) * 100:.2f}%")
    print(f"Actual token size of entries over 2048: {over_2048_size}")
    print(f"- Total remaining usable tokens: {verigen_tot - over_2048_size}")
    print(f"Percentage of token size of entries greater than 2048: {(over_2048_size / (verigen_tot)) * 100:.2f}%")
    print(f"\nNumber of entries Less than 200 tokens: {less_than_100_tokens}")
    print(f"Actual token size of entries less than 200 tokens: {less_than_100_tokens_size}")

# Define logarithmic bins, e.g., from 1 to 10 million
bins = np.logspace(1, 8, num=40)  # 20 bins from 10^1 (10) to 10^8 (100M)

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 4))

# Set bar width for side-by-side placement
plt.rcParams.update({"font.size": 8})
bar_width = 0.7
data = [array1, array2]
colors = ['#FFF2CC', '#DAE8FC']
labels = ['FreeSet', 'VeriGen']
# Plot histograms with a slight offset for each dataset
# plt.hist(array1, bins=bins, color='#FFF2CC', edgecolor='grey', label='OpenSet', alpha=0.7, align='left')
# plt.hist(array2, bins=bins, color='#DAE8FC', edgecolor='grey', label='VeriGen', alpha=0.7)
plt.hist(data, bins, histtype='bar', color=colors, edgecolor='grey', label=labels)
plt.axvline(x = 2048, color = 'b', label = 'Context Window - 2048 Tokens')
# Add labels and title
plt.xlabel('Tokens Per File')
plt.ylabel('Frequency (# Files)')
plt.xscale('log')  # Set x-axis to logarithmic scale
# bin_labels = ['10^0-10^1', '10^1-10^2', '10^2-10^3', '10^3-10^4', '10^4-10^5', '10^5-10^6', '10^6-10^7', '10^7-10^8']

bin_labels = ['$10^1$', '$10^2$', '$10^3$', '$10^4$', '$10^5$', '$10^6$', '$10^7$', '$10^8$']
# plt.xticks(bins, labels=[f'{int(b):,}' for b in bins], rotation=45)  # Format ticks with commas
# plt.xticks(bins, labels=bin_labels, rotation=45)
y_labels = ['5k', '10k', '15k']
plt.yticks(ticks=[5000, 10000,15000], labels=y_labels)
# Add legend
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
plt.savefig('combined_histogram_result.pdf')
