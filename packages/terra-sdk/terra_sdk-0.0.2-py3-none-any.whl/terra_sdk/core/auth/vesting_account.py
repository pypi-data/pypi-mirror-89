from __future__ import annotations
from typing import List, Union

import attr
from terra_sdk.core.common import coin

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin
from terra_sdk.core.common.public_key import MultiSigPublicKey, PublicKey, get_pub_key

__all__ = ["VestingAccount"]


@attr.s
class Schedule(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    start_time: str = attr.ib()
    end_time: str = attr.ib()
    ratio: str = attr.ib()

    @classmethod
    def from_data(cls, schedule: dict) -> Schedule:
        """
        docstring
        """
        return cls(schedule["start_time"], schedule["end_time"], schedule["ratio"])


@attr.s
class VestingSchedule(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    denom: str = attr.ib()
    schedules: List[Schedule] = attr.ib()

    @classmethod
    def from_data(cls, vesting_schedule: dict) -> VestingSchedule:
        """
        docstring
        """
        return cls(
            vesting_schedule["denom"],
            [
                Schedule.from_data(schedule)
                for schedule in vesting_schedule["schedules"]
            ],
        )


@attr.s
class VestingAccount(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "core/LazyGradedVestingAccount"
    address: str = attr.ib()
    coins: List[Coin] = attr.ib()
    public_key: Union[PublicKey, MultiSigPublicKey] = attr.ib()
    account_number: str = attr.ib()
    sequence: str = attr.ib()
    original_vesting: List[Coin] = attr.ib()
    delegated_free: List[Coin] = attr.ib()
    delegated_vesting: List[Coin] = attr.ib()
    end_time: str = attr.ib()
    vesting_schedules: List[VestingSchedule] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> VestingAccount:
        """
        docstring
        """
        value = data["value"]
        public_key = None
        if value["public_key"] is not None:
            public_key = get_pub_key(value["public_key"])
        return cls(
            value["address"],
            [Coin.from_data(coin) for coin in value["coins"]],
            public_key,
            value["account_number"],
            value["sequence"],
            [Coin.from_data(coin) for coin in value["original_vesting"]],
            [Coin.from_data(coin) for coin in value["delegated_free"]],
            [Coin.from_data(coin) for coin in value["delegated_vesting"]],
            value["end_time"],
            [
                VestingSchedule.from_data(vesting_schedule)
                for vesting_schedule in value["vesting_schedules"]
            ],
        )