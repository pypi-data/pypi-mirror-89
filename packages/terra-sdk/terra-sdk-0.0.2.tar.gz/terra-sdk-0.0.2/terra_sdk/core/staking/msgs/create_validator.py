from __future__ import annotations
from typing import List

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

from terra_sdk.core.staking.validator import Description, CommissionRate

__all__ = ["MsgCreateValidator"]


@attr.s
class MsgCreateValidator(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "staking/MsgCreateValidator"
    description: Description = attr.ib()
    commission: CommissionRate = attr.ib()
    min_self_delegation: str = attr.ib()
    delegator_address: str = attr.ib()
    validator_address: str = attr.ib()
    pubkey: str = attr.ib()
    value: Coin = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgCreateValidator:
        """
        docstring
        """
        value = data["value"]
        return cls(
            Description.from_data(value["description"]),
            CommissionRate.from_data(value["commission"]),
            value["min_self_delegation"],
            value["delegator_address"],
            value["validator_address"],
            value["pubkey"],
            Coin.from_data(value["value"]),
        )