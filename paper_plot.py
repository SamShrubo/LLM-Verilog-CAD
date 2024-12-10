import numpy as np
import matplotlib.pyplot as plt
import csv

array1 = []
with open('row_tokens.csv', mode='r', newline='') as filed:
        reader = csv.DictReader(filed)
        for row in reader:
            array1.append(int(row["row_length"]))
array2 = []
with open('verigen_row_tokens.csv', mode='r', newline='') as filed:
        reader = csv.DictReader(filed)
        for row in reader:
            array2.append(int(row["row_length"]))

# Define logarithmic bins, e.g., from 1 to 10 million
bins = np.logspace(1, 8, num=8)  # 20 bins from 10^1 (10) to 10^7 (10M)

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(4.5, 2.2))

# Set bar width for side-by-side placement
plt.rcParams.update({"font.size": 8})
bar_width = 0.7
data = [array1, array2]
colors = ['#FFF2CC', '#DAE8FC']
labels = ['FreeSet', 'VeriGen']
# Plot histograms with a slight offset for each dataset
# plt.hist(array1, bins=bins, color='#FFF2CC', edgecolor='grey', label='OpenSet', alpha=0.7, align='left')
# plt.hist(array2, bins=bins, color='#DAE8FC', edgecolor='grey', label='VeriGen', alpha=0.7)
plt.hist(data, bins, histtype='bar', color=colors, edgecolor='grey', label=labels, rwidth=0.9)
# Add labels and title
plt.xlabel('File Length (# Chars)')
plt.ylabel('Frequency (# Files)')
plt.xscale('log')  # Set x-axis to logarithmic scale
# bin_labels = ['10^0-10^1', '10^1-10^2', '10^2-10^3', '10^3-10^4', '10^4-10^5', '10^5-10^6', '10^6-10^7', '10^7-10^8']

bin_labels = ['$10^1$', '$10^2$', '$10^3$', '$10^4$', '$10^5$', '$10^6$', '$10^7$', '$10^8$']
# plt.xticks(bins, labels=[f'{int(b):,}' for b in bins], rotation=45)  # Format ticks with commas
plt.xticks(bins, labels=bin_labels, rotation=45)
plt.minorticks_off()
y_labels = ['20k', '40k', '60k', '80k', '100k']
plt.yticks(ticks=[20000,40000,60000,80000, 100000], labels=y_labels)
# Add legend
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
plt.savefig('combined_histogram_result.pdf')
