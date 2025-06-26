
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data: Attack success rates for each server type under different defenses
data = {
    "Server Type": ["Filesystem", "Filesystem", "Filesystem", "Filesystem",
                    "Database", "Database", "Database", "Database",
                    "API Integration", "API Integration", "API Integration", "API Integration"],
    "Configuration": ["Baseline", "Prompt Shield", "RBAC", "Rate Limit"] * 3,
    "Success Rate (%)": [80, 42, 35, 51, 75, 41, 38, 45, 67, 36, 33, 40]
}

df = pd.DataFrame(data)

# Unique values
server_types = df["Server Type"].unique()
configs = df["Configuration"].unique()
bar_width = 0.2
x = np.arange(len(server_types))  # [0, 1, 2]

# Group the data
fig, ax = plt.subplots(figsize=(10, 6))

# Offsets for each bar group
offsets = np.linspace(-1.5 * bar_width, 1.5 * bar_width, len(configs))

# Plot each configuration group
for i, config in enumerate(configs):
    subset = df[df["Configuration"] == config]
    values = subset["Success Rate (%)"].values
    positions = x + offsets[i]
    bars = ax.bar(positions, values, width=bar_width, label=config)

    # Add labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

# Axes and styling
ax.set_xticks(x)
ax.set_xticklabels(server_types, rotation=15)
ax.set_ylabel("Success Rate (%)")
ax.set_ylim(0, 100)
ax.legend(title="Configuration")

# Grid lines
ax.yaxis.grid(True, linestyle='--', linewidth=0.5, color='gray')
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()
