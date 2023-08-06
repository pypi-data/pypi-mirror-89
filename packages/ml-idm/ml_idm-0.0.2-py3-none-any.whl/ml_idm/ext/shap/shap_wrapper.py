import typing as t
import numpy as np

SHAP_WRAPPER_DEP_KEY = "shap_wrapper"


class ShapWrapper:
    def __init__(self, shap_explainer, shap_values_index: t.Optional[int] = None, preproc: t.Optional[t.Any] = None):
        self._shap_explainer = shap_explainer
        self._shap_values_index = shap_values_index
        self._preproc = preproc

    def base_value(self):
        result = self._shap_explainer.expected_value
        if self._shap_values_index:
            result = result[self._shap_values_index]
        return result

    def shap_values(self, input_values) -> np.ndarray:
        if self._preproc:
            input_values = self._preproc.transform(input_values)

        result = self._shap_explainer.shap_values(input_values)
        if self._shap_values_index:
            result = result[self._shap_values_index]
        return result
