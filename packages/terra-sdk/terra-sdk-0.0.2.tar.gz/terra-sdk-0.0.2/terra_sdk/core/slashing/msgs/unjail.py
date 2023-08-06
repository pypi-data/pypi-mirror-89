from __future__ import annotations
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MsgUnjail"]


@attr.s
class MsgUnjail(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "cosmos/MsgUnjail"
    address: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgUnjail:
        """
        docstring
        """
        return cls(data["value"]["address"])