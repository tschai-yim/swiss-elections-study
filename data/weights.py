import pandas as pd
import numpy as np
from typing import List, Callable, Tuple


def create_marginal_corrector(
        sample_col: str,
        population_df: pd.DataFrame,
        pop_col: str,
        pop_weight_col: str
) -> Callable[[pd.DataFrame, pd.Series], pd.Series]:
    """
    Factory to create a raking function for a standard marginal distribution.
    """
    pop_total = population_df[pop_weight_col].sum()
    target_dist = population_df.groupby(pop_col, observed=True)[pop_weight_col].sum()

    def corrector(df: pd.DataFrame, weights: pd.Series) -> pd.Series:
        current_dist = weights.groupby(df[sample_col], observed=True).sum()
        scaled_target = (target_dist / pop_total) * weights.sum()
        factors = scaled_target / current_dist
        return df[sample_col].map(factors).astype(float)

    return corrector


def create_rate_corrector(
        grouping_col: str,
        rate_col: str,
        target_rates: pd.Series
) -> Callable[[pd.DataFrame, pd.Series], pd.Series]:
    """
    Factory to create a raking function for correcting a weighted average (rate).
    """

    def corrector(df: pd.DataFrame, weights: pd.Series) -> pd.Series:
        current_rates = df.groupby(grouping_col, observed=True).apply(
            lambda x: np.average(x[rate_col], weights=weights.loc[x.index])
        )
        factors = target_rates / current_rates
        return df[grouping_col].map(factors).astype(float)

    return corrector


def rake_survey_weights(
        sample_df: pd.DataFrame,
        raking_functions: List[Callable[[pd.DataFrame, pd.Series], pd.Series]],
        iterations: int = 100,
        clip_range: Tuple[float, float] = (0.2, 5.0),
        external_weights: pd.Series = None,
        tolerance: float = 1e-7
) -> pd.Series:
    """
    Performs iterative weighting (raking) and returns the final weights.

    Includes an early exit if the mean of absolute weight changes between
    iterations falls below a specified tolerance.

    Args:
        sample_df: The DataFrame containing the survey sample data (read-only).
        raking_functions: A list of functions. Each function must accept a
            DataFrame and a weights Series and return correction factors.
        iterations: The maximum number of raking iterations to perform.
        clip_range: A tuple (min, max) for clipping the final weights.
        external_weights: Optional Series of external weights to consider
            while correcting. Meaning final weights must be multiplied by
            these external weights to get the final weights.
        tolerance: The convergence threshold. If the mean of absolute
            differences in weights between iterations is less than this
            value, the loop will terminate early.

    Returns:
        A pandas Series containing the final calculated weights, with the same
        index as `sample_df`.
    """
    # Initialize a local Series for weights, indexed identically to the sample DataFrame.
    weights = pd.Series(1.0, index=sample_df.index)

    for i in range(iterations):
        # Store a copy of the weights from the start of the iteration
        prev_weights = weights.copy()

        for corrector_func in raking_functions:
            # If constant weights are provided, apply them to the current weights.
            input_weights = weights if external_weights is None else external_weights * weights

            # Pass the original df (as read-only) and the current state of our local weights
            correction_factors = corrector_func(sample_df, input_weights)

            # Update the local weights Series
            weights *= correction_factors.fillna(1.0)

        # Clip and renormalize the weights
        weights = weights.clip(lower=clip_range[0], upper=clip_range[1])
        mean_weight = weights.mean()
        if mean_weight > 0:
            weights /= mean_weight

        # Maybe early exit
        change = (weights - prev_weights).abs().mean()
        if change < tolerance:
            break

    return weights
