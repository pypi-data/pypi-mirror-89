from __future__ import annotations
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MsgRevokeAuthorization"]


@attr.s
class MsgRevokeAuthorization(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "msgauth/MsgRevokeAuthorization"
    granter: str = attr.ib()
    grantee: str = attr.ib()
    authorization_msg_type: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgRevokeAuthorization:
        """
        docstring
        """
        value = data["value"]
        return cls(value["granter"], value["grantee"], value["authorization_msg_type"])