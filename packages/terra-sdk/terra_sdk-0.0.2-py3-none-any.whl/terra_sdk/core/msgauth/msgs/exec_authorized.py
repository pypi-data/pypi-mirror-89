from __future__ import annotations
from typing import List, TYPE_CHECKING
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

if TYPE_CHECKING:
    from terra_sdk.core.msgs import MSG_TYPES

__all__ = ["MsgExecAuthorized"]


@attr.s
class MsgExecAuthorized(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type = "msgauth/MsgExecAuthorized"
    grantee: str = attr.ib()
    msgs: List[MSG_TYPES] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgExecAuthorized:
        """
        docstring
        """
        from terra_sdk.core.msgs import get_msgs

        value = data["value"]
        return cls(value["grantee"], [get_msgs(msg) for msg in value["msgs"]])