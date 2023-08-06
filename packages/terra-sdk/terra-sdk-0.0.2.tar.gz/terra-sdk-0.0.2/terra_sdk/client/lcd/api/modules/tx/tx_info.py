from __future__ import annotations
from typing import List
from terra_sdk.client.lcd.api.modules.tx.tx_log import TxLog
import attr

from terra_sdk.utils.serdes import JsonDeserializable, JsonSerializable
from .tx_log import TxLog
from terra_sdk.core.common.std_tx import StdTx


@attr.s
class TxInfo(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    height: str = attr.ib()
    txhash: str = attr.ib()
    raw_log: str = attr.ib()
    logs: List[TxLog] = attr.ib()
    gas_wanted: str = attr.ib()
    gas_used: str = attr.ib()
    tx: StdTx = attr.ib()
    timestamp: str = attr.ib()
    code: str = attr.ib()
    codespace: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> TxInfo:
        """
        docstring
        """
        return cls(
            data["height"],
            data["txhash"],
            data["raw_log"],
            [TxLog.from_data(log) for log in data["logs"]],
            data["gas_wanted"],
            data["gas_used"],
            StdTx.from_data(data["tx"]),
            data["timestamp"],
            data["code"],
            data["codespace"],
        )