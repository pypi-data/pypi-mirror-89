from typing import List

from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.common.coin import Coin

__all__ = ["SupplyApi"]


class SupplyApi(BaseApi):
    def total(self) -> List[Coin]:
        res = self._api_get("/supply/total")
        return [Coin.from_data(coin) for coin in res]
