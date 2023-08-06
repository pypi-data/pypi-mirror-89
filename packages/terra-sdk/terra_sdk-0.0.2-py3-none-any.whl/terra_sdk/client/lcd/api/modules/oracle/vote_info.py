from __future__ import annotations
from typing import List
import attr

from terra_sdk.utils.serdes import JsonDeserializable, JsonSerializable


@attr.s
class ExchangeRateVote(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    exchange_rate: str = attr.ib()
    denom: str = attr.ib()
    voter: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ExchangeRateVote:
        """
        docstring
        """
        return cls(data["exchange_rate"], data["denom"], data["voter"])


@attr.s
class ExchangeRatePrevote(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    hash: str = attr.ib()
    denom: str = attr.ib()
    voter: str = attr.ib()
    submit_block: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ExchangeRatePrevote:
        """
        docstring
        """
        return cls(data["hash"], data["denom"], data["voter"], data["submit_block"])


@attr.s
class ExchangeRate(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    denom: str = attr.ib()
    exchange_rate: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ExchangeRate:
        """
        docstring
        """
        return cls(data["denom"], data["exchange_rate"])


@attr.s
class ExchangeRateAggregateVote(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    exchange_rate_tuples: List[ExchangeRate] = attr.ib()
    voter: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ExchangeRateAggregateVote:
        """
        docstring
        """
        return cls(
            [ExchangeRate.from_data(er) for er in data["exchange_rate_tuples"]],
            data["voter"],
        )


@attr.s
class ExchangeRateAggregatePrevote(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    hash: str = attr.ib()
    voter: str = attr.ib()
    submit_block: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ExchangeRateAggregatePrevote:
        """
        docstring
        """
        return cls(data["hash"], data["voter"], data["submit_block"])