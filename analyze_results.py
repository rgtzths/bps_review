import argparse

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch


def plot_full_heatmap(df : pd.DataFrame, output_dir : Path, bp_labels : list[str]):

    df = df.iloc[1:].reset_index(drop=True)

    plt.rcParams.update({'font.size': 22})  # Global font size
    results_for_full_heatmap = df.drop(columns=['Title', 'Year', 'ISSN', 'Telecom Category', 'Link', 'Score'])
    # Set DOI as index
    df = results_for_full_heatmap.set_index('DOI')

    # Manually define the mapping to ensure correct order
    value_to_int = {
        'Yes': 3,
        'Partial': 2,
        'No': 1,
        'NA': 0
    }

    # Manually define blue scale colors for Yes, Partial, No and gray for NA
    custom_colors = [
        '#cacbcc',  # Gray for NA (value 0)
        '#c5d3e6',  # Light blue for No (value 1)
        '#729ECE',  # Medium blue for Partial (value 2)
        '#156399'   # Dark blue for Yes (value 3)
    ]

    # Create the plot with appropriate size
    plt.figure(figsize=(16, 30))

    # Create heatmap by replacing values with integers and using custom colors
    ax = sns.heatmap(df.replace(value_to_int),
                     cmap=sns.color_palette(custom_colors),
                     yticklabels=df.index,
                     xticklabels=df.columns,
                     linewidths=0.5,
                     cbar=False)  # Disable the default colorbar

    # Add hatch pattern to NA cells
    # First, find all the positions where value is NA
    na_positions = np.where(df.replace(value_to_int) == 0)

    # Add hatch pattern to these cells
    for i, j in zip(na_positions[0], na_positions[1]):
        ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=False, hatch='////',
                                  edgecolor='white', linewidth=0.5, alpha=0.7))

    # Create custom legend patches
    legend_elements = [
        Patch(facecolor='#156399', label='Yes'),
        Patch(facecolor='#729ECE', label='Partial'),
        Patch(facecolor='#c5d3e6', label='No'),
        Patch(facecolor='#cacbcc', hatch='////', edgecolor='white', label='NA')
    ]

    # Add custom legend to the plot
    ax.legend(handles=legend_elements,
                       bbox_to_anchor=(1.02, 1.0),  # Position legend to the right, at the top
                       loc='upper left',  # Anchor point is upper left of legend
                       frameon=True,
                       fancybox=True,
                       shadow=True,
                       title='Values')

    # Customize the plot
    # plt.title('Research Paper Analysis Heatmap', fontsize=16, pad=20)
    # plt.xlabel('Analysis Criteria', fontsize=12)
    # plt.ylabel('DOI', fontsize=12)
    plt.ylabel('')
    # remove the y labels
    ax.set_yticklabels([])
    # remove the tick marks (the small "-" lines)
    ax.tick_params(axis='y', which='both', length=0)

    plt.xticks(rotation=45, ha='right')

    ax.set_xticklabels(bp_labels, rotation=45, ha='right')

    # Adjust layout to prevent cutting off labels
    plt.tight_layout()

    # Save the plot as SVG and PNG
    plt.savefig(output_dir / 'full_heatmap.pdf', format='pdf', bbox_inches='tight')
    plt.savefig(output_dir / 'full_heatmap.png', format='png', bbox_inches='tight', dpi=300)

    # Show the plot
    plt.show()

def plot_bp_correlation_heatmap(
    df: pd.DataFrame,
    bp_labels: list[str],
    encoding_dict: dict[str, float] = None,
    method: str = "pearson",
    output_dir: Path = None,
    figsize=(12, 10),
    annot: bool = False,
    cmap: str = "Blues",
):
    """
    Plots the correlation matrix between the best practices (BPs) as a heatmap.
    method: 'pearson', 'spearman', or 'kendall'
    """
    bp_df = df.drop(columns=['Title', 'Year', 'ISSN', 'Telecom Category', 'Link', 'Score', 'DOI']).replace(encoding_dict).dropna()

    corr = bp_df.corr(method=method)

    plt.figure(figsize=figsize)
    sns.heatmap(
        corr,
        annot=annot,
        cmap=cmap,
        linewidths=0.8,
        xticklabels=bp_labels,
        yticklabels=bp_labels,
        vmin=-1, vmax=1
    )

    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    if output_dir is not None:
        plt.savefig(output_dir / 'bp_correlation_heatmap.pdf', format='pdf', bbox_inches='tight')
        plt.savefig(output_dir / 'bp_correlation_heatmap.png', format='png', bbox_inches='tight', dpi=300)
    plt.show()
    return corr
    
