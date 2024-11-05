import os
import sys
import shutil
import time
from datasketch import MinHash, MinHashLSH
from sklearn.feature_extraction.text import CountVectorizer


# params
minhash_num_perm = 512 # can increase for more precision
similarity_threshold = 0.85

# initialize LSH
lsh = MinHashLSH(threshold=similarity_threshold, num_perm=minhash_num_perm)

def preprocess_file(file_path):
    '''This function processes a file into tokens for deduplication'''
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    # defining token pattern to get all unicode
    token_pattern = r'(?u)\b\w+\b'
    vectorizer = CountVectorizer(token_pattern=token_pattern, ngram_range=(1, 1), stop_words='english').fit([text])
    tokens = set(vectorizer.get_feature_names_out())
    return tokens

def get_minhash_sig (tokens):
    '''This function processes a set of tokens to a minhash signature'''
    m = MinHash(num_perm=minhash_num_perm)
    for token in tokens:
        m.update(token.encode('utf8'))
    return m

def dedupe_files(dirpath, destpath, log):
    duplicates = []
    files = os.listdir(dirpath)
    size = len(files)
    for file_name in files:
        logfd = open(log, 'a', encoding='utf-8', errors='ignore')
        try:
            file_path = os.path.join(dirpath, file_name)
            tokens = preprocess_file(file_path)
            minhash = get_minhash_sig(tokens)

            if len(lsh.query(minhash)) > 0:
                duplicates.append(file_name)
                logfd.write(f'Duplicate - {file_name}\n')
            else:
                lsh.insert(file_name, minhash)
                # copy file to deduplicated folder
                shutil.copy(file_path, os.path.join(destpath, file_name))
            # print loading bar
            loading(files.index(file_name), size)
        except:
            print(f'\n\nFailed to check file: {file_name}\n\n')
            logfd.write(f'Failed to check file: {file_name}\n')
        logfd.close()
    
    return duplicates

def loading(current, total, length=50):
    '''
    This function is a random loading animation function so you can see
    the scraper and builder are just slow not broken.
    '''
    progress = current / total
    bar_length = int(length * progress)
    bar = "[" + "#" * bar_length + "-" * (length - bar_length) + "]"
    # Display the progress bar with percentage
    sys.stdout.write(f"\r{bar} {progress * 100:.2f}% : [{current}/{total} Files]")
    sys.stdout.flush()

filepath = input("Where are your files located?\n\n\n\n(ex. .\\files-here\\)>> ")
destpath = input("Where would you like to send deduplicated files?\n\n\n\n(ex. .\\files-here\\)>> ")
run_name = input("What do you want to name this run?\n\n\n\n(ex. dedupe1)>> ")
log_file = run_name + '.txt'
os.makedirs(destpath, exist_ok=True)  # Create the folder if it doesn't exist

# run deduplication
start_time = time.time()
dupes = dedupe_files(filepath, destpath, log_file)
end_time = time.time()
print(f'Completed in {end_time - start_time} seconds')
print(f'Found {len(dupes)} duplicate files')
print(f'Deduplicated files sent to {destpath}')