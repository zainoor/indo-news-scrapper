import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrap_article(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # Title
    title_tag = soup.select_one("h1.entry-title")
    title = title_tag.get_text(strip=True) if title_tag else "Judul tidak ditemukan"

    # Date
    date_tag = soup.select_one("span.entry-meta-date a")
    date = date_tag.get_text(strip=True) if date_tag else "Tanggal tidak ditemukan"

    # Author
    author_tag = soup.select_one("span.entry-meta-author a")
    author = author_tag.get_text(strip=True) if author_tag else "Penulis tidak ditemukan"

    # Full Text
    content_div = soup.select_one("div.entry-content")
    paragraphs = content_div.find_all("p") if content_div else []
    fulltext = " ".join(p.get_text(strip=True) for p in paragraphs).replace("\n", " ")


    return {
        "Title": title,
        "FullText": fulltext,
        "Author": author,
        "Url": url,
        "Date": date
    }

# List of URLs to scrape
urls = [
    "https://turnbackhoax.id/2025/05/28/penipuan-ada-bantuan-tunai-dari-kerajaan-brunei/",
    "https://turnbackhoax.id/2025/05/28/salah-pesan-berantai-buah-daun-kelor-dan-soda-untuk-obat-sakit-sendi/",
    "https://turnbackhoax.id/2025/05/29/penipuan-tautan-lowongan-kerja-pt-hwa-seung-indonesia-hwi/",
    "https://turnbackhoax.id/2025/05/28/penipuan-ada-aplikasi-bluetooth-pendeteksi-penerima-vaksin-covid-19/",
    "https://turnbackhoax.id/2025/05/28/salah-gubernur-jabar-dedi-mulyadi-resmikan-layanan-pinjol/",
    "https://turnbackhoax.id/2025/05/27/salah-manuver-pesawat-india-sebelum-jatuh-tertembak-oleh-pakistan/",
    "https://turnbackhoax.id/2025/05/27/penipuan-ustaz-abdul-somad-bagi-bagi-uang-untuk-tki/",
    "https://turnbackhoax.id/2025/05/27/penipuan-garuda-indonesia-bagi-bagi-uang/",
    "https://turnbackhoax.id/2025/05/27/salah-ada-bansos-untuk-peserta-uji-coba-vaksin-tbc-bill-gates/",
    "https://turnbackhoax.id/2025/05/27/salah-dokumentasi-penggerebekan-lokasi-penyekapan-wni-di-thailand/",
    "https://turnbackhoax.id/2025/05/26/salah-ikan-lele-penyebab-gagal-ginjal/",
    "https://turnbackhoax.id/2025/05/24/penipuan-tautan-rekrutmen-jne-express/",
    "https://turnbackhoax.id/2025/05/23/salah-tni-membunuh-1-200-tentara-israel/",
    "https://turnbackhoax.id/2025/05/23/penipuan-gibran-bagi-bagi-uang-untuk-bayar-utang-hingga-modal-usaha/",
    "https://turnbackhoax.id/2025/05/23/salah-vaksin-mrna-tbc-dan-malaria-disebarkan-lewat-udara/",
    "https://turnbackhoax.id/2025/05/23/salah-juru-bicara-opm-menyatakan-menyerah/",
    "https://turnbackhoax.id/2025/05/23/penipuan-ada-bantuan-tunai-untuk-tki-dari-bpjs-kesehatan/",
    "https://turnbackhoax.id/2025/05/22/salah-pawai-people-power/",
    "https://turnbackhoax.id/2025/05/21/salah-dedi-mulyadi-hanya-kaum-radikal-yang-meragukan-ijazah-pak-jokowi/",
    "https://turnbackhoax.id/2025/05/21/salah-dokumentasi-tkw-ditemukan-hidup-dalam-peti-es-di-vietnam/",
    "https://turnbackhoax.id/2025/05/21/salah-makanan-mbg-di-indonesia-terkontaminasi-bangkai-ular/",
    "https://turnbackhoax.id/2025/05/21/salah-as-larang-warga-ke-ri-karena-ada-uji-coba-vaksin-tbc-bill-gates/",
    "https://turnbackhoax.id/2025/05/21/salah-petugas-bea-cukai-vietnam-menemukan-tkw-indonesia-di-dalam-peti-es-besar-dari-kamboja/",
    "https://turnbackhoax.id/2025/05/20/penipuan-raffi-ahmad-bagi-bagi-uang-untuk-warga-timor-leste/",
    "https://turnbackhoax.id/2025/05/20/penipuan-youtuber-aisar-khaled-bagi-bagi-uang/",
    "https://turnbackhoax.id/2025/05/19/salah-penerapan-sistem-jalan-berbayar-erp-di-25-ruas-jalan-jakarta/",
    "https://turnbackhoax.id/2025/05/19/salah-video-tni-gandakan-serangan-ke-pusat-kota-israel/",
    "https://turnbackhoax.id/2025/05/19/salah-37-ribu-warga-israel-mengungsi-karena-kebakaran/",
    "https://turnbackhoax.id/2025/05/18/salah-video-pembangunan-patung-paus-fransiskus-berukuran-raksasa/",
    "https://turnbackhoax.id/2025/05/18/salah-video-pasukan-garuda-indonesia-tiba-di-palestina/",
    "https://turnbackhoax.id/2025/05/18/penipuan-tautan-lowongan-kerja-cleo-pure-water/",
    "https://turnbackhoax.id/2025/05/17/penipuan-tautan-lowongan-kerja-tenaga-staf-universitas-pertamina/",
    "https://turnbackhoax.id/2025/05/17/penipuan-tautan-pendaftaran-program-rumah-gratis-dari-pemerintah/",
    "https://turnbackhoax.id/2025/05/16/penipuan-tautan-pendaftaran-peserta-jkn-gratis-seumur-hidup/",
    "https://turnbackhoax.id/2025/05/16/salah-ibadah-sambil-joget/",
    "https://turnbackhoax.id/2025/05/16/salah-video-truk-nekat-terobos-dan-tabrak-tarub-resepsi/",
    "https://turnbackhoax.id/2025/05/16/salah-video-prabowo-dan-megawati-di-sidang-paripurna-pemakzulan-gibran/",
    "https://turnbackhoax.id/2025/05/16/salah-israel-pakai-bom-buatan-turkiye-untuk-menyerang-gaza/",
    "https://turnbackhoax.id/2025/05/16/penipuan-tautan-lowongan-kerja-pt-pupuk-indonesia/"
]

# Scrape each article and save to CSV
all_data = [scrap_article(url) for url in urls]
df = pd.DataFrame(all_data, columns=["Title", "FullText", "Author", "Url", "Date"])
df.to_csv("rawdata/turnbackhoax_scraped.csv", index=False, encoding="utf-8")
