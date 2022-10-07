import os
import time
import datetime
import logging
import pandas as pd
import numpy as np
import requests
from typing import Any, Dict, List, Optional, TypedDict, Union


class EtherscanConnector:

    api_endpoint_preamble = "https://api.etherscan.io/api?"
    API_KEY = 'FCD48UAF7G87XBTK3G934Q42MCV8PE3TVM'

    def __init__(self, max_api_calls_sec: int = 30):
        self._api_call_sleep_time = 1 / max_api_calls_sec

    def _rate_limit(self) -> None:
        time.sleep(self._api_call_sleep_time)

    @staticmethod
    def _validate_timestamp_format(self, timestamp: Union[int, str, pd.Timestamp]):
        raise NotImplementedError()  # TODO

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

    def get_tx_receipt(self, tx_hash: str):
        tx_receipt_url = "".join(
            [
                self.api_endpoint_preamble,
                "module=proxy",
                "&action=eth_getTransactionReceipt",
                "&txhash={transaction_hash}",
                "&apikey={api_key}",
            ]
        )

        tx_receipt_query = tx_receipt_url.format(
            transaction_hash=tx_hash, api_key=self.API_KEY
        )
        tx_receipt: types.TxReceipt = self.run_query(tx_receipt_query)
        return tx_receipt

    def get_normal_transactions(self, address):

        api_key = self.API_KEY
        tx_list_url: str = "".join(
            [
                self.api_endpoint_preamble,
                "module=account",
                f"&action=txlist&address={address}&",
                f"sort=desc&apikey={api_key}",
            ]
        )
        return self.run_query(query=tx_list_url)

    def get_contract_abi(self, address: str) -> dict:
        contract_abi_url = "".join(
            [
                self.api_endpoint_preamble,
                "module=contract&",
                "action=getabi",
                "&address={address}",
                "&apikey={api_key}",
            ]
        )
        contract_abi_query: str = contract_abi_url.format(
            address=address, api_key=self.API_KEY
        )
        print(contract_abi_query)
        return self.run_query(query=contract_abi_query)

    def get_event_log_byaddress(self, address: str, topic0: str, fromblock=None, toblock=None) -> List[Dict[str, Any]]:
        event_log_url: List[str] = [
            self.api_endpoint_preamble,
            "module=logs&",
            "action=getLogs&",
            "address={address}&",
            "topic0={topic0}&",
            "apikey={api_key}",
        ]

        event_log_url: str = "".join(event_log_url)
        if fromblock:
            event_log_url += '&fromBlock'+str(fromblock)
        if toblock:
            event_log_url += '&toBlock'+str(toblock)
        event_log_query = event_log_url.format(
            address=address, topic0=topic0, api_key=self.API_KEY
        )
        return self.run_query(event_log_query)

    def get_event_log_bytopic(self, topic0, topic1, topic2, fromblock=None, toblock=None) -> List[Dict[str, Any]]:
        event_log_url: List[str] = [
            self.api_endpoint_preamble,
            "module=logs&",
            "action=getLogs&",
            "topic0={topic0}&",
            "topic1={topic1}&",
            "topic2={topic2}&",
            "apikey={api_key}",
        ]

        event_log_url: str = "".join(event_log_url)
        if fromblock:
            event_log_url += '&fromBlock'+str(fromblock)
        if toblock:
            event_log_url += '&toBlock'+str(toblock)
        event_log_query = event_log_url.format(
            topic0=topic0, topic1=topic1, topic2=topic2, api_key=self.API_KEY
        )
        print(event_log_query)
        return self.run_query(event_log_query)

    def get_account_eth(self, address: str) -> dict:
        account_eth_url = "".join(
            [
                self.api_endpoint_preamble,
                "module=account&",
                "action=balance",
                "&address={address}",
                "&apikey={api_key}",
            ]
        )
        account_eth_query: str = account_eth_url.format(
            address=address, api_key=self.API_KEY
        )
        # print(account_eth_query)
        return self.run_query(query=account_eth_query)
