import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
from datetime import datetime

def get_tempo_article_urls(base_url="https://www.tempo.co/indeks", pages=2):
    headers = {"User-Agent": "Mozilla/5.0"}
    urls = set()

    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")

            for a in soup.find_all("a", href=True):
                href = a["href"]

                # Convert relative URLs to full
                if href.startswith("/"):
                    href = "https://www.tempo.co" + href

                # ✅ Match proper article URLs using pattern: /category/title-slug-articleid
                if re.match(r"^https://www\.tempo\.co/[a-z]+/.+-\d+$", href):
                    urls.add(href)

        except Exception as e:
            print(f"[Error scraping page {page}] {e}")
    
    return list(urls)

def scrap_tempo_article(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Title
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "Judul tidak ditemukan"

        # Author
        author_meta = soup.find("meta", {"name": "author"})
        author = author_meta["content"] if author_meta else "Penulis tidak ditemukan"

        # Date
        date_meta = soup.find("meta", {"name": "publishdate"})
        date = date_meta["content"] if date_meta else "Tanggal tidak ditemukan"

        # ✅ Extract full text from JSON-LD script tag
        ld_json_tag = soup.find("script", type="application/ld+json")
        fulltext = ""
        if ld_json_tag:
            try:
                data = json.loads(ld_json_tag.string)
                fulltext = data.get("articleBody", "")
            except Exception as e:
                print(f"[Warning] Gagal parse JSON-LD: {e}")

        fulltext = re.sub(r"\s+", " ", fulltext).strip()

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
    
# 🔁 Run everything
if __name__ == "__main__":
    article_urls = get_tempo_article_urls(pages=3)
    print(f"🔗 Found {len(article_urls)} article URLs")

    articles = [scrap_tempo_article(url) for url in article_urls]
    df = pd.DataFrame(articles, columns=["Title", "FullText", "Author", "Url", "Date"])
    timestamp = datetime.now().strftime("%d%m%Y")
    filename = f"result/tempo_scraped_{timestamp}.csv"
    df.to_csv(filename, index=False, encoding="utf-8")

    print(f"✅ Saved {len(df)} articles to {filename}")
