from __future__ import annotations
import attr

from terra_sdk.utils.serdes import JsonDeserializable, JsonSerializable

__all__ = ["SigningInfo"]


@attr.s
class SigningInfo(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    address: str = attr.ib()
    start_height: str = attr.ib()
    index_offset: str = attr.ib()
    jailed_until: str = attr.ib()
    tombstoned: str = attr.ib()
    missed_blocks_counter: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> SigningInfo:
        """
        docstring
        """
        return cls(
            data["address"],
            data["start_height"],
            data["index_offset"],
            data["jailed_until"],
            data["tombstoned"],
            data["missed_blocks_counter"],
        )