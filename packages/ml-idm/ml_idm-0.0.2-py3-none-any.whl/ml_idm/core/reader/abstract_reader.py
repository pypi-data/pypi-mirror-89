import os
import typing as t
from abc import ABC, abstractmethod

from ml_idm.core.reader.path_providers.path_provider import PathProvider

DOWNLOADS_DIR = "downloads"


class AbstractReader(ABC):
    def __init__(
        self,
        custom_readers_map: t.Optional[t.Dict[str, t.Callable[[str], t.Any]]] = None,
        custom_path_providers_map: t.Optional[t.Dict[str, PathProvider]] = None,
    ):
        custom_readers_map = custom_readers_map or {}
        custom_path_providers_map = custom_path_providers_map or {}
        self._readers_map = {**self._built_in_readers_map(), **custom_readers_map}
        self._path_providers_map: t.Dict[str, PathProvider] = {
            **self._built_in_readers_map(),
            **custom_path_providers_map,
        }
        if not os.path.isdir(DOWNLOADS_DIR):
            os.mkdir(DOWNLOADS_DIR)

    @abstractmethod
    def read(self, path: str, transform: t.Optional[t.Callable[[t.Any], t.Any]] = None) -> t.Any:
        pass

    @classmethod
    def _built_in_readers_map(cls) -> t.Dict[str, t.Callable[[str], t.Any]]:
        return {}

    @classmethod
    def _built_in_path_providers_map(cls) -> t.Dict[str, PathProvider]:
        return {}
