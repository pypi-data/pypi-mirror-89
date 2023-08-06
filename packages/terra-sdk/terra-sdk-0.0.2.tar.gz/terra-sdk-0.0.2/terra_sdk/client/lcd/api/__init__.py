from __future__ import annotations

from typing import Any

import requests

from terra_sdk.utils.error import UnhandledResponse

__all__ = ["BaseApi"]


class BaseApi(object):
    """Base class for Terra API objects. Provides functions for turning an API response
    into a wrapped object proxy called an `ApiResponse`."""

    def __init__(self, terra):
        self.terra = terra

    @property
    def lcd(self):
        return self.terra.lcd

    def _api_get(self, path, unwrap=True, **kwargs) -> Any:
        return self._handle_response(self.terra.lcd.get(path, **kwargs), unwrap)

    def _api_post(self, path, unwrap=True, **kwargs) -> Any:
        return self._handle_response(self.terra.lcd.post(path, **kwargs), unwrap)

    @staticmethod
    def _handle_response(response: requests.Response, unwrap=True) -> Any:
        """Creates an ApiResponse object from the LCD Client's response.

        :param response: LCD response
        :param unwrap: whether the LCD response will include height
        """
        # TODO: refactor into middleware? --
        # NOTE: This actually should be in the last step, but the user can decide to do
        # some post-processing on their own, such as parsing, by writing a library that
        # parses the result. Outside the scope of the SDK.
        try:
            res = response.json()
            if unwrap:
                return res["result"]
            else:
                return res
        except ValueError:  # if the response cannot be parsed to JSON
            raise UnhandledResponse(f"unhandled response {str(response.content)}")
