from typing import List, Optional, Union

from terra_sdk.client.lcd.api import BaseApi
from terra_sdk.core.common import Dec, AccAddress
from .authorization import AuthorizationInfo

__all__ = ["MsgAuthApi"]


class MsgAuthApi(BaseApi):
    def grants(
        self, granter: AccAddress, grantee: AccAddress, msg_type: Optional[str] = None
    ) -> List[AuthorizationInfo]:

        res = self._api_get(
            f"/msgauth/granters/{granter}/grantees/{grantee}/grants/{msg_type}"
            if msg_type
            else f"/msgauth/granters/{granter}/grantees/{grantee}/grants"
        )
        res = res or []
        return [AuthorizationInfo.from_data(auth_info) for auth_info in res]
