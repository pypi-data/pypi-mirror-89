from abc import ABC, abstractmethod


class PathProvider(ABC):
    @abstractmethod
    def get_local_path(self, initial_path: str, local_dir: str) -> str:
        pass
