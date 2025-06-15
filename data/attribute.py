from dataclasses import dataclass

import numpy as np
import pandas as pd

ATTR_TO_CACHE_MAPPER = {}
CACHE_TO_ATTR_MAPPER = {}


@dataclass(frozen=True)
class Attribute:
    id: str
    name: str
    type: np.typing.DTypeLike
    description: str

    def __post_init__(self):
        if self.id in ATTR_TO_CACHE_MAPPER:
            raise ValueError(f"Attribute ID '{self.id}' is already defined.")
        ATTR_TO_CACHE_MAPPER[self] = self.id
        CACHE_TO_ATTR_MAPPER[self.id] = self

    def convert(self, value: pd.Series) -> pd.Series:
        return value.astype(self.type).rename(self)

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class CategoricalAttribute(Attribute):
    categories: tuple
    ordered: bool = False

    def convert(self, value: pd.Series) -> pd.Series:
        return pd.Series(
            pd.Categorical(value, categories=self.categories, ordered=self.ordered),
            name=self
        )


YEAR_ATTR = Attribute('year', 'Year', np.uint16, 'Year the record is about')

# Demographic attributes
IS_PERMANENT_RESIDENT_ATTR = Attribute(
    'is_permanent_resident', 'Is Permanent Resident', np.bool,
    'If swiss citizen or stay permit > 12 months ' +
    '(https://www.bfs.admin.ch/asset/de/26867302, https://www.bfs.admin.ch/asset/de/5928373)'
)
IS_CITIZEN_ATTR = Attribute('is_citizen', 'Is Citizen', np.bool, 'If swiss citizen')
AGE_ATTR = Attribute(
    'age', 'Age', np.int8,
    'Age in whole years (-1 = Unknown, 100 = 100 years or older, sometimes approximate)'
)

SEX_MALE = 'Male'
SEX_FEMALE = 'Female'
SEX_ATTR = CategoricalAttribute(
    'sex', 'Sex', 'category', 'Legal sex',
    categories=(SEX_MALE, SEX_FEMALE)
)

# From sg7b feature from fors_selects_1971_2019
COMMUNE_SIZES = (
    '1-999',
    '1\'000-1\'999',
    '2\'000-4\'999',
    '5\'000-9\'999',
    '10\'000-19\'999',
    '20\'000-49\'999',
    '50\'000-99\'999',
    '> 100\'000'
)
COMMUNE_SIZE_ATTR = CategoricalAttribute(
    'commune_size', 'Commune Size', 'category', 'Size category of the commune',
    categories=COMMUNE_SIZES,
    ordered=True
)

# BFS Population
POPULATION_ATTR = Attribute('population', 'Population', np.uint32,
                            'Number of residents at the end of the year (https://www.bfs.admin.ch/asset/de/26857466)')
