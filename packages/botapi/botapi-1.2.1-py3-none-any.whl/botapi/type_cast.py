from datetime import datetime
from typing import Any

from .exceptions import TypeCastException
from .serialize import SerializableModel
from .types import TypedList, DateTime


def type_cast(func):
    def wrapper(var_name: str, value: Any, *args, **kwargs):
        if value is None:
            return None
        return func(var_name, value, *args, **kwargs)

    return wrapper


class TypeCast:
    @staticmethod
    @type_cast
    def cast(var_name: str, value: Any, var_type: Any = None, *args, **kwargs) -> Any:
        """
        Casts the value to the new_type. If new_type is TypedList, casts every
        item of value to item_type if item_type is not None

        :param var_name: name of the attribute (used to raise errors)
        :param value: value to cast
        :param var_type: desired type
        :return: casted value
        """
        if var_type is None or isinstance(value, var_type):
            return value
        elif issubclass(var_type, SerializableModel) and isinstance(value, dict):
            return var_type(**value)
        elif issubclass(var_type, datetime) and type(value) == str:
            return datetime.fromisoformat(value)
        else:
            raise TypeCastException(var_name, value, var_type)

    @staticmethod
    @type_cast
    def datetime_cast(var_name, value, date_format: str = None, *args, **kwargs):
        """Returns DateTime casted from value

        :param var_name: name of the attribute (used to raise errors)
        :param value: str or datetime object
        :param date_format: str with date format
        :return: DateTime
        """
        if type(value) == str:
            if date_format is None:
                result = DateTime.fromisoformat(value)
            else:
                result = DateTime.strptime(value, date_format)
        elif type(value) == DateTime:
            result = value
        elif isinstance(value, datetime):
            result = DateTime(
                value.year,
                value.month,
                value.day,
                value.hour,
                value.minute,
                value.second,
                value.microsecond,
                value.tzinfo
            )
        else:
            raise TypeCastException(var_name, value, DateTime)
        result.set_format(date_format=date_format)
        return result

    @staticmethod
    @type_cast
    def typed_list_cast(var_name, value, item_type=None, *args, **kwargs) -> TypedList:
        """Returns TypedList with type casted items

        :param var_name: name of the attribute (used to raise errors)
        :param value: iterable to cast
        :param item_type: type of EVERY item
        :return: TypedList
        """
        if item_type is None:
            return TypedList(value, None)
        elif issubclass(item_type, SerializableModel):
            return TypedList([
                TypeCast.cast(var_name, item, item_type) for item in value
            ], item_type)
        else:
            return TypedList(value, item_type)
