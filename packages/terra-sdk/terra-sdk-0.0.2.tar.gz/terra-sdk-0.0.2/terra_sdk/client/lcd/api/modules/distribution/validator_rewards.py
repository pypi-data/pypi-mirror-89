from __future__ import annotations
from typing import List

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common import Coin

__all__ = ["ValidatorRewards"]


@attr.s
class ValidatorRewards(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    operator_address: str = attr.ib()
    self_bond_rewards: List[Coin] = attr.ib()
    val_commission: List[Coin] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ValidatorRewards:
        """
        docstring
        """
        if data["val_commission"] is None:  # zero commission
            return cls(
                data["operator_address"],
                [Coin.from_data(coin) for coin in data["self_bond_rewards"]],
                None,
            )
        return cls(
            data["operator_address"],
            [Coin.from_data(coin) for coin in data["self_bond_rewards"]],
            [Coin.from_data(coin) for coin in data["val_commission"]],
        )