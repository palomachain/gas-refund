import etherscan_api
from functions import get_refundlist, conv_dt_rev
import sys
import os
import datetime
from web3 import Web3
from eth_account import Account
from web3.gas_strategies.rpc import rpc_gas_price_strategy
current_dir = os.getcwd()
sys.path.insert(1, os.path.abspath(os.path.join(current_dir, '../../')))

"""
This script requires the following environment variables:
NODE: a EVM node https endpoint
WALLET: refund wallet address
PRIVATE_KEY: refund wallet private key
"""

node = os.environ['NODE']
w3 = Web3(Web3.HTTPProvider(node))
print('check EVM node connected: ', w3.isConnected())

# fromtime = argv[1] # '2022-08-25 15:00:00'
# totime = argv[2] # '2022-08-26 09:00:00'
# eth_lowercap = float(argv[3]) #0.1
# refund_cap =  float(argv[4]) #0.15

private_key = os.environ['PRIVATE_KEY']
account_from = Account.from_key(private_key)
assert account_from.address == os.environ['REFUND_WALLET']  # this is the refund wallet address
contract_address = "0x2e89c7e795a162Acda3eAac8f4abbb321517F20F"  # this is the refund contract
abi = [{"type": "function", "name": "refund", "stateMutability": "payable", "inputs": [
    {"name": "receivers", "type": "address[]"}, {"name": "amounts", "type": "uint256[]"}], "outputs": []}]

eth = etherscan_api.EtherscanConnector()
txs_account = eth.get_normal_transactions(address=account_from.address)

txs_contract = eth.get_normal_transactions(address=contract_address)

fromtime = conv_dt_rev(0)
for tx in txs_account:
    if tx["functionName"][0:6] == "refund":
        fromtime = conv_dt_rev(tx['timeStamp'])
        break

for tx in txs_contract:
    if fromtime > conv_dt_rev(tx['timeStamp']):
        break
    if tx["functionName"][0:6] == "refund":
        if fromtime < conv_dt_rev(tx['timeStamp']):
            fromtime = conv_dt_rev(tx['timeStamp'])
        break

totime = datetime.datetime.utcnow()

print(fromtime, totime)


def send(refund_list, gas=21000, account_from=account_from):

    value = 0
    address_list = []
    amount_list = []
    for receiver in refund_list.keys():
        value += refund_list[receiver]
        address_list.append(w3.toChecksumAddress(receiver))
        amount_list.append(refund_list[receiver])
    if value > 0:  # this should be added. if value equals zero, we don't need to run tx.
        refund_sc = w3.eth.contract(
            address=contract_address,
            abi=abi)
        nonce = w3.eth.get_transaction_count(account_from.address)
        max_priority_fee = w3.eth.max_priority_fee
        gas_price = w3.eth.gas_price * 2 + max_priority_fee
        tx_create = refund_sc.functions.refund(address_list, amount_list).build_transaction(
            {"value": value, "nonce": nonce, "from": account_from.address, "maxFeePerGas": gas_price,
             "maxPriorityFeePerGas": max_priority_fee})
        print(tx_create)
        signed_tx = w3.eth.account.sign_transaction(
            tx_create, private_key=private_key)
        print(signed_tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        #print(f"Transaction successful with hash: { tx_receipt.transactionHash.hex() }")
        print("Transaction successful")
    else:
        print('no refund needed')


if 1:
    refund_list = get_refundlist(fromtime, totime)
    print(refund_list)
    send(refund_list, gas=21000, account_from=account_from)
