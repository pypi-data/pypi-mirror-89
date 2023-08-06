from __future__ import annotations
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin

__all__ = ["MsgMigrateContract"]


@attr.s
class MsgMigrateContract(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "wasm/MsgMigrateContract"
    owner: str = attr.ib()
    contract: str = attr.ib()
    new_code_id: str = attr.ib()
    migrate_msg: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgMigrateContract:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["owner"],
            value["contract"],
            value["new_code_id"],
            value["migrate_msg"],
        )
