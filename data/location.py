import functools
from datetime import datetime

import numpy as np
import pandas as pd

from data.attribute import Attribute

# Administrative region codes defined by https://www.agvchapp.bfs.admin.ch/
# as specified by https://www.ech.ch/de/ech/ech-0071/1.2.0
CANTON_ATTR = Attribute(
    'canton', 'Canton', 'Int64',
    'BFS canton code'
)
COMMUNE_ATTR = Attribute(
    'commune', 'Commune', 'Int64',
    'BFS commune code'
)


@functools.cache
def load_cantons_metadata() -> pd.DataFrame:
    return pd.read_csv(
        'data_raw/bfs_historical_commune_registry/dz-b-00.04-hgv-01/1.2.0/20250406_GDEHist_KT.txt',
        sep='\t',
        encoding='latin_1',
        names=[
            CANTON_ATTR,
            'cantonAbbreviation',
            'cantonLongName',
            'cantonDateOfChange',
        ],
        parse_dates=['cantonDateOfChange'],
        date_format='%d.%m.%Y'
    )


@functools.cache
def load_communes_metadata() -> pd.DataFrame:
    return pd.read_csv(
        'data_raw/bfs_historical_commune_registry/dz-b-00.04-hgv-01/1.2.0/20250406_GDEHist_GDE.txt',
        sep='\t',
        encoding='latin_1',
        names=[
            'historyMunicipalityId',
            'districtHistId',
            'cantonAbbreviation',
            COMMUNE_ATTR,
            'municipalityLongName',
            'municipalityShortName',
            'municipalityEntryMode',
            'municipalityStatus',
            'municipalityAdmissionNumber',
            'municipalityAdmissionMode',
            'municipalityAdmissionDate',
            'municipalityAbolitionNumber',
            'municipalityAbolitionMode',
            'municipalityAbolitionDate',
            'municipalityDateOfChange',
        ],
        parse_dates=[
            'municipalityAdmissionDate',
            'municipalityAbolitionDate',
            'municipalityDateOfChange'
        ],
        date_format='%d.%m.%Y'
    )


def load_communes_metadata_year(year: int) -> pd.DataFrame:
    """Load communes metadata for the start of a specific year."""
    date = datetime(year, 1, 1)
    df = load_communes_metadata()
    df = df[df['municipalityAdmissionDate'] <= date]
    df = df[df['municipalityAbolitionDate'].isna() | (date < df['municipalityAbolitionDate'])]
    return df.reset_index(drop=True)
