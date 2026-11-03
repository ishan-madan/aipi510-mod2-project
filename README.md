# Background Music and Human Visual Reaction Time

## Project Overview

This project investigates whether listening to background instrumental music affects human visual reaction time compared with performing the same task in silence.

The experiment uses a within-subjects design in which each participant completes reaction-time trials under both conditions. The collected data is cleaned, explored, and analyzed using Python to determine whether there is a statistically significant difference in reaction time between silence and background instrumental music.

## Research Question

Does listening to background instrumental music affect human visual reaction time compared with performing the same task in silence?

## Experimental Design

The experiment includes 40 participants. Each participant completes 10 reaction-time trials in silence and 10 trials while listening to background instrumental music, resulting in 800 total observations.

The experimental design is within-subjects, meaning every participant experiences both conditions. To reduce potential order effects, participants are assigned to one of two sequences:

- **Order 1:** Silence first, followed by music.
- **Order 2:** Music first, followed by silence.

### Variables

- **Independent variable:** Audio condition (silence or instrumental music).
- **Dependent variable:** Visual reaction time, measured in milliseconds.
- **Experimental unit:** Individual participant.

### Hypotheses

The experiment uses a two-sided hypothesis test:

- **Null hypothesis (H₀):** There is no difference in mean reaction time between the music and silence conditions.
- **Alternative hypothesis (H₁):** There is a difference in mean reaction time between the music and silence conditions.

The significance level is set at α = 0.05.

## Repository Structure

```text
reaction-time-experiment/
├── data/
│   ├── raw/
│   │   └── reaction_time_data.csv
│   └── cleaned/
│       ├── reaction_time_cleaned.csv
│       └── participant_averages.csv
├── figures/
│   ├── reaction_time_distributions.png
│   ├── participant_comparison.png
│   ├── paired_comparison.png
│   ├── mean_difference.png
│   ├── statistical_difference_distribution.png
│   └── paired_difference_qq_plot.png
├── report/
│   ├── report.pdf
├── scripts/
│   ├── data_cleaning.py
│   ├── exploratory_analysis.py
│   ├── statistical_analysis.py
│   └── power_analysis.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Dataset

The raw dataset is stored in `data/raw/reaction_time_data.csv`.

Each row represents one reaction-time trial and contains the following columns:

| Column | Description |
|---|---|
| `participant_id` | Unique participant identifier |
| `condition` | Experimental condition (`silence` or `music`) |
| `order` | Condition sequence (1 = silence first, 2 = music first) |
| `trial` | Trial number within each condition |
| `reaction_time_ms` | Measured reaction time in milliseconds |

The cleaned dataset and participant-level averages are saved in `data/cleaned/`.

## Statistical Methodology

### Power Analysis

An a priori power analysis was conducted using a paired-samples t-test. The analysis used the following assumptions:

- Significance level: 0.05
- Desired statistical power: 80%
- Assumed effect size (Cohen's dz): 0.50
- Minimum required sample size: 34 participants
- Planned sample size: 40 participants

With 40 participants, the estimated statistical power was approximately 86.9%.

### Data Cleaning

The `data_cleaning.py` script prepares the raw dataset for analysis. It:

- Checks that all required columns are present.
- Cleans column values and converts variables to appropriate data types.
- Checks for missing values, invalid reaction times, and unexpected condition labels.
- Verifies participant and trial counts.
- Checks for duplicate observations and inconsistent condition orders.
- Creates a cleaned trial-level dataset.
- Calculates each participant's average reaction time under both conditions and the paired difference between them.

### Exploratory Data Analysis

The `exploratory_analysis.py` script calculates descriptive statistics and generates visualizations to examine reaction-time distributions and differences between conditions.

The visualizations include:

- Reaction-time distributions by condition.
- Participant-level comparisons.
- Paired comparisons between silence and music.
- Distribution of mean differences.

### Statistical Analysis

The `statistical_analysis.py` script performs the primary statistical analysis using participant-level averages.

The analysis includes:

- A paired-samples t-test to compare mean reaction times between conditions.
- A 95% confidence interval for the mean paired difference.
- Cohen's dz to measure effect size.
- A Shapiro-Wilk test to assess the normality of paired differences.
- A Wilcoxon signed-rank test as a sensitivity analysis.
- An exploratory analysis examining whether experimental order influenced the observed differences.

The paired difference is calculated as:

**Music mean reaction time − Silence mean reaction time**

A positive difference indicates slower reaction times during the music condition.

## Results

The analysis of 40 participants produced the following results:

| Statistic | Silence | Music |
|---|---:|---:|
| Mean reaction time | 257.71 ms | 265.24 ms |
| Standard deviation | 29.58 ms | 31.46 ms |

The average paired difference was **7.53 ms**, indicating that participants responded more slowly while listening to music.

The paired-samples t-test produced:

- t-statistic: 2.9687
- Degrees of freedom: 39
- p-value: 0.005093
- 95% confidence interval: [2.40, 12.66] ms
- Cohen's dz: 0.4694

Because the p-value is below 0.05, the null hypothesis was rejected. The results indicate a statistically significant difference in reaction time between the two conditions.

The Wilcoxon signed-rank sensitivity analysis also supported this finding (p = 0.006096).

### Experimental Order Analysis

An exploratory Welch independent-samples t-test compared the paired differences between participants who completed silence first and those who completed music first.

| Experimental order | Mean paired difference |
|---|---:|
| Silence first | 2.73 ms |
| Music first | 12.33 ms |

The test produced a p-value of 0.057546. This result was not statistically significant at the 0.05 level, although the difference between the group averages suggests that experimental order may have influenced the observed effect.

## Limitations

Several limitations should be considered when interpreting the results:

- The experiment includes 40 participants, which limits the extent to which the findings can be generalized to larger populations.
- Reaction time can be influenced by factors such as attention, fatigue, familiarity with the task, and individual differences.
- The exploratory order analysis suggests possible sequence-related variation that should be investigated further.
- The experiment examines one particular reaction-time task and music condition. The findings should not automatically be generalized to other types of music, tasks, or listening environments.

## Conclusion

The results suggest that background instrumental music was associated with slower visual reaction times compared with silence in this experiment. Participants responded an average of 7.53 milliseconds slower in the music condition, and the difference was statistically significant.

Although the primary analysis supports a difference between conditions, the exploratory order analysis suggests that experimental sequence may be worth investigating in future studies.

## Installation and Reproducibility

### Requirements

The project uses Python and the following libraries:

- pandas
- numpy
- scipy
- matplotlib
- seaborn
- statsmodels

### Setup

Clone the repository:

```bash
git clone <repository-url>
cd aipi510-mod2-project
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On MacOS, activate the environment with:

```bash
source venv\bin\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Analysis

Run the scripts from the project root directory in the following order:

```bash
python scripts/power_analysis.py
python scripts/data_cleaning.py
python scripts/exploratory_analysis.py
python scripts/statistical_analysis.py
```

The scripts generate cleaned datasets, descriptive statistics, statistical test results, and visualizations in the corresponding project directories.

## Tools and Technologies

- **Python:** Primary programming language.
- **pandas:** Data manipulation and cleaning.
- **NumPy:** Numerical operations.
- **SciPy:** Statistical hypothesis testing.
- **Statsmodels:** Power analysis.
- **Matplotlib and Seaborn:** Data visualization.

---

**Project:** Module Project 2: Statistical Analysis  
**Research Topic:** Effects of Background Instrumental Music on Human Visual Reaction Time

*AI Tool Declaration: ChatGPT Codex was used to format this README*