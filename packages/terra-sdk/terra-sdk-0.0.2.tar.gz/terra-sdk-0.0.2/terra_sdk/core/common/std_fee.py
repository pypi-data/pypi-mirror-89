from __future__ import annotations
from typing import List
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from .coin import Coin

__all__ = ["StdFee"]


@attr.s
class StdFee(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    gas: str = attr.ib()
    amount: List[Coin] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> StdFee:
        """
        docstring
        """
        return cls(data["gas"], [Coin.from_data(coin) for coin in data["amount"]])