from terra_sdk.client.lcd.api.modules.distribution import params
from typing import List, Optional, Union
from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.common import Coin, Dec, AccAddress

from .code import CodeInfo
from .contract import ContractInfo

__all__ = ["WasmApi"]


class WasmApi(BaseApi):
    def code_info(self, code_id: int) -> CodeInfo:
        """
        return code info
        """
        uri = f"/wasm/codes/${code_id}"
        info = self._api_get(uri)
        return CodeInfo.from_data(info)

    def contract_info(self, contract_address: AccAddress) -> ContractInfo:
        """
        return contract info
        """
        uri = f"/wasm/contracts/{contract_address}"
        info = self._api_get(uri)
        return ContractInfo.from_data(info)

    def contract_query(self, contract_address: AccAddress, query: dict) -> dict:
        """
        return contract store info
        """
        uri = f"/wasm/contracts/{contract_address}/store"
        return self._api_get(uri, params=query)

    def parameters(self, key: Optional[str] = None) -> Union[dict, str]:
        """
        docstring
        """
        uri = f"/wasm/parameters"
        params = self._api_get(uri)
        return params[key] if key else params