from __future__ import annotations
from typing import List
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.msgs import MSG_TYPES, get_msgs
from .std_fee import StdFee
from .std_signature import StdSignature


@attr.s
class StdTx(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type = "core/StdTx"

    msg: List[MSG_TYPES] = attr.ib()
    fee: StdFee = attr.ib()
    signatures: List[StdSignature] = attr.ib()
    memo: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> StdTx:
        """
        docstring
        """
        value = data["value"]
        return cls(
            [get_msgs(msg_data) for msg_data in value["msg"]],
            StdFee.from_data(value["fee"]),
            [StdSignature.from_data(sig) for sig in value["signatures"]],
            value["memo"],
        )