import pickle
import json
import yaml
import typing as t
import joblib

from ml_idm.core.reader.abstract_reader import AbstractReader
from ml_idm.core.reader.path_providers.local import LocalPathProvider
from ml_idm.core.reader.path_providers.path_provider import PathProvider

PATH_SLASHES = "://"
DOWNLOADS_DIR = "downloads"


def read_joblib(path: str) -> t.Any:
    return joblib.load(path)


def read_pickle(path: str) -> t.Any:
    with open(path, "rb") as file:
        return pickle.load(file)


def read_json(path: str) -> t.Any:
    with open(path, "r") as file:
        return json.load(file)


def read_yaml(path: str) -> t.Any:
    with open(path, "r") as file:
        return yaml.safe_load(file)


class Reader(AbstractReader):
    @classmethod
    def supported_readers(cls) -> t.List[str]:
        return list(cls._built_in_readers_map().keys())

    @classmethod
    def _built_in_readers_map(cls) -> t.Dict[str, t.Callable[[str], t.Any]]:
        built_in_readers_map: t.Dict[str, t.Callable[[str], t.Any]] = {
            "joblib": read_joblib,
            "pickle": read_pickle,
            "pkl": read_pickle,
            "json": read_json,
            "yaml": read_yaml,
        }

        return built_in_readers_map

    @classmethod
    def _built_in_path_providers_map(cls) -> t.Dict[str, PathProvider]:
        return {"local": LocalPathProvider()}

    def read(self, path: str, transform: t.Optional[t.Callable[[t.Any], t.Any]] = None) -> t.Any:
        path = self._get_local_path(path=path)
        result = None
        for reader in self._readers_map.values():
            try:
                result = reader(path)
            except Exception:
                pass

        if result:
            if transform:
                result = transform(result)

            return result

        raise Exception(
            f"Coulnd't read file at path {path}, "
            f"please serialize it with one of the following tools: {list(self._readers_map.keys())}"
        )

    def _get_local_path(self, path: str) -> str:
        path_provider = LocalPathProvider()
        destination_prefix = ""
        if PATH_SLASHES in path:
            destination_prefix = path.split(PATH_SLASHES)[0]
            path_provider = self._path_providers_map.get(destination_prefix)
            if not path_provider:
                raise Exception(
                    f"Could not recognize the destination you have provided "
                    f"{destination_prefix}{PATH_SLASHES}. "
                    f"Consider using one of the following prefixes: "
                    f"{[f'{prefix}{PATH_SLASHES}' for prefix in list(self._path_providers_map.keys())]}"
                )
        return path_provider.get_local_path(
            initial_path=path.replace(f"{destination_prefix}{PATH_SLASHES}", ""), local_dir=DOWNLOADS_DIR
        )
