from typing import Dict, List, Union

from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.common import AccAddress, Coins
from .proposal import Proposal, Tally
from .votes import ProposalVote
from .deposits import ProposalDeposit

__all__ = ["GovApi"]


class GovApi(BaseApi):
    """Interface for interacting with the Governance API."""

    def proposals(self) -> Union[List[Proposal]]:
        """Get all proposals."""
        res = self._api_get("/gov/proposals")
        return [Proposal.from_data(p) for p in res]

    def proposal(self, proposal_id: int) -> Proposal:
        """Get a single proposal by ID."""
        res = self._api_get(f"/gov/proposals/{proposal_id}")
        return Proposal.from_data(res)

    def proposer(self, proposal_id: int) -> AccAddress:
        """Gets a proposal's proposer."""
        res = self._api_get(f"/gov/proposals/{proposal_id}/proposer")
        return res["proposer"]

    def deposits(self, proposal_id: int) -> List[ProposalDeposit]:
        """Get the proposal's deposits."""
        res = self._api_get(f"/gov/proposals/{proposal_id}/deposits")
        ds = res or []
        deposits = [ProposalDeposit.from_data(dep) for dep in ds]
        return deposits

    def votes(self, proposal_id: str) -> List[ProposalVote]:
        res = self._api_get(f"/gov/proposals/{proposal_id}/votes")
        vs = res or []
        votes = [ProposalVote.from_data(vote) for vote in res]
        return votes

    def tally(self, proposal_id: str) -> Tally:
        res = self._api_get(f"/gov/proposals/{proposal_id}/tally")
        return Tally.from_data(res)

    def parameters(self, key: str = None) -> dict:
        """Puts all the parameters together."""
        deposit = self.deposit_parameters()
        voting = self.voting_parameters()
        tally = self.tally_parameters()
        p = {"deposit_params": deposit, "voting_params": voting, "tally_params": tally}

        return p

    def deposit_parameters(self, key: str = None) -> Dict[str, Union[int, Coins]]:
        res = self._api_get(f"/gov/parameters/deposit")
        return res

    def voting_parameters(self, key: str = None) -> dict:
        res = self._api_get(f"/gov/parameters/voting")
        return res

    def tally_parameters(self, key: str = None) -> dict:
        res = self._api_get(f"/gov/parameters/tallying")
        return res
