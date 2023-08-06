from __future__ import annotations

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MsgExchangeRateVote"]


@attr.s
class MsgExchangeRateVote(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "oracle/MsgExchangeRateVote"
    exchange_rate: str = attr.ib()
    denom: str = attr.ib()
    salt: str = attr.ib()
    feeder: str = attr.ib()
    validator: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExchangeRateVote:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["exchange_rate"],
            value["denom"],
            value["salt"],
            value["feeder"],
            value["validator"],
        )
