from __future__ import annotations
from typing import List
import attr
from terra_sdk.utils.serdes import JsonDeserializable, JsonSerializable

from .tx_log import TxLog


@attr.s
class TxBroadcastResult(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    height: str = attr.ib()
    txhash: str = attr.ib()
    raw_log: str = attr.ib()
    gas_wanted: str = attr.ib()
    gas_used: str = attr.ib()
    logs: List[TxLog] = attr.ib()
    code: str = attr.ib()
    codespace: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> TxBroadcastResult:
        """
        docstring
        """
        return cls(
            data["height"],
            data["txhash"],
            data["raw_log"],
            data["gas_wanted"],
            data["gas_used"],
            [TxLog.from_data(log) for log in data["logs"]],
            data.get("code", ""),
            data.get("codespace", ""),
        )