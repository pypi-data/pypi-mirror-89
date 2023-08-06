from __future__ import annotations
from typing import List

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

__all__ = ["MsgMultiSend"]


@attr.s
class IO(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    address: str = attr.ib()
    coins: List[Coin] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> IO:
        """
        docstring
        """
        return cls(data["address"], [Coin.from_data(coin) for coin in data["coins"]])


@attr.s
class MsgMultiSend(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type = "bank/MsgMultiSend"
    inputs: List[IO] = attr.ib()
    outputs: List[IO] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgMultiSend:
        """
        docstring
        """
        value = data["value"]
        return cls(
            [IO.from_data(inp) for inp in value["inputs"]],
            [IO.from_data(inp) for inp in value["outputs"]],
        )