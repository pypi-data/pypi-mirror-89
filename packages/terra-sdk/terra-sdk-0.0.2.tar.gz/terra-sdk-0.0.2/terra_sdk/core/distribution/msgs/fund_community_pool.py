from __future__ import annotations
from typing import List

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin


__all__ = ["MsgFundCommunityPool"]


@attr.s
class MsgFundCommunityPool(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type = "distribution/MsgFundCommunityPool"
    depositor: str = attr.ib()
    amount: List[Coin] = attr.ib()  # Coin Array

    @classmethod
    def from_data(cls, data: dict) -> MsgFundCommunityPool:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["depositor"], [Coin.from_data(coin) for coin in value["amount"]]
        )