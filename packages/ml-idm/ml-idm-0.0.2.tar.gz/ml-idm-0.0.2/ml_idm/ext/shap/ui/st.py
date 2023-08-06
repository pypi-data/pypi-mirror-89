import typing as t
import pandas as pd
import streamlit as st
import shap
import matplotlib.pyplot as plt
from ml_idm.core.dependencies import Dependencies
from ml_idm.core.utils.ui_utils import empty_text_to_none
from ml_idm.ext.shap.utils import add_shap_wrapper_from_path, get_shap_wrapper
from ml_idm.ui.st import st_plot


def draw_shap_config_ui(deps: Dependencies):
    shap_explainer_path_input = st.text_input("Path to a shap explainer", key="explainer_path")
    shap_values_index = st.text_input(
        "Shap values index " "( optional, if shap produces list of lists " "for the given model )", key="explainer_path"
    )
    shap_explainer_path = empty_text_to_none(shap_explainer_path_input)
    shap_values_index = empty_text_to_none(shap_values_index)
    if shap_values_index:
        shap_values_index = int(shap_values_index)

    add_shap_wrapper_from_path(deps=deps, shap_explainer_path=shap_explainer_path, shap_values_index=shap_values_index)


def draw_shap_values(deps: Dependencies, input_values, cols: t.List[str], draw_force: bool, draw_decision: bool):
    st.markdown("**SHAP values**")
    shap_values = get_shap_wrapper(deps=deps).shap_values(input_values=input_values)

    st.text("SHAP values")
    shap_values_df = pd.DataFrame(shap_values, columns=cols).T
    shap_values_df.rename(columns={0: "shap_value"}, inplace=True)
    if isinstance(input_values, pd.DataFrame):
        input_values = input_values.values

    shap_values_df["feature_value"] = input_values[0]
    st.write(shap_values_df)
    if draw_force:
        st.markdown("**Force plot**")
        shap.force_plot(
            get_shap_wrapper(deps=deps).base_value(), shap_values, feature_names=cols, matplotlib=True, link="logit"
        )
        st_plot()

    if draw_decision:
        plt.clf()
        st.markdown("**Decision plot**")
        shap.decision_plot(get_shap_wrapper(deps=deps).base_value(), shap_values, feature_names=cols, link="logit")
        st_plot()
