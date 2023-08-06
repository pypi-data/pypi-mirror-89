import typing as t
from ml_idm.core.cols_meta import ColMeta
from ml_idm.core.inputs_cache import InputsCache
from ml_idm.core.model_wrapper import ModelWrapper
from ml_idm.core.reader.abstract_reader import AbstractReader
from ml_idm.core.reader.reader import Reader

MODEL_DEP_KEY = "model"
COLS_META_DEP_KEY = "cols_meta"
PREPROC_DEP_KEY = "preproc"


class Dependencies:
    def __init__(
        self,
        model_path: str,
        cols_meta_path: str,
        reader: AbstractReader = Reader(),
        preproc_path: t.Optional[str] = None,
    ):
        self._objects: t.Dict[str, t.Any] = {}
        self._reader = reader

        self.add(obj_key=MODEL_DEP_KEY, obj_path=model_path)
        self.add(obj_key=COLS_META_DEP_KEY, obj_path=cols_meta_path, transform=self._cols_meta_transform)
        if preproc_path:
            self.add(obj_key=PREPROC_DEP_KEY, obj_path=preproc_path)

        self._inputs_cache = InputsCache(cols_meta=self.cols_meta)

        self._model_wrapper = ModelWrapper(model=self.model, preproc=self.preproc)

    @property
    def reader(self) -> AbstractReader:
        return self._reader

    @property
    def model(self) -> t.Any:
        return self[MODEL_DEP_KEY]

    @property
    def cols_meta(self) -> t.List[ColMeta]:
        return self[COLS_META_DEP_KEY]

    @property
    def preproc(self) -> t.Optional[t.Any]:
        return self[PREPROC_DEP_KEY]

    @property
    def model_wrapper(self) -> ModelWrapper:
        return self._model_wrapper

    @property
    def inputs_cache(self) -> InputsCache:
        return self._inputs_cache

    def add(self, obj_key: str, obj_path: str, transform: t.Optional[t.Callable[[t.Any], t.Any]] = None):
        self._objects[obj_key] = self._reader.read(path=obj_path, transform=transform)

    @staticmethod
    def _cols_meta_transform(cols_meta: t.Any) -> t.Any:
        result = cols_meta
        if isinstance(cols_meta[0], str):
            # just a list of cols
            result = [{"name": col_name} for col_name in cols_meta]
        result = [ColMeta(**col_meta) for col_meta in result]

        return result

    def __setitem__(self, dependency_key, dependency):
        self._objects[dependency_key] = dependency

    def __getitem__(self, dependency_key):
        return self._objects.get(dependency_key)
