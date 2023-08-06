from __future__ import annotations

import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable


@attr.s
class Description(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    moniker: str = attr.ib()
    identity: str = attr.ib()
    website: str = attr.ib()
    security_contact: str = attr.ib()
    details: str = attr.ib()

    def to_data(self) -> dict:
        mp: dict = {}
        for k in self.__dict__.keys():
            if self.__dict__.get(k, "") != "":
                mp[k] = self.__dict__.get(k)
        return mp

    @classmethod
    def from_data(cls, data: dict) -> Description:
        """
        docstring
        """
        return cls(
            data.get("moniker", ""),
            data.get("identity", ""),
            data.get("website", ""),
            data.get("security_contact", ""),
            data.get("details", ""),
        )


@attr.s
class CommissionRate(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    rate: str = attr.ib()
    max_rate: str = attr.ib()
    max_change_rate: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> CommissionRate:
        """
        docstring
        """
        return cls(data["rate"], data["max_rate"], data["max_change_rate"])