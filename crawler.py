import requests
import time
from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout, ConnectionError


def crawl(url, max_pages, file_name):
    page = 1
    sublinks = []
    request_success = False
    while page <= max_pages:
        # Make a request to the URL
        try:
            response = requests.get(url)
            request_success = True
        except (ConnectTimeout, ConnectionError):
            request_success = False
        except Exception as e:
            request_success = False
            print("Error_Skipped: ", e)
        if request_success:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all the links on the page
            links = soup.find_all('a')
            # Open file in append mode or create if not exists.
            with open(file_name, 'a+', encoding="utf-8") as f:
                f.seek(0)  # move cursor to start of file
                contents = f.read()
                for link in links:
                    href = link.get('href')
                    # Check if the link is valid and not already in file
                    if (href is not None) and (href.startswith('http')) and (href not in contents):
                        # Write the link to file and print it to console
                        sublinks.append(href)
                        f.write(href + '\n')
                        print(href)
            # Move on to the next page by modifying the URL parameters (if applicable)
            page += 1
            # Pause briefly before crawling the next page to avoid overwhelming the server
            time.sleep(0.5)
        else:
            break
        for link in sublinks:
            print("Adding: ", link)
            crawl(link, 5, 'links.txt')
            sublinks.remove(link)


# Example usage
url = 'https://www.wikipedia.org/'
max_pages = 5
file_name = 'links.txt'
crawl(url, max_pages, file_name)
