from typing import List, Optional, Union

from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.common import AccAddress, Coin, ValAddress

from .validator import Validator
from .undelegation import UnbondingDelegation
from .redelegation import Redelegation
from .delegation import Delegation

__all__ = ["StakingApi"]

uLuna = "uluna"


class StakingApi(BaseApi):
    def delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
    ) -> List[Delegation]:
        """Queries the delegation between a delegator and a validator."""
        if delegator is not None and validator is not None:
            res = self._api_get(
                f"/staking/delegators/{delegator}/delegations/{validator}"
            )
            return [Delegation.from_data(res)]
        elif delegator:
            res = self._api_get(f"/staking/delegators/{delegator}/delegations")
        elif validator:
            res = self._api_get(f"/staking/validators/{validator}/delegations")
        else:
            raise TypeError("arguments delegator and validator cannot both be None")
        return [Delegation.from_data(d) for d in res]

    def delegation(self, delegator: AccAddress, validator: ValAddress) -> Delegation:
        return self.delegations(delegator, validator)[0]

    def unbonding_delegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator: Optional[ValAddress] = None,
    ) -> List[UnbondingDelegation]:
        if delegator is not None and validator is not None:
            res = self._api_get(
                f"/staking/delegators/{delegator}/unbonding_delegations/{validator}"
            )
            return [UnbondingDelegation.from_data(res)]
        elif delegator:
            res = self._api_get(
                f"/staking/delegators/{delegator}/unbonding_delegations"
            )
        elif validator:
            res = self._api_get(
                f"/staking/validators/{validator}/unbonding_delegations"
            )
        else:
            raise TypeError("arguments delegator and validator cannot both be None")
        return [UnbondingDelegation.from_data(ud) for ud in res]

    def unbonding_delegation(
        self, delegator: AccAddress, validator: ValAddress
    ) -> UnbondingDelegation:
        return self.unbonding_delegations(delegator, validator)[0]

    def redelegations(
        self,
        delegator: Optional[AccAddress] = None,
        validator_src: Optional[ValAddress] = None,
        validator_dst: Optional[ValAddress] = None,
    ) -> List[Redelegation]:
        params = {}
        if delegator:
            params["delegator"] = delegator
        if validator_src:
            params["validator_from"] = validator_src
        if validator_dst:
            params["validator_to"] = validator_dst
        res = self._api_get(f"/staking/redelegations", params=params)
        return [Redelegation.from_data(rd) for rd in res]

    def bonded_validators(self, delegator: AccAddress) -> List[Validator]:
        vs = self._api_get(f"/staking/delegators/{delegator}/validators")
        return [Validator.from_data(v) for v in vs]

    def validators(self, status: Optional[str] = None) -> List[Validator]:
        params = dict()
        if status is not None:
            params["status"] = status
        res = self._api_get("/staking/validators", params=params)
        return [Validator.from_data(v) for v in res]

    def validator(self, validator: ValAddress) -> Validator:
        res = self._api_get(f"/staking/validators/{validator}")
        return Validator.from_data(res)

    def pool(self, key: Optional[str] = None) -> Union[str, Coin]:
        res = self._api_get("/staking/pool")
        pool = {
            "bonded": Coin(uLuna, res["bonded_tokens"]),
            "not_bonded": Coin(uLuna, res["not_bonded_tokens"]),
        }
        return pool[key] if key else pool

    def parameters(self, key: Optional[str] = None) -> Union[str, dict]:
        res = self._api_get("/staking/parameters")
        return res[key] if key else res
