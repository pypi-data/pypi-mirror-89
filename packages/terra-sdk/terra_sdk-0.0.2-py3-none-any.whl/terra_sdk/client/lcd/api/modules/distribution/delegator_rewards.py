from __future__ import annotations

import attr
from typing import List

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common import Coin

__all__ = ["DelegatorRewards"]


@attr.s
class ValidatorReward(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    validator_address: str = attr.ib()
    reward: List[Coin] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ValidatorReward:
        """
        docstring
        """
        return cls(
            data["validator_address"],
            [Coin.from_data(coin) for coin in data["reward"]],
        )


@attr.s
class DelegatorRewards(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    rewards: List[ValidatorReward] = attr.ib()
    total: List[Coin] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> DelegatorRewards:
        """
        docstring
        """
        return cls(
            [
                ValidatorReward.from_data(per_validator_reward)
                for per_validator_reward in data["rewards"]
            ],
            [Coin.from_data(coin) for coin in data["total"]],
        )