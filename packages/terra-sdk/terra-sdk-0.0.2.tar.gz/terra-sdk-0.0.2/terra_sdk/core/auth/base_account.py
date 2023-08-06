from __future__ import annotations
from typing import List, Union

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin
from terra_sdk.core.common.public_key import get_pub_key, PublicKey, MultiSigPublicKey

__all__ = ["BaseAccount"]


@attr.s
class BaseAccount(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type = "core/Account"
    address: str = attr.ib()
    coins: List[Coin] = attr.ib()
    public_key: Union[PublicKey, MultiSigPublicKey] = attr.ib()
    account_number: str = attr.ib()
    sequence: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> BaseAccount:
        """
        docstring
        """
        value = data["value"]
        public_key = None
        if value["public_key"] is not None:
            public_key = get_pub_key(value["public_key"])
        coins = value["coins"]
        return cls(
            value["address"],
            [Coin.from_data(coin) for coin in coins],
            public_key,
            value["account_number"],
            value["sequence"],
        )
