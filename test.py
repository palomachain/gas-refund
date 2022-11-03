from web3 import Web3
import os

infura_key = os.environ['WEB3_INFURA_PROJECT_ID']
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/" + infura_key))

from_block = 0 # will be better if it is stored in the file

contract = '0xBb4FAc66AffD17365C447C837fd0A2F064313d64'
topic0 = w3.toHex(w3.keccak(text="Minted(address,string,uint256)"))

def get_logs(fromBlock,contract,topic):
    """
    get logs by contract and topic0
    """
    txs = w3.eth.get_logs({"fromBlock":fromBlock,"address":contract,"topics":topic})

    return txs

def parse_logs(logs):
    global from_block
    data = []
    for log in logs:
        datum = []
        for element in log['topics']:
            datum.append(w3.toHex(element))
        data.append(datum)
        if from_block < log['blockNumber']:
            from_block = log['blockNumber']
    return data

if __name__ == '__main__':
    logs = get_logs(from_block,contract,[topic0])
    data = parse_logs(logs)
    print(data)
