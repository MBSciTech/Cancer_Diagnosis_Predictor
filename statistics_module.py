import numpy as np

def chi_square_test(observed, expected):
    if len(observed) != len(expected):
        raise ValueError("Observed and Expected lists must be the same length.")

    chi_square_value = sum(((o - e) ** 2) / e for o, e in zip(observed, expected))
    return chi_square_value

def t_test(group1, group2):
    mean1, mean2 = np.mean(group1), np.mean(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    n1, n2 = len(group1), len(group2)

    t_statistic = (mean1 - mean2) / np.sqrt((var1 / n1) + (var2 / n2))
    return t_statistic

def calculate_regression(x_values, y_values):
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length.")

    x_mean, y_mean = np.mean(x_values), np.mean(y_values)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
    denominator = sum((x - x_mean) ** 2 for x in x_values)

    slope = numerator / denominator
    intercept = y_mean - slope * x_mean

    return slope, intercept
