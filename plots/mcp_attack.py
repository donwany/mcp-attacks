import matplotlib.pyplot as plt
import pandas as pd

# Data
data = {
    "Server Type": ["Filesystem", "Database", "API Integration", "System Tools"],
    "Success Rate (%)": [80, 75, 67, 50],
    "False Positives (%)": [5, 3, 6, 2],
    "Avg. Exploit Time (s)": [41.2, 34.7, 28.5, 37.1]
}
df = pd.DataFrame(data)

# Matplotlib styling
plt.rcParams.update({
    "font.size": 12,
    "font.family": "serif",
    "axes.edgecolor": "gray",
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.linewidth": 0.5
})

# Define colors
colors = {
    "Success Rate": "#4E79A7",
    "False Positives": "#F28E2B",
    "Exploit Time": "#59A14F"
}

# Bar settings
bar_width = 0.25
x = range(len(df))

fig, ax = plt.subplots(figsize=(11, 6))

# Bar positions
x1 = [i - bar_width for i in x]
x2 = x
x3 = [i + bar_width for i in x]

# Plot bars
bars1 = ax.bar(x1, df["Success Rate (%)"], width=bar_width,
               label="Success Rate (%)", color=colors["Success Rate"])
bars2 = ax.bar(x2, df["False Positives (%)"], width=bar_width,
               label="False Positives (%)", color=colors["False Positives"])
bars3 = ax.bar(x3, df["Avg. Exploit Time (s)"], width=bar_width,
               label="Avg. Exploit Time (s)", color=colors["Exploit Time"])

# Add text labels above bars
def add_labels(bars, is_percent=False):
    for bar in bars:
        height = bar.get_height()
        label = f'{int(height)}%' if is_percent else f'{height:.1f}'
        ax.annotate(label,
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # Offset
                    textcoords="offset points",
                    ha='center', va='bottom')

add_labels(bars1, is_percent=True)
add_labels(bars2, is_percent=True)
add_labels(bars3, is_percent=False)

# Axes and labels
ax.set_xticks(x)
ax.set_xticklabels(df["Server Type"], rotation=15)
ax.set_ylabel("Percentage / Time (seconds)")
# ax.set_title("MCP Server Evaluation Metrics by Server Type")
ax.legend(loc='upper right')

# Cap the y-axis to 100 (percent) or slightly more if needed
ax.set_ylim(0, max(100, max(df["Avg. Exploit Time (s)"]) + 10))
ax.grid(True, axis='y')

plt.tight_layout()
plt.show()