def print_bp_correlations(
    df: pd.DataFrame,
    bp_labels: list[str],
    encoding_dict: dict[str, float] = None,
    method: str = "pearson",
    output_path: Path = None,
):
    """
    Computes and prints the correlation matrix between the best practices (BPs).
    method: 'pearson', 'spearman', or 'kendall'
    """
    # Extract only BP columns
    bp_df = df.drop(columns=['Title', 'Year', 'ISSN', 'Telecom Category', 'Link', 'Score', 'DOI']).replace(encoding_dict).dropna()
    corr = bp_df.corr(method=method)
    # Print as markdown table
    header = "| BP | " + " | ".join(bp_labels) + " |"
    separator = "|---" * (len(bp_labels)+1) + "|"
    rows = [
        "| " + bp_labels[i] + " | " + " | ".join(f"{corr.iloc[i, j]:.2f}" if not pd.isna(corr.iloc[i, j]) else "" for j in range(len(bp_labels))) + " |"
        for i in range(len(bp_labels))
    ]
    markdown_table = "\n".join([header, separator] + rows)
    #print(f"\nCorrelation matrix between BPs (method: {method}):\n")
    #print(markdown_table)

    # Print only correlations above 0.4 (absolute value), excluding self-correlations
    print("\nCorrelations above 0.4 (|corr| > 0.4):")
    correlations = []
    for i in range(len(bp_labels)):
        for j in range(i + 1, len(bp_labels)):
            val = corr.iloc[i, j]
            if pd.notna(val) and abs(val) > 0.4:
                correlations.append((bp_labels[i], bp_labels[j], val))

    if correlations:
        correlations.sort(key=lambda item: abs(item[2]), reverse=True)
        for bp_i, bp_j, val in correlations:
            print(f"{bp_i} - {bp_j}: {val:.2f}")
    else:
        print("None above threshold.")

    if output_path is not None:
        Path(output_path).write_text(markdown_table, encoding="utf-8")
    return corr

def plot_heatmap_by_category(grouped_results : pd.DataFrame, output_dir : Path, bp_labels : list[str]):
    plt.figure(figsize=(11, 4))
    grouped_results = grouped_results.set_index('Telecom Category')
    ax = sns.heatmap(
        grouped_results,
        annot=False,
        cmap=sns.color_palette("Blues", 7),
        linewidths=0.8
    )
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(['Not compliant', 'Compliant'])

    ax.set_xticks(np.arange(len(grouped_results.columns))+0.5)
    ax.set_xticklabels(bp_labels, rotation=45, ha='right')

    # removing the ylabel
    plt.ylabel('')

    plt.tight_layout()

    plt.savefig(output_dir / 'heatmap_by_category.pdf', format='pdf', bbox_inches='tight')
    plt.savefig(output_dir / 'heatmap_by_category.png', format='png', bbox_inches='tight', dpi=300)
    plt.show()

def print_compliance_by_telecom_category(
    df: pd.DataFrame,
    value_format: str = "{:.2f}",
    encoding_dict: dict[str, float] = None,
    output_path: Path = None,
):
    """
    Prints the average compliance by telecom category over all best practices as a markdown table.
    """
    results = df.drop(columns=['Title', 'Year', 'ISSN', 'DOI', 'Link', 'Score'])
    results['Telecom Category'] = results['Telecom Category'].replace({
        'Channel and Physical Layer': 'Channel Man & PHY layer',
        'Network Slicing and Management': 'Network Slicing & Management',
        'Resource and Traffic Management': 'Resource & Traffic Management',
        'User Mobility and Positioning': 'User Mobility & Positioning',
        'Computing and Edge': 'Edge Computing',
        'Security and Privacy': 'Security & Privacy',
    })
    for col in results.columns[1:]:
        results[col] = results[col].map(encoding_dict)
    grouped = results.groupby('Telecom Category').mean()
    avg_compliance = grouped.mean(axis=1)
    # Markdown table
    header = "| Telecom Category | Avg Compliance |"
    separator = "| --- | --- |"
    rows = [
        f"| {cat} | {value_format.format(val) if not pd.isna(val) else ''} |"
        for cat, val in avg_compliance.items()
    ]
    markdown_table = "\n".join([header, separator] + rows)
    print(markdown_table)
    if output_path is not None:
        Path(output_path).write_text(markdown_table, encoding="utf-8")
    return markdown_table

