from __future__ import annotations
from typing import List
import attr

from terra_sdk.utils.serdes import JsonDeserializable, JsonSerializable
from terra_sdk.core.common import Coin

__all__ = ["ProposalDeposit"]


@attr.s
class ProposalDeposit(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    proposal_id: str = attr.ib()
    depositor: str = attr.ib()
    amount: List[Coin] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ProposalDeposit:
        """
        docstring
        """
        return cls(
            data["proposal_id"],
            data["depositor"],
            [Coin.from_data(coin) for coin in data["amount"]],
        )