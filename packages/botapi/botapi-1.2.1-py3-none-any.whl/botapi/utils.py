from .serialize import SerializableModel


def print_model(
    obj,
    key: str = None,
    level: int = None,
    add_comma: bool = None,
    ignore_str_check: bool = None
) -> None:
    """
    Pretty print for botapi models

    :param obj: model object
    :param key: field
    :param level: nesting level
    :param add_comma: if True adds a comma after serialized string
    :param ignore_str_check: if obj type is str adds quotes
    :return: None
    """
    level = 0 if level is None else level
    if isinstance(obj, SerializableModel):
        obj = obj.serialize()
    if isinstance(obj, dict):
        print_model('{', key=key, level=level, ignore_str_check=True)
        for key, value in obj.items():
            print_model(value, key, level + 1, add_comma=True)
        print_model('}', level=level, add_comma=bool(level), ignore_str_check=True)
    else:
        key = '' if key is None else f"'{key}': "
        str_obj = f"\"{obj}\"" if isinstance(
            obj, str
        ) and not ignore_str_check else str(obj)
        print(f"{' ' * 4 * level}{key}{str_obj}{',' if add_comma else ''}")
