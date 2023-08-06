from __future__ import annotations
from typing import List
import attr
from enum import Enum

from terra_sdk.utils.serdes import JsonDeserializable, JsonSerializable
from terra_sdk.core.gov.proposal import CONTENT_TYPES, contents
from terra_sdk.core.common import Coin

__all__ = ["Proposal"]


class Status(Enum):
    """
    docstring
    """

    deposit_period = "DepositPeriod"
    voting_period = "VotingPeriod"
    rejected = "Rejected"
    passed = "Passed"

    def to_data(self) -> str:
        return self.value


@attr.s
class Tally(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    yes = attr.ib()
    abstain = attr.ib()
    no = attr.ib()
    no_with_veto = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> Tally:
        """
        docstring
        """
        return cls(data["yes"], data["abstain"], data["no"], data["no_with_veto"])


@attr.s
class Proposal(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    content: CONTENT_TYPES = attr.ib()
    id: str = attr.ib()
    proposal_status: Status = attr.ib()
    final_tally_result: Tally = attr.ib()
    submit_time: str = attr.ib()
    deposit_end_time: str = attr.ib()
    total_deposit: List[Coin] = attr.ib()
    voting_start_time: str = attr.ib()
    voting_end_time: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> Proposal:
        """
        docstring
        """
        return cls(
            contents[data["content"]["type"]].from_data(data["content"]),
            data["id"],
            Status(data["proposal_status"]),
            Tally.from_data(data["final_tally_result"]),
            data["submit_time"],
            data["deposit_end_time"],
            [Coin.from_data(coin) for coin in data["total_deposit"]],
            data["voting_start_time"],
            data["voting_end_time"],
        )