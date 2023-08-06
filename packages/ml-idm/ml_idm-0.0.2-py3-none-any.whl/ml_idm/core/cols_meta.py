from pydantic import BaseModel, root_validator
import typing as t

UNKNOWN_TYPE = "unknown"

NUM_TYPE = "num"
BIN_TYPE = "bin"
CAT_TYPE = "cat"


class ColMeta(BaseModel):
    name: str
    type: str
    description: t.Optional[str]

    @root_validator(pre=True, allow_reuse=True)
    def set_id(cls, v):
        if v.get("type"):
            return v

        # try to infer type from col name
        split = v["name"].split("__")
        if len(split) == 0:
            v["type"] = UNKNOWN_TYPE

        if split[0] not in [NUM_TYPE, BIN_TYPE, CAT_TYPE]:
            raise Exception(f"Unknown type {split[0]} for col {v['name']}")

        v["type"] = split[0]
        return v

    @property
    def is_unknown(self):
        return self.type == UNKNOWN_TYPE

    @property
    def is_num(self) -> bool:
        return self.type == NUM_TYPE

    @property
    def is_bin(self) -> bool:
        return self.type == BIN_TYPE

    @property
    def is_cat(self) -> bool:
        return self.type == CAT_TYPE

    def convert_value(self, value):
        if self.is_unknown:
            return self._convert_unknown(value=value)

        if self.is_num:
            return float(value)
        elif self.is_bin:
            return bool(value)

        return value

    @staticmethod
    def _convert_unknown(value) -> t.Any:
        result = value

        if value.startswith("'") or value.startswith('"'):
            return value.replace("'", "").replace('"', "")

        try:
            result = float(value)
        except Exception:
            pass

        return result
