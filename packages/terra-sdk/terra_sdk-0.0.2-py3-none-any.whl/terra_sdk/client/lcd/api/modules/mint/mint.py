from typing import Optional, Union

from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.common import Dec

__all__ = ["MintApi"]


class MintApi(BaseApi):
    def inflation(self) -> Dec:
        res = self._api_get(f"/minting/inflation")
        return Dec.from_data(res)

    def annual_provisions(self) -> Dec:
        res = self._api_get("/minting/annual-provisions")
        return Dec.from_data(res)

    def parameters(self, key: Optional[str] = None) -> Union[Dec, dict]:
        res = self._api_get("/minting/parameters")
        return res[key] if key else res
