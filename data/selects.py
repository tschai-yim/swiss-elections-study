import functools

import numpy as np
import pandas as pd

from data.attribute import YEAR_ATTR, SEX_ATTR, AGE_ATTR, SEX_UNKNOWN, SEX_MALE, SEX_FEMALE, COMMUNE_SIZE_ATTR, \
    COMMUNE_SIZE_UNKNOWN

SG7B_TO_COMMUNE_SIZE_MAPPER = {
    '-999': 0,
    '1\'000-1\'999': 1,
    '2\'000-4\'999': 2,
    '5\'000-9\'999': 3,
    '10\'000-19\'999': 4,
    '20\'000-49\'999': 5,
    '50\'000-99\'999': 6,
    '> 100\'000 inhab.': 7,
}

_SELECTS_TO_ATTR_MAPPER = {
    'year': YEAR_ATTR,
    'sex': SEX_ATTR,
    'age': AGE_ATTR,
    'sg7b': COMMUNE_SIZE_ATTR
}
_SELECTS_PROCESSORS = {
    'sex': lambda x: x.map({
        'nan': SEX_UNKNOWN,
        'male': SEX_MALE,
        'female': SEX_FEMALE
    }).astype(np.float16).fillna(SEX_UNKNOWN),
    'age': lambda x: x.astype(np.float16).clip(-1, 100).fillna(-1),
    'sg7b': lambda x: x.map(SG7B_TO_COMMUNE_SIZE_MAPPER).astype(np.float16).fillna(COMMUNE_SIZE_UNKNOWN)
}


@functools.cache
def get_fors_selects() -> pd.DataFrame:
    df = pd.read_stata('data_raw/fors_selects_1971_2019/495_Selects_CumulativeFile_Data_1971-2019_v2.3.0.dta')
    for name, attribute in _SELECTS_TO_ATTR_MAPPER.items():
        processor = _SELECTS_PROCESSORS.get(name, lambda x: x)
        df[name] = attribute.convert(processor(df[name]))
    return df.rename(_SELECTS_TO_ATTR_MAPPER, axis=1)
