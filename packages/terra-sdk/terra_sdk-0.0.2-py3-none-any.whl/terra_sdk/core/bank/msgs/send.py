from __future__ import annotations
from typing import List

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

__all__ = ["MsgSend"]


@attr.s
class MsgSend(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type = "bank/MsgSend"
    from_address: str = attr.ib()
    to_address: str = attr.ib()
    amount: List[Coin] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgSend:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["from_address"],
            value["to_address"],
            [Coin.from_data(coin) for coin in value["amount"]],
        )