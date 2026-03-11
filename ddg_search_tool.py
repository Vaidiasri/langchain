import os
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun

def main():
    # Load environment variables if needed
    load_dotenv()

    # Initialize the DuckDuckGo Search tool
    search = DuckDuckGoSearchRun()

    # Define a query
    query = "Google"

    print(f"Searching for: {query}...")
    
    try:
        # Run the search
        results = search.run(query)
        
        print("\nSearch Results:")
        print("-" * 20)
        print(results)
        print("-" * 20)
    except Exception as e:
        print(f"\nError during search: {e}")
        print("\nTip: Ensure 'duckduckgo-search' is installed (pip install duckduckgo-search).")

if __name__ == "__main__":
    main()
