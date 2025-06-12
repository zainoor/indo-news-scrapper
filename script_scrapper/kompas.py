import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

# Get Kompas article URLs from paginated section pages
def get_kompas_article_urls(base_url, pages=3, limit_per_page=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    collected_links = set()

    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")

            for a in soup.find_all("a", href=True):
                href = a["href"]
                if (
                    "kompas.com/read/" in href
                    and "/2025/" in href
                    and href.startswith("https://")
                ):
                    collected_links.add(href)
                    if len(collected_links) >= limit_per_page * pages:
                        break
        except Exception as e:
            print(f"[Error scraping {url}] {e}")
            continue

    return list(collected_links)

# Scrape full article content
def scrap_kompas_article(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        title_tag = soup.find("h1", class_="read__title")
        author_tag = soup.find("div", class_="read__author")
        date_tag = soup.find("div", class_="read__time")
        content_div = soup.find("div", class_="read__content")
        paragraphs = content_div.find_all("p") if content_div else []

        title = title_tag.get_text(strip=True) if title_tag else "Judul tidak ditemukan"
        author = author_tag.get_text(strip=True).replace("\n", " ") if author_tag else "Penulis tidak ditemukan"
        date = date_tag.get_text(strip=True).replace("\n", " ") if date_tag else "Tanggal tidak ditemukan"
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

# Run everything
if __name__ == "__main__":
    # Sections to scrape
    section_bases = [
        "https://nasional.kompas.com",
        "https://regional.kompas.com",
        "https://www.kompas.com/global"
    ]

    all_urls = set()
    for base_url in section_bases:
        urls = get_kompas_article_urls(base_url, pages=2, limit_per_page=10)
        all_urls.update(urls)

    print(f"🔗 Found {len(all_urls)} unique Kompas article URLs")

    all_data = [scrap_kompas_article(url) for url in all_urls]

    df = pd.DataFrame(all_data, columns=["Title", "FullText", "Author", "Url", "Date"])
    
    timestamp = datetime.now().strftime("%d%m%Y")
    filename = f"result/kompas_scraped_{timestamp}.csv"
    df.to_csv(filename, index=False, encoding="utf-8")

    print(f"✅ Saved {len(df)} articles to {filename}")