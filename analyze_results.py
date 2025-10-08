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
    plt.rcParams.update({'font.size': 22})  # Global font size
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
    num_xticks = len(ax.get_xticks())

    # new_labels = [f'BP{i+1}' for i in range(num_xticks)]
    new_labels = [
        'BP1', 'BP2', 'BP3', 'BP4', 'BP5', 'BP6', 'BP7', 'BP8', 'BP9', 'BP10',
        'BP11', 'BP12', 'BP13', 'BP14.1', 'BP14.2', 'BP15', 'BP16',
        'BP17', 'BP18', 'BP19', 'BP20', 'BP21',
    ]

    ax.set_xticklabels(new_labels, rotation=45, ha='right')

    # Adjust layout to prevent cutting off labels
    plt.tight_layout()

    # Save the plot as SVG and PNG
    plt.savefig('full_heatmap.pdf', format='pdf', bbox_inches='tight')
    plt.savefig('full_heatmap.png', format='png', bbox_inches='tight', dpi=300)

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
    # plt.title('Compliance Levels by ML Subcategory')
    # plt.ylabel('Telecom Category')
    # plt.xlabel('Criteria')
    # plt.xticks(rotation=45, ha='right')
    num_xticks = len(ax.get_xticks())

    # new_labels = [f'BP{i+1}' for i in range(num_xticks)]
    new_labels = [
        'BP1', 'BP2', 'BP3', 'BP4', 'BP5', 'BP6', 'BP7', 'BP8', 'BP9', 'BP10',
        'BP11', 'BP12', 'BP13', 'BP14.1', 'BP14.2', 'BP15', 'BP16',
        'BP17', 'BP18', 'BP19', 'BP20', 'BP21',
    ]

    ax.set_xticklabels(new_labels, rotation=45, ha='right')

    # removing the ylabel
    plt.ylabel('')

    plt.tight_layout()

    plt.savefig('heatmap_by_category.pdf', format='pdf', bbox_inches='tight')
    plt.savefig('heatmap_by_category.png', format='png', bbox_inches='tight', dpi=300)
    plt.show()

def plot_heatmap_by_parent_category():
    global grouped_results

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



    # plt.figure(figsize=(7.5, 7))
    # plt.figure(figsize=(7.5, 8))
    plt.figure(figsize=(16*.6, 9*.6))
    ax = sns.heatmap(
        grouped_by_parent.set_index('Telecom Category'),
        annot=False,
        cmap=sns.color_palette("Blues", 7),
        # cbar_kws={'label': 'Compliance Level'},
        linewidths=0.8  # Adds separation between squares
    )

    gap_factor = 0.10  # try values between 0.1 and 0.3

    bottom, top = ax.get_ylim()
    row_height = (top - bottom) / grouped_by_parent.shape[0]

    ax.set_ylim(bottom - gap_factor * row_height, top)





    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, 0.88])
    cbar.set_ticklabels(['Not compliant', 'Compliant'])
    # plt.title('Compliance Levels by ML Category')
    plt.xticks(rotation=45, ha='right')
    # removing the ylabel
    plt.ylabel('')
    plt.tight_layout()

    # saving to the plots as pdf
    plt.savefig('heatmap_by_parent_category.svg', format='svg', bbox_inches='tight')
    plt.savefig('heatmap_by_parent_category.png', format='png', bbox_inches='tight', dpi=300)
    plt.show()


# Plotting the heatmaps
plot_full_heatmap()
plot_heatmap_by_category()
plot_heatmap_by_parent_category()