def plot_heatmap_by_parent_category(grouped_results : pd.DataFrame, output_dir : Path):
    print(grouped_results)
    parent_cat_dict = {
        'Presents the task to solve': 'Conceptualization',
        'Presents the state-of-the-art approaches': 'Conceptualization',
        'Describes the available data': 'Conceptualization',
        'Describes the model inputs/ outputs': 'Conceptualization',
        'Describes the model': 'Conceptualization',
        'Presents data preprocessing': 'Data Handling',
        'Presents data division': 'Data Handling',
        'Presents data distribution': 'Data Handling',
        'Presents hyperparameter tuning': 'Model Development\n& Evaluation',
        'Uses the correct metrics for evaluation': 'Model Development\n& Evaluation',
        'Describes the experiments performed': 'Model Development\n& Evaluation',
        'Describes the testing environment': 'Model Development\n& Evaluation',
        'Describes the used hyperparameters': 'Model Development\n& Evaluation',
        'Uses real-world datasets': 'Model Development\n& Evaluation',
        'Uses open datasets': 'Model Development\n& Evaluation',
        'Uses multiple datasets': 'Model Development\n& Evaluation',
        'Compares with state-of-the-art models': 'Model Development\n& Evaluation',
        'Critically analyzes production applicability': 'Model Deployment',
        'Publishes the used dataset': 'Publication',
        'Publishes the trained model': 'Publication',
        'Publishes the code': 'Publication',
        'Publish the seeds used': 'Publication',
    }

    # Grouping the columns (categories) by their parent category with mean
    parent_categories = ['Conceptualization', 'Data Handling', 'Model Development\n& Evaluation', 'Model Deployment', 'Publication']
    grouped_by_parent = pd.DataFrame(columns=['Telecom Category'] + parent_categories)
    grouped_by_parent['Telecom Category'] = grouped_results['Telecom Category']
    for parent in parent_categories:
        cols = [col for col, p in parent_cat_dict.items() if p == parent]
        grouped_by_parent[parent] = grouped_results[cols].mean(axis=1)


    # adding a new row for General Telecommunications (is a average of all columns)
    general_telecom_data = grouped_by_parent[parent_categories].mean().values
    general_telecom_row = pd.DataFrame([['General Telecommunications'] + list(general_telecom_data)], columns=grouped_by_parent.columns)
    grouped_by_parent = pd.concat([grouped_by_parent, general_telecom_row], ignore_index=True)

    # adding General ML as another row
    general_ml_data = [0.56470295, 0.28473979, 0.82753725, 0.08602814, 0.54932314]
    general_ml_row = pd.DataFrame([['General ML'] + general_ml_data], columns=grouped_by_parent.columns)
    grouped_by_parent = pd.concat([grouped_by_parent, general_ml_row], ignore_index=True)

    plt.figure(figsize=(16*.6, 9*.6))
    ax = sns.heatmap(
        grouped_by_parent.set_index('Telecom Category'),
        annot=False,
        cmap=sns.color_palette("Blues", 7),
        linewidths=0.8,
    )

    gap_factor = 0.10  # try values between 0.1 and 0.3

    bottom, top = ax.get_ylim()
    row_height = (top - bottom) / grouped_by_parent.shape[0]

    ax.set_ylim(bottom - gap_factor * row_height, top)

    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, 0.85])
    cbar.set_ticklabels(['Not compliant', 'Compliant'])
    # plt.title('Compliance Levels by ML Category')
    plt.xticks(rotation=45, ha='right')
    # removing the ylabel
    plt.ylabel('')
    plt.tight_layout()

    # saving to the plots as pdf
    plt.savefig(output_dir / 'heatmap_by_parent_category.svg', format='svg', bbox_inches='tight')
    plt.savefig(output_dir / 'heatmap_by_parent_category.pdf', format='pdf', bbox_inches='tight')
    plt.savefig(output_dir / 'heatmap_by_parent_category.png', format='png', bbox_inches='tight', dpi=300)
    plt.show()

