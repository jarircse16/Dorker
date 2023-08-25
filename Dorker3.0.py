import requests
from bs4 import BeautifulSoup

# Common SQL error messages to look for in the response
sql_error_messages = [
    "error in your SQL syntax",
    "mysql_fetch_assoc()",
    "You have an error in your SQL syntax",
    # Add more error messages as needed
]

def bing_search(query, num_results=10):
    try:
        search_url = f"https://www.bing.com/search?q={query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract search results from the HTML
        results = soup.find_all("li", class_="b_algo")

        for i, result in enumerate(results[:num_results], start=1):
            link = result.find("h2").a["href"]
            print(f"Checking URL {i}: {link}")

            if check_sql_injection_vulnerability(link):
                print(f"Potentially SQL Injection Vulnerable: {link}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def check_sql_injection_vulnerability(url):
    try:
        response = requests.get(url)
        response_text = response.text.lower()

        # Check if the response contains any SQL error messages
        for error_message in sql_error_messages:
            if error_message in response_text:
                return True

        return False

    except requests.exceptions.RequestException:
        return False

def main():
    query = "inurl:index.php?id="  # Your SQL injection dork query

    try:
        bing_search(query, num_results=10)
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
