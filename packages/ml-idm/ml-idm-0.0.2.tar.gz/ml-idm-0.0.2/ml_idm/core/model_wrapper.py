import typing as t


class ModelWrapper:
    def __init__(self, model: t.Any, preproc: t.Optional[t.Any] = None):
        self._model = model
        self._preproc = preproc

    @property
    def is_proba(self) -> bool:
        return hasattr(self._model, "predict_proba") and callable(self._model.predict_proba)

    def predict(self, input_values):
        if self._preproc:
            input_values = self._preproc.transform(input_values)

        if self.is_proba:
            pred = self._model.predict_proba(input_values)
        else:
            pred = self._model.predict(input_values)

        return pred
