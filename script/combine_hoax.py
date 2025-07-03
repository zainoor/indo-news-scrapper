import os
import pandas as pd

# Folder containing hoax data
hoax_folder = 'result_hoax'
output_file = 'raw_hoax.csv'

# Collect all CSV files in the folder and subfolders
csv_files = []
for root, dirs, files in os.walk(hoax_folder):
    for file in files:
        if file.endswith('.csv'):
            full_path = os.path.join(root, file)
            csv_files.append(full_path)

# Combine all CSVs with 'source' and 'label = 1'
combined_df = pd.concat(
    [
        pd.read_csv(file).assign(source=os.path.basename(file), label=1)
        for file in csv_files
    ],
    ignore_index=True
)

# Save to CSV
combined_df.to_csv(os.path.join(hoax_folder, output_file), index=False)

print(f"✅ Combined {len(csv_files)} hoax CSV files and labeled them as 1 in '{output_file}'.")
