from __future__ import annotations

import attr
from typing import List, Union
from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from bech32 import bech32_decode, bech32_encode

from terra_sdk.utils.validation import (
    validate_acc_pubkey,
    validate_val_pubkey,
    validate_val_conspubkey,
)


@attr.s
class PublicKey(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type = "tendermint/PubKeySecp256k1"
    value: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> PublicKey:
        """
        docstring
        """
        return cls(data["value"])

    def to_data(self) -> dict:
        """
        docstring
        """
        return {"type": self.type, "value": self.value}


@attr.s
class MultiSigPublicKey(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    type = "tendermint/PubKeyMultisigThreshold"
    threshold: str = attr.ib()
    pubkeys: List[PublicKey] = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MultiSigPublicKey:
        """
        docstring
        """
        value = data["value"]
        return cls(
            value["threshold"],
            [PublicKey.from_data(pub_key) for pub_key in value["pubkeys"]],
        )


def get_pub_key(data: dict) -> Union[PublicKey, MultiSigPublicKey]:
    """
    docstring
    """
    if data["type"] == PublicKey.type:
        return PublicKey.from_data(data)
    return MultiSigPublicKey.from_data(data)


class AccPubKey(str):
    """`terrapub-` prefixed Bech32-enconded account public eky, works anywhere a `str` is
    accepted but will perform verification on the checksum.

    :param arg: string-convertable object to convert.
    """

    def __new__(cls, arg):
        validate_acc_pubkey(arg)
        return str.__new__(cls, arg)

    @property
    def val_pubkey(self) -> ValPubKey:
        """The associated validator public key."""
        decoded = bech32_decode(self)
        return ValPubKey(bech32_encode("terravalpub", decoded[1]))


class ValPubKey(str):
    """`terravalpub-` prefixed Bech32-enconded validator public key, works anywhere a `str`
    is accepted but will perform verification on the checksum.

    :param arg: string-convertable object to convert.
    """

    def __new__(cls, arg):
        validate_val_pubkey(arg)
        return str.__new__(cls, arg)

    @property
    def acc_pubkey(self) -> AccPubKey:
        """The associated account public key."""
        decoded = bech32_decode(self)
        return AccPubKey(bech32_encode("terrapub", decoded[1]))


class ValConsPubKey(str):
    """`terravalpub-` prefixed Bech32-enconded validator consensus public key, works \
    anywhere a `str` is accepted but will perform verification on the checksum.

    :param arg: string-convertable object to convert.
    """

    def __new__(cls, arg):
        validate_val_conspubkey(arg)
        return str.__new__(cls, arg)
