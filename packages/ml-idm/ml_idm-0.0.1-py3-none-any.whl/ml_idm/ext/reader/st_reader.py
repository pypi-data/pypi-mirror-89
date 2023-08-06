import streamlit as st
import typing as t
from ml_idm.core.reader.abstract_reader import AbstractReader
from ml_idm.core.reader.path_providers.path_provider import PathProvider
from ml_idm.core.reader.reader import Reader


class StreamlitReader(AbstractReader):
    def __init__(
        self,
        custom_readers_map: t.Optional[t.Dict[str, t.Callable[[str], t.Any]]] = None,
        custom_path_providers_map: t.Optional[t.Dict[str, PathProvider]] = None,
    ):
        # I don't like that this initialization is kinda useless, but don't know how to override read neatly
        super().__init__(custom_readers_map=custom_readers_map, custom_path_providers_map=custom_path_providers_map)

        self._reader = Reader(
            custom_readers_map=custom_readers_map, custom_path_providers_map=custom_path_providers_map
        )

    @classmethod
    def _built_in_path_providers_map(cls) -> t.Dict[str, PathProvider]:
        return super()._built_in_path_providers_map()

    # TODO: figure out why it warns me about the mutation without this param
    @st.cache(show_spinner=False, allow_output_mutation=True)
    def read(self, path: str, transform: t.Optional[t.Callable[[t.Any], t.Any]] = None) -> t.Any:
        return self._reader.read(path=path, transform=transform)
