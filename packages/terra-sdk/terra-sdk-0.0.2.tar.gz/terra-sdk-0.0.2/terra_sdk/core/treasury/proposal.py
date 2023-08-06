from __future__ import annotations
import attr
from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable


@attr.s
class TaxRateUpdateProposalContent(JsonSerializable, JsonDeserializable):
    type: str = "treasury/TaxRateUpdateProposal"
    title: str = attr.ib()
    description: str = attr.ib()
    tax_rate: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> TaxRateUpdateProposalContent:
        """
        docstring
        """
        value = data["value"]
        return cls(value["title"], value["description"], value["tax_rate"])


@attr.s
class RewardWeightUpdateProposalContent(JsonSerializable, JsonDeserializable):
    type: str = "treasury/RewardWeightUpdateProposal"
    title: str = attr.ib()
    description: str = attr.ib()
    reward_weight: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> RewardWeightUpdateProposalContent:
        """
        docstring
        """
        value = data["value"]
        return cls(value["title"], value["description"], value["reward_weight"])