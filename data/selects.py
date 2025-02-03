import functools

import numpy as np
import pandas as pd

from data.attribute import YEAR_ATTR, SEX_ATTR, AGE_ATTR, SEX_UNKNOWN, SEX_MALE, SEX_FEMALE

_SELECTS_TO_ATTR_MAPPER = {
    'year': YEAR_ATTR,
    'sex': SEX_ATTR,
    'age': AGE_ATTR
}
_SELECTS_PROCESSORS = {
    'sex': lambda x: x.map({
        'nan': SEX_UNKNOWN,
        'male': SEX_MALE,
        'female': SEX_FEMALE
    }).astype(np.float16).fillna(SEX_UNKNOWN),
    'age': lambda x: x.astype(np.float16).clip(-1, 100).fillna(-1),
}


@functools.cache
def get_fors_selects() -> pd.DataFrame:
    df = pd.read_stata('data_raw/fors_selects_1971_2019/495_Selects_CumulativeFile_Data_1971-2019_v2.3.0.dta')
    for name, attribute in _SELECTS_TO_ATTR_MAPPER.items():
        processor = _SELECTS_PROCESSORS.get(name, lambda x: x)
        df[name] = attribute.convert(processor(df[name]))
    return df.rename(_SELECTS_TO_ATTR_MAPPER, axis=1)
