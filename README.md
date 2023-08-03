# Web Scraping Wikipedia and DBPedia with Python

This script automates the process of scraping random Wikipedia articles, parsing the information and storing it into a CSV file. It fetches the title and content of each Wikipedia page and attempts to fetch corresponding structured information from DBPedia. 

## Dependencies

This script depends on several Python packages:

* `requests` for making HTTP requests.
* `beautifulsoup4` for parsing HTML.
* `SPARQLWrapper` for querying DBPedia.
* `pandas` for managing and saving data.
* `tqdm` for showing a progress bar.
* `lxml` as a parser for BeautifulSoup.

All requirements can be installed using pip:

```
pip install -r requirements.txt
```

## Usage

The script can be run with Python 3.7 and later versions:

```
python wikipedia_dbpedia_scraper.py
```

## Output

The script writes the scraped data to `outputData/wikidata.csv`. Each row in the CSV file corresponds to a single Wikipedia page, with columns for the page title, page contents, and corresponding DBPedia information.

## Customization

There are a few variables in the script that you can customize:

* `num_requests`: The number of Wikipedia pages to fetch. The default is 10,000.
* `wait_time`: The time to wait (in seconds) between HTTP requests to avoid overloading the server. The default is 0.5 seconds.
* `wait_period`: The number of iterations after which the script will wait. The default is 20.

Please ensure that your usage of this script complies with the Wikipedia and DBPedia terms of service, particularly with respect to the rate of requests. You should avoid making too many requests in a short period of time, as this could be disruptive to the services.

## Disclaimer

The script is provided as is, without any guarantees. The author is not responsible for any consequences of its use.
