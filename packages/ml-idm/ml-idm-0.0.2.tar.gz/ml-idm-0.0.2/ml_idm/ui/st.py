import streamlit as st
import typing as t
import json

from matplotlib import pyplot as plt

from ml_idm.core.cols_meta import ColMeta
from ml_idm.core.reader.abstract_reader import AbstractReader
from ml_idm.core.dependencies import Dependencies
from ml_idm.core.utils.ui_utils import empty_text_to_none
from ml_idm.core.utils.common_utils import get_features_summary_dict, save_inputs


def draw_model_config_ui(reader: AbstractReader) -> Dependencies:
    st.subheader("Provide paths for artifacts:")
    model_path_input = st.text_input("Path to a model", key="model_path")
    preproc_path_input = st.text_input("Path to a preproc ( optional )", key="preproc_path")
    cols_meta_path_input = st.text_input("Path to cols meta", key="cols_meta")
    preproc_path = empty_text_to_none(preproc_path_input)

    app = Dependencies(
        model_path=model_path_input, cols_meta_path=cols_meta_path_input, reader=reader, preproc_path=preproc_path
    )

    return app


def draw_features_inputs_ui(deps: Dependencies) -> t.Tuple[bool, t.Dict[str, t.Any]]:
    st.subheader("Please enter features values below:")
    enable_advanced = st.checkbox(label="Enable advanced mode")
    result: t.Dict[str, t.Any] = {}

    if enable_advanced:
        features = {}
        for col_meta in deps.cols_meta:
            features[col_meta.name] = deps.inputs_cache[col_meta.name]

        pretty_features = json.dumps(features, indent=2)

        user_features_json = st.text_area(
            label="Modify only features values in the following JSON", value=pretty_features, height=400
        )
        result = json.loads(user_features_json)
    else:
        for col_meta in deps.cols_meta:
            text_input = st.text_input(
                col_meta.description or col_meta.name, value=deps.inputs_cache[col_meta.name], key=col_meta.name
            )
            result[col_meta.name] = text_input

    return enable_advanced, result


def draw_model_prediction_ui(deps: Dependencies, input_values):
    st.subheader("Model prediction")

    if deps.model_wrapper.is_proba:
        st.write("Output proba")
    else:
        st.write("Output prediction")

    st.text(deps.model_wrapper.predict(input_values=input_values))


def draw_features_summary_ui(deps: Dependencies, input_values: t.List[t.List[t.Any]]):
    st.markdown("**Features summary:**")
    features_summary = get_features_summary_dict(cols_meta=deps.cols_meta, input_values=input_values)
    st.write(features_summary)


def draw_inputs_save_ui(
    cols_meta: t.List[ColMeta],
    input_values: t.List[t.List[t.Any]],
    metadata_getter: t.Optional[t.Callable[[], t.Dict[str, t.Any]]] = None,
):
    st.markdown("**Save inputs:**")

    description = st.text_input(label="Inputs description", key="description")
    metadata = {}
    if metadata_getter:
        metadata = metadata_getter()

    if st.button(label="Save"):
        if len(description) == 0:
            st.error(body="Fill the description of your inputs")
            return

        save_inputs(description=description, metadata=metadata, cols_meta=cols_meta, input_values=input_values)
        st.success(f'Saved "{description}"!')


def st_plot():
    f = plt.gcf()
    st.pyplot(f)
