from __future__ import annotations
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.staking.validator import Description, CommissionRate


@attr.s
class Commission(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    commission_rates: CommissionRate = attr.ib()
    update_time: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> Commission:
        """
        docstring
        """
        return cls(
            CommissionRate.from_data(data["commission_rates"]), data["update_time"]
        )


@attr.s
class Validator(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    operator_address: str = attr.ib()
    consensus_pubkey: str = attr.ib()
    tokens: str = attr.ib()
    jailed: str = attr.ib()
    status: str = attr.ib()
    delegator_shares: str = attr.ib()
    description: Description = attr.ib()
    unbonding_height: str = attr.ib()
    unbonding_time: str = attr.ib()
    commission: Commission = attr.ib()
    min_self_delegation: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict):
        """
        docstring
        """
        return cls(
            data["operator_address"],
            data["consensus_pubkey"],
            data["tokens"],
            data["jailed"],
            data["status"],
            data["delegator_shares"],
            Description.from_data(data["description"]),
            data["unbonding_height"],
            data["unbonding_time"],
            Commission.from_data(data["commission"]),
            data["min_self_delegation"],
        )