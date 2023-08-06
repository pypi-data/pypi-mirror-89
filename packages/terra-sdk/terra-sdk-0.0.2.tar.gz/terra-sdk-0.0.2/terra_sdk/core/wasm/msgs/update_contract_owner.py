from __future__ import annotations
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MsgUpdateContractOwner"]


@attr.s
class MsgUpdateContractOwner(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "wasm/MsgUpdateContractOwner"
    owner: str = attr.ib()
    new_owner: str = attr.ib()
    contract: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgUpdateContractOwner:
        """
        docstring
        """
        value = data["value"]
        return cls(value["owner"], value["new_owner"], value["contract"])