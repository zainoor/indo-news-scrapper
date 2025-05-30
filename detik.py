import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Step 1: Automatically get article URLs from a section page
def get_detik_article_urls(section_url, limit=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(section_url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if re.match(r"^https://news\.detik\.com/.+/d-\d+", href) and href not in links:
                links.append(href)
            if len(links) >= limit:
                break
        return links
    except Exception as e:
        print(f"[Error scraping section] {e}")
        return []

# Step 2: Scrape article content
def scrap_detik_article(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "Judul tidak ditemukan"

        author_meta = soup.find("meta", {"name": "author"})
        author = author_meta["content"] if author_meta else "Penulis tidak ditemukan"

        date_meta = soup.find("meta", {"name": "publishdate"})
        date = date_meta["content"] if date_meta else "Tanggal tidak ditemukan"

        content_div = soup.find("div", class_="detail__body itp_bodycontent_wrapper")
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

# Step 3: Run the process
if __name__ == "__main__":
    section_urls = [
        "https://news.detik.com/berita",
        "https://news.detik.com/internasional"
    ]

    all_article_urls = set()
    for section in section_urls:
        urls = get_detik_article_urls(section, limit=30)
        all_article_urls.update(urls)  # Use set to avoid duplicates

    print(f"🔗 Total unique URLs: {len(all_article_urls)}")


    all_detik_data = [scrap_detik_article(url) for url in all_article_urls]

    df = pd.DataFrame(all_detik_data, columns=["Title", "FullText", "Author", "Url", "Date"])
    df.to_csv("result/detik_scraped.csv", index=False, encoding="utf-8")
    print(f"✅ Saved {len(df)} articles to result/detik_scraped.csv")

    # section_url = "https://news.detik.com/berita"
    # article_urls = get_detik_article_urls(section_url, limit=20)

    # print(f"🔗 Found {len(article_urls)} Detik article URLs")