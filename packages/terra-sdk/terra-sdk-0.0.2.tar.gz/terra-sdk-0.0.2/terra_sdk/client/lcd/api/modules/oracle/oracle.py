from typing import List, Optional, Set, Union

from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.common import (
    AccAddress,
    Coin,
    Dec,
    ValAddress,
)

from .vote_info import (
    ExchangeRatePrevote,
    ExchangeRateVote,
    ExchangeRateAggregatePrevote,
    ExchangeRateAggregateVote,
)
from terra_sdk.utils.error import DenomNotFound

__all__ = ["OracleApi"]


class OracleApi(BaseApi):
    def votes(
        self, denom: Optional[str] = None, validator: Optional[ValAddress] = None
    ) -> List[ExchangeRateVote]:
        if validator is not None and denom is not None:
            res = self._api_get(f"/oracle/denoms/{denom}/votes/{validator}")
        elif validator:
            res = self._api_get(f"/oracle/voters/{validator}/votes")
        elif denom:
            res = self._api_get(f"/oracle/denoms/{denom}/votes")
        else:
            raise ValueError("arguments validator and denom cannot both be None")
        return [ExchangeRateVote.from_data(vote) for vote in res]

    def prevotes(
        self, denom: Optional[str] = None, validator: Optional[ValAddress] = None
    ) -> List[ExchangeRatePrevote]:
        if validator is not None and denom is not None:
            res = self._api_get(f"/oracle/denoms/{denom}/prevotes/{validator}")
        elif validator:
            res = self._api_get(f"/oracle/voters/{validator}/prevotes")
        elif denom:
            res = self._api_get(f"/oracle/denoms/{denom}/prevotes")
        else:
            raise ValueError("arguments validator and denom cannot both be None")
        return [ExchangeRatePrevote.from_data(prevote) for prevote in res]

    def aggregate_prevote(self, validator: ValAddress) -> ExchangeRateAggregatePrevote:
        """
        Gets the validator's aggregated prevote
        """

        res = self._api_get(f"/oracle/voters/{validator}/aggregate_prevote")
        return ExchangeRateAggregatePrevote.from_data(res)

    def aggregate_vote(self, validator: ValAddress) -> ExchangeRateAggregateVote:
        """
        Gets the validator's aggregated prevote info
        """
        res = self._api_get(f"/oracle/voters/{validator}/aggregate_vote")
        return ExchangeRateAggregateVote.from_data(res)

    def exchange_rates(self) -> List[Coin]:
        """Gets all exchange rates."""
        res = self._api_get("/oracle/denoms/exchange_rates")
        return [Coin.from_data(coin) for coin in res]

    def exchange_rate(self, denom: str) -> Coin:
        """Gets the exchange rate of LUNA against one denomination."""
        res = self.exchange_rates()
        denom_exists = False
        for er in res:
            if er.denom == denom:
                denom_exists = True
                return er
        if denom_exists == False:
            raise DenomNotFound(
                f"denom '{denom}' not found, available denoms: {res.denoms}"
            )
        return res

    def active_denoms(self) -> Set[str]:
        res = self._api_get("/oracle/denoms/actives")
        return res

    def feeder_address(self, validator: ValAddress) -> AccAddress:
        return self._api_get(f"/oracle/voters/{validator}/feeder")

    def misses(self, validator: ValAddress) -> int:
        res = self._api_get(f"/oracle/voters/{validator}/miss")
        return int(res)

    def parameters(self, key: Optional[str] = None) -> Union[dict, int, Dec, List[str]]:
        return self._api_get("/oracle/parameters")
