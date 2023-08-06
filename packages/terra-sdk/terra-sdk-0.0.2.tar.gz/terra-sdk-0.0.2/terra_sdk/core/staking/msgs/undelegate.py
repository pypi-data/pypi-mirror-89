from __future__ import annotations

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

__all__ = ["MsgUndelegate"]


@attr.s
class MsgUndelegate(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "staking/MsgUndelegate"
    delegator_address: str = attr.ib()
    validator_address: str = attr.ib()
    amount: Coin = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgUndelegate:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["delegator_address"],
            value["validator_address"],
            Coin.from_data(value["amount"]),
        )