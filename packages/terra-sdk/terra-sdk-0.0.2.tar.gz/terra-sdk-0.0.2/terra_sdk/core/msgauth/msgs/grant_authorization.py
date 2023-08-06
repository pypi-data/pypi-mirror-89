from __future__ import annotations
from typing import Union

import attr

from terra_sdk.utils.serdes import JsonDeserializable, JsonSerializable

from .authorization import GenericAuthorization, SendAuthorization, get_authorization

__all__ = ["MsgGrantAuthorization"]


@attr.s
class MsgGrantAuthorization(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "msgauth/MsgGrantAuthorization"
    granter: str = attr.ib()
    grantee: str = attr.ib()
    authorization: Union[SendAuthorization, GenericAuthorization] = attr.ib()
    period: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgGrantAuthorization:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["granter"],
            value["grantee"],
            get_authorization(value["authorization"]),
            value["period"],
        )