from __future__ import annotations
from typing import Union

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin
from terra_sdk.core.treasury.proposal import (
    TaxRateUpdateProposalContent,
    RewardWeightUpdateProposalContent,
)


@attr.s
class ParamChanges(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    subspace = attr.ib()
    key = attr.ib()
    value = (
        attr.ib()
    )  # TODO: this value will be string for now. will add the params changes value with it

    @classmethod
    def from_data(cls, data: dict) -> ParamChanges:
        """
        docstring
        """
        return cls(data["subspace"], data["key"], data["value"])


@attr.s
class ParamsChangeProposalContent(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type = "params/ParameterChangeProposal"
    title = attr.ib()
    description = attr.ib()
    changes = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ParamsChangeProposalContent:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["title"],
            value["description"],
            [ParamChanges.from_data(change) for change in value["changes"]],
        )


@attr.s
class TextProposalContent(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type = "gov/TextProposal"
    title = attr.ib()
    description = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> TextProposalContent:
        """
        docstring
        """
        value = data["value"]
        return cls(value["title"], value["description"])


@attr.s
class CommunityPoolSpendProposalContent(JsonSerializable, JsonDeserializable):

    type = "distribution/CommunityPoolSpendProposal"
    title = attr.ib()
    description = attr.ib()
    recipient = attr.ib()
    amount = attr.ib()  # Coins

    @classmethod
    def from_data(cls, data: dict) -> CommunityPoolSpendProposalContent:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["title"],
            value["description"],
            value["recipient"],
            [Coin.from_data(coin) for coin in value["amount"]],
        )


CONTENT_TYPES = Union[
    ParamsChangeProposalContent,
    TextProposalContent,
    CommunityPoolSpendProposalContent,
    TaxRateUpdateProposalContent,
    RewardWeightUpdateProposalContent,
]

contents: dict = {
    "params/ParameterChangeProposal": ParamsChangeProposalContent,
    "gov/TextProposal": TextProposalContent,
    "distribution/CommunityPoolSpendProposal": CommunityPoolSpendProposalContent,
    "treasury/TaxRateUpdateProposal": TaxRateUpdateProposalContent,
    "treasury/RewardWeightUpdateProposal": RewardWeightUpdateProposalContent,
}