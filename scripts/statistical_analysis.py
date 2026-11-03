from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


# set project paths
project_root = Path(__file__).resolve().parents[1]
data_file = project_root / "data" / "cleaned" / "participant_averages.csv"
figures_dir = project_root / "figures"

figures_dir.mkdir(parents=True, exist_ok=True)

# load data
df = pd.read_csv(data_file)

silence = df["silence_mean_ms"]
music = df["music_mean_ms"]
differences = df["music_minus_silence_ms"]

# set significance level
alpha = 0.05

# descriptive statistics
print("DESCRIPTIVE STATISTICS")
print("----------------------")
print(f"Participants: {len(df)}")
print(f"Silence mean: {silence.mean():.2f} ms")
print(f"Silence standard deviation: {silence.std():.2f} ms")
print(f"Music mean: {music.mean():.2f} ms")
print(f"Music standard deviation: {music.std():.2f} ms")
print(f"Mean paired difference: {differences.mean():.2f} ms")
print(f"SD of paired differences: {differences.std():.2f} ms")

# paired t-test
t_statistic, p_value = stats.ttest_rel(music, silence)

# calculate confidence interval for paired difference
sample_size = len(differences)
degrees_freedom = sample_size - 1
standard_error = stats.sem(differences)

critical_value = stats.t.ppf(1 - alpha / 2, degrees_freedom)

ci_lower = differences.mean() - critical_value * standard_error
ci_upper = differences.mean() + critical_value * standard_error

# calculate Cohen's dz effect size
cohens_dz = differences.mean() / differences.std()

print("\nPAIRED T-TEST")
print("-------------")
print(f"t-statistic: {t_statistic:.4f}")
print(f"Degrees of freedom: {degrees_freedom}")
print(f"p-value: {p_value:.6f}")
print(f"95% confidence interval: [{ci_lower:.2f}, {ci_upper:.2f}] ms")
print(f"Cohen's dz: {cohens_dz:.4f}")

if p_value < alpha:
    print("Result: Reject the null hypothesis.")
else:
    print("Result: Fail to reject the null hypothesis.")

# check normality of paired differences
shapiro_statistic, shapiro_p = stats.shapiro(differences)

print("\nNORMALITY CHECK")
print("----------------")
print(f"Shapiro-Wilk statistic: {shapiro_statistic:.4f}")
print(f"Shapiro-Wilk p-value: {shapiro_p:.6f}")

if shapiro_p > alpha:
    print("No statistically significant evidence against normality.")
else:
    print("Evidence suggests the paired differences may not be normally distributed.")

# wilcoxon signed-rank sensitivity analysis
wilcoxon_statistic, wilcoxon_p = stats.wilcoxon(
    music,
    silence,
    alternative="two-sided",
)

print("\nWILCOXON SIGNED-RANK SENSITIVITY TEST")
print("------------------------------------")
print(f"Test statistic: {wilcoxon_statistic:.4f}")
print(f"p-value: {wilcoxon_p:.6f}")

# exploratory comparison by experimental order
print("\nEXPLORATORY ORDER ANALYSIS")
print("--------------------------")

order_summary = (
    df.groupby("order")["music_minus_silence_ms"]
    .agg(["count", "mean", "std"])
    .rename(index={1: "Silence first", 2: "Music first"})
)

print(order_summary.round(2))

# test whether experimental order affected the music effect
silence_first = df.loc[df["order"] == 1, "music_minus_silence_ms"]
music_first = df.loc[df["order"] == 2, "music_minus_silence_ms"]

order_test = stats.ttest_ind(
    silence_first,
    music_first,
    equal_var=False,
)

print("\nORDER EFFECT TEST")
print("-----------------")
print(f"Silence-first mean difference: {silence_first.mean():.2f} ms")
print(f"Music-first mean difference: {music_first.mean():.2f} ms")
print(f"Difference between groups: {music_first.mean() - silence_first.mean():.2f} ms")
print(f"Welch t-statistic: {order_test.statistic:.4f}")
print(f"p-value: {order_test.pvalue:.6f}")

# plot paired differences
plt.figure(figsize=(9, 6))

plt.hist(differences, bins=12, edgecolor="black", alpha=0.75)
plt.axvline(0, color="red", linestyle="--", label="No difference")
plt.axvline(
    differences.mean(),
    color="green",
    linestyle="-",
    label="Mean difference",
)

plt.title("Distribution of Paired Reaction Time Differences")
plt.xlabel("Music - Silence (ms)")
plt.ylabel("Number of Participants")
plt.legend()
plt.tight_layout()
plt.savefig(figures_dir / "statistical_difference_distribution.png", dpi=300)
plt.close()

# create Q-Q plot to assess normality
plt.figure(figsize=(7, 6))

stats.probplot(differences, dist="norm", plot=plt)
plt.title("Q-Q Plot of Paired Reaction Time Differences")
plt.tight_layout()
plt.savefig(figures_dir / "paired_difference_qq_plot.png", dpi=300)
plt.close()

print("\nStatistical analysis completed successfully.")
print(f"Figures saved to: {figures_dir}")