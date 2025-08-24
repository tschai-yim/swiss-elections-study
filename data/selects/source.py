import functools

import numpy as np
import pandas as pd

from data.attribute import YEAR_ATTR, SEX_ATTR, AGE_ATTR, COMMUNE_SIZE_ATTR, SEX_MALE, SEX_FEMALE
from data.location import load_cantons_metadata, CANTON_ATTR

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


@functools.cache
def get_fors_selects() -> pd.DataFrame:
    cantons_metadata = load_cantons_metadata()
    canton_map = cantons_metadata.set_index(cantons_metadata.cantonAbbreviation.str.lower())[CANTON_ATTR]
    processors = {
        'sex': lambda x: x.map({
            'male': SEX_MALE,
            'female': SEX_FEMALE
        }),
        'age': lambda x: x.astype(np.float16).clip(-1, 100).fillna(-1),
        'sg3': lambda x: x.map(canton_map).astype(CANTON_ATTR.type),
        'sg4': lambda x: x.map(canton_map).astype(CANTON_ATTR.type),
        'sg2': lambda x: x.map(canton_map).astype(CANTON_ATTR.type),
        'sg7b': lambda x: x.map(SG7B_TO_COMMUNE_SIZE_MAPPER),
    }

    df = pd.read_stata('data_raw/fors_selects_1971_2019/495_Selects_CumulativeFile_Data_1971-2019_v2.3.0.dta')

    for name, attribute in _SELECTS_TO_ATTR_MAPPER.items():
        processor = processors.get(name, lambda x: x)
        df[name] = attribute.convert(processor(df[name]))
    for name, processor in processors.items():
        if name in _SELECTS_TO_ATTR_MAPPER:
            continue
        df[name] = processor(df[name])

    return df.rename(_SELECTS_TO_ATTR_MAPPER, axis=1)
