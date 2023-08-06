from __future__ import annotations
from typing import Union
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from .public_key import MultiSigPublicKey, PublicKey, get_pub_key


@attr.s
class StdSignature(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    signature: str = attr.ib()
    pub_key: Union[PublicKey, MultiSigPublicKey] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> StdSignature:
        """
        docstring
        """
        return cls(data["signature"], get_pub_key(data["pub_key"]))