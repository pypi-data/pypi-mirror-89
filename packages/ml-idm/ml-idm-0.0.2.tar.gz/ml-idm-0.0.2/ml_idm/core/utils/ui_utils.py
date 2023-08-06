import typing as t


def empty_text_to_none(text: str) -> t.Optional[t.Any]:
    if text == "":
        return None

    return text
