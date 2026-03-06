# bps_review

Code and data artifacts used for a systematic review of best practices (BPs) in ML for telecommunications. The repository includes crawlers, dataset cleaning, statistics extraction, and plotting scripts.

## Repository layout

```
bps_review/
	analyze_results.py
	filter_results.py
	statistics_extractor.py
	crawlers/
		ieee.side
		ieeexplore_scraper.py
		scopus.side
		scopus_scraper.py
		wos.side
		wos_scraper.py
	dataset/
		complete_revision_process.xlsx
		crawler_results_cleaned.csv
		final_results.csv
		scimagojr_concatenated.csv
	figures/
		full_heatmap.pdf
		full_heatmap.png
		heatmap_by_category.pdf
		heatmap_by_category.png
		heatmap_by_category_old.png
		heatmap_by_parent_category.pdf
		heatmap_by_parent_category.png
		heatmap_by_parent_category.svg
		heatmap_by_year.pdf
		heatmap_by_year.png
	results_ieee/
		export2025.01.14-03.49.37.csv
		export2025.01.14-03.50.40.csv
		export2025.01.14-03.51.43.csv
		export2025.01.14-03.52.48.csv
		export2025.01.14-03.52.55.csv
		export2025.01.14-03.54.01.csv
		export2025.01.14-03.54.10.csv
		ieeexplore_export.csv
		ieeexplore_quartile_filter.csv
	results_scopus/
		scopus.csv
		scopus_export.csv
		scopus_quartile_filter.csv
	results_wos/
		savedrecs.xls
		wos_export.csv
	scimagojr/
		preprocess_scimagojr.py
		scimagojr 2019.csv
		scimagojr 2020.csv
		scimagojr 2021.csv
		scimagojr 2022.csv
		scimagojr 2023.csv
```

## Scripts

- analyze_results.py: generates heatmaps from the final results CSV and can plot year-based averages.
- filter_results.py: filters and cleans raw crawler outputs.
- statistics_extractor.py: extracts aggregate statistics for reporting.
- crawlers/*: scrapers for IEEE Xplore, Scopus, and Web of Science.
- scimagojr/preprocess_scimagojr.py: prepares ScimagoJR data for filtering.

## Usage

Generate plots from the final dataset:

```
python analyze_results.py --all
```

Run specific plots:

```
python analyze_results.py --full_heatmap
python analyze_results.py --heatmap_by_category
python analyze_results.py --heatmap_by_parent_category
python analyze_results.py --results_by_year
```

Customize input and output paths:

```
python analyze_results.py --all --input_csv dataset/final_results.csv --output_dir figures
```

## Data flow (high level)

1. Crawler exports land in results_ieee/, results_scopus/, and results_wos/.
2. filter_results.py cleans and consolidates crawler outputs into dataset/crawler_results_cleaned.csv.
3. Based on the crawler_results_cleaned.csv the complete_revision_process.xlsx is created.
4. The Excel has five sheets
 - one for abstract filtering 'Initial Screening Abstract', 
 - the second extracts the valid papers from the second,
 - the third/fourth frezes the results extracted from the second and provides a second in-depth filter after full-read and categorization
 - the fifth removes any paper that was filtered out in the fourth sheet leaving only the works that were fully categorized.
5. The fifth sheet is extracted from the excel and is named final_results.csv
6. The analyze_results.py creates plots based on the final_results.csv.

## Notes

- Plots are saved into the figures/ directory.
- Some files are large; keep raw exports under their respective results_* folders.


