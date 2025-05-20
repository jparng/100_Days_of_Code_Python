#Basic Web Scraper

import requests
from bs4 import BeautifulSoup

    
url = "https://www.bbc.com/news"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    html_content = response.text
else:
    print("Failed to fetch the page")

soup = BeautifulSoup(html_content, "html.parser")

headlines = soup.find_all("h2")
for idx, headline in enumerate(headlines, 1):
    print(f"{idx}. {headline.text.strip()}")

links = soup.find_all("a", href=True)
for link in links:
    print(link["href"])

