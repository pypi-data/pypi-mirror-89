"""Low-level Tendermint Node API."""
from typing import List

from .lcd.api import BaseApi

__all__ = ["TendermintApi"]


class TendermintApi(BaseApi):
    def node_info(self) -> dict:
        """Get information for the node.
        Returns:
            Node information with the following schema.
        """
        return self._api_get("/node_info", unwrap=False)

    def syncing(self) -> bool:
        """Get whether the node is currently syncing with updates on the blockchain.

        Returns:
            If node is syncing.
        """
        res = self._api_get("/syncing", unwrap=False)
        return res["syncing"]

    def block(self, height: int = None) -> dict:
        """Get the raw block data at a height on the blockchain.

        Args:
            height (int, optional): block height

        Returns:
            - The block at the provided height. If no height was specified, get the latest
            block at the time of calling.

        """
        if height:
            res = self._api_get(f"/blocks/{height}", unwrap=False)
        else:
            res = self._api_get("/blocks/latest", unwrap=False)
        return res

    def validator_set(self, height: int = None) -> List[dict]:
        """Retrieves the current set of validators in the actively validating set.

        ## Arguments
        - **height** `int` *optional*

            block height

        ## Returns
        List of `dict` with the following keys:

        - **address** `ValConsAddress`

            validator's consensus address

        - **pub_key** `ValConsPubKey`

            validator's consensus public key

        - **proposer_priority** `int`
        - **voting_power** `int`
        """
        if height:
            res = self._api_get(f"/validatorsets/{height}")
        else:
            res = self._api_get("/validatorsets/latest")
        return res["validators"]
