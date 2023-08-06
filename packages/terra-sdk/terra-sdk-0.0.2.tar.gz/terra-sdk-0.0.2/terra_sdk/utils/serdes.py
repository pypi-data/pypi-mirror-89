"""terra sdk internal utilities for serialization to / de-serialization from JSON."""

from __future__ import annotations

import abc
import json
from typing import Any, Generic, TypeVar

# import fastjsonschema
# # from box import Box

from terra_sdk.utils.pretty import PrettyPrintable

# _cached_schemas = dict()

T = TypeVar("T")


class JsonDeserializable(Generic[T], metaclass=abc.ABCMeta):
    """Abstract base class for objects which define a unmarshalling strategy after being
    deserialized into a Python data type (dict, list, str, etc.) from a JSON string. Can
    be used as a generic type like `JsonDeserializable[dict]` to define the Python data
    type from which the object is reconstructed."""

    # __schema__ = {}

    # @property
    # @abc.abstractmethod
    # def __schema__(self) -> dict:
    #     """Draft-7 compliant JSONSchema for validating inputs expressed as a Python `dict`."""
    #     raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_data(cls, data: dict) -> JsonDeserializable[T]:
        """Deserialize the object from a native Python format

        :param data: Python data object (dict, int, list, etc.)
        :return: un-marshalled object
        """
        raise NotImplementedError

    # @classmethod
    # def deserialize(cls, data: T, *args, **kwargs) -> JsonDeserializable[T]:
    #     """Applies JSON Schema-validation checks before attempting to recreate a
    #     Python object. Calls `from_data()` internally.

    #     :param data: Python data to construct object from
    #     :return: unmarshalled object
    #     :raises: JsonSchemaValidationError: did not pass the schema-validation check
    #     """
    #     raise NotImplementedError


class TerraJsonEncoder(json.JSONEncoder):
    """Encoder class for `JsonSerializable`"""

    def default(self, o) -> Any:
        if hasattr(o, "to_data"):
            return o.to_data()
        else:
            return json.JSONEncoder.default(self, o)


def serialize_to_json(item: Any, sort: bool = False, debug: bool = False) -> str:
    """Serializes an object using the serialization strategy for `JsonSerializable`.

    :param item: object to serialize
    :type item: Any
    :param sort: sort keys alphabetically
    :type sort: bool
    :param debug: pretty-print indentation
    :type debug: bool
    """
    return json.dumps(
        item,
        indent=2 if debug else None,
        sort_keys=sort,
        separators=(",", ":") if not debug else None,
        cls=TerraJsonEncoder,
    )


class JsonSerializable(PrettyPrintable, Generic[T]):
    """Abstract base class for an object that can be serialized to a JSON string. It should
    define in `.to_data()` how to marshal its contents into a native Python data type whose]
    contents are also normally JSON-serializable, or other instances of `JsonSerializable`.
    Can be used as a type like `JsonSerializable[dict]` or `JsonSerializable[int]` to indicate
    its marshalled data value type immediately prior to conversion to a string.
    """

    def to_data(self) -> dict:
        """Override this to define a marshalling strategy. By default, uses a copy of
        the object's `__dict__` property.

        :return: marshalled contents of object
        """
        if hasattr(self, "type") and self.__dict__.get("type", "") == "":
            return dict({"type": self.type, "value": dict(self.__dict__)})
        return dict(self.__dict__)

    def to_json(self, sort: bool = False, debug: bool = False) -> str:
        """Applies the JSON-serialization strategy to the marshalled contents of the object.

        :param sort: sort by key
        :type sort: bool

        :param debug: pretty-print with indentation
        :type debug: bool

        :return: serialized object as a JSON string
        :rtype: str
        """
        return serialize_to_json(self.to_data(), sort=sort, debug=debug)

    def to_dict(self) -> dict:
        return json.loads(self.to_json())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, JsonSerializable):
            return self.to_data() == other.to_data()
        else:
            return self.to_data() == other
