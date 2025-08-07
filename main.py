import os
from dotenv import load_dotenv
from prod_input import get_structured_input
from generate_queries import generate_queries
from scraper import search_serper 
from generate_report import generate_report


load_dotenv()

if __name__ == "__main__":
    print("\nGenerating search queries...\n")
    result = generate_queries()
    queries_text = str(result)
    queries = [q.strip("-• \n") for q in queries_text.split("\n") if q.strip()]

    print("\nSearching the web using Serper API...\n")
    query_results = {}
    for query in queries:
        print(f"Searching: {query}")
        results = search_serper(query)
        query_results[query] = [
            {"content": item["snippet"], "url": item["link"]}
            for item in results
        ]

    with open("scraped_results.json", "w", encoding="utf-8") as f:
        import json
        json.dump(query_results, f, indent=2, ensure_ascii=False)

    print("\nGenerating final report sections...\n")
    report = generate_report()

    print("\nFinal Market Research Report:\n")
    for section, content in report.items():
        print(f"\n=== {section.upper()} ===\n")
        print(content)
        print("\n" + "="*60 + "\n")
