import time
import logging
import requests
from typing import Any, Dict, List, Optional, TypedDict, Union


class BlockscanConnector:

    def __init__(self, api_endpoint_preamble, api_key, max_api_calls_sec: int = 5):
        self.api_endpoint_preamble = api_endpoint_preamble
        self.api_key = api_key
        self._api_call_sleep_time = 1 / max_api_calls_sec

    def _rate_limit(self) -> None:
        time.sleep(self._api_call_sleep_time)

    def run_query(self, query: str, rate_limit: bool = True) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json"}
        try:
            response: requests.Response = requests.get(query, headers=headers)

            if not (response and response.ok):
                msg = (
                    f"Failed request with status code {response.status_code}"
                    + f": {response.text}"
                )
                logging.warning(msg)
                raise Exception(msg)

            if rate_limit:
                self._rate_limit()
            return response.json()["result"]
        except Exception:
            logging.exception(f"Problem in query: {query}")
            # Raise so retry can retry
            raise

    def get_normal_transactions(self, address, start_block:Optional[int]=None, end_block:Optional[int]=None):
        tx_list_url: str = "".join(
            [
                self.api_endpoint_preamble,
                "module=account",
                f"&action=txlist&address={address}&",
                f"sort=desc&apikey={self.api_key}",
            ]
        )
        if start_block is not None:
            tx_list_url += f"&startblock={start_block}"
        if end_block is not None:
            tx_list_url += f"&startblock={end_block}"
        return self.run_query(query=tx_list_url)