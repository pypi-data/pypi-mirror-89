from typing import Dict, List, Union

from .lcd.api.modules import (
    AuthApi,
    BankApi,
    DistributionApi,
    GovApi,
    MarketApi,
    MintApi,
    MsgAuthApi,
    OracleApi,
    SlashingApi,
    StakingApi,
    SupplyApi,
    TreasuryApi,
    WasmApi,
    TxApi,
)
from .tendermint import TendermintApi
from .lcd_client import LcdClient
from terra_sdk.key import Key
from .wallet import Wallet

from terra_sdk.utils.error import DenomNotFound
from terra_sdk.core.common.coin import Coin


class Terra(object):
    # TODO: Dropping circular imports

    def __init__(
        self,
        chain_id: str,
        lcd_url: str,
        ws_url: str = None,
        gas_prices: List[Coin] = None,
        gas_adjustment: Union[float, str] = "1.4",  # sensible defaults
    ):
        gas_prices = gas_prices or [Coin("uluna", "0.015")]  # sensible defaults

        self.gas_prices = gas_prices
        self.gas_adjustment = gas_adjustment

        # LCD APIs
        self.lcd = LcdClient(self, lcd_url)

        # LCD module APIs
        self._auth = AuthApi(self)
        self._bank = BankApi(self)
        self._supply = SupplyApi(self)
        self._distribution = DistributionApi(self)
        self._staking = StakingApi(self)
        self._slashing = SlashingApi(self)
        self._oracle = OracleApi(self)
        self._market = MarketApi(self)
        self._mint = MintApi(self)
        self._msgauth = MsgAuthApi(self)
        self._treasury = TreasuryApi(self)
        self._gov = GovApi(self)
        self._wasm = WasmApi(self)

        # LCD lower-level APIs
        self._tendermint = TendermintApi(self)
        self._tx = TxApi(self)

        # LCD query APIs
        # self._blocks = jigu.client.object_query.BlocksQuery(self)

        # if no chain_id, trust the node's chain_id
        if chain_id is None:
            # TODO: add warning if not same!
            self.chain_id = self.node_info()["node_info"]["network"]
        else:
            self.chain_id = chain_id

        # WebSocket APIs
        # self.ws = WebSocketClient(self, ws_url)

    def __repr__(self):
        s = self
        return f"Terra('{s.chain_id}', '{s.lcd.url}')"

    def __str__(self):
        return f"{self.chain_id} via {self.lcd.url}"

    # Terra Core Module APIs provided through LCD:

    @property
    def auth(self):
        return self._auth

    @property
    def bank(self):
        return self._bank

    @property
    def supply(self):
        return self._supply

    @property
    def distribution(self):
        return self._distribution

    @property
    def staking(self):
        return self._staking

    @property
    def slashing(self):
        return self._slashing

    @property
    def oracle(self):
        return self._oracle

    @property
    def market(self):
        return self._market

    @property
    def mint(self):
        return self._mint

    @property
    def msgauth(self):
        return self._msgauth

    @property
    def treasury(self):
        return self._treasury

    @property
    def gov(self):
        return self._gov

    @property
    def tx(self):
        return self._tx

    @property
    def wasm(self):
        return self._wasm

    def is_connected(self) -> bool:
        """Checks that a connection can be made to the node specified, and has the same `chain_id`."""
        try:
            node_info = self.node_info()
            return self.chain_id == node_info["node_info"]["network"]
        except:  # not recommended, but if we run into any error, we are not connected.
            return False

    # lower-level APIs

    def is_syncing(self) -> bool:
        """Checks whether the node is currently syncing with the blockchain."""
        return self._tendermint.syncing()

    def node_info(self) -> Dict[str, dict]:
        """Get information about the node."""
        return self._tendermint.node_info()

    # Convenient Aliases for TX

    def tx_info(self, *args, **kwargs):
        return self._tx.tx_info(*args, **kwargs)

    def estimate_fee(self, *args, **kwargs):
        return self._tx.estimate_fee(*args, **kwargs)

    def broadcast(self, *args, **kwargs):
        return self._tx.broadcast(*args, **kwargs)

    # Object query based APIs

    def wallet(self, arg: Key) -> Wallet:
        return Wallet(self, arg)