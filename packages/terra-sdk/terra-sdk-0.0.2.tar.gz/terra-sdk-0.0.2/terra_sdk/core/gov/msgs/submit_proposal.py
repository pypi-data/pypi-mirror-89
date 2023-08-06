from __future__ import annotations
from typing import List

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

from terra_sdk.core.gov.proposal import CONTENT_TYPES, contents

__all__ = ["MsgSubmitProposal"]


@attr.s
class MsgSubmitProposal(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "gov/MsgSubmitProposal"
    content: CONTENT_TYPES = attr.ib()
    initial_deposit: List[Coin] = attr.ib()
    proposer: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgSubmitProposal:
        """
        docstring
        """
        value = data["value"]
        return cls(
            contents[value["content"]["type"]].from_data(value["content"]),
            [Coin.from_data(coin) for coin in value["initial_deposit"]],
            value["proposer"],
        )
