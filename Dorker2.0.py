import time
import requests
from bs4 import BeautifulSoup

# Add a delay between requests to avoid rate limiting (in seconds)
REQUEST_DELAY = 5

def is_sql_injection_vulnerable(url):
    # Append a single quote to the URL
    test_url = url + "'"

    try:
        # Send a GET request to the modified URL
        response = requests.get(test_url)

        # Check if the response content contains SQL error messages
        if "SQL error" in response.text:
            return True
        else:
            # Compare the response content with the original URL
            if response.text != requests.get(url).text:
                return True

    except requests.exceptions.RequestException:
        pass

    return False

def search_sqli_dorks(query, num_results=30):
    try:
        print("Searching for SQLi dorks on Bing...")
        
        # Create Bing search URL
        search_url = f"https://www.bing.com/search?q={query}"

        results = []

        # Keep fetching results until the desired number of results is reached
        while len(results) < num_results:
            # Send a GET request to Bing
            response = requests.get(search_url)

            # Parse the HTML response
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find search result links
            links = soup.find_all('a')

            for link in links:
                url = link.get('href')
                if url and url.startswith('http'):
                    results.append(url)

            # Check if we have enough results
            if len(results) >= num_results:
                break

            # Delay between requests to avoid rate limiting
            time.sleep(REQUEST_DELAY)

        num_vulnerable_found = 0  # Track the number of vulnerable URLs found

        for i, url in enumerate(results, start=1):
            if is_sql_injection_vulnerable(url):
                print(f"{i}. {url} (SQL Injection Vulnerable)")
                num_vulnerable_found += 1

                # Exit the loop if the desired number of vulnerable URLs is found
                if num_vulnerable_found >= num_results:
                    break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Example SQLi dork queries
    dork_queries = [
        "inurl:index.php?id=",
        "inurl:news.php?id=",
        "inurl:article.php?id=",
    ]

    num_results = 30  # Number of search results to retrieve per query

    for dork_query in dork_queries:
        search_sqli_dorks(dork_query, num_results)
