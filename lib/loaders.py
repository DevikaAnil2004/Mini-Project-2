"""Cached loaders for the model and dataset files.

Each request used to construct a fresh predictor/assistant, and every
construction re-read a joblib model or CSV from disk — the dominant cost of an
otherwise trivial API call. These loaders read each artefact once per process.
"""

import os
from functools import lru_cache

import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _path(*parts):
    """Resolve against the project root so the working directory is irrelevant."""
    return os.path.join(BASE_DIR, *parts)


@lru_cache(maxsize=None)
def load_model(name):
    """Return a joblib model from models/, or None when it is missing."""
    try:
        return joblib.load(_path('models', name))
    except Exception:
        return None


@lru_cache(maxsize=None)
def load_dataset(name):
    """Return a DataFrame from data/, or None when it is missing.

    Treat the result as read-only: every caller shares this one object.
    """
    try:
        return pd.read_csv(_path('data', name))
    except Exception:
        return None
