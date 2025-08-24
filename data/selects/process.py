import numpy as np
import pandas as pd

from data.attribute import SEX_ATTR, AGE_ATTR, POPULATION_ATTR
from data.location import CANTON_ATTR
from data.selects.columns import TOTAL_WEIGHT, AGE_WEIGHT
from data.weights import rake_survey_weights, create_marginal_corrector


def spread_age(
        df: pd.DataFrame,
        age_std: float = 3.0,
        min_age: int = 18,
        max_age: int = 100,
        kernel_size_std: float = 4,
) -> pd.DataFrame:
    """
    Spread every respondent to multiple ages and weight using a Gaussian kernel.
    """
    # Offsets and raw Gaussian weights for candidates.
    kernel_radius = int(np.ceil(kernel_size_std * age_std))
    offsets = np.arange(-kernel_radius, kernel_radius + 1)
    kernel = np.exp(-0.5 * (offsets / age_std) ** 2)

    # Create candidate ages and corresponding weights.
    candidate_ages = df[AGE_ATTR].values[:, None] + offsets  # shape: (n, n_offsets)
    candidate_weights = np.tile(kernel, (len(df), 1))

    # Duplicate the DataFrame for each offset.
    duplicated_df = df.loc[df.index.repeat(len(offsets))].copy()
    duplicated_df[AGE_ATTR] = candidate_ages.flatten()
    duplicated_df[AGE_WEIGHT] = candidate_weights.flatten()

    # Keep only candidates within the allowed age range.
    valid = (duplicated_df[AGE_ATTR] >= min_age) & (duplicated_df[AGE_ATTR] <= max_age)
    duplicated_df = duplicated_df[valid].copy().reset_index(drop=True)

    # Normalize and update weights
    duplicated_df[AGE_WEIGHT] /= duplicated_df[AGE_WEIGHT].mean()
    duplicated_df[TOTAL_WEIGHT] = duplicated_df[TOTAL_WEIGHT] * duplicated_df[AGE_WEIGHT]
    return duplicated_df


def correct_selects_year_weights(
        selects_df: pd.DataFrame,
        electorate_df: pd.DataFrame,
        acceptable_correction: float = 5.0,
        external_weights: pd.Series = None,
) -> pd.DataFrame:
    """
    Correct the demographic distribution of a selects survey dataframe to match
    the distribution in the electorate.

    Args:
        selects_df: The selects dataframe
        electorate_df: The electorate dataframe
        acceptable_correction: Maximum allowed over- or under-weighting for correction
        external_weights: Optional Series of external weights to incorporate

    Returns:
        DataFrame with corrected demographic weights
    """
    raked_weights = rake_survey_weights(
        sample_df=selects_df,
        raking_functions=[
            create_marginal_corrector(
                sample_col=AGE_ATTR,
                population_df=electorate_df,
                pop_col=AGE_ATTR,
                pop_weight_col=POPULATION_ATTR
            ),
            create_marginal_corrector(
                sample_col=SEX_ATTR,
                population_df=electorate_df,
                pop_col=SEX_ATTR,
                pop_weight_col=POPULATION_ATTR
            ),
            create_marginal_corrector(
                sample_col='sg3',
                population_df=electorate_df,
                pop_col=CANTON_ATTR,
                pop_weight_col=POPULATION_ATTR
            ),
            # TODO: add participation rate and party correction
        ],
        iterations=1000,
        clip_range=(1 / acceptable_correction, acceptable_correction),
        external_weights=external_weights,
    )

    selects_df = selects_df.copy()
    selects_df[TOTAL_WEIGHT] = raked_weights if external_weights is None else external_weights * raked_weights
    return selects_df


def post_process_selects(
        selects_df: pd.DataFrame,
        electorate_df: pd.DataFrame,
        acceptable_correction: float = 5.0,
        age_std: float = 3.0,
) -> pd.DataFrame:
    """
    Post-process the selects dataframe by spreading ages and correcting weights.

    Args:
        selects_df: The selects dataframe
        electorate_df: The electorate dataframe
        acceptable_correction: Maximum allowed over- or under-weighting for correction
        age_std: Standard deviation for age spreading

    Returns:
        DataFrame with processed demographic weights
    """
    selects_df = spread_age(selects_df, age_std=age_std)
    selects_df = correct_selects_year_weights(
        selects_df=selects_df,
        electorate_df=electorate_df,
        acceptable_correction=acceptable_correction,
        external_weights=selects_df[TOTAL_WEIGHT]
    )
    return selects_df
