import os
import pandas as pd

# Base folder
base_folder = 'result'
output_file = 'raw_valid.csv'

# Function to collect all CSV files in a folder (including subfolders)
csv_files = []
for root, dirs, files in os.walk(base_folder):
    for file in files:
        if file.endswith('.csv'):
            full_path = os.path.join(root, file)
            csv_files.append(full_path)

# Combine all CSV files with 'source' and 'label = 0'
combined_df = pd.concat(
    [
        pd.read_csv(file).assign(source=os.path.basename(file), label=0)
        for file in csv_files
    ],
    ignore_index=True
)

# Save to base folder
combined_df.to_csv(os.path.join(base_folder, output_file), index=False)

print(f"✅ Combined {len(csv_files)} CSV files and labeled them as 0 in '{output_file}'.")
