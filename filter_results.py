import pandas as pd

scimago_results = pd.read_csv("scimagojr_concatenated.csv")
ieeexplore_results = pd.read_csv("ieeexplore_export.csv")
scopus_results = pd.read_csv("scopus_export.csv")
wos_results = pd.read_csv("wos_export.csv")
issns = set()

for issn in scimago_results["Issn"]:
    issns.update(issn.split(", "))

ieeexplore_results["ISSN"] = ieeexplore_results["ISSN"].str.replace("-", "")
ieeexplore_results = ieeexplore_results[ieeexplore_results["ISSN"].isin(issns)]

ieeexplore_results.to_csv("ieeexplore_quartile_filter.csv", index=False)

scopus_results = scopus_results[scopus_results["ISSN"].isin(issns)]

scopus_results.to_csv("scopus_quartile_filter.csv", index=False)

wos_results["ISSN"] = wos_results["ISSN"].str.replace("-", "")
wos_results = wos_results[wos_results["ISSN"].isin(issns)]


ieeexplore_results = ieeexplore_results[["Document Title", "Publication Year", "ISSN", "DOI", "PDF Link"]]

wos_results = wos_results[["Article Title", "Publication Year", "ISSN", "DOI"]]

wos_results["PDF Link"] = ""

scopus_results = scopus_results[["Title", "Year", "ISSN", "DOI", "Link"]]

ieeexplore_results = ieeexplore_results.rename(columns={'Document Title': 'Title', "Publication Year" : "Year", "PDF Link": "Link"})

wos_results = wos_results.rename(columns={'Article Title': 'Title', "Publication Year" : "Year", "PDF Link": "Link"})

concatenated_df = pd.concat([scopus_results, ieeexplore_results, wos_results], ignore_index=True)

# Remove duplicates based on column 'A'
result_df = concatenated_df.drop_duplicates(subset='DOI')
result_df.to_csv("aggregated_results.csv", index=False)

