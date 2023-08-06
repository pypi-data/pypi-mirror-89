from __future__ import annotations

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MsgAggregateExchangeRateVote"]


@attr.s
class MsgAggregateExchangeRateVote(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "oracle/MsgAggregateExchangeRateVote"
    salt: str = attr.ib()
    feeder: str = attr.ib()
    validator: str = attr.ib()
    exchange_rates: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgAggregateExchangeRateVote:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["salt"], value["feeder"], value["validator"], value["exchange_rates"]
        )
