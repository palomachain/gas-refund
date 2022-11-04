from web3 import Web3
import os
import json
import subprocess

infura_key = os.environ['WEB3_INFURA_PROJECT_ID']
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/" + infura_key))

from_block = 0  # will be better if it is stored in the file

contract = '0xBb4FAc66AffD17365C447C837fd0A2F064313d64'
topic_add_liquidity = w3.toHex(
    w3.keccak(text="AddLiquidity(uint256,address,uint256,address,string)"))
topic_swap_in = w3.toHex(w3.keccak(text="SwapIn(uint256,uint256,string)"))


def get_logs(fromBlock, contract, topic):
    """
    get logs by contract and topic0
    """
    txs = w3.eth.get_logs(
        {"fromBlock": fromBlock, "address": contract, "topics": topic})

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


def get_latest_block(js):
    """
    js is the logs json object
    """
    txs = json.loads(js)
    from_block = 0
    for tx in txs:
        block_ = int(float.fromhex(tx['blockNumber']))
        if block_ > from_block:
            from_block = block_

    return from_block


if __name__ == '__main__':
    logs = get_logs(from_block, contract, [topic_add_liquidity, topic_swap_in])
    data = parse_logs(logs)
    print(data)

chain_id = "0"  # different per chains
cw_contract = ""  # Paloma CW smart contract address
grain_amount = "1000000ugrain" # need to check with Paloma team(?)
paloma_chain_id = "paloma-testnet-13" # paloma chain id
wallet_address = "" # paloma wallet address to run transaction
fees = "1000ugrain" # need to confirm


def run_cosmwasm_transaction(cw_contract, json_data, grain_amount, paloma_chain_id, wallet_address, fees):
    res = subprocess.call([
        'palomad', 'tx', 'wasm', 'execute', cw_contract, json_data,
        '--amount', grain_amount,
        '--chain-id', paloma_chain_id,
        '--from', wallet_address,
        '-fees', fees,
        '--gas', 'auto',
        '-y', '-b', 'block'
    ])
    assert res == 0


def call_add_liquidity_cosmwasm(pool_id, token, amount, depositor, recipient):
    data = {"add_liquidity": {"pool_id": pool_id,
                              "chain_id": chain_id, "token": token, "amount": amount, "sender": depositor, "receiver": recipient}}
    json_data = json.dumps(data)
    run_cosmwasm_transaction(
        cw_contract, json_data, grain_amount, paloma_chain_id, wallet_address, fees)


def call_swap_in_cosmwasm(pool_id, token, amount, recipient):
    data = {"swap": {"pool_id": pool_id, "chain_from_id": chain_id, "token": token, "amount": amount, "receiver": recipient}}
    json_data = json.dumps(data)
    run_cosmwasm_transaction(
        cw_contract, json_data, grain_amount, paloma_chain_id, wallet_address, fees)
