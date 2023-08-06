from __future__ import annotations

import attr
from enum import Enum

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

__all__ = ["MsgVote"]


class VoteOption(Enum):
    """
    docstring
    """

    yes = "Yes"
    no = "No"
    no_with_veto = "NoWithVeto"
    abstain = "Abstain"

    def to_data(self) -> str:
        return self.value


@attr.s
class MsgVote(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "gov/MsgVote"
    proposal_id: str = attr.ib()
    voter: str = attr.ib()
    option: VoteOption = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgVote:
        """
        docstring
        """
        value = data["value"]
        return cls(value["proposal_id"], value["voter"], VoteOption(value["option"]))