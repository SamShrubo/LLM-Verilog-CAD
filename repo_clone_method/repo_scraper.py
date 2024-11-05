import requests
import subprocess
import os
import os.path as op
import time
import pandas as pd
import winsound
from datetime import datetime

#-----Constants-----#
# grab API Key, replace with path to key file
fd = open("API_KEY/githubKey.txt", 'r')
GITHUB_API = fd.read()
fd.close()

# github URL
SEARCH_API_URL = 'https://api.github.com/search/repositories'
RATE_LIMIT_URL = 'https://api.github.com/rate_limit'

#-----Global Variables-----#
info_filename = ""
url_filename = ""
rawdata_foldername = ""
log_filename = ""
clone_dir = ""

#request headers
headers = {
    'Authorization': f'token {GITHUB_API}',
    'Accept': 'application/vnd.github.v3+json'
}

# Define the query parameters
# tons of options mit and apaches have most
licenses  = ['mit', 'apache-2.0', 'gpl-2.0', 'gpl-3.0', 'lgpl-2.1', 'lgpl-3.0', 'mpl-2.0', 'unlicense', 
             'cc0-1.0', 'epl-1.0', 'epl-2.0', 'bsd-2-clause', 'bsd-3-clause', 'bsl-1.0', 'zlib']
languages = ['Verilog']
filenames =['.v', '.vh', '.vlg', '.verilog']


#-----Functions-----#
def getMetricNames():
    '''
    This Function names the files required for tracking the data within this scraper
    '''
    global info_filename, url_filename, rawdata_foldername, log_filename, clone_dir
    while True:
        uin = input("What would you like to title this scraper run?\n.\n.\n.\n(ex. repos, datarun1, etc.)>> ")
        if uin.find(" ") != -1:
            print("Error: There cannot be spaces in the name")
            continue
        break
    run_foldername     = ".\\" + uin
    info_filename      = run_foldername + "\\" + uin + "_info.txt"
    url_filename       = run_foldername + "\\" + uin + "_urls.csv"
    rawdata_foldername = run_foldername + "\\" + uin + "-Raw-Data"
    log_filename       = run_foldername + "\\" + uin + "_log.txt"
    #create clone dir
    clone_dir = rawdata_foldername
    os.makedirs(clone_dir, exist_ok=True)

def check_rate_limit():
    '''
    This function checks for errors related to maxing out the github api rate limit, if reached
    '''
    rate_response = requests.get(RATE_LIMIT_URL, headers=headers)
    if rate_response.status_code == 200:
        rate_data = rate_response.json()
        core_remaining = int(rate_data['resources']['core']['remaining'])
        reset_time = int(rate_data['resources']['core']['reset'])

        if core_remaining <= 10:
            # Wait until the reset time
            current_time = int(time.time())
            wait_time = max(reset_time - current_time, 0)
            print(f"Rate limit reached. Waiting for {wait_time / 60:.2f} minutes until reset...")
            time.sleep(wait_time + 10)  # Wait for rate limit reset plus a buffer
            return True
        else:
            return False

