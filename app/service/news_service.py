from config.config import config
import requests

def fetch_global_news(country="us", category=None):
    url = f"https://newsapi.org/v2/top-headlines?apiKey={config.NEWS_API_KEY}"
    if country:
        url += f"&country={country}"
    if category:
        url += f"&category={category}"
    res=requests.get(url)
    data = res.json()
    print(f"NewsAPI URL: {url} | Status: {res.status_code}")
    if res.status_code != 200:
        print(f"NewsAPI Error: {data}")
    return data
