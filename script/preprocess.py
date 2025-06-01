import pandas as pd
import os
import re

# Your source files
files = {
    "kompas": "result/kompas_scraped.csv",
    "cnn": "result/cnnindonesia_scraped.csv",
    "detik": "result/detik_scraped.csv",
    "tempo": "result/tempo_scraped.csv",
    "turnbackhoax": "result/turnbackhoax_scraped.csv"
}

# Cleaning function
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = text.lower()
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Process each file
dataframes = []
for source, path in files.items():
    print(f"Processing: {path}")
    df = pd.read_csv(path)

    # Combine Title + FullText
    df["cleaned"] = (df["Title"].fillna("") + " " + df["FullText"].fillna("")).apply(clean_text)

    # Drop rows where 'cleaned' is empty after cleaning
    df = df[df["cleaned"].str.strip() != ""]

    # Label
    df["label"] = 1 if source == "turnbackhoax" else 0

    # Select columns
    df = df[["cleaned", "label"]]
    dataframes.append(df)

# Combine all
merged_df = pd.concat(dataframes).reset_index(drop=True)

# Drop duplicates based on the 'cleaned' column
before = len(merged_df)
merged_df.drop_duplicates(subset=["cleaned"], inplace=True)
after = len(merged_df)
print(f"Removed {before - after} duplicate entries.")

# Shuffle
merged_df = merged_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
os.makedirs("cleandata", exist_ok=True)
merged_df.to_csv("cleandata/hoax_dataset_2025.csv", index=False)

print(f"✅ Done! Final cleaned dataset saved to cleandata/hoax_dataset_2025.csv ({after} entries).")
