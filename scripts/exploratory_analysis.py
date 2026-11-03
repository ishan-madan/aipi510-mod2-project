from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# set project paths
project_root = Path(__file__).resolve().parents[1]
data_file = project_root / "data" / "cleaned" / "reaction_time_cleaned.csv"
averages_file = project_root / "data" / "cleaned" / "participant_averages.csv"
figures_dir = project_root / "figures"

figures_dir.mkdir(parents=True, exist_ok=True)

# load cleaned data
df = pd.read_csv(data_file)
averages = pd.read_csv(averages_file)

sns.set_theme(style="whitegrid")

# calculate descriptive statistics
print("DESCRIPTIVE STATISTICS")
print("----------------------")

descriptive_stats = (
    df.groupby("condition")["reaction_time_ms"]
    .agg(["count", "mean", "std", "median", "min", "max"])
    .round(2)
)

print(descriptive_stats)

# calculate participant-level summary
print("\nPARTICIPANT-LEVEL AVERAGES")
print("--------------------------")

participant_stats = averages[
    ["silence_mean_ms", "music_mean_ms", "music_minus_silence_ms"]
].agg(["mean", "std", "median"]).round(2)

print(participant_stats)

# plot 1: reaction time distributions
plt.figure(figsize=(9, 6))

sns.histplot(
    data=df,
    x="reaction_time_ms",
    hue="condition",
    kde=True,
    bins=25,
    alpha=0.4,
    element="step",
)

plt.title("Reaction Time Distributions by Condition")
plt.xlabel("Reaction Time (ms)")
plt.ylabel("Number of Trials")
plt.tight_layout()
plt.savefig(figures_dir / "reaction_time_distributions.png", dpi=300)
plt.close()

# plot 2: participant average comparison
comparison_data = averages.melt(
    id_vars="participant_id",
    value_vars=["silence_mean_ms", "music_mean_ms"],
    var_name="condition",
    value_name="reaction_time_ms",
)

comparison_data["condition"] = comparison_data["condition"].map(
    {
        "silence_mean_ms": "Silence",
        "music_mean_ms": "Music",
    }
)

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=comparison_data,
    x="condition",
    y="reaction_time_ms",
)

sns.stripplot(
    data=comparison_data,
    x="condition",
    y="reaction_time_ms",
    color="black",
    alpha=0.5,
    jitter=True,
)

plt.title("Participant Average Reaction Times by Condition")
plt.xlabel("Condition")
plt.ylabel("Average Reaction Time (ms)")
plt.tight_layout()
plt.savefig(figures_dir / "participant_comparison.png", dpi=300)
plt.close()

# plot 3: paired participant comparison
plt.figure(figsize=(9, 6))

for _, row in averages.iterrows():
    plt.plot(
        ["Silence", "Music"],
        [row["silence_mean_ms"], row["music_mean_ms"]],
        marker="o",
        alpha=0.35,
        linewidth=1,
    )

plt.title("Paired Reaction Time Comparison")
plt.xlabel("Condition")
plt.ylabel("Average Reaction Time (ms)")
plt.tight_layout()
plt.savefig(figures_dir / "paired_comparison.png", dpi=300)
plt.close()

# plot 4: distribution of paired differences
plt.figure(figsize=(9, 6))

sns.histplot(
    averages["music_minus_silence_ms"],
    kde=True,
    bins=15,
)

plt.axvline(
    0,
    color="red",
    linestyle="--",
    label="No difference",
)

plt.axvline(
    averages["music_minus_silence_ms"].mean(),
    color="green",
    linestyle="-",
    label="Mean difference",
)

plt.title("Distribution of Paired Reaction Time Differences")
plt.xlabel("Music - Silence (ms)")
plt.ylabel("Number of Participants")
plt.legend()
plt.tight_layout()
plt.savefig(figures_dir / "mean_difference.png", dpi=300)
plt.close()

print("\nVisualizations saved to:", figures_dir)
print("Exploratory analysis completed successfully.")