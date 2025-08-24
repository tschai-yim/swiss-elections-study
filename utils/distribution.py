import numpy as np
import pandas as pd


def merge_proportional(distribution: pd.Series, *distributions: tuple[pd.Series, ...]) -> pd.DataFrame:
    """
    Merge multiple distributions into a DataFrame, normalizing each to sum to 1.
    """
    distributions = [distribution] + list(distributions)
    # Ensure all series have a name for the concat keys
    named_distributions = []
    for i, d in enumerate(distributions):
        if d.name is None:
            d.name = f'dist_{i}'
        named_distributions.append(d)
    return pd.concat([d / d.sum() for d in named_distributions if d.sum() > 0], axis=1)


def total_variance_distance(distribution1: pd.Series, distribution2: pd.Series) -> float:
    """
    Calculate Total Variation Distance between two distributions.
    """
    if distribution1.sum() == 0 or distribution2.sum() == 0:
        return np.nan
    return 0.5 * (distribution1 / distribution1.sum() - distribution2 / distribution2.sum()).abs().sum()


def column_total_variance_distance(distribution: pd.DataFrame, reference: str) -> pd.Series:
    """
    Calculate Total Variation Distance between each column and a reference column.
    """
    if reference not in distribution.columns or distribution[reference].sum() == 0:
        return pd.Series({col: np.nan for col in distribution.columns if col != reference})
    return pd.Series({
        column: total_variance_distance(distribution[column], distribution[reference])
        for column in distribution.columns if column != reference
    })
