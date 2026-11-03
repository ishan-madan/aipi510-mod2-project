from pathlib import Path
import pandas as pd


# set project paths
project_root = Path(__file__).resolve().parents[1]
raw_file = project_root / "data" / "raw" / "reaction_time_data.csv"
cleaned_dir = project_root / "data" / "cleaned"

cleaned_dir.mkdir(parents=True, exist_ok=True)

# load raw data
df = pd.read_csv(raw_file)

# check required columns
required_columns = [
    "participant_id",
    "condition",
    "order",
    "trial",
    "reaction_time_ms",
]

if not set(required_columns).issubset(df.columns):
    raise ValueError("The dataset is missing required columns.")

df = df[required_columns].copy()

# clean column values and data types
df["participant_id"] = df["participant_id"].astype("string").str.strip()
df["condition"] = df["condition"].astype("string").str.strip().str.lower()

for column in ["order", "trial", "reaction_time_ms"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# check missing and invalid values
if df.isnull().any().any():
    raise ValueError("The dataset contains missing or invalid values.")

if (df["reaction_time_ms"] <= 0).any():
    raise ValueError("Reaction times must be positive.")

if not set(df["condition"].unique()) == {"silence", "music"}:
    raise ValueError("Unexpected experimental conditions.")

if not set(df["order"].unique()).issubset({1, 2}):
    raise ValueError("Unexpected condition order values.")

# check participant and trial counts
if df["participant_id"].nunique() != 40:
    raise ValueError("Expected 40 participants.")

trial_counts = df.groupby(["participant_id", "condition"]).size()

if not (trial_counts == 10).all() or len(trial_counts) != 80:
    raise ValueError("Each participant must have 10 trials per condition.")

# check duplicate observations
if df.duplicated(
    subset=["participant_id", "condition", "trial"]
).any():
    raise ValueError("Duplicate trial records found.")

# check consistent condition order for each participant
if not (df.groupby("participant_id")["order"].nunique() == 1).all():
    raise ValueError("Inconsistent condition order for a participant.")

# save cleaned trial-level data
df = df.sort_values(
    ["participant_id", "condition", "trial"]
).reset_index(drop=True)

df.to_csv(cleaned_dir / "reaction_time_cleaned.csv", index=False)

# calculate participant-level averages
averages = (
    df.groupby(["participant_id", "condition"])["reaction_time_ms"]
    .mean()
    .unstack()
    .reset_index()
)

# calculate paired differences
averages["music_minus_silence_ms"] = (
    averages["music"] - averages["silence"]
)

# include experimental order
orders = df.groupby("participant_id")["order"].first().reset_index()

averages = averages.merge(orders, on="participant_id")

averages = averages.rename(
    columns={
        "silence": "silence_mean_ms",
        "music": "music_mean_ms",
    }
)

averages = averages[
    [
        "participant_id",
        "order",
        "silence_mean_ms",
        "music_mean_ms",
        "music_minus_silence_ms",
    ]
]

averages.to_csv(
    cleaned_dir / "participant_averages.csv",
    index=False,
)

# print summary
print("Data cleaning completed successfully.")
print(f"Participants: {df['participant_id'].nunique()}")
print(f"Observations: {len(df)}")
print(f"Missing values: {df.isnull().sum().sum()}")
print(f"Duplicate records: {df.duplicated(
    subset=['participant_id', 'condition', 'trial']
).sum()}")

print("\nCondition order:")
print(
    orders["order"].value_counts().sort_index().rename(
        index={1: "Silence first", 2: "Music first"}
    )
)

print("\nParticipant averages saved.")