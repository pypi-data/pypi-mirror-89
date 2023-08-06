from __future__ import annotations

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable

__all__ = ["DistributionParmasChanges"]


@attr.s
class DistributionParmasChanges(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    communitytax: str = attr.ib()
    baseproposerreward: str = attr.ib()
    bonusproposerreward: str = attr.ib()
    withdrawaddrenabled: str = attr.ib()

    def to_data(self) -> dict:
        mp: dict = {}
        for k in self.__dict__.keys():
            if self.__dict__.get(k, "") != "":
                mp[k] = self.__dict__.get(k, "")
        return mp

    @classmethod
    def from_data(cls, data: dict) -> DistributionParmasChanges:
        """
        docstring
        """
        return cls(
            data.get("communitytax", ""),
            data.get("baseproposerreward", ""),
            data.get("bonusproposerreward", ""),
            data.get("withdrawaddrenabled", ""),
        )