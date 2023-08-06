from typing import List, Union

from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.common.coin import Coins

__all__ = ["BankApi"]


class BankApi(BaseApi):
    def balance(self, address: str) -> Union[List]:
        """Gets the balance of an account by its address."""
        res = self._api_get(f"/bank/balances/{address}")
        return Coins.from_data(res)
