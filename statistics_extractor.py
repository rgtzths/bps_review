import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def substitute_value(x):
    for issn in test:
        if x != issn and x in issn:
            return issn
    return x

scimago_results = pd.read_csv("scimagojr_concatenated.csv")
final_results = pd.read_csv("final_results.csv")

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