from __future__ import annotations

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MsgExchangeRatePrevote"]


@attr.s
class MsgExchangeRatePrevote(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "oracle/MsgExchangeRatePrevote"
    hash: str = attr.ib()
    denom: str = attr.ib()
    feeder: str = attr.ib()
    validator: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExchangeRatePrevote:
        """
        docstring
        """
        value = data["value"]
        return cls(value["hash"], value["denom"], value["feeder"], value["validator"])
