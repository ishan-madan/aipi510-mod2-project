
from statsmodels.stats.power import TTestPower

# define power analysis assumptions
alpha = 0.05
desired_power = 0.80
effect_size = 0.50
planned_sample_size = 40

# calculate required sample size
power_analysis = TTestPower()

required_sample_size = power_analysis.solve_power(
    effect_size=effect_size,
    power=desired_power,
    alpha=alpha,
    alternative="two-sided",
)

# calculate achieved power with planned sample size
achieved_power = power_analysis.power(
    effect_size=effect_size,
    nobs=planned_sample_size,
    alpha=alpha,
    alternative="two-sided",
)

# print results
print("POWER ANALYSIS")
print("--------------")
print("Test: Paired-samples t-test")
print(f"Significance level: {alpha}")
print(f"Desired statistical power: {desired_power:.0%}")
print(f"Assumed effect size (Cohen's dz): {effect_size}")
print(f"Required sample size: {int(required_sample_size) + 1} participants")
print(f"Planned sample size: {planned_sample_size} participants")
print(f"Achieved power: {achieved_power:.4f} ({achieved_power:.1%})")
