from __future__ import annotations
import attr

from terra_sdk.utils.serdes import JsonDeserializable, JsonSerializable
from terra_sdk.core.gov.msgs.vote import VoteOption


__all__ = ["ProposalVote"]


@attr.s
class ProposalVote(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    proposal_id: str = attr.ib()
    voter: str = attr.ib()
    option: VoteOption = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ProposalVote:
        """
        docstring
        """
        return cls(data["proposal_id"], data["voter"], VoteOption(data["option"]))