import requests
import csv
import xml.etree.ElementTree as ET

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils" # Base url for the NCBI E-Utilities API


def identify_non_academic_author(author):
    academic_keywords = ["University", "Institute", "Department", "Lab", "College", "Academy"] # Keywords that indicate an academic affiliation
    non_academic_keywords = ["Pharma", "Biotech", "Inc", "Corporation", "Company", "Labs"]
    
    affiliation = author.find(".//Affiliation") # Extracting the affiliation of the author
    email = author.find(".//Email") # Extracting the email of the author
    
    # Check for affiliation
    is_academic = False
    is_non_academic = False
    if affiliation is not None: # If affiliation is not none then it checks whether the author is academic or non-academic based on the keywords
        affiliation_text = affiliation.text.lower()
        is_academic = any(keyword.lower() in affiliation_text for keyword in academic_keywords)
        is_non_academic = any(keyword.lower() in affiliation_text for keyword in non_academic_keywords)
    
    # Check for email
    is_academic_email = False
    is_non_academic_email = False
    if email is not None: # If email is not none then it checks whether the author is academic or non-academic based on the keywords
        email_text = email.text.lower()
        is_academic_email = ".edu" in email_text or "university" in email_text
        is_non_academic_email = ".com" in email_text or ".org" in email_text
    
    # Combine heuristics to classify
    if is_non_academic or is_non_academic_email:
        return True  # Non-academic author
    return False  # Academic author


def fetch_details(pmid): # Fetches the details of the research paper
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': pmid,
        'retmode': 'xml'
    }
    response = requests.get(efetch_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching data for PubMed ID {pmid}")
        return None


def parse_details(xml_data):
    root = ET.fromstring(xml_data)
    article = root.find(".//PubmedArticle")
    
    # Extracting the PubMed ID and title
    pubmed_id = article.find(".//PMID").text # Extracting the PubMed ID
    title = article.find(".//ArticleTitle").text # Extracting the title of the article
    authors = []

    author_elements = article.findall(".//Author") # Extracting the authors of the article
    for author in author_elements:
        last_name = author.find(".//LastName") # Extracting the last name of the author
        first_name = author.find(".//ForeName") # Extracting the first name of the author
        if last_name is not None and first_name is not None:
            authors.append(f"{first_name.text} {last_name.text}") # Joining the first name and last name of the author
    
    publication_date = article.find(".//PubDate/Year").text if article.find(".//PubDate/Year") is not None else 'N/A' # Extracting the publication date of the article
    
    non_academic_authors = []
    company_affiliations = []
    corresponding_email = 'N/A'
    
    
    for author in author_elements:
        if identify_non_academic_author(author):
            last_name = author.find(".//LastName")
            first_name = author.find(".//ForeName")
            if last_name is not None and first_name is not None:
                non_academic_authors.append(f"{first_name.text} {last_name.text}") # Appending the non-academic authors
        affiliation = author.find(".//Affiliation")
        if affiliation is not None:
            affiliation_text = affiliation.text.lower()
            # Look for company-related keywords in affiliation
            company_keywords = ["pharma", "biotech", "inc", "corporation", "company", "labs"]
            if any(keyword in affiliation_text for keyword in company_keywords):
                company_affiliations.append(affiliation.text) # Appending the company affiliations
            
            
        # Check for corresponding author email
        emails = []
        # Checking whether the author contains email or not
        email = author.find(".//Email")
        if email is not None:
            emails.append(email.text)
    
    # Return the parsed details
    return {
        'Pubmed ID': pubmed_id,
        'Title': title,
        'Authors': ', '.join(authors) if authors else 'N/A',
        'Publication Date': publication_date,
        'Non-academic Author(s)': ', '.join(non_academic_authors) if non_academic_authors else 'N/A',
        'Company Affiliation(s)': ', '.join(company_affiliations) if company_affiliations else 'N/A',
        'Corresponding Author Email': ', '.join(emails) if emails else 'N/A'
    }


def save_to_csv(results, filename="pubmed_results.csv"): # Saves the results to a csv file
    fieldnames = ['Pubmed ID', 'Title', 'Authors', 'Publication Date', 'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames) # Writing the results to a csv file
        writer.writeheader()
        for result in results:
            writer.writerow(result)


def search_pubmed_and_fetch_results(query, max_results=10):
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed', # pubmed is database name
        'term': query, # Query
        'retmode': 'xml', # Return mode
        'retmax': str(max_results) # Maximum number of results to return
    }

    response = requests.get(esearch_url, params=params) # Fetch the search results from PubMed
    if response.status_code == 200: # If the response is successful and 200 indicates success
        root = ET.fromstring(response.text) # Parse the XML response
        pmids = [pmid.text for pmid in root.findall(".//Id")] #Extract ids from the XML response
        return pmids
    else:
        print("Error in fetching search results from PubMed database")
        return []