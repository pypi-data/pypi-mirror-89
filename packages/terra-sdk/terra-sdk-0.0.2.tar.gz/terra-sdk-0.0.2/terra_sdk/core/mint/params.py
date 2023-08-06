from __future__ import annotations
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable


@attr.s
class MintParmasChanges(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    MintDenom: str = attr.ib()
    InflationRateChange: str = attr.ib()
    InflationMax: str = attr.ib()
    InflationMin: str = attr.ib()
    GoalBonded: str = attr.ib()
    BlocksPerYear: str = attr.ib()

    def to_data(self) -> dict:
        mp: dict = {}
        for k in self.__dict__.keys():
            if self.__dict__.get(k, "") != "":
                mp[k] = self.__dict__.get(k, "")
        return mp

    @classmethod
    def from_data(cls, data: dict) -> MintParmasChanges:
        """
        docstring
        """
        return cls(
            data.get("MintDenom", ""),
            data.get("InflationRateChange", ""),
            data.get("InflationMax", ""),
            data.get("InflationMin", ""),
            data.get("GoalBonded", ""),
            data.get("BlocksPerYear", ""),
        )