import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

BASE_URL = "https://turnbackhoax.id"

def get_article_links(archive_url, max_articles=50):
    res = requests.get(archive_url)
    soup = BeautifulSoup(res.text, "html.parser")
    links = []

    # Each post title link
    for a in soup.select("h3.entry-title a")[:max_articles]:
        href = a.get("href")
        if href and href.startswith("https://turnbackhoax.id"):
            links.append(href)

    return links

def scrap_article(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.select_one("h1.entry-title")
        date = soup.select_one("span.entry-meta-date a")
        author = soup.select_one("span.entry-meta-author a")
        content_div = soup.select_one("div.entry-content")
        paragraphs = content_div.find_all("p") if content_div else []

        fulltext = " ".join(p.get_text(strip=True) for p in paragraphs)
        fulltext = re.sub(r"\s+", " ", fulltext)

        return {
            "Title": title.get_text(strip=True) if title else "Judul tidak ditemukan",
            "FullText": fulltext,
            "Author": author.get_text(strip=True) if author else "Penulis tidak ditemukan",
            "Url": url,
            "Date": date.get_text(strip=True) if date else "Tanggal tidak ditemukan"
        }

    except Exception as e:
        print(f"[Error] {url}: {e}")
        return {
            "Title": "Error",
            "FullText": "",
            "Author": "",
            "Url": url,
            "Date": ""
        }

# Example: Use May 2025 archive (or replace with any other)
months = ["2025/05", "2025/04", "2025/03"]
for month in months:
    archive_url = f"https://turnbackhoax.id/{month}/"


# Get article URLs automatically
urls = get_article_links(archive_url, max_articles=50)  # set how many you want

# Scrape each article
all_data = [scrap_article(url) for url in urls]

# Save to CSV
df = pd.DataFrame(all_data, columns=["Title", "FullText", "Author", "Url", "Date"])
df.to_csv("rawdata/turnbackhoax_new.csv", index=False, encoding="utf-8")
