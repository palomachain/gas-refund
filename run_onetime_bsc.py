import bscscan_api
from functions_bsc import get_refundlist, conv_dt_rev
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
BSC_NODE: a BSC node https endpoint
WALLET: refund wallet address
BSC_PRIVATE_KEY: refund wallet private key
"""

node = "https://bsc-dataseed.binance.org/"  # node = os.environ['BSC_NODE']
w3 = Web3(Web3.HTTPProvider(node))
print('check bsc node connected: ', w3.isConnected())

# fromtime = argv[1] # '2022-08-25 15:00:00'
# totime = argv[2] # '2022-08-26 09:00:00'
# eth_lowercap = float(argv[3]) #0.1
# refund_cap =  float(argv[4]) #0.15

if 1:
    private_key = os.environ['BSC_PRIVATE_KEY']
    account_from = Account.from_key(private_key)
    assert account_from.address == "0x83334ef0C6f6396413C508A7762741e9FD8B20E9" ## this is the refund wallet address
contract_address = "0x4F62AF8fF4b9B22f53eE56cB576B02EFE2866825"  ## this is the refund contract address
abi = [{"type": "function", "name": "refund", "stateMutability": "payable", "inputs": [
    {"name": "receivers", "type": "address[]"}, {"name": "amounts", "type": "uint256[]"}], "outputs": []}]

bsc = bscscan_api.BscscanConnector()
txs = bsc.get_normal_transactions(address=account_from.address)
#txs = bsc.get_normal_transactions('0xF48F4e86dE6a30D75dbe3A6C67E17Cf3cbDE5768')
fromtime = 0

totime = "2022-10-12 12:53:07"

print(fromtime, totime)

def send_EIP1559(refund_list, gas=21000, account_from=account_from):

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

def send(refund_list, gas=21000, account_from=account_from):

    w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
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
        tx_create = refund_sc.functions.refund(address_list, amount_list).build_transaction(
            {"value": value, "nonce": nonce, "from": account_from.address})
        print(tx_create)
        signed_tx = w3.eth.account.sign_transaction(
            tx_create, private_key=private_key)
        print(signed_tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(
            f"Transaction successful with hash: { tx_receipt.transactionHash.hex() }")
    else:
        print('no refund needed')


if 1:
    refund_list = get_refundlist(fromtime, totime)
    print(refund_list)
    send(refund_list, gas=21000, account_from=account_from)
