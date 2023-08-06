from __future__ import annotations
from typing import List

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

__all__ = ["MsgBeginRedelegate"]


@attr.s
class MsgBeginRedelegate(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "staking/MsgBeginRedelegate"
    delegator_address: str = attr.ib()
    validator_src_address: str = attr.ib()
    validator_dst_address: str = attr.ib()
    amount: Coin = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgBeginRedelegate:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["delegator_address"],
            value["validator_src_address"],
            value["validator_dst_address"],
            Coin.from_data(value["amount"]),
        )