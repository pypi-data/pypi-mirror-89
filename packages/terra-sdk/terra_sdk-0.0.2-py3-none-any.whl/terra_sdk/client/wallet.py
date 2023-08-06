from __future__ import annotations

from contextlib import contextmanager
from typing import Any, List, Optional, Tuple, Union, TYPE_CHECKING

from .account import AccountQuery
from terra_sdk.core.common.std_fee import StdFee
from terra_sdk.core.common.std_sign_msg import StdSignMsg
from terra_sdk.core.common.std_tx import StdTx
from terra_sdk.key import Key

if TYPE_CHECKING:
    from terra_sdk.client.terra import Terra
    from terra_sdk.core.msgs import MSG_TYPES


# StdMsg

__all__ = ["Wallet"]


class Wallet(AccountQuery):
    """A Wallet is an augmented AccountQuery, and provides `chain_id`, `account_number`,
    and `sequence` information for signing transactions, which is performed by a Key."""

    def __init__(self, terra: Terra, key: Key):
        AccountQuery.__init__(self, terra, key.acc_address)
        self.key = key
        self.terra = terra
        self._account_number = 0
        self._manual_sequence = False
        self._sequence = None

    def __repr__(self) -> str:
        return f"Wallet<{self.address}> -> {self.terra}"

    @property
    def account_number(self) -> int:
        """Account number is fetched for the first time it is found, then saved."""
        if self._account_number == 0:
            self._account_number = self.info().account_number
        return self._account_number

    @property
    def sequence(self) -> int:
        """Property that dynamically fetches sequence number everytime it is called."""
        return self.info().sequence

    def create_tx(
        self,
        *msgs: Tuple[MSG_TYPES],
        fee: Optional[StdFee] = None,
        memo: str = "",
    ) -> StdSignMsg:
        """Creates a sign message (`StdSignMsg`), which contains the necessary info to
        sign the transaction. Helpful to think of it as "create unsigned tx".
        """
        if not fee:
            # estimate our fee if fee not supplied
            tx = StdTx(msg=msgs, fee=None, signatures=None, memo=memo)
            fee = self.terra.tx.estimate_fee(tx)
        if self._manual_sequence:
            sequence = self._sequence
            self._sequence += 1
        else:
            sequence = self.sequence
        return StdSignMsg(
            chain_id=self.terra.chain_id,
            account_number=self.account_number,
            sequence=sequence,
            fee=fee,
            msgs=msgs,
            memo=memo,
        )

    def sign_tx(self, *args, **kwargs):
        """Uses the Wallet's key to sign the transaction."""
        return self.key.sign_tx(*args, **kwargs)

    def create_and_sign_tx(
        self,
        *msgs: Tuple[MSG_TYPES],
        fee: Optional[StdFee] = None,
        memo: str = "",
    ) -> StdTx:
        """Creates a sign message, signs it, and produces a transaction in one go.
        Outputs a ready-to-broadcast `StdTx`.
        """
        return self.sign_tx(self.create_tx(*msgs, fee=fee, memo=memo))

    @contextmanager
    def manual(self) -> Wallet:
        """Manual mode is a context that creates sign messages (and transactions) with the
        sequence number incremented on each TX generation rather than polling from the
        blockchain every time, so they can be saved and broadcasted at a later time.
        """
        self._sequence = self.sequence
        self._manual_sequence = True
        yield self
        self._manual_sequence = False

    def broadcast(self, *args, **kwargs):
        return self.terra.tx.broadcast(*args, **kwargs)