def runScraper():
    '''
    This function handles running the scraping script
    '''
    count = 0 #incorrect make sure to subtract from this to get the starting value + u r a dingbat
    total_repo_size = 0
    successful = count
    successful_repo_size = 0
    getMetricNames()
    print("Beginning search run...")
    start_time = time.time()

    # Loop through each year from 2008 to the current year
    current_year = datetime.now().year
    for year in range(2023, current_year+1):
        # start_date = f"{year}-01-01"
        # end_date = f"{year}-12-31"
        quarters = [
            ("Q1", f"{year}-01-01", f"{year}-03-31"),
            ("Q2", f"{year}-04-01", f"{year}-06-30"),
            ("Q3", f"{year}-07-01", f"{year}-09-30"),
            ("Q4", f"{year}-10-01", f"{year}-12-31"),
        ]
        for quarter_name, start_date, end_date in quarters:
            print(f"\n--- Searching for repos created in {year} {quarter_name} ---\n")
            for license_ in licenses:
                for language in languages:
                    params = {
                        'q': f'language:{language} license:{license_} created:{start_date}..{end_date}',
                        'sort': 'stars',                      # Sort by stars (popularity)
                        'order': 'desc',                      # Descending order
                        'per_page': 100,                       # Number of results per page
                        'page': 1                             # Page number
                    }

                    # while loop for any pagination
                    while True:
                        # Send the request to GitHub's search API
                        response = requests.get(SEARCH_API_URL, headers=headers, params=params)

                        # Check if the response is successful
                        print(f"Querying: {params['q']}, Page: {params['page']}...", end='')
                        while response.status_code == 403:
                            print("403 Error: Potential rate limit cap")
                            if check_rate_limit():
                                # after wait period attempt the request again
                                response = requests.get(SEARCH_API_URL, headers=headers, params=params)
                            else:
                                print(f"Unknown Error Received: skipping query: {response.status_code} - {response.text}")
                                break
                        
                        if response.status_code == 200:
                            data = response.json()
                            repositories = data['items']
                            print(f" Success, returned {len(repositories)} repos")
                            logfd = open(log_filename, 'a')
                            logfd.write(f"Querying: {params['q']}, Page: {params['page']}... Success, returned {len(repositories)} repos\n")
                            logfd.close()
                            # if no files returned then page is empty
                            if not repositories:
                                print("No more files found on this page. Moving to the next query.")
                                params['page'] += 1
                                time.sleep(7)
                                break
                            
                            # Print repository information
                            outfd = open(info_filename, 'a', encoding='utf-8', errors="ignore")
                            for repo in repositories:
                                # fill dataframe
                                newStructure = {'URL' : [repo['html_url']]}
                                if not op.isfile(url_filename):
                                    df = pd.DataFrame(newStructure)
                                else:
                                    df = pd.read_csv(url_filename)
                                    df = pd.concat([df, pd.DataFrame(newStructure)], ignore_index=True)
                                    # duplicate checking - prevent adding duplicates
                                    dupes = df.duplicated()
                                    if not (df[dupes].empty):
                                        continue
                                df.to_csv(url_filename, index=False)


                                # write to doc file
                                outfd.write(f"Name: {repo['name']}\n")
                                outfd.write(f"Owner: {repo['owner']['login']}\n")
                                outfd.write(f"Size (KB): {repo['size']}\n")
                                outfd.write(f"URL: {repo['html_url']}\n")
                                outfd.write(f"Description: {repo['description']}\n")
                                count += 1
                                total_repo_size += repo['size']
                                outfd.write(f"Repo-Count: {count}\n")
                                outfd.write(f"Current-Bank-Size-(KB): {total_repo_size}\n\n")
                                print(f"Current Bank Size: {total_repo_size} KB")
                                print(f"Time Elapsed: {time.time() - start_time} Seconds")

                                # clone into clone dir
                                # add count into the clone name to prevent failures due to same repo names
                                clone_path = os.path.join(clone_dir, license_, f"{count}-{repo['name']}")
                                try:
                                    subprocess.run(['git', 'clone', repo['html_url'], clone_path], check=True)
                                    print(f"Successfully cloned {repo['name']} to {clone_path}\n")
                                    successful += 1
                                    outfd.write(f"Cloned Successfully Count: {successful}\n\n")
                                    successful_repo_size += repo['size']
                                #check for failed cloning
                                except subprocess.CalledProcessError as e:
                                    print(f"Failed to clone {repo['name']}: {e}\n")
                                    outfd.write(f"Cloned Successfully Count: {successful}\n\n")
                                    logfd = open(log_filename, 'a')
                                    logfd.write(f"Failed to clone {repo['name']}: {e}\n")
                                    logfd.close()
                            # print(count)
                            # Go to the next page of results
                            params['page'] += 1
                        else:
                            print(f"Failed to fetch repositories: {response.status_code} - {response.text}")
                            break
                    time.sleep(2)

    outfd.close()
    end_time = time.time()
    elapsed_time = end_time - start_time

    # print metrics to console
    print("\n\n\nSearch run completed:")
    print(f'Size of found repos: {total_repo_size} KB')
    print(f'Total # found repos: {count}')
    print(f'Total # successfully cloned repos: {successful}')
    print(f'Total # failed repo clones: {count - successful}')
    print(f'Size of successfully cloned repos: {successful_repo_size} KB')
    print(f'Size of failed repo clones: {total_repo_size - successful_repo_size} KB')
    print(f"Completed in {elapsed_time} seconds")

    #write metrics to log
    logfd = open(log_filename, 'a')
    logfd.write("Search run completed:\n")
    logfd.write(f'Size of found repos: {total_repo_size} KB\n')
    logfd.write(f'Total # found repos: {count}\n')
    logfd.write(f'Total # successfully cloned repos: {successful}\n')
    logfd.write(f'Total # failed repo clones: {count - successful}\n')
    logfd.write(f'Size of successfully cloned repos: {successful_repo_size} KB\n')
    logfd.write(f'Size of failed repo clones: {total_repo_size - successful_repo_size} KB\n')
    logfd.write(f"Completed in {elapsed_time} seconds\n\n\n")
    logfd.close()

    #notify sound of completion
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)    