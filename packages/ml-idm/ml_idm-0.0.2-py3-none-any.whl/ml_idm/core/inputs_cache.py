import typing as t
import json
import os

from ml_idm.core.cols_meta import ColMeta

INPUTS_CACHE_PATH = "inputs_cache.json"


class InputsCache:
    def __init__(self, cols_meta: t.List[ColMeta]):
        self._inputs_cache = {}

        if os.path.exists(INPUTS_CACHE_PATH):
            with open(INPUTS_CACHE_PATH, "r") as file:
                self._inputs_cache = json.load(file)

            col_names = [col.name for col in cols_meta]
            cached_col_names = self._inputs_cache.keys()
            cached_col_names_diff = set(cached_col_names).symmetric_difference(set(col_names))
            if len(cached_col_names_diff) != 0:
                self._inputs_cache = {}

        self._col_to_meta = dict([(col_meta.name, col_meta) for col_meta in cols_meta])

    def __getitem__(self, col_name):
        default_value = 0.0
        col_meta = self._col_to_meta[col_name]
        if col_meta.is_unknown:
            default_value = "0.0"
        elif col_meta.is_bin:
            default_value = 0
        elif col_meta.is_cat:
            default_value = "unknown"

        return self._inputs_cache.get(col_name, default_value)

    def __setitem__(self, col_name, col_value):
        self._inputs_cache[col_name] = col_value

    def save(self):
        with open(INPUTS_CACHE_PATH, "w") as file:
            file.write(json.dumps(self._inputs_cache))
