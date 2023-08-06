from typing import List, Optional, Union

from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.common import Dec
from terra_sdk.core.common.public_key import ValConsPubKey
from .signing_info import SigningInfo

__all__ = ["SlashingApi"]


class SlashingApi(BaseApi):
    def signing_infos(self, pubkey: ValConsPubKey = None) -> Union[List[SigningInfo]]:
        uri = f"/slashing/signing_infos"
        if pubkey is not None:
            uri = f"/slashing/validators/{pubkey}/signing_info"
        res = self._api_get(uri)
        if pubkey is not None:
            return [SigningInfo.from_data(res)]
        return [SigningInfo.from_data(si) for si in res]

    def parameters(self, key: Optional[str] = None) -> Union[int, Dec, dict]:
        res = self._api_get("/slashing/parameters")
        return res[key] if key else res
