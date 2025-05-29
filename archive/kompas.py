import requests
from bs4 import BeautifulSoup
import re

def scrap_kompas_article(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # Title
    title_tag = soup.find("h1", class_="read__title")
    title = title_tag.get_text(strip=True) if title_tag else "Judul tidak ditemukan"

    # Author
    author_tag = soup.find("div", class_="read__author")
    author = author_tag.get_text(strip=True).replace("\n", " ") if author_tag else "Penulis tidak ditemukan"

    # Date
    date_tag = soup.find("div", class_="read__time")
    date = date_tag.get_text(strip=True).replace("\n", " ") if date_tag else "Tanggal tidak ditemukan"

    # Article content
    content_div = soup.find("div", class_="read__content")
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

# Example usage
url = "https://nasional.kompas.com/read/2025/05/28/13300711/pengacara-ronald-tannur-dituntut-14-tahun-kurungan"
data = scrap_kompas_article(url)

# Print or save
import pandas as pd
df = pd.DataFrame([data])
df.to_csv("rawdata/kompas_article.csv", index=False, encoding="utf-8")
