import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_cnn_article_urls(section_url, limit=10):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        res = requests.get(section_url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        article_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("https://www.cnnindonesia.com/") and "/2025" in href and href not in article_links:
                article_links.append(href)
            if len(article_links) >= limit:
                break

        return article_links
    except Exception as e:
        print(f"[Error scraping {section_url}] {e}")
        return []

def scrap_cnnindonesia_article(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Judul tidak ditemukan"

        date_meta = soup.find("meta", {"name": "publishdate"})
        date = date_meta["content"] if date_meta else "Tanggal tidak ditemukan"

        author_meta = soup.find("meta", {"name": "author"})
        author = author_meta["content"] if author_meta and author_meta["content"].strip() else "Penulis tidak ditemukan"

        content_div = soup.find("div", attrs={
            "class": "detail-text text-cnn_black text-sm grow min-w-0"
        })
        paragraphs = content_div.find_all("p") if content_div else []

        fulltext = " ".join(p.get_text(strip=True) for p in paragraphs)
        fulltext = re.sub(r"\s+", " ", fulltext)

        return {
            "Title": title,
            "Author": author,
            "Date": date,
            "Url": url,
            "FullText": fulltext
        }

    except Exception as e:
        print(f"[Error scraping {url}] {e}")
        return {
            "Title": "Error",
            "Author": "",
            "Date": "",
            "Url": url,
            "FullText": ""
        }

if __name__ == "__main__":
    # 🔗 Add more CNN sections here
    section_urls = [
        "https://www.cnnindonesia.com/nasional",
        "https://www.cnnindonesia.com/internasional"
    ]

    all_article_urls = set()
    for section in section_urls:
        urls = get_cnn_article_urls(section, limit=30)
        all_article_urls.update(urls)  # Use set to avoid duplicates

    print(f"🔗 Total unique URLs: {len(all_article_urls)}")

    # Scrape all articles
    all_cnn_data = [scrap_cnnindonesia_article(url) for url in all_article_urls]

    # Save to CSV
    df = pd.DataFrame(all_cnn_data, columns=["Title", "FullText", "Author", "Url", "Date"])
    df.to_csv("result/cnnindonesia_scraped.csv", index=False, encoding="utf-8")

    print(f"✅ Saved {len(df)} articles to result/cnnindonesia_scraped.csv")
