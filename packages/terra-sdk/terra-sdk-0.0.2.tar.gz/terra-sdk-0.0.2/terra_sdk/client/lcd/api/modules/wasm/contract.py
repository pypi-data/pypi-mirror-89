from __future__ import annotations
import attr
from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable


class ContractInfo(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    address: str = attr.ib()
    owner: str = attr.ib()
    code_id: str = attr.ib()
    init_msg: str = attr.ib()
    migratable: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> ContractInfo:
        """
        docstring
        """
        return cls(
            data["address"],
            data["owner"],
            data["code_id"],
            data["init_msg"],
            data["migratable"],
        )