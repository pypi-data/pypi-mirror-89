import typing as t
from ml_idm.core.dependencies import Dependencies
from ml_idm.ext.shap.shap_wrapper import ShapWrapper, SHAP_WRAPPER_DEP_KEY


def add_shap_wrapper_from_path(
    deps: Dependencies, shap_explainer_path: str, shap_values_index: t.Optional[int] = None
) -> ShapWrapper:
    shap_explainer = deps.reader.read(path=shap_explainer_path)
    shap_wrapper = ShapWrapper(shap_explainer=shap_explainer, preproc=deps.preproc, shap_values_index=shap_values_index)

    deps[SHAP_WRAPPER_DEP_KEY] = shap_wrapper

    return shap_wrapper


def get_shap_wrapper(deps: Dependencies) -> ShapWrapper:
    return deps[SHAP_WRAPPER_DEP_KEY]
