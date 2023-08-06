from __future__ import annotations
from typing import Union
import attr
import copy

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable


@attr.s
class OracleWhitelist(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    name: str = attr.ib()
    tobin_tax: str = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> OracleWhitelist:
        """
        docstring
        """
        return cls(data["name"], data["tobin_tax"])


@attr.s
class OracleParamsChanges(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    voteperiod: str = attr.ib()
    votethreshold: str = attr.ib()
    rewardband: str = attr.ib()
    rewarddistributionwindow: str = attr.ib()
    whitelist: Union[str, OracleWhitelist] = attr.ib()
    slashfraction: str = attr.ib()
    slashwindow: str = attr.ib()
    minvalidperwindow: str = attr.ib()

    def to_data(self) -> dict:
        mp: dict = {}
        for k in self.__dict__.keys():
            if self.__dict__.get(k, "") != "":
                mp[k] = self.__dict__.get(k, "")
        return mp

    @classmethod
    def from_data(cls, data: dict) -> OracleParamsChanges:
        """
        docstring
        """
        tmp_data = copy.deepcopy(data)
        if data.get("whitelist", "") != "":
            whitelisted = [
                OracleWhitelist.from_data(new_d) for new_d in data["whitelist"]
            ]
            tmp_data["whitelist"] = whitelisted

        return cls(
            tmp_data.get("voteperiod", ""),
            tmp_data.get("votethreshold", ""),
            tmp_data.get("rewardband", ""),
            tmp_data.get("rewarddistributionwindow", ""),
            tmp_data.get("whitelist", ""),
            tmp_data.get("slashfraction", ""),
            tmp_data.get("slashwindow", ""),
            tmp_data.get("minvalidperwindow", ""),
        )