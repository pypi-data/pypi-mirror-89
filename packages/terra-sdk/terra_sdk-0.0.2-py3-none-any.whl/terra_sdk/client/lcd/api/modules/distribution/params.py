from __future__ import annotations

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.dec import Dec

__all__ = ["DistributionParameters"]


@attr.s
class DistributionParameters(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    community_tax: str = attr.ib()
    base_proposer_reward: str = attr.ib()
    bonus_proposer_reward: str = attr.ib()
    withdraw_addr_enabled: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> DistributionParameters:
        """
        docstring
        """

        return cls(
            data["community_tax"],
            data["base_proposer_reward"],
            data["bonus_proposer_reward"],
            data["withdraw_addr_enabled"],
        )