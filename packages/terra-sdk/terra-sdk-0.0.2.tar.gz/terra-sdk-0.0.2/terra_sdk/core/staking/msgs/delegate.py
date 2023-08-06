from __future__ import annotations
from typing import List

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

__all__ = ["MsgDelegate"]


@attr.s
class MsgDelegate(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "staking/MsgDelegate"
    delegator_address: str = attr.ib()
    validator_address: str = attr.ib()
    amount: Coin = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgDelegate:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["delegator_address"],
            value["validator_address"],
            Coin.from_data(value["amount"]),
        )