"""
plot_value_counts.py

Reads a CSV file and for each column, plots a bar chart of value counts
(x = unique values, y = frequency). All subplots are saved together in one image.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# ==== USER SETTINGS ====
csv_path = "C:/research_work_DIMAAG_AI_SSE/work_progress_reports/work_report_2025_2026/my_projects/AUTOMATIC_AGING/DATASETS/AA_DATASETS/subject-info.csv"                 # Path to your CSV file
output_image = "C:/research_work_DIMAAG_AI_SSE/work_progress_reports/work_report_2025_2026/my_projects/AUTOMATIC_AGING/RESULTS/value_count_bars.png" # Output image file name

figsize = (14, 10)                      # Size of the overall figure

# ==== READ CSV ====
df = pd.read_csv(csv_path)

# ==== CREATE SUBPLOTS ====
num_cols = len(df.columns)
rows = (num_cols + 1) // 2   # Two plots per row
fig, axes = plt.subplots(rows, 2, figsize=figsize)
axes = axes.flatten()

# ==== PLOT VALUE COUNTS FOR EACH COLUMN ====
for i, col in enumerate(df.columns):
    ax = axes[i]
    
    # Count frequency of unique values (sorted descending)
    value_counts = df[col].value_counts().sort_values(ascending=False)
    
    # Plot vertical bars
    bars = ax.bar(value_counts.index.astype(str), value_counts.values, color='royalblue', alpha=0.85)
    
    # Add count labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{int(height)}',
                ha='center', va='bottom', fontsize=9, color='black')
    
    ax.set_title(f"{col} (Value Counts)", fontsize=11)
    ax.set_xlabel("Unique Values")
    ax.set_ylabel("Count")
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.tick_params(axis='x', rotation=45)

# Hide unused subplots (if odd number of columns)
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.suptitle("Bar Plots of Value Counts with Labels for Each Column", fontsize=9, y=1.03)

# ==== SAVE IMAGE ====
plt.savefig(output_image, dpi=300, bbox_inches="tight")
plt.close()

print(f"✅ Bar plots with count labels saved as '{output_image}' in {os.getcwd()}")
