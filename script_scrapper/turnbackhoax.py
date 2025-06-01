import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def get_article_links_by_month(month, max_pages=10):
    base_url = "https://turnbackhoax.id"
    links = []

    for page in range(1, max_pages + 1):
        url = f"{base_url}/{month}/" if page == 1 else f"{base_url}/{month}/page/{page}/"
        print(f"Fetching: {url}")
        try:
            res = requests.get(url, timeout=10)
            if res.status_code != 200:
                break
            soup = BeautifulSoup(res.text, "html.parser")
            article_tags = soup.select("h3.entry-title a")
            if not article_tags:
                break  # no more articles/pages
            for a in article_tags:
                href = a.get("href")
                if href and href.startswith("https://turnbackhoax.id"):
                    links.append(href)
        except Exception as e:
            print(f"[Error fetching {url}]: {e}")
            break
        time.sleep(1)  # be polite

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
        print(f"[Error scraping {url}]: {e}")
        return {
            "Title": "Error",
            "FullText": "",
            "Author": "",
            "Url": url,
            "Date": ""
        }

# Auto-scrape across months and pages
months = ["2025/05", "2025/04", "2025/03"]
all_urls = []

for month in months:
    links = get_article_links_by_month(month, max_pages=5)
    all_urls.extend(links)

# Remove duplicates
all_urls = list(set(all_urls))
print(f"Total articles to scrape: {len(all_urls)}")

# Scrape all articles
all_data = [scrap_article(url) for url in all_urls]

# Save to CSV
df = pd.DataFrame(all_data, columns=["Title", "FullText", "Author", "Url", "Date"])
df.to_csv("result/turnbackhoax_scraped.csv", index=False, encoding="utf-8")
