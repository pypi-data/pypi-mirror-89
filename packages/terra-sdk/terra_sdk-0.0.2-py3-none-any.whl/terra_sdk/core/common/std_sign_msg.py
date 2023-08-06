from __future__ import annotations
from typing import List
import attr
from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

from .std_fee import StdFee
from terra_sdk.core.msgs import get_msgs, MSG_TYPES


@attr.s
class StdSignMsg(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    chain_id: str = attr.ib()
    account_number: str = attr.ib()
    sequence: str = attr.ib()
    fee: StdFee = attr.ib()
    msgs: List[MSG_TYPES] = attr.ib()
    memo: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> StdSignMsg:
        """
        docstring
        """
        value = data["value"]

        return cls(
            value["chain_id"],
            value["account_number"],
            value["sequence"],
            StdFee.from_data(value["fee"]),
            [get_msgs(msg) for msg in value["msgs"]],
            value["memo"],
        )