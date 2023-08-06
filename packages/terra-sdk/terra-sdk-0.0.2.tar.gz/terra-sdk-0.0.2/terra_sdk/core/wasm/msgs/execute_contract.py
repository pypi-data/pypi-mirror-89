from __future__ import annotations
from typing import List
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

__all__ = ["MsgExecuteContract"]


@attr.s
class MsgExecuteContract(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "wasm/MsgExecuteContract"
    sender: str = attr.ib()
    contract: str = attr.ib()
    execute_msg: str = attr.ib()
    coins: List[Coin] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExecuteContract:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["sender"],
            value["contract"],
            value["execute_msg"],
            [Coin.from_data(coin) for coin in value["coins"]],
        )