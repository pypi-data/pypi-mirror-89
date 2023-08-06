from __future__ import annotations
from terra_sdk.client.lcd.api.modules.distribution.delegator_rewards import (
    DelegatorRewards,
    ValidatorReward,
)

from typing import Dict, List, Optional, Union, TYPE_CHECKING

from cached_property import cached_property

from terra_sdk.core.auth.base_account import BaseAccount
from terra_sdk.core.auth.vesting_account import VestingAccount

if TYPE_CHECKING:
    from terra_sdk.client.terra import Terra

from terra_sdk.core.common import (
    AccAddress,
    Coin,
    Coins,
    ValAddress,
)
from terra_sdk.client.lcd.api.modules.staking import (
    Validator,
    Delegation,
    Redelegation,
    UnbondingDelegation,
)
from terra_sdk.utils.validation import validate_val_address


class AccountQuery(object):
    def __init__(self, terra: Terra, address: str):
        self.terra = terra
        self.address = AccAddress(address)

    def __str__(self):
        return self.address

    def __repr__(self):
        return f"AccountQuery({self.address!r}) -> {self.terra}"

    @cached_property
    def validator(self):
        return self.terra.staking.validator(self.address.val_address)

    # Auth

    def info(self) -> Union[BaseAccount, VestingAccount]:
        return self.terra.auth.account_info(self.address)

    # Bank

    def balance(self, denom: Optional[str] = None) -> Union[Coin, Coins]:
        res = self.terra.bank.balance(self.address)
        return [it for it in res.coins if it.denom == denom][0] if denom else res

    # Distribution

    def rewards(
        self, validator: Optional[ValAddress] = None
    ) -> Union[Dict[ValAddress, Coins], Coins]:
        if validator:
            validator = validate_val_address(validator)
        res = self.terra.distribution.rewards(delegator=self.address)
        rewards: List[ValidatorReward] = res.rewards
        return (
            [
                val_reward
                for val_reward in rewards
                if val_reward.validator_address == validator
            ][0]
            if validator
            else rewards
        )

    def total_rewards(self, denom: Optional[str] = None) -> Coins:
        res = self.terra.distribution.rewards(delegator=self.address)
        total = res.total
        return [coin for coin in total if coin.denom == denom][0] if denom else total

    def withdraw_address(self) -> AccAddress:
        return self.terra.distribution.withdraw_address(delegator=self.address)

    # Staking

    def delegations(self, validator: Optional[ValAddress] = None) -> List[Delegation]:
        return self.terra.staking.delegations(
            delegator=self.address, validator=validator
        )

    def unbonding_delegations(
        self, validator: Optional[ValAddress] = None
    ) -> List[UnbondingDelegation]:
        return self.terra.staking.unbonding_delegations(
            delegator=self.address, validator=validator
        )

    def redelegations(
        self, validator_src=None, validator_dst=None
    ) -> List[Redelegation]:
        return self.terra.staking.redelegations(
            delegator=self.address,
            validator_src=validator_src,
            validator_dst=validator_dst,
        )

    def bonded_validators(self) -> List[Validator]:
        return self.terra.staking.bonded_validators(delegator=self.address)
