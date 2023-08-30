import requests
from bs4 import BeautifulSoup
import re
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

# MongoDB Atlas connection URI with the password properly encoded
password = quote_plus("M15@2dwin0n7y")
uri = f"mongodb+srv://stevefox_linux:{password}@cluster0.cz85k.mongodb.net/?retryWrites=true&w=majority"
 
 
data = []
def get_urls_from_page(url):
    try:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for any bad response (4xx or 5xx)
            soup = BeautifulSoup(response.content, 'html.parser')
            urls = set()  # Using a set to avoid duplicates
               # Extract URLs from anchor tags (a) with 'href' attribute
            for link in soup.find_all('a', href=True):
                absolute_url = link['href']

                urls.add(absolute_url)

            return urls
        except Exception as e:
            try:
                with open(url, 'r', encoding='utf-8') as f:
                      soup = BeautifulSoup(f.read(), 'html.parser')
                      urls = set()  # Using a set to avoid duplicates
                         # Extract URLs from anchor tags (a) with 'href' attribute
                      for link in soup.find_all('a', href=True):
                          absolute_url = link['href']

                          urls.add(absolute_url)

                      return urls
            except Exception as e:
                 print("error")



    except requests.exceptions.RequestException as e:
        #logging.error(f"Error while crawling {url}: {e}")
        #return set()
        return ""
def get_urls(text):
    # Regular expression pattern to match URLs
    url_pattern = r'https?://(?!.*\bgoogle\b)\S+'

    # Find all occurrences of URLs in the text
    urls = re.findall(url_pattern, text)

    # Convert the list of URLs to a set
    #url_set = set(urls)


    return ','.join(urls)

def insert(url):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['crawler']

    # Access a collection (create it if it doesn't exist)
    collection = db['urls']



    existing_url = collection.find_one({"url": url})

    if existing_url:
        print("URL already exists in the collection.")
    else:
        # If the URL does not exist, insert it into the collection
        data = {"url": url}
        collection.insert_one(data)
        print(data)
def main():
    seed_url = "/python.html"  # Replace with the URL you want to start crawling from
    get_urls_from_page(seed_url)
    max_depth = 2  # Maximum depth to crawl from the seed URL

    visited_urls = set()
    url_queue = [(seed_url, 0)]

    while url_queue:
        current_url, depth = url_queue.pop(0)

        if depth <= max_depth and current_url not in visited_urls:
            #print(f"Crawling: {current_url}")
            #data.append(get_urls(current_url).strip())
            data = get_urls(current_url).strip()
            #print(data)
            if data:
              insert(data)
            urls = get_urls_from_page(current_url)
            visited_urls.add(current_url)
            try:
                for url in urls:
                    url_queue.append((url, depth + 1))
            except Exception as e:
                 print("error")


            # Log the crawled URLs to the JSON log file
            # urlss = get_urls(urls)
            # for dd in urlss:


            #logging.info(get_urls(urls))

if __name__ == "__main__":
    main()