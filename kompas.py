import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrap_kompas_article(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
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
        print(f"[Error] {url}: {e}")
        return {
            "Title": "Error",
            "Author": "",
            "Date": "",
            "Url": url,
            "FullText": ""
        }


# 🔗 List of Kompas article URLs
kompas_urls = [
    "https://nasional.kompas.com/read/2025/05/28/13300711/pengacara-ronald-tannur-dituntut-14-tahun-kurungan",
    "https://nasional.kompas.com/read/2025/05/29/22033651/kedatangan-perdana-44-jemaah-haji-khusus-tiba-di-bandara-taif",
    "https://nasional.kompas.com/read/2025/05/29/21235881/momen-presiden-macron-makan-siang-bareng-taruna-di-akmil-dimulai-prabowo",
    "https://nasional.kompas.com/read/2025/05/29/21043761/candi-borobudur-jadi-saksi-kerja-sama-indonesia-dan-perancis-apa-saja",
    "https://nasional.kompas.com/read/2025/05/29/20364451/cuaca-panas-ekstrem-saat-puncak-haji-menag-ingatkan-jemaah-perbanyak-minum"
]

# 🔁 Scrape all
all_kompas_data = [scrap_kompas_article(url) for url in kompas_urls]

# 💾 Save to CSV
df = pd.DataFrame(all_kompas_data, columns=["Title", "FullText", "Author", "Url", "Date"])
df.to_csv("rawdata/kompas_scraped.csv", index=False, encoding="utf-8")
