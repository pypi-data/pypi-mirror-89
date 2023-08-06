from __future__ import annotations
from typing import List

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

__all__ = ["MsgSwap"]


@attr.s
class MsgSwap(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "market/MsgSwap"
    trader: str = attr.ib()
    offer_coin: List[Coin] = attr.ib()
    ask_denom: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgSwap:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["trader"], Coin.from_data(value["offer_coin"]), value["ask_denom"]
        )