from __future__ import annotations

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MsgAggregateExchangeRatePrevote"]


@attr.s
class MsgAggregateExchangeRatePrevote(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "oracle/MsgAggregateExchangeRatePrevote"
    hash: str = attr.ib()
    feeder: str = attr.ib()
    validator: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgAggregateExchangeRatePrevote:
        """
        docstring
        """
        value = data["value"]
        return cls(value["hash"], value["feeder"], value["validator"])