from __future__ import annotations

import attr

from terra_sdk.utils.serdes import JsonDeserializable, JsonSerializable
from terra_sdk.core.common import Coin


__all__ = ["PolicyConstraints"]


@attr.s
class PolicyConstraints(JsonDeserializable, JsonSerializable):
    """
    docstring
    """

    rate_min: str = attr.ib()
    rate_max: str = attr.ib()
    cap: Coin = attr.ib()
    change_max: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> PolicyConstraints:
        """
        docstring
        """
        return cls(
            data["rate_min"],
            data["rate_max"],
            Coin.from_data(data["cap"]),
            data["change_max"],
        )