from __future__ import annotations
from typing import List

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

__all__ = ["MsgDeposit"]


@attr.s
class MsgDeposit(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "gov/MsgDeposit"
    proposal_id: str = attr.ib()
    depositor: str = attr.ib()
    amount: List[Coin] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgDeposit:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["proposal_id"],
            value["depositor"],
            [Coin.from_data(coin) for coin in value["amount"]],
        )