def get_results_by_year(df, encoding_dict=None):

    results = df.drop(columns=['Title', 'ISSN', 'DOI', 'Link', 'Score'])
    criteria_cols = [col for col in results.columns if col not in ['Year', 'Telecom Category']]

    for col in criteria_cols:
        results[col] = results[col].map(encoding_dict)

    grouped_by_year = (
        results
        .groupby('Year')[criteria_cols]
        .mean()
        .reset_index()
        .sort_values('Year')
    )

    return grouped_by_year

def plot_heatmap_by_year(
    df : pd.DataFrame,
    output_dir : Path,
    bp_labels : list[str],
    encoding_dict : dict[str, float] = None,
):

    grouped_by_year = get_results_by_year(df, encoding_dict=encoding_dict)
    table = grouped_by_year.set_index('Year').T

    if len(bp_labels) == len(table.index):
        table.index = bp_labels

    plt.figure(figsize=(12, 6))
    ax = sns.heatmap(
        table,
        annot=False,
        cmap=sns.color_palette("Blues", 7),
        linewidths=0.8
    )

    ax.set_xticks(np.arange(len(table.columns)) + 0.5)
    ax.set_xticklabels([str(col) for col in table.columns], rotation=45, ha='right')
    ax.set_yticks(np.arange(len(table.index)) + 0.5)
    ax.set_yticklabels(table.index, rotation=0)

    plt.ylabel('')
    plt.tight_layout()

    plt.savefig(output_dir / 'heatmap_by_year.pdf', format='pdf', bbox_inches='tight')
    plt.savefig(output_dir / 'heatmap_by_year.png', format='png', bbox_inches='tight', dpi=300)
    plt.show()

def print_results_by_year_markdown(
    df : pd.DataFrame,
    bp_labels : list[str],
    value_format : str = "{:.2f}",
    encoding_dict : dict[str, float] = None,
    output_path : Path = None,
):

    grouped_by_year = get_results_by_year(df, encoding_dict=encoding_dict)
    table = grouped_by_year.set_index('Year').T

    if len(bp_labels) == len(table.index):
        table.index = bp_labels

    formatted = table.applymap(
        lambda value: "" if pd.isna(value) else value_format.format(value)
    )

    columns = ["BP"] + [str(col) for col in formatted.columns]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = [
        "| " + " | ".join([str(index)] + row.tolist()) + " |"
        for index, row in formatted.iterrows()
    ]

    markdown_table = "\n".join([header, separator] + rows)
    print(markdown_table)

    # Print average compliance per year
    avg_compliance_per_year = grouped_by_year.set_index('Year').mean(axis=1)
    print("\nAverage compliance per year:")
    for year, avg in avg_compliance_per_year.items():
        print(f"{year}: {value_format.format(avg) if not pd.isna(avg) else ''}")

    if output_path is not None:
        Path(output_path).write_text(markdown_table, encoding="utf-8")

    return markdown_table

