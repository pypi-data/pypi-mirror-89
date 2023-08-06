from __future__ import annotations
import attr

from terra_sdk.core.common.coin import Coin
from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MsgWithdrawValidatorCommission"]


@attr.s
class MsgWithdrawValidatorCommission(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "distribution/MsgWithdrawValidatorCommission"
    validator_address: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgWithdrawValidatorCommission:
        """
        docstring
        """
        return cls(data["value"]["validator_address"])
