import pandas as pd
import os
import re

# 💡 Define cleaning function
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

# 📁 Directories to process
directories = ["result", "result_archive", "result_old"]

# 🔍 Find all CSV files
csv_files = []
for dir_path in directories:
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))

print(f"🔍 Found {len(csv_files)} CSV files.")

dataframes = []
for path in csv_files:
    try:
        df = pd.read_csv(path)

        # Ensure required columns exist
        if not {"Title", "FullText"}.issubset(df.columns):
            print(f"⚠️ Skipped (missing columns): {path}")
            continue

        # Combine and clean
        df["cleaned"] = (df["Title"].fillna("") + " " + df["FullText"].fillna("")).apply(clean_text)

        # Drop empty cleaned rows
        df = df[df["cleaned"].str.strip() != ""]

        # Determine label based on filename
        label = 1 if "turnbackhoax" in path.lower() else 0
        df["label"] = label

        # Keep only necessary columns
        df = df[["cleaned", "label"]]
        dataframes.append(df)

        print(f"✅ Processed {path} ({len(df)} rows)")

    except Exception as e:
        print(f"❌ Failed to process {path}: {e}")

# Combine and deduplicate
if dataframes:
    merged_df = pd.concat(dataframes, ignore_index=True)
    before = len(merged_df)
    merged_df.drop_duplicates(subset=["cleaned"], inplace=True)
    after = len(merged_df)

    print(f"🧹 Removed {before - after} duplicate entries.")

    # Shuffle
    merged_df = merged_df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Save
    os.makedirs("cleandata", exist_ok=True)
    merged_df.to_csv("cleandata/hoax_dataset_2025.csv", index=False)

    print(f"🎉 Done! Final cleaned dataset saved to cleandata/hoax_dataset_2025.csv ({after} entries)")
else:
    print("⚠️ No valid data found to merge.")
