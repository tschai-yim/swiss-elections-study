import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm


def kish_effective_sample_size(weights: pd.Series, clusters: pd.Series = None) -> float:
    """
    Calculates Kish's effective sample size (ESS).

    If clusters are provided, this assumes perfect intra-cluster correlation (unmodified duplications).

    Args:
        weights: A pandas Series of weights for each observation.
        clusters: An optional pandas Series with cluster IDs for each observation.

    Returns:
        The effective sample size.
    """
    if clusters is not None:
        weights = weights.groupby(clusters).sum()
    weights_square = weights.pow(2).sum()
    return np.nan if weights_square == 0 else (weights.sum() ** 2) / weights_square


def infinite_population_sample_size(
        confidence=0.95, margin_error=0.05,
        population_proportion=0.5,
) -> float:
    """ Calculate the required sample size for an infinite population. """
    if not (0 < confidence < 1 and 0 < margin_error < 1 and 0 <= population_proportion <= 1):
        raise ValueError("Invalid inputs for sample size calculation.")
    zscore_confidence = stats.norm.ppf((1 + confidence) / 2)
    return (zscore_confidence ** 2) * population_proportion * (1 - population_proportion) / (margin_error ** 2)


def finite_population_sample_size(
        population_size: float,
        confidence: float = 0.95,
        margin_error: float = 0.05,
        population_proportion: float = 0.5,
) -> float:
    """ Calculate the required sample size for a finite population. """
    if population_size <= 0:
        raise ValueError("Population size must be positive.")
    infinite_sample_size = infinite_population_sample_size(confidence, margin_error, population_proportion)
    return infinite_sample_size / (1 + (infinite_sample_size - 1) / population_size)


def finite_population_correction(
        infinite_moe: float,
        sample_size: float,
        population_size: float,
) -> float:
    """Apply Finite Population Correction (FPC) to a pre-calculated infinite margin of error."""
    if sample_size > population_size:
        raise ValueError(f'Sample size {sample_size} cannot be greater than population size {population_size}.')
    if sample_size == population_size:
        return 0.0
    fpc_factor = np.sqrt((population_size - sample_size) / (population_size - 1))
    return infinite_moe * fpc_factor if not pd.isna(fpc_factor) else infinite_moe


def infinite_classical_error_margin(
        sample_size: float,
        confidence=0.95,
        population_proportion=0.5,
) -> float:
    """ Calculate the margin of error for a infinite population. """
    if not sample_size > 0:
        return np.nan
    if not (0 < confidence < 1 and 0 <= population_proportion <= 1):
        raise ValueError("Invalid confidence or proportion.")
    zscore_confidence = stats.norm.ppf((1 + confidence) / 2)
    return zscore_confidence * np.sqrt(population_proportion * (1 - population_proportion) / sample_size)


def finite_classical_error_margin(
        sample_size: float,
        population_size: float,
        confidence=0.95,
        population_proportion=0.5,
) -> float:
    """ Calculate the margin of error for a finite population. """
    return finite_population_correction(
        infinite_classical_error_margin(
            sample_size, confidence, population_proportion
        ),
        sample_size, population_size
    )


def _robust_standard_error(
        metric: pd.Series, weights: pd.Series, clusters: pd.Series = None
) -> float:
    """ Calculate robust or cluster-robust standard error for a 0/1 metric using WLS."""
    if weights.sum() == 0:
        return np.nan
    if len(metric) != len(weights):
        raise ValueError(f"Length mismatch: metric {len(metric)} and weights {len(weights)}")
    if clusters is not None and len(clusters) != len(metric):
        raise ValueError(f"Length mismatch: metric {len(metric)} and clusters {len(clusters)}")

    # Drop any NaNs by removing the entry from all series.
    model_data = {'metric': metric.astype(float), 'weights': weights.astype(float)}
    if clusters is not None:
        model_data['clusters'] = clusters
    model_df = pd.DataFrame(model_data).dropna()
    if model_df['weights'].sum() == 0:
        return np.nan

    x = pd.DataFrame({'intercept': np.ones(len(model_df))}, index=model_df.index)
    wls = sm.WLS(model_df['metric'], x, weights=model_df['weights'])
    res = wls.fit()
    if res.df_resid <= 0:
        return np.nan
    robust_res = (
        res.get_robustcov_results(cov_type='HC1')
        if clusters is None else
        res.get_robustcov_results(cov_type='cluster', groups=model_df['clusters'])
    )
    return robust_res.bse[0] if isinstance(robust_res.bse, (np.ndarray, list)) else \
        robust_res.bse.get('intercept', np.nan)


def infinite_weighted_error_margin(
        metric: pd.Series, weights: pd.Series,
        clusters: pd.Series = None,
        confidence=0.95,
) -> float:
    """ Calculate the margin of error for a weighted sample, with optional clustering. """
    if not 0 < confidence < 1:
        raise ValueError("Invalid confidence.")
    standard_error = _robust_standard_error(metric, weights, clusters)
    zscore = stats.norm.ppf((1 + confidence) / 2)
    return zscore * standard_error


def finite_weighted_error_margin(
        metric: pd.Series, weights: pd.Series,
        population_size: float,
        clusters: pd.Series = None,
        confidence=0.95,
) -> float:
    """
    Calculate the margin of error for a weighted sample of a finite population,
    with optional clustering.

    If clusters are provided, this assumes perfect intra-cluster correlation (unmodified duplications)
    for the effective sample size. Will underestimate the sample size if this assumption is broken.
    """
    if population_size <= 0:
        raise ValueError("Population size must be positive.")
    infinite_moe = infinite_weighted_error_margin(metric, weights, clusters, confidence)
    sample_size = kish_effective_sample_size(weights, clusters)
    return finite_population_correction(infinite_moe, sample_size, population_size)


def propagate_error_for_weighted_mean(weights: pd.Series, error_margins: pd.Series) -> float:
    """ Calculate the propagated error for a weighted mean. """
    return np.sqrt((((weights / weights.sum()) ** 2) * (error_margins ** 2)).sum())
