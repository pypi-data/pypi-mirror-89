from __future__ import annotations
from typing import Union
import attr
import copy

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable
from terra_sdk.core.common.coin import Coin


@attr.s
class PolicyConstraints(JsonSerializable, JsonDeserializable):
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


@attr.s
class TreasuryParamsChanges(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    taxpolicy: Union[PolicyConstraints, str] = attr.ib()  # Policy Constraints
    rewardpolicy: Union[PolicyConstraints, str] = attr.ib()  # Policy Constraints
    seigniorageburdentarget: str = attr.ib()
    miningincrement: str = attr.ib()
    windowshort: str = attr.ib()
    windowlong: str = attr.ib()
    windowprobation: str = attr.ib()

    def to_data(self) -> dict:
        mp: dict = {}
        for k in self.__dict__.keys():
            if self.__dict__.get(k, "") != "":
                mp[k] = self.__dict__.get(k, "")
        return mp

    @classmethod
    def from_data(cls, data: dict) -> TreasuryParamsChanges:
        """
        docstring
        """
        tmp_data = copy.deepcopy(data)
        if data.get("taxpolicy", "") != "":
            tmp_data["taxpolicy"] = PolicyConstraints.from_data(data["taxpolicy"])

        if data.get("rewardpolicy", "") != "":
            tmp_data["rewardpolicy"] = PolicyConstraints.from_data(data["rewardpolicy"])

        return cls(
            tmp_data.get("taxpolicy", ""),
            tmp_data.get("rewardpolicy", ""),
            tmp_data.get("seigniorageburdentarget", ""),
            tmp_data.get("miningincrement", ""),
            tmp_data.get("windowshort", ""),
            tmp_data.get("windowlong", ""),
            tmp_data.get("windowprobation", ""),
        )