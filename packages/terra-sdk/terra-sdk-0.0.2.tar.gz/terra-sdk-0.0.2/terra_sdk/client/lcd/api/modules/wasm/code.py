from __future__ import annotations
import attr
from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable


class CodeInfo(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    code_id: str = attr.ib()
    code_hash: str = attr.ib()
    creator: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> CodeInfo:
        """
        docstring
        """
        return cls(data["code_id"], data["code_hash"], data["creator"])