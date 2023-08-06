from __future__ import annotations
from typing import List

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

__all__ = ["MsgSwapSend"]


@attr.s
class MsgSwapSend(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "market/MsgSwapSend"
    from_address: str = attr.ib()
    to_address: str = attr.ib()
    offer_coin: Coin = attr.ib()
    ask_denom: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgSwapSend:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["from_address"],
            value["to_address"],
            Coin.from_data(value["offer_coin"]),
            value["ask_denom"],
        )