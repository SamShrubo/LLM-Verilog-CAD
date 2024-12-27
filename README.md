# GitGuru V0.0 (Dataset Builder)

This GitHub Repository contains all file used in the process of scraping and designing Verilog datasets for continuous pretraining on large language models. This README contains documentation and instructions to find files to recreate any dataset created from GitHub open source data.

The bulk of data processing runs through ds_builder.py, which manages webscraping and dataset creation, deduplication checks and cleaning scripts are separate from the ds_builder.py file.

## NOTE: GitHub API

The webscraper requires a GitHub API access key to gather the data, the script will read an API key by default from the route `./API_KEY/githubKey.txt` from the root directory you are runing the ds_builder.py script from.

## Instructions:

1. Acquire a GitHub API key and add it into a file at the path `./API_KEY/githubKey.txt`
2. All imported modules are not included, you must run pip install for any missing modules in the code
3. To begin scraping data:
   - Run ds_builder.py
   - Follow the instructions in the script and provide user input to specify your target search criteria, destination paths, etc, the script will then be able to begin scraping data from GitHub based on your inputs
   - To filter scraped data to get specific file types (the scraper will blindly clone repositories, not target files) from the scraper window you can run the command "manage scraped file banks" and then set settings to filter for the desired files
4. To begin creating a dataset from a target set of scraped data there are 2 main steps - Forming a dataframe, and then building the dataset:
   - For forming the dataframe, run the command for "manage dataframes" then run the command for "read all files within a target directory" to easily read all of the files from a filtered webscraping run, or any general bank of files, the script will then autoformat them into individual rows into 1GB dataframe files, it is divided to prevent memory issues when handling massive amounts of data.
   - For forming the final dataset .JSON file, run the command for "manage datasets" in the ds_builder home, and you can create, or append dataframes to a dataset file as necessary using the commands
5. *Cleaning Processes and File-Level Copyright Checks* are handled in a separate set of scripts
