from __future__ import annotations
import attr
from terra_sdk.core.msgauth.msgs.authorization import (
    AUTHORIZATION_TYPES,
    get_authorization,
)
from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable


@attr.s
class AuthorizationInfo(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    authorization: AUTHORIZATION_TYPES = attr.ib()
    expiration: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> AuthorizationInfo:
        """
        docstring
        """
        return cls(get_authorization(data["authorization"]), data["expiration"])