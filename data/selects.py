import functools

import numpy as np
import pandas as pd

from data.attribute import YEAR_ATTR, SEX_ATTR, AGE_ATTR, SEX_MALE, SEX_FEMALE, COMMUNE_SIZE_ATTR, \
    POPULATION_ATTR

AGE_WEIGHT = 'weight_age'
DEMOGRAPHIC_WEIGHT = 'weight_demographic'

SG7B_TO_COMMUNE_SIZE_MAPPER = {
    '-999': '1-999',
    '1\'000-1\'999': '1\'000-1\'999',
    '2\'000-4\'999': '2\'000-4\'999',
    '5\'000-9\'999': '5\'000-9\'999',
    '10\'000-19\'999': '10\'000-19\'999',
    '20\'000-49\'999': '20\'000-49\'999',
    '50\'000-99\'999': '50\'000-99\'999',
    '> 100\'000 inhab.': '> 100\'000',
}

_SELECTS_TO_ATTR_MAPPER = {
    'year': YEAR_ATTR,
    'sex': SEX_ATTR,
    'age': AGE_ATTR,
    'sg7b': COMMUNE_SIZE_ATTR
}
_SELECTS_PROCESSORS = {
    'sex': lambda x: x.map({
        'male': SEX_MALE,
        'female': SEX_FEMALE
    }),
    'age': lambda x: x.astype(np.float16).clip(-1, 100).fillna(-1),
    'sg7b': lambda x: x.map(SG7B_TO_COMMUNE_SIZE_MAPPER)
}


@functools.cache
def get_fors_selects() -> pd.DataFrame:
    df = pd.read_stata('data_raw/fors_selects_1971_2019/495_Selects_CumulativeFile_Data_1971-2019_v2.3.0.dta')
    for name, attribute in _SELECTS_TO_ATTR_MAPPER.items():
        processor = _SELECTS_PROCESSORS.get(name, lambda x: x)
        df[name] = attribute.convert(processor(df[name]))
    return df.rename(_SELECTS_TO_ATTR_MAPPER, axis=1)


def apply_age_smoothing(
        df: pd.DataFrame,
        age_std: float = 2,
        min_age: int = 18,
        max_age: int = 100,
        ref_weight: str = 'weightc',
        kernel_size_std: float = 4,
) -> pd.DataFrame:
    """
    Smooth the age distribution in three steps:

    1. Build a target smoothed age histogram using `ref_weight`.
    2. Duplicate and spread each respondent to neighboring ages.
    3. Scale each age-bin to match the target smoothed histogram.

    All other weight columns are adjusted accordingly.
    """
    #
    kernel_radius = int(np.ceil(kernel_size_std * age_std))

    # --- Step 1: Target smoothed age histogram ---
    # Aggregate the reference weight by age.
    agg = df.groupby(AGE_ATTR)[ref_weight].sum()
    all_ages = np.arange(min_age, max_age + 1)
    agg = agg.reindex(all_ages, fill_value=0)

    # Use pandas' rolling with a Gaussian window to smooth the histogram.
    target_distribution = agg.rolling(
        window=2 * kernel_radius + 1,
        win_type='gaussian', center=True, min_periods=1
    ).mean(std=age_std)

    # --- Step 2: Duplicate respondents with candidate weights ---
    # Offsets and raw Gaussian weights for candidates.
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

    # --- Step 3: Scale candidate weights to match the target histogram ---
    # Total candidate weight per age bin.
    candidate_sum = (duplicated_df[ref_weight] * duplicated_df[AGE_WEIGHT]) \
        .groupby(duplicated_df[AGE_ATTR]).transform('sum')
    # Scale candidate age weight to match the target distribution.
    duplicated_df[AGE_WEIGHT] *= (duplicated_df[AGE_ATTR].map(target_distribution) / candidate_sum).fillna(0)

    # Update all weight columns.
    for col in ('weightc', 'weightst', 'weightp', 'weighttot'):
        duplicated_df[col] = duplicated_df[col] * duplicated_df[AGE_WEIGHT]
    return duplicated_df


def apply_demographic_correction(
        selects_df: pd.DataFrame,
        electorate_df: pd.DataFrame,
        acceptable_correction: float = 5.0,
        demographic_attributes: list = None,
        selects_weight: str = 'weightc',
) -> pd.DataFrame:
    """
    Correct the demographic distribution of a selects survey dataframe to match
    the distribution in the electorate.

    Args:
        selects_df: The selects dataframe
        electorate_df: The electorate dataframe
        acceptable_correction: Maximum allowed over- or under-weighting for correction
        demographic_attributes: Variables to use for demographic correction
        selects_weight: The weight used to calculate the demographic distribution

    Returns:
        DataFrame with corrected demographic weights
    """
    if demographic_attributes is None:
        demographic_attributes = [AGE_ATTR, SEX_ATTR, COMMUNE_SIZE_ATTR]

    # Calculate demographic distributions
    selects_demographics = selects_df.groupby(demographic_attributes, observed=True)[selects_weight] \
        .sum().rename('Selects')
    electorate_demographics = electorate_df.groupby(demographic_attributes, observed=True)[POPULATION_ATTR] \
        .sum().rename('Electorate')

    # Only use demographics present in both selects and electorate data
    demographic_proportions = pd.concat([
        selects_demographics / selects_demographics.sum(),
        electorate_demographics / electorate_demographics.sum()
    ], axis=1)
    demographic_proportions = demographic_proportions[
        (demographic_proportions['Selects'] > 0) &
        (demographic_proportions['Electorate'] > 0)
        ]
    demographic_proportions = demographic_proportions.div(demographic_proportions.sum(), axis=1)

    # Calculate correction multipliers
    correction_multiplier = (demographic_proportions['Electorate'] / demographic_proportions['Selects']) \
        .clip(upper=acceptable_correction, lower=1 / acceptable_correction)

    # Apply demographic correction to selects
    corrected_selects_df = selects_df.copy()
    corrected_selects_df[DEMOGRAPHIC_WEIGHT] = 0.0

    # Apply multipliers based on demographic variables
    for demographic_values, factor in correction_multiplier.items():
        if not isinstance(demographic_values, tuple):
            # If only one demographic variable is used, convert to tuple
            demographic_values = (demographic_values,)
        mask = pd.Series(True, index=corrected_selects_df.index)
        for value, var in zip(demographic_values, demographic_attributes):
            mask &= (corrected_selects_df[var] == value)
        corrected_selects_df.loc[mask, DEMOGRAPHIC_WEIGHT] = factor

    # Apply demographic weights to all weight columns
    for col in ('weightc', 'weightst', 'weightp', 'weighttot'):
        corrected_selects_df[col] *= corrected_selects_df[DEMOGRAPHIC_WEIGHT]

    return corrected_selects_df
