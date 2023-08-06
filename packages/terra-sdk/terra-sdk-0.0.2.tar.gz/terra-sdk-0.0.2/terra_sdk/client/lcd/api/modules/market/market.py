from typing import Optional, Union

from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.common import Coin, Dec

__all__ = ["MarketApi"]


class MarketApi(BaseApi):
    def swap_rate(self, offer_coin: Coin, ask_denom: str) -> Coin:
        params = {
            "offer_coin": f"{int(offer_coin.amount)}{offer_coin.denom}",
            "ask_denom": ask_denom,
        }
        res = self._api_get(f"/market/swap", params=params)
        return Coin.from_data(res)

    def terra_pool_delta(self) -> Dec:
        res = self._api_get("/market/terra_pool_delta")
        return Dec.from_data(res)

    def parameters(self, key: Optional[str] = None) -> Union[Dec, dict]:
        res = self._api_get("/market/parameters")
        p = res
        p["pool_recovery_period"] = int(p["pool_recovery_period"])
        p["base_pool"] = Dec.from_data(p["base_pool"])
        p["min_spread"] = Dec.from_data(p["min_spread"])
        return p[key] if key else p
