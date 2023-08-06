from __future__ import annotations
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MsgStoreCode"]


@attr.s
class MsgStoreCode(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "wasm/MsgStoreCode"
    sender: str = attr.ib()
    wasm_byte_code: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgStoreCode:
        """
        docstring
        """
        value = data["value"]
        return cls(value["sender"], value["wasm_byte_code"])
