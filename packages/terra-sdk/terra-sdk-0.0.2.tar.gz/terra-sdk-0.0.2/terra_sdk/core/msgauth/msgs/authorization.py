from __future__ import annotations
from typing import List, Union
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin


@attr.s
class GenericAuthorization(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type: str = "msgauth/GenericAuthorization"
    grant_msg_type: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> GenericAuthorization:
        """
        docstring
        """
        value = data["value"]
        return cls(value["grant_msg_type"])


@attr.s
class SendAuthorization(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type = "msgauth/SendAuthorization"
    spend_limit: List[Coin] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> SendAuthorization:
        """
        docstring
        """
        value = data["value"]
        return cls([Coin.from_data(coin) for coin in value["spend_limit"]])


AUTHORIZATION_TYPES = Union[GenericAuthorization, SendAuthorization]


def get_authorization(data: dict) -> Union[GenericAuthorization, SendAuthorization]:
    """
    docstring
    """

    if data["type"] == "msgauth/GenericAuthorization":
        return GenericAuthorization.from_data(data)
    elif data["type"] == "msgauth/SendAuthorization":
        return SendAuthorization.from_data(data)
    raise Exception("Authorization types not found")