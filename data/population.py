import functools
from typing import cast

import numpy as np
import pandas as pd
from pyaxis import pyaxis

from data.attribute import CACHE_TO_ATTR_MAPPER, ATTR_TO_CACHE_MAPPER, YEAR_ATTR, COMMUNE_ATTR, \
    IS_PERMANENT_RESIDENT_ATTR, IS_CITIZEN_ATTR, SEX_ATTR, AGE_ATTR, POPULATION_ATTR, COMMUNE_SIZE_UNKNOWN
from data.cache import POPULATION_CACHE


def _load_raw_bfs_population_cga():
    # Slow to load
    raw_df = pyaxis.parse(
        'data_raw/bfs_population_commune_gender_age_2010_2023.px',
        encoding='ISO-8859-15', lang='en'
    )['DATA']
    # Filter out cumulative rows
    raw_df = raw_df[
        (raw_df['Canton (-) / District (>>) / Commune (......)'].str.startswith('......')) &
        (raw_df['Citizenship (category)'] != 'Citizenship (category) - total') &
        (raw_df['Sex'] != 'Sex - total') &
        (raw_df['Age'] != 'Age - total')
        ].reset_index(drop=True)
    # Convert to correct types
    return pd.concat((
        YEAR_ATTR.convert(raw_df['Year']),
        COMMUNE_ATTR.convert(raw_df['Canton (-) / District (>>) / Commune (......)'].str.slice(6, 10)),
        IS_PERMANENT_RESIDENT_ATTR.convert(
            cast(pd.Series, raw_df['Population type'] == 'Permanent resident population')
        ),
        IS_CITIZEN_ATTR.convert(cast(pd.Series, raw_df['Citizenship (category)'] == 'Switzerland')),
        SEX_ATTR.convert(cast(pd.Series, raw_df['Sex'] == 'Female')),
        AGE_ATTR.convert(raw_df['Age'].str.split(' ', n=1).str[0]),
        POPULATION_ATTR.convert(raw_df['DATA'])
    ), axis=1)


@functools.cache
def get_bfs_population_cga() -> pd.DataFrame:
    cache_file = POPULATION_CACHE.dir().joinpath('population_cga.feather')
    if cache_file.exists():
        return pd.read_feather(cache_file).rename(CACHE_TO_ATTR_MAPPER, axis=1)
    df = _load_raw_bfs_population_cga()
    df.rename(ATTR_TO_CACHE_MAPPER, axis=1).to_feather(cache_file)
    return df


def _population_to_commune_size(population: np.number) -> int:
    if np.isnan(population):
        return COMMUNE_SIZE_UNKNOWN
    if population > 100000:
        return 7
    if population > 50000:
        return 6
    if population > 20000:
        return 5
    if population > 10000:
        return 4
    if population > 5000:
        return 3
    if population > 2000:
        return 2
    if population > 1000:
        return 1
    return 0


@functools.cache
def get_commune_to_size_map(year: int) -> pd.Series:
    population = get_bfs_population_cga()
    return population[population[YEAR_ATTR] == year] \
        .groupby(COMMUNE_ATTR)[POPULATION_ATTR].sum() \
        .map(_population_to_commune_size)
