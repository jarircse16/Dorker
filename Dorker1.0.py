from googlesearch import search

def search_sqli_dorks(query, num_results=10):
    try:
        print("Searching for SQLi dorks...")
        results = search(query, num_results=num_results)

        for i, url in enumerate(results, start=1):
            print(f"{i}. {url}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Example SQLi dork queries
    dork_queries = [
        "inurl:index.php?id=",
        "inurl:news.php?id=",
        "inurl:article.php?id=",
    ]

    num_results = 10  # Number of search results to retrieve per query

    for dork_query in dork_queries:
        search_sqli_dorks(dork_query, num_results)
