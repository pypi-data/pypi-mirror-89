from ml_idm.core.reader.path_providers.path_provider import PathProvider


class LocalPathProvider(PathProvider):
    def get_local_path(self, initial_path: str, local_dir: str) -> str:
        return initial_path
