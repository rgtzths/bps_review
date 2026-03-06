import argparse
from pathlib import Path

import pandas as pd

def substitute_value(x):
    for issn in test:
        if x != issn and x in issn:
            return issn
    return x

'''
Script to extract statistics from the filtered results.
It reads the final results CSV file, counts the number of publications per journal and publisher,
and prints the counts by year and category, journal and publisher.
'''
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Extract statistics from the filtered results.')
    parser.add_argument('--scimago_file', type=str, default="./dataset/scimagojr_concatenated.csv", help='Path to the ScimagoJR CSV file.')
    parser.add_argument('--final_results_file', type=str, default="./dataset/final_results.csv", help='Path to the final results CSV file.')
    args = parser.parse_args()

    scimago_results = pd.read_csv(args.scimago_file)
    final_results = pd.read_csv(args.final_results_file)

    issns_pub = scimago_results[["Issn", "Publisher"]].set_index('Issn')['Publisher'].to_dict()

    issns_name = scimago_results[["Title", "Issn"]].set_index('Issn')['Title'].to_dict()

    test = list(scimago_results["Issn"])

    test = set(scimago_results["Issn"])

    final_results['ISSN'] = final_results['ISSN'].apply(substitute_value)


    journal_counts = final_results['ISSN'].value_counts().to_dict()

    print(sum(list(journal_counts.values())))

    publisher_counts = dict()

    for journal in journal_counts:
        if issns_pub[journal] in publisher_counts:
            publisher_counts[issns_pub[journal]][0] += journal_counts[journal]
            publisher_counts[issns_pub[journal]][1].append((issns_name[journal], journal_counts[journal]))

        else:
            publisher_counts[issns_pub[journal]] = [journal_counts[journal], [(issns_name[journal], journal_counts[journal])]]

    print("Number of Journals considered:", len(list(journal_counts.keys())))
    print("Number of Publishers considered:", len(list(publisher_counts.keys())))

    for publisher in publisher_counts:
        print(publisher, publisher_counts[publisher][0], len(publisher_counts[publisher][1]))
        for journal_tuple in publisher_counts[publisher][1]:
            print(journal_tuple)

    print("Counts by Year")
    print(final_results['Year'].value_counts())

    print("Counts by category")
    print(final_results['Telecom Category'].value_counts())