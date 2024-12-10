import json
from rouge import Rouge
from datasets import load_dataset
from huggingface_hub import login
import sys

def loading(current, total, length=30):
    '''
    This function is a random loading animation function so you can see
    the scraper and builder are just slow not broken.
    '''
    progress = current / total
    bar_length = int(length * progress)
    bar_fraction = ((progress * length) - bar_length)
    partial_bar = ""
    if bar_fraction > (7/8):
        partial_bar = "▉"
    elif bar_fraction > (3/4):
        partial_bar = "▊"
    elif bar_fraction > (5/8):
        partial_bar = "▋"
    elif bar_fraction > (1/2):
        partial_bar = "▌"
    elif bar_fraction > (3/8):
        partial_bar = "▍"
    elif bar_fraction > (1/4):
        partial_bar = "▎"
    elif bar_fraction > (1/8):
        partial_bar = "▏"
    bar = "[" + "█" * bar_length + partial_bar + "-" * (length - bar_length - len(partial_bar)) + "]"
    # Display the progress bar with percentage
    sys.stdout.write(f"\r{bar} {progress * 100:.2f}%")
    sys.stdout.flush()

login()
# Load the Hugging Face dataset
print("loading dataset")
dataset = load_dataset('SamShrubo/F24-FFH-Verilog', split='train')
print("loaded dataset")
# Initialize the ROUGE scorer
rouge = Rouge()

# List of concatenated strings (golden model references)
concatenated_strings = []
print("creating verilogeval datasets")
# Open the JSONL file
with open('VerilogEval_Machine.jsonl', 'r') as file:
    # Iterate through each line in the file
    for line in file:
        # Parse the line as a JSON object
        data = json.loads(line)
        
        # Concatenate the 'prompt' and 'canonical_solution' fields
        concatenated_string = data['prompt'] + data['canonical_solution']
        
        # Add the concatenated string to the list
        concatenated_strings.append(concatenated_string)

# Initialize a list to store the results
results = []

# Start index
start_index = 0

print("Iterating through items")
# Iterate through each item in the dataset starting from start_index
length = len(dataset)
for idx in range(start_index, length):
    item = dataset[idx]
    text = item['text']
    max_rouge_l_score = 0


    # Compare with each unique item in concatenated_strings
    for reference in concatenated_strings:
        try:
            scores = rouge.get_scores(text, reference, avg=True)
            rouge_l_f_score = scores["rouge-l"]["f"]
            if rouge_l_f_score > max_rouge_l_score:
                max_rouge_l_score = rouge_l_f_score
        except Exception as e:
            print(f"Error encountered for index {idx}: {e}.")
            continue

    # Check if the maximum ROUGE-L score is greater than 0.5
    pass_check = max_rouge_l_score <= 0.5
    print("Idx: ", idx, "Passed: ", pass_check, "Score: ", max_rouge_l_score)
    # Store the result with index
    results.append({
        'index': idx,
        'text': text,
        'max_rouge_l_score': max_rouge_l_score,
        'pass': pass_check
    })

# Save the results to a JSON file
with open('results.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)

# Print the results
for result in results:
    print(result)