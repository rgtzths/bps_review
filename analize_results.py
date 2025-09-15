import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

# opening aggregated results
df = pd.read_csv('aggregated_results_filtered_categorized.csv', keep_default_na=False)

# removing columns that are not needed for analysis
results = df.drop(columns=['Title', 'Year', 'ISSN', 'DOI', 'Link', 'Score'])

# Preparing data for grouped heatmap plots #
# adding break-lines in Telecom Category to better displayed in the heatmap
break_line_dict = {
    'Channel and Physical Layer': 'Channel and Physical\nLayer',
    'Network Slicing and Management': 'Network Slicing\nand Management',
    'Resource and Traffic Management': 'Resource and\nTraffic Management',
    'User Mobility and Positioning': 'User Mobility\nand Positioning',
}
results['Telecom Category'] = results['Telecom Category'].replace(break_line_dict)

# encoding the values
encoding_dict = {
    'Yes': 1,
    'Partial': 0.5,
    'No': 0,
    'NA': None
}
for col in results.columns[1:]:
    results[col] = results[col].map(encoding_dict)

# grouping by Telecom Category and calculating the mean for each category
grouped_results = results.groupby('Telecom Category').mean().reset_index()

def plot_full_heatmap():
    global df
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
    legend = ax.legend(handles=legend_elements,
                       bbox_to_anchor=(1.05, 1.0),  # Position legend to the right, at the top
                       loc='upper left',  # Anchor point is upper left of legend
                       frameon=True,
                       fancybox=True,
                       shadow=True,
                       title='Values')

    # Customize the plot
    plt.title('Research Paper Analysis Heatmap', fontsize=16, pad=20)
    # plt.xlabel('Analysis Criteria', fontsize=12)
    plt.ylabel('DOI', fontsize=12)
    plt.xticks(rotation=45, ha='right')

    num_xticks = len(ax.get_xticks())
    new_labels = [f'BP{i+1}' for i in range(num_xticks)]
    ax.set_xticklabels(new_labels, rotation=45, ha='right')

    # Adjust layout to prevent cutting off labels
    plt.tight_layout()

    # Show the plot
    plt.show()

def plot_heatmap_by_category():
    global grouped_results

    plt.figure(figsize=(11, 4))
    ax = sns.heatmap(
        grouped_results.set_index('Telecom Category'),
        annot=False,
        cmap=sns.color_palette("Blues", 7),
        # cbar_kws={'label': 'Compliance Level'},
        linewidths=0.8  # Adds separation between squares
    )
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(['Not compliant', 'Compliant'])
    plt.title('Compliance Levels by ML Subcategory')
    # plt.ylabel('Telecom Category')
    # plt.xlabel('Criteria')
    # plt.xticks(rotation=45, ha='right')
    num_xticks = len(ax.get_xticks())
    new_labels = [f'BP{i+1}' for i in range(num_xticks)]
    ax.set_xticklabels(new_labels, rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_heatmap_by_parent_category():
    global grouped_results

    parent_cat_dict = {
        'Presents the task to solve': 'Scope Definition',
        'Presents the state-of-the-art approaches': 'Scope Definition',
        'Describes the available data': 'Scope Definition',
        'Describes the model inputs/ outputs': 'Scope Definition',
        'Describes the model': 'Scope Definition',
        'Presents data preprocessing': 'Data Handling',
        'Presents data division': 'Data Handling',
        'Presents data distribution': 'Data Handling',
        'Presents hyperparameter tuning': 'Model Training/evaluation',
        'Uses the correct metrics for evaluation': 'Model Training/evaluation',
        'Describes the experiments performed': 'Model Training/evaluation',
        'Describes the testing environment': 'Model Training/evaluation',
        'Describes the used hyperparameters': 'Model Training/evaluation',
        'Uses real-world datasets': 'Model Training/evaluation',
        'Uses open datasets': 'Model Training/evaluation',
        'Uses multiple datasets': 'Model Training/evaluation',
        'Compares with state-of-the-art models': 'Model Training/evaluation',
        'Critically analyzes production applicability': 'Model Deployment',
        'Publishes the used dataset': 'Publication',
        'Publishes the trained model': 'Publication',
        'Publishes the code': 'Publication',
        'Publish the seeds used': 'Publication',
    }

    # Grouping the columns (categories) by their parent category with mean
    parent_categories = ['Scope Definition', 'Data Handling', 'Model Training/evaluation', 'Model Deployment', 'Publication']
    grouped_by_parent = pd.DataFrame(columns=['Telecom Category'] + parent_categories)
    grouped_by_parent['Telecom Category'] = grouped_results['Telecom Category']
    for parent in parent_categories:
        cols = [col for col, p in parent_cat_dict.items() if p == parent]
        grouped_by_parent[parent] = grouped_results[cols].mean(axis=1)

    plt.figure(figsize=(7.5, 7))
    ax = sns.heatmap(
        grouped_by_parent.set_index('Telecom Category'),
        annot=False,
        cmap=sns.color_palette("Blues", 7),
        # cbar_kws={'label': 'Compliance Level'},
        linewidths=0.8  # Adds separation between squares
    )
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, 0.88])
    cbar.set_ticklabels(['Not compliant', 'Compliant'])
    plt.title('Compliance Levels by ML Category')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


# Plotting the heatmaps
plot_full_heatmap()
plot_heatmap_by_category()
plot_heatmap_by_parent_category()




