import urllib.request

# read links from file
with open('link.txt', 'r') as f:
    links = f.readlines()

# remove newline characters from links
links = [link.strip() for link in links]

# get user input for search query
query = input("Enter search query: ")

# loop through each link and search for query
for link in links:
    try:
        # open the link and read the contents
        response = urllib.request.urlopen(link)
        html = response.read()

        # check if query is present in the html content
        if query.lower() in html.decode().lower():
            print(f"{query} found in {link}")
    except Exception as e:
        print(f"Error accessing {link}: {e}")