def percentage_compliant_rows(df: pd.DataFrame, bp_list: list[str], encoding_dict: dict[str, float] = None, compliance_value: float = 1.0) -> float:
    """
    Returns the percentage of rows that comply with all BPs in bp_list.
    A row is compliant if all specified BPs have the compliance_value (default: 1.0, i.e., 'Yes').
    """
    if encoding_dict is None:
        encoding_dict = {
            'Yes': 1.0,
            'Partial': 0.5,
            'No': 0.0,
            'NA': None
        }

    bp_df = df[bp_list].replace(encoding_dict)
    compliant = (bp_df == compliance_value).all(axis=1)
    total_rows = len(bp_df)
    if total_rows == 0:
        return 0.0
    percentage = compliant.sum() / total_rows * 100
    return percentage

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Analyze the results of the systematic review.')
    parser.add_argument('--full_heatmap', action='store_true', help='Plot the full heatmap of all papers and criteria.')
    parser.add_argument('--heatmap_by_category', action='store_true', help='Plot the heatmap grouped by telecom category.')
    parser.add_argument('--heatmap_by_parent_category', action='store_true', help='Plot the heatmap grouped by parent category.')
    parser.add_argument('--heatmap_by_year', action='store_true', help='Plot the results by year as a heatmap.')
    parser.add_argument('--print_results_by_year', action='store_true', help='Print the results by year as a markdown table and average compliance.')
    parser.add_argument('--print_compliance_by_telecom_category', action='store_true', help='Print the average compliance by telecom category over all best practices.')
    parser.add_argument('--print_bp_correlations', action='store_true', help='Print the correlation matrix between best practices (BPs).')
    parser.add_argument('--plot_bp_correlation_heatmap', action='store_true', help='Plot the correlation matrix between best practices (BPs) as a heatmap.')
    parser.add_argument('--count_compliant_rows', action='store_true', help='Count the number of compliant rows for specific BPs.')
    parser.add_argument('--all', action='store_true', help='Run all analyses and plots.')
    parser.add_argument('--input_csv', type=str, default='dataset/final_results.csv', help='Path to the input CSV file containing the results.')
    parser.add_argument('--output_dir', type=str, default='figures', help='Directory to save the output plots.')

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bp_labels = [
        'BP1', 'BP2', 'BP3', 'BP4', 'BP5', 'BP6', 'BP7', 'BP8', 'BP9', 'BP10',
        'BP11', 'BP12', 'BP13', 'BP14.1', 'BP14.2', 'BP15', 'BP16',
        'BP17', 'BP18', 'BP19', 'BP20', 'BP21'
    ]
    
    # opening aggregated results (first two lines are the header)
    df = pd.read_csv(args.input_csv, header=[0, 1], keep_default_na=False)

    df.columns = [
        sub if isinstance(sub, str) and sub.strip() and not str(sub).startswith('Unnamed:') else main
        for main, sub in df.columns
    ]

    # removing columns that are not needed for analysis
    results = df.drop(columns=['Title', 'Year', 'ISSN', 'DOI', 'Link', 'Score'])

    # Preparing data for grouped heatmap plots #
    # adding break-lines in Telecom Category to better displayed in the heatmap
    break_line_dict = {
        'Channel and Physical Layer': 'Channel Man & PHY layer',
        'Network Slicing and Management': 'Network Slicing & Management',
        'Resource and Traffic Management': 'Resource & Traffic Management',
        'User Mobility and Positioning': 'User Mobility & Positioning',
        'Computing and Edge': 'Edge Computing',
        'Security and Privacy': 'Security & Privacy',
    }
    results['Telecom Category'] = results['Telecom Category'].replace(break_line_dict)

    # encoding the values
    encoding_dict = {
        'Yes': 1.0,
        'Partial': 0.5,
        'No': 0.0,
        'NA': None
    }
    for col in results.columns[1:]:
        results[col] = results[col].map(encoding_dict)

    # grouping by Telecom Category and calculating the mean for each category
    grouped_results = results.groupby('Telecom Category').mean().reset_index()

    # Plotting the heatmaps and printing results
    if args.full_heatmap or args.all:
        plot_full_heatmap(df, output_dir=output_dir, bp_labels=bp_labels)
    if args.heatmap_by_category or args.all:
        plot_heatmap_by_category(grouped_results, bp_labels=bp_labels, output_dir=output_dir)
    if args.heatmap_by_parent_category or args.all:
        plot_heatmap_by_parent_category(grouped_results, output_dir=output_dir)
    if args.heatmap_by_year or args.all:
        plot_heatmap_by_year(df, output_dir=output_dir, bp_labels=bp_labels, encoding_dict=encoding_dict)
    if args.print_results_by_year:
        print_results_by_year_markdown(df, bp_labels=bp_labels, encoding_dict=encoding_dict)
    if args.print_compliance_by_telecom_category:
        print_compliance_by_telecom_category(df, encoding_dict=encoding_dict)
    if args.print_bp_correlations:
        print_bp_correlations(df, bp_labels=bp_labels, encoding_dict=encoding_dict)
    if args.plot_bp_correlation_heatmap:
        plot_bp_correlation_heatmap(df, bp_labels=bp_labels, encoding_dict=encoding_dict, output_dir=output_dir)
    if args.count_compliant_rows:
        compliant_percentage = percentage_compliant_rows(df, ['Presents the task to solve', 'Presents the state-of-the-art approaches', 'Uses the correct metrics for evaluation'], encoding_dict=encoding_dict)
        print(f"Percentage of compliant rows for ['Presents the task to solve', 'Presents the state-of-the-art approaches', 'Uses the correct metrics for evaluation']: {compliant_percentage:.2f}%")




