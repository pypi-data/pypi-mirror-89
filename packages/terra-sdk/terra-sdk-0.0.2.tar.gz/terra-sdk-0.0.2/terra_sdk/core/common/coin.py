from __future__ import annotations
from typing import List
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable


@attr.s
class Coin(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    denom: str = attr.ib()
    amount: str = attr.ib()

    @classmethod
    def from_data(cls, coin: dict) -> Coin:
        """
        docstring
        """
        return cls(coin["denom"], coin["amount"])


@attr.s
class Coins(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    coins: List[Coin] = attr.ib()

    def to_data(self) -> dict:
        return [coin.to_data() for coin in self.coins]

    def __getitem__(self, item: int) -> Coin:
        return self.coins[item]

    @classmethod
    def from_data(cls, coins: dict) -> Coin:
        """
        docstring
        """
        return cls([Coin.from_data(coin) for coin in coins])