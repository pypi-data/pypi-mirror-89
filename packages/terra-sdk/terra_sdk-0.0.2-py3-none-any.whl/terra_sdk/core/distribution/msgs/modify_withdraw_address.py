from __future__ import annotations

import attr
from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MsgModifyWithdrawAddress"]


@attr.s
class MsgModifyWithdrawAddress(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "distribution/MsgModifyWithdrawAddress"
    delegator_address: str = attr.ib()
    withdraw_address: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgModifyWithdrawAddress:
        """
        docstring
        """
        value = data["value"]
        return cls(value["delegator_address"], value["withdraw_address"])