from html import parser
from pathlib import Path
import argparse

import pandas as pd


'''
Script to filter results from IEEE Xplore, Scopus, and Web of Science based on ISSN.
The ISSNs are obtained from the ScimagoJR CSV file, which contains information about Q1 journals.
The script reads the results from the three sources, filters them based on the ISSNs,
and saves the filtered results to new CSV files.
'''
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Filter results from ScimagoJR, IEEE Xplore, Scopus, and Web of Science based on ISSN.')
    parser.add_argument('--scimago_file', type=str, default="./dataset/scimagojr_concatenated.csv", help='Path to the ScimagoJR CSV file.')
    parser.add_argument('--ieeexplore_file', type=str, default="./results_ieee/ieeexplore_export.csv", help='Path to the IEEE Xplore CSV file.')
    parser.add_argument('--scopus_file', type=str, default="./results_scopus/scopus_export.csv", help='Path to the Scopus CSV file.')
    parser.add_argument('--wos_file', type=str, default="./results_wos/wos_export.csv", help='Path to the Web of Science CSV file.')
    parser.add_argument('--output_dir', type=str, default="./filtered_results", help='Directory to save the filtered CSV files.')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ieee_folder = Path(args.ieeexplore_file).parent
    scopus_folder = Path(args.scopus_file).parent
    wos_folder = Path(args.wos_file).parent

    scimago_results = pd.read_csv(args.scimago_file)
    ieeexplore_results = pd.read_csv(args.ieeexplore_file)
    scopus_results = pd.read_csv(args.scopus_file)
    wos_results = pd.read_csv(args.wos_file)
    issns = set()

    for issn in scimago_results["Issn"]:
        issns.update(issn.split(", "))

    ieeexplore_results["ISSN"] = ieeexplore_results["ISSN"].str.replace("-", "")
    ieeexplore_results = ieeexplore_results[ieeexplore_results["ISSN"].isin(issns)]

    ieeexplore_results.to_csv(ieee_folder / "ieeexplore_quartile_filter.csv", index=False)

    scopus_results = scopus_results[scopus_results["ISSN"].isin(issns)]

    scopus_results.to_csv(scopus_folder /"scopus_quartile_filter.csv", index=False)

    wos_results["ISSN"] = wos_results["ISSN"].str.replace("-", "")
    wos_results = wos_results[wos_results["ISSN"].isin(issns)]
    wos_results.to_csv(wos_folder / "wos_quartile_filter.csv", index=False)

    ieeexplore_results = ieeexplore_results[["Document Title", "Publication Year", "ISSN", "DOI", "PDF Link"]]

    wos_results = wos_results[["Article Title", "Publication Year", "ISSN", "DOI"]]

    wos_results["PDF Link"] = ""

    scopus_results = scopus_results[["Title", "Year", "ISSN", "DOI", "Link"]]

    ieeexplore_results = ieeexplore_results.rename(columns={'Document Title': 'Title', "Publication Year" : "Year", "PDF Link": "Link"})

    wos_results = wos_results.rename(columns={'Article Title': 'Title', "Publication Year" : "Year", "PDF Link": "Link"})

    concatenated_df = pd.concat([scopus_results, ieeexplore_results, wos_results], ignore_index=True)

    # Remove duplicates based on column 'A'
    result_df = concatenated_df.drop_duplicates(subset='DOI')
    result_df.to_csv(output_dir / "crawler_results_cleaned.csv", index=False)

