from __future__ import annotations

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MsgDelegateFeedConsent"]


@attr.s
class MsgDelegateFeedConsent(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "oracle/MsgDelegateFeedConsent"
    operator: str = attr.ib()
    delegate: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgDelegateFeedConsent:
        """
        docstring
        """
        value = data["value"]
        return cls(value["operator"], value["delegate"])
