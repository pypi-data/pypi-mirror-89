from __future__ import annotations
from typing import List
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

__all__ = ["MsgInstantiateContract"]


@attr.s
class MsgInstantiateContract(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "wasm/MsgInstantiateContract"
    owner: str = attr.ib()
    code_id: str = attr.ib()
    init_msg: str = attr.ib()
    init_coins: List[Coin] = attr.ib()
    migratable: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgInstantiateContract:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["owner"],
            value["code_id"],
            value["init_msg"],
            [Coin.from_data(coin) for coin in value["init_coins"]],
            value["migratable"],
        )