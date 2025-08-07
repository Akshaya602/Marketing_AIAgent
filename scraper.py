import os
import requests

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_serper(query):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "q": query
    }

    response = requests.post(url, headers=headers, json=data)
    results = response.json()

    output = []
    for item in results.get("organic", []):
        output.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })

    return output
