import glob
import argparse
from pathlib import Path

import pandas as pd

'''
Script to preprocess ScimagoJR CSV files. 
It reads all CSV files in the specified directory, 
filters for Q1 journals, and concatenates the results into a single CSV file.
'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Preprocess ScimagoJR CSV files.')
    parser.add_argument('--path', type=str, default="./scimagojr", help='Path where scimagojr CSV files are located.')
    parser.add_argument('--output_dir', type=str, default="./dataset", help='Output CSV file name for the concatenated results.')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Path where scimagojr CSV files are located
    path = args.path  

    # Use glob to find all files starting with 'scimagojr' and ending with '.csv'
    csv_files = glob.glob(f"{path}/scimagojr*.csv")
    dataframes = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, sep=";")
        df = df[["Title", "Issn", "SJR Best Quartile", "Categories", "Publisher"]]
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
    concatenated_df.to_csv(output_dir / "scimagojr_concatenated.csv", index=False)

    print("Files concatenated successfully!")