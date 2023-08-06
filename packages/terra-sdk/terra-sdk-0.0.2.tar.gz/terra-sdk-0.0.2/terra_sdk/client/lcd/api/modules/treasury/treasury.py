from typing import List
from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.common import Coin, Dec
from .policy import PolicyConstraints

__all__ = ["TreasuryApi"]


class TreasuryApi(BaseApi):
    def tax_cap(self, denom: str) -> Coin:
        res = self._api_get(f"/treasury/tax_cap/{denom}")
        return Coin(denom, res)

    def tax_rate(self) -> Dec:
        res = self._api_get("/treasury/tax_rate")  # tr
        return Dec.from_data(res)

    def reward_weight(self) -> Dec:
        res = self._api_get("/treasury/reward_weight")  # rw
        return Dec.from_data(res)

    def tax_proceeds(self) -> List[Coin]:
        res = self._api_get("/treasury/tax_proceeds")
        return [Coin.from_data(coin) for coin in res]

    def seigniorage_proceeds(self) -> Coin:
        res = self._api_get("/treasury/seigniorage_proceeds")
        return Coin("uluna", int(res))  # TODO: stop using magic string

    def parameters(self) -> dict:
        res = self._api_get("/treasury/parameters")
        res["tax_policy"] = PolicyConstraints.from_data(res["tax_policy"])
        res["reward_policy"] = PolicyConstraints.from_data(res["reward_policy"])
        return res