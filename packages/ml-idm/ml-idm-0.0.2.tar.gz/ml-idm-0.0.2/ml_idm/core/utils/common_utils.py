import typing as t
import os
import yaml
from ml_idm.core.cols_meta import ColMeta
from ml_idm.core.inputs_cache import InputsCache


def make_input_values(cols_meta: t.List[ColMeta], value_getter: t.Callable[[str], t.Any]) -> t.List[t.List[t.Any]]:
    result = [[col_meta.convert_value(value=value_getter(col_meta.name)) for col_meta in cols_meta]]
    return result


def get_features_summary_str(cols_meta: t.List[ColMeta], input_values: t.List[t.List[t.Any]]) -> str:
    result = ""
    for col_meta, value in zip(cols_meta, input_values[0]):
        result += f"{col_meta.description or col_meta.name}:\n{value}\n\n"

    return result


def get_features_summary_dict(cols_meta: t.List[ColMeta], input_values: t.List[t.List[t.Any]]) -> t.Dict[str, t.Any]:
    result = {}
    for col_meta, value in zip(cols_meta, input_values[0]):
        key = col_meta.description or col_meta.name
        result[key] = value

    return result


def update_inputs_cache(cols_meta: t.List[ColMeta], input_values: t.List[t.List[t.Any]], inputs_cache: InputsCache):
    for col_meta, value in zip(cols_meta, input_values[0]):
        inputs_cache[col_meta.name] = value

    inputs_cache.save()


def get_filename(path: str):
    return os.path.basename(os.path.normpath(path))


def save_inputs(
    description: str, metadata: t.Dict[str, t.Any], cols_meta: t.List[ColMeta], input_values: t.List[t.List[t.Any]]
):
    saved_inputs: t.List[t.Dict[str, t.Any]] = []
    saved_inputs_filename = "saved_inputs.yaml"
    if os.path.exists(saved_inputs_filename):
        with open(saved_inputs_filename, "r") as file:
            saved_inputs = yaml.safe_load(file)

    named_input_values = dict(zip([col_meta.name for col_meta in cols_meta], input_values[0]))

    new_record = {"description": description, "metadata": metadata, "input_values": named_input_values}

    saved_inputs.append(new_record)

    with open(saved_inputs_filename, "w") as file:
        file.write(yaml.dump(saved_inputs))
