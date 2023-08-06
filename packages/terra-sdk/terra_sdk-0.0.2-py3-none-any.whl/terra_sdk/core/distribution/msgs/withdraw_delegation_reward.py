from __future__ import annotations
import attr

from terra_sdk.core.common.coin import Coin
from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MsgWithdrawDelegationReward"]


@attr.s
class MsgWithdrawDelegationReward(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "distribution/MsgWithdrawDelegationReward"
    delegator_address: str = attr.ib()
    validator_address: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgWithdrawDelegationReward:
        """
        docstring
        """
        value = data["value"]
        return cls(value["delegator_address"], value["validator_address"])