import functools
from typing import cast

import numpy as np
import pandas as pd
from pyaxis import pyaxis

from data.attribute import CACHE_TO_ATTR_MAPPER, ATTR_TO_CACHE_MAPPER, YEAR_ATTR, \
    IS_PERMANENT_RESIDENT_ATTR, IS_CITIZEN_ATTR, SEX_ATTR, AGE_ATTR, POPULATION_ATTR, \
    COMMUNE_SIZE_ATTR
from data.cache import POPULATION_CACHE
from data.location import COMMUNE_ATTR, CANTON_ATTR, load_cantons_metadata, \
    load_communes_metadata_year


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
        SEX_ATTR.convert(cast(pd.Series, raw_df['Sex'])),
        AGE_ATTR.convert(raw_df['Age'].str.split(' ', n=1).str[0]),
        POPULATION_ATTR.convert(raw_df['DATA'])
    ), axis=1)


def _population_to_commune_size(population: np.number) -> str | None:
    if np.isnan(population):
        return None
    if population > 100000:
        return '> 100\'000'
    if population > 50000:
        return '50\'000-99\'999'
    if population > 20000:
        return '20\'000-49\'999'
    if population > 10000:
        return '10\'000-19\'999'
    if population > 5000:
        return '5\'000-9\'999'
    if population > 2000:
        return '2\'000-4\'999'
    if population > 1000:
        return '1\'000-1\'999'
    return '1-999'


@functools.cache
def get_bfs_population_cga() -> pd.DataFrame:
    cache_file = POPULATION_CACHE.dir().joinpath('population_cga.feather')
    if cache_file.exists():
        df = pd.read_feather(cache_file).rename(CACHE_TO_ATTR_MAPPER, axis=1)
    else:
        df = _load_raw_bfs_population_cga()
        df.rename(ATTR_TO_CACHE_MAPPER, axis=1).to_feather(cache_file)
    df[COMMUNE_SIZE_ATTR] = df.groupby([YEAR_ATTR, COMMUNE_ATTR])[POPULATION_ATTR] \
        .transform(lambda x: _population_to_commune_size(x.sum()))
    df[CANTON_ATTR] = CANTON_ATTR.convert(
        # Groups using communes from 2023 no matter the statistic year
        df[COMMUNE_ATTR].map(load_communes_metadata_year(2023).set_index(COMMUNE_ATTR).cantonAbbreviation)
        .map(load_cantons_metadata().set_index('cantonAbbreviation')[CANTON_ATTR])
    )
    return df


def can_vote_mask(df: pd.DataFrame) -> pd.Series:
    return df[IS_CITIZEN_ATTR] & (df[AGE_ATTR] >= 18)


def get_electorate(df: pd.DataFrame) -> pd.DataFrame:
    return df[can_vote_mask(df)]
