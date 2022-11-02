
import os
import time,datetime,requests
import logging
import sys
current_dir = os.getcwd()
sys.path.insert(1, os.path.abspath(os.path.join(current_dir, os.pardir)))
from etherscan import etherscan_api

txhash = ''
topics = ''

tx = eth.get_tx_receipt(tx_hash='0x310741cbfb0c3605fafceddd1d9be324948b353c405539b50da86d007bd9df68')

print(tx['logs'][0]['data'][2:66])
print(tx['logs'][0]['data'][66:130])
print(tx['logs'][0]['data'][130:194])
print(tx['logs'][0]['data'][154:194])

def get_event_log_data(tx_hash, topics):
    eth=etherscan_api.EtherscanConnector()
    tx = eth.get_tx_receipt(tx_hash=tx_has)
    data_ = None
    for log_ in tx['logs']:
        if log_ == topics:
            data_ = log_['data']
    
    return data_

def parse_addliquidity(tx_hash, topics):