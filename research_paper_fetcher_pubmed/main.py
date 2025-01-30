import sys #Importing necessary libraries
import os
from research_paper_fetcher_pubmed.fetcher import search_pubmed_and_fetch_results, fetch_details, parse_details, save_to_csv

def print_csv(results): #Prints the results in a csv format
    if not results:
        print("No results to display.")
        return
    
    print(f"Contents of results:")
    for index, result in enumerate(results):
        print(f"\nArticle {index + 1}")
        for key, value in result.items():
            print(f"{key}: {value}")
        print("-" * 50)


def print_help(): #Prints the help message
    print("""
Usage: get-papers-list <query>

Options:
  get-papers-list -h  (or) get-papers-list --help                                              Display usage instructions.
  get-papers-list -d "query" (or)  get-papers-list --debug "query"                             Print debug information during execution.
  get-papers-list -f filename.csv "query" (or) get-papers-list --file filename.csv "query"     Save results to a CSV file.
  get-papers-list "query"                                                                      Search for papers and print to console.
    """)


def main(): #Main function
    debug_mode = False
    file_output = None
    
    # Check if the user has provided any arguments
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print_help()
        sys.exit(0) # If length of arguments is less than 2 or the first argument is -h or --help, print help and exit the program

    # Check for optional arguments
    if '-d' in sys.argv or '--debug' in sys.argv: # Searches for -d or --debug in the arguments
        debug_mode = True
    
    # Check for file output argument
    if '-f' in sys.argv or '--file' in sys.argv:
        try:
            file_index = sys.argv.index('-f') if '-f' in sys.argv else sys.argv.index('--file')
            file_output = sys.argv[file_index + 1]  # Get the filename argument after -f or --file
        except IndexError:
            print("Error: -f / --file requires a filename argument.")
            sys.exit(1) # Exit the program with an error code if the command is incorrect

    query = sys.argv[-1] # Gets the query
    
    if debug_mode:
        print(f"Debug mode enabled. Searching for papers on: {query}") # If the query is running in debug mode
    else:
        print(f"Searching for papers on: {query}") # If the query is not running in debug mode

    results = []
    pmids = search_pubmed_and_fetch_results(query) #Searches for the query in pubmed and fetches the results
    if debug_mode:
        print(f"Found {len(pmids)} PubMed IDs.")

    for pmid in pmids:
        if debug_mode:
            print(f"Fetching details for PubMed ID: {pmid}")
        xml_data = fetch_details(pmid) # Fetches the details of the paper
        if xml_data:
            details = parse_details(xml_data) # Parses the details of the paper
            results.append(details)
        else:
            if debug_mode:
                print(f"Failed to fetch details for PubMed ID: {pmid}")

    if results: # If there are results
        if file_output:
            print(f"Saving {len(results)} results to {file_output}.")
            save_to_csv(results, filename=file_output) # Saves the results to a csv file
            full_path = os.path.abspath(file_output) # Gets the absolute path of the file
            print(f"Results saved to {full_path}")
        else:
            print("Results:")
            print_csv(results) # Prints the results
    else:
        print("No results to save.")


if __name__ == "__main__":
    main()
