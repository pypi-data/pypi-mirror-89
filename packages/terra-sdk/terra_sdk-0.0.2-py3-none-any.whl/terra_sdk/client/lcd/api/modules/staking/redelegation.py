from __future__ import annotations
from typing import List
from terra_sdk.core.common.coin import Coin
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable


@attr.s
class RedelegationEntry(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    initial_balance: str = attr.ib()
    balance: str = attr.ib()
    shares_dst: str = attr.ib()
    creation_height: str = attr.ib()
    completion_time: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> RedelegationEntry:
        """
        docstring
        """
        return cls(
            data["initial_balance"],
            data["balance"],
            data["shares_dst"],
            data["creation_height"],
            data["completion_time"],
        )


@attr.s
class Redelegation(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    delegator_address: str = attr.ib()
    validator_src_address: str = attr.ib()
    validator_dst_address: str = attr.ib()
    entries: List[RedelegationEntry] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> Redelegation:
        """
        docstring
        """
        return cls(
            data["delegator_address"],
            data["validator_src_address"],
            data["validator_dst_address"],
            [RedelegationEntry.from_data(entry) for entry in data["entries"]],
        )