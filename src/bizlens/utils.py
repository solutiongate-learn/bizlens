"""
BizLens Shared Utilities v2.3.2
Central helper functions to avoid code duplication.
"""

import pandas as pd
import numpy as np

try:
    import polars as pl
except ImportError:
    pl = None


def to_pandas(data):
    """Convert any input (pandas, polars, list, numpy) to pandas DataFrame/Series."""
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, pd.Series):
        return data
    elif pl and isinstance(data, pl.DataFrame):
        return data.to_pandas()
    elif pl and isinstance(data, pl.Series):
        return data.to_pandas()
    elif isinstance(data, (list, np.ndarray)):
        return pd.Series(data)
    else:
        try:
            return pd.DataFrame(data)
        except Exception:
            raise TypeError(f"BizLens: Unsupported data type: {type(data)}")


def get_numeric_columns(df):
    """Return list of numeric columns."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_categorical_columns(df):
    """Return list of categorical columns."""
    return df.select_dtypes(include=['object', 'category']).columns.tolist()