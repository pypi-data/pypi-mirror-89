from __future__ import annotations
import attr

from terra_sdk.utils.serdes import JsonSerializable, JsonDeserializable


@attr.s
class SlashingParamsChanges(JsonSerializable, JsonDeserializable):
    """
    docstring
    """

    MaxEvidenceAge: str = attr.ib()
    SignedBlocksWindow: str = attr.ib()
    MinSignedPerWindow: str = attr.ib()
    DowntimeJailDuration: str = attr.ib()
    SlashFractionDoubleSign: str = attr.ib()
    SlashFractionDowntime: str = attr.ib()

    def to_data(self) -> dict:
        mp: dict = {}
        for k in self.__dict__.keys():
            if self.__dict__.get(k, "") != "":
                mp[k] = self.__dict__.get(k, "")
        return mp

    @classmethod
    def from_data(cls, data: dict) -> SlashingParamsChanges:
        """
        docstring
        """

        return cls(
            data.get("MaxEvidenceAge", ""),
            data.get("SignedBlocksWindow", ""),
            data.get("MinSignedPerWindow", ""),
            data.get("DowntimeJailDuration", ""),
            data.get("SlashFractionDoubleSign", ""),
            data.get("SlashFractionDowntime", ""),
        )