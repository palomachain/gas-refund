import os
import time,datetime,requests
import logging
import sys
current_dir = os.getcwd()
sys.path.insert(1, os.path.abspath(os.path.join(current_dir, os.pardir)))
import etherscan_api

eth=etherscan_api.EtherscanConnector()

def get_logs(contract,topic0, eth=eth):
    """
    get logs by contract and topic0
    """
    txs = eth.get_event_log_byaddress(address=contract,topic0=topic0)
    return txs

if __name__ == '__main__':
    contract = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
    topic0='0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
    print(get_logs(contract,topic0))


"""
unfinished testing code

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

"""