from __future__ import annotations

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["MarketParmasChanges"]


@attr.s
class MarketParmasChanges(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    poolrecoveryperiod: str = attr.ib()
    basepool: str = attr.ib()
    minspread: str = attr.ib()

    def to_data(self) -> dict:
        mp: dict = {}
        for k in self.__dict__.keys():
            if self.__dict__.get(k, "") != "":
                mp[k] = self.__dict__.get(k, "")
        return mp

    @classmethod
    def from_data(cls, data: dict) -> MarketParmasChanges:
        """
        docstring
        """
        return cls(
            data.get("poolrecoveryperiod", ""),
            data.get("basepool", ""),
            data.get("minspread", ""),
        )