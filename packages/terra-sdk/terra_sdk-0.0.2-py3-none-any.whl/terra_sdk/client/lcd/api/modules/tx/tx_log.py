from __future__ import annotations
from typing import List
import attr

from terra_sdk.utils.serdes import JsonDeserializable, JsonSerializable


from .event import Event


@attr.s
class TxLog(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    msg_index: str = attr.ib()
    log: str = attr.ib()
    events: List[Event] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> TxLog:
        """
        docstring
        """
        return cls(
            data["msg_index"], data["log"], [Event.from_data(e) for e in data["events"]]
        )