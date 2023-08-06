from __future__ import annotations
from typing import List

import attr
from terra_sdk.utils.serdes import JsonDeserializable, JsonSerializable
from terra_sdk.core.common import Coin


@attr.s
class Delegation(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    delegator_address: str = attr.ib()
    validator_address: str = attr.ib()
    shares: str = attr.ib()
    balance: Coin = attr.ib()

    @classmethod
    def from_data(cls, data: dict):
        """
        docstring
        """
        return cls(
            data["delegator_address"],
            data["validator_address"],
            data["shares"],
            Coin.from_data(data["balance"]),
        )


@attr.s
class UnbondingEntry(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    creation_height: str = attr.ib()
    completion_time: str = attr.ib()
    initial_balance: str = attr.ib()
    balance: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> UnbondingEntry:
        """
        docstring
        """
        return cls(
            data["creation_height"],
            data["completion_time"],
            data["initial_balance"],
            data["balance"],
        )


@attr.s
class UnbondingDelegation(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    delegator_address: str = attr.ib()
    validator_address: str = attr.ib()
    entries: List[UnbondingEntry] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> UnbondingDelegation:
        """
        docstring
        """
        return cls(
            data["delegator_address"],
            data["validator_address"],
            [UnbondingEntry.from_data(entry) for entry in data["entries"]],
        )