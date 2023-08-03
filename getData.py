import requests
from bs4 import BeautifulSoup
import re
from SPARQLWrapper import SPARQLWrapper, JSON
import csv
import time
import logging
import pandas as pd
from tqdm import tqdm
import os

def clean_text(text):
    """Clean text of citation links"""
    return re.sub(r'\[\d+\]', '', text)

def get_paragraphs(soup):
    """Find and return paragraph 'p' tags from the soup object"""
    paragraphs = soup.find_all('p')
    return ' '.join([clean_text(p.get_text()) for p in paragraphs])

def get_tables(soup):
    """Find all tables on the page, extract content, and return it as a string"""
    tables = soup.find_all('table')
    table_text = ''
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if columns:
                table_text += ' '.join([clean_text(col.get_text()) for col in columns])
    return table_text

def get_infobox_content(infobox_content):
    """Return the content of the infobox as a string"""
    return ' '.join([f"{clean_text(k)}: {clean_text(v)}" for k, v in infobox_content.items()])

def extract_infobox_content(infobox):
    """Extract rows from infobox and return a dictionary with their content"""
    rows = infobox.find_all('tr')
    infobox_content = {}
    for row in rows:
        header = row.find('th')
        data = row.find('td')
        if header and data:
            infobox_content[header.text.strip()] = data.text.strip()
    return infobox_content

def clean_html_tags(text):
    """Clean text of HTML tags"""
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

def get_dbpedia_info(title):
    """Get and return information from DBpedia as a string"""
    # remove any HTML tags from the title
    title = clean_html_tags(title)
    query = """
    SELECT ?predicate ?object WHERE {{
      <http://dbpedia.org/resource/{}> ?predicate ?object
    }}
    """.format(title.replace(" ", "_"))

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    dbpedia_results = []
    for result in results["results"]["bindings"]:
        predicate = result["predicate"]["value"]
        obj = result["object"]["value"]
        dbpedia_results.append(f"{predicate}: {obj}")
    return ' '.join(dbpedia_results)


def clean_text(text):
    """Clean text of citation links and other undesirable characters or sequences"""
    # remove citation links
    text = re.sub(r'\[\d+\]', '', text)
    # remove newline characters
    text = text.replace('\n', ' ')
    # remove double quotes
    text = text.replace('"', '')
    # replace comma with semicolon to prevent issues with csv
    text = text.replace(',', ';')
    return text.strip()

def main():
    """Main function to run the script"""
    num_requests = 10000  # Number of requests to be made. Modify this as per your requirement.
    wait_time = 0.5  # Wait time in seconds between requests.
    wait_period = 20

    csv_filename = 'outputData/wikidata.csv'

    # Check if CSV file exists, if so initialize DataFrame with the same structure,
    # else initialize a new one
    if os.path.isfile(csv_filename):
        existing_df = pd.read_csv(csv_filename, nrows=0)
        data = pd.DataFrame(columns=existing_df.columns)
    else:
        data = pd.DataFrame(columns=["Title", "PageContents", "dbpediaTriples"])

    for i in tqdm(range(num_requests)):

        url = "https://en.wikipedia.org/api/rest_v1/page/random/html"
        try:
            response_html = requests.get(url)
            response_html.raise_for_status()  # raise exception for status codes like 4xx and 5xx
            soup = BeautifulSoup(response_html.content, 'html.parser')
            page_title = clean_text(soup.title.string.replace(" - Wikipedia", "").strip())
            page_title = clean_html_tags(page_title) 

            page_contents = clean_text(get_paragraphs(soup))
            page_contents += ' ' + clean_text(get_tables(soup))
            infobox = soup.find('table', {'class': 'infobox'})
            if infobox is not None:
                infobox_content = extract_infobox_content(infobox)
                page_contents += ' ' + clean_text(get_infobox_content(infobox_content))

            dbpedia_triples = get_dbpedia_info(page_title)
            #dbpedia_triples = clean_text(get_dbpedia_info(page_title))

            # Append the row to the DataFrame
            data = data.append({"Title": page_title, 
                                "PageContents": page_contents, 
                                "dbpediaTriples": dbpedia_triples}, ignore_index=True)

            # If csv file does not exist, write with header, else append without writing header
            if i == 0 and not os.path.isfile(csv_filename):
                data.to_csv(csv_filename, mode='a', index=False)
            else:
                data.to_csv(csv_filename, mode='a', index=False, header=False)

            # Clear data to prevent high memory usage
            data = data.iloc[0:0]

        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")

        if i % wait_period == 0: 
            time.sleep(wait_time)  # Wait for a defined number of seconds between each request.


if __name__ == "__main__":
    main()

