from __future__ import annotations
from typing import List
import attr

from terra_sdk.utils.serdes import JsonDeserializable, JsonSerializable


@attr.s
class EventKV(JsonSerializable, JsonDeserializable):
    key: str = attr.ib()
    value: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> EventKV:
        """
        docstring
        """
        return cls(data["key"], data["value"])


@attr.s
class Event(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = attr.ib()
    attributes: List[EventKV] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> Event:
        """
        docstring
        """
        return cls(data["type"], [EventKV.from_data(e) for e in data["attributes"]])