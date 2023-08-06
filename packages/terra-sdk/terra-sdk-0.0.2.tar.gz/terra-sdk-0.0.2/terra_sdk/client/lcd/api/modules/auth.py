import warnings
from typing import Union

from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.auth import BaseAccount, VestingAccount
from terra_sdk.utils.error import AccountNotFoundWarning

__all__ = ["account_info_type", "AuthApi"]
account_info_type = Union[BaseAccount, VestingAccount]


class AuthApi(BaseApi):
    def account_info(self, address: str) -> Union[account_info_type]:
        info = self._api_get(f"/auth/accounts/{address}")
        if info["type"] == "core/Account":
            res = BaseAccount.from_data(info)
        elif info["type"] == "core/LazyGradedVestingAccount":
            res = VestingAccount.from_data(info)
        else:
            raise ValueError("could not deserialize account in auth.acc_info")
        if res.address is None:
            warnings.warn(
                "Account was not found; perhaps wrong chain or account needs to first be sent funds.",
                AccountNotFoundWarning,
            )
        return res
