from __future__ import annotations
from typing import Union

from terra_sdk.core.bank import *
from terra_sdk.core.distribution import *
from terra_sdk.core.gov import *
from terra_sdk.core.market import *
from terra_sdk.core.msgauth import *
from terra_sdk.core.oracle import *
from terra_sdk.core.slashing import *
from terra_sdk.core.staking import *
from terra_sdk.core.wasm import *

MSG_TYPES = Union[
    MsgSend,
    MsgMultiSend,
    # distribution
    MsgModifyWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
    MsgFundCommunityPool,
    # gov
    MsgDeposit,
    MsgSubmitProposal,
    MsgVote,
    # market
    MsgSwap,
    MsgSwapSend,
    # msgauth
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
    MsgExecAuthorized,
    # oracle
    MsgExchangeRateVote,
    MsgExchangeRatePrevote,
    MsgDelegateFeedConsent,
    MsgAggregateExchangeRatePrevote,
    MsgAggregateExchangeRateVote,
    # slashing
    MsgUnjail,
    # staking
    MsgDelegate,
    MsgUndelegate,
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgEditValidator,
    # wasm
    MsgStoreCode,
    MsgInstantiateContract,
    MsgExecuteContract,
    MsgMigrateContract,
    MsgUpdateContractOwner,
]

MSGS: dict = {
    "bank/MsgSend": MsgSend,
    "bank/MsgMultiSend": MsgMultiSend,
    # distribution
    "distribution/MsgModifyWithdrawAddress": MsgModifyWithdrawAddress,
    "distribution/MsgWithdrawDelegationReward": MsgWithdrawDelegationReward,
    "distribution/MsgWithdrawValidatorCommission": MsgWithdrawValidatorCommission,
    "distribution/MsgFundCommunityPool": MsgFundCommunityPool,
    # gov
    "gov/MsgDeposit": MsgDeposit,
    "gov/MsgSubmitProposal": MsgSubmitProposal,
    "gov/MsgVote": MsgVote,
    # market
    "market/MsgSwap": MsgSwap,
    "market/MsgSwapSend": MsgSwapSend,
    # msgauth
    "msgauth/MsgGrantAuthorization": MsgGrantAuthorization,
    "msgauth/MsgRevokeAuthorization": MsgRevokeAuthorization,
    "msgauth/MsgExecAuthorized": MsgExecAuthorized,
    # oracle
    "oracle/MsgExchangeRateVote": MsgExchangeRateVote,
    "oracle/MsgExchangeRatePrevote": MsgExchangeRatePrevote,
    "oracle/MsgDelegateFeedConsent": MsgDelegateFeedConsent,
    "oracle/MsgAggregateExchangeRatePrevote": MsgAggregateExchangeRatePrevote,
    "oracle/MsgAggregateExchangeRateVote": MsgAggregateExchangeRateVote,
    # slashing
    "cosmos/MsgUnjail": MsgUnjail,
    # staking
    "staking/MsgDelegate": MsgDelegate,
    "staking/MsgUndelegate": MsgUndelegate,
    "staking/MsgBeginRedelegate": MsgBeginRedelegate,
    "staking/MsgCreateValidator": MsgCreateValidator,
    "staking/MsgEditValidator": MsgEditValidator,
    # wasm
    "wasm/MsgStoreCode": MsgStoreCode,
    "wasm/MsgInstantiateContract": MsgInstantiateContract,
    "wasm/MsgExecuteContract": MsgExecuteContract,
    "wasm/MsgMigrateContract": MsgMigrateContract,
    "wasm/MsgUpdateContractOwner": MsgUpdateContractOwner,
}


def get_msgs(data: dict) -> MSG_TYPES:
    """
    docstring
    """
    return MSGS[data["type"]].from_data(data)