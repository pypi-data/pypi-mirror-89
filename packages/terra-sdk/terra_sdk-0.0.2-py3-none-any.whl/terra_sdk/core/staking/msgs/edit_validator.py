from __future__ import annotations

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.staking.validator import Description

__all__ = ["MsgEditValidator"]


@attr.s
class MsgEditValidator(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "staking/MsgEditValidator"
    Description: Description = attr.ib()
    address: str = attr.ib()
    commission_rate: str = attr.ib()
    min_self_delegation: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgEditValidator:
        """
        docstring
        """
        value = data["value"]
        return cls(
            Description.from_data(value["Description"]),
            value["address"],
            value["commission_rate"],
            value["min_self_delegation"],
        )