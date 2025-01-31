import glob
import pandas as pd


# Path where scimagojr CSV files are located
path = "./scimagojr"  # Replace with your directory path

# Use glob to find all files starting with 'scimagojr' and ending with '.csv'
csv_files = glob.glob(f"{path}/scimagojr*.csv")
dataframes = []
for csv_file in csv_files:
    df = pd.read_csv(csv_file, sep=";")
    df = df[["Title", "Issn", "SJR Best Quartile", "Categories"]]
    df = df[df['SJR Best Quartile'] == 'Q1']
    df["Year"] = csv_file.split(" ")[1].split(".")[0]
    dataframes.append(df)

## Concatenate all files
concatenated_df = pd.concat(dataframes, ignore_index=True)

aggregated_df = concatenated_df.groupby('Issn').agg({'SJR Best Quartile': " ".join}).reset_index()
aggregated_df = aggregated_df[aggregated_df['SJR Best Quartile'] == 'Q1 Q1 Q1 Q1 Q1']

issn = set(aggregated_df["Issn"])
concatenated_df = concatenated_df[concatenated_df["Issn"].isin(issn)]

# Save the concatenated DataFrame to a new CSV file (optional)
concatenated_df.to_csv("scimagojr_concatenated.csv", index=False)

print("Files concatenated successfully!")