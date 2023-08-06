from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.common import AccAddress, Coins, ValAddress

from .delegator_rewards import DelegatorRewards
from .validator_rewards import ValidatorRewards
from .params import DistributionParameters

__all__ = ["DistributionApi"]


class DistributionApi(BaseApi):
    def rewards(self, delegator: AccAddress) -> DelegatorRewards:
        """Get an account's delegation rewards."""
        res = self._api_get(f"/distribution/delegators/{delegator}/rewards")
        return DelegatorRewards.from_data(res)

    def withdraw_address(self, delegator: AccAddress) -> AccAddress:
        return self._api_get(f"/distribution/delegators/{delegator}/withdraw_address")

    def validator_rewards(self, validator: ValAddress) -> ValidatorRewards:
        res = self._api_get(f"/distribution/validators/{validator}")
        return ValidatorRewards.from_data(res)

    def community_pool(self) -> Coins:
        res = self._api_get("/distribution/community_pool")
        return Coins.from_data(res)

    def parameters(self) -> DistributionParameters:
        res = self._api_get("/distribution/parameters")
        return DistributionParameters.from_data(res)
