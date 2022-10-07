import os
from web3 import Web3
from eth_account import Account

node = os.environ['NODE']
w3 = Web3(Web3.HTTPProvider(node))
print('check EVM node connected: ', w3.isConnected())
private_key = os.environ['PRIVATE_KEY']
account_from = Account.from_key(private_key)

nonce = w3.eth.get_transaction_count(account_from.address)
max_priority_fee = w3.eth.max_priority_fee
gas_price = w3.eth.gas_price * 2 + max_priority_fee
transaction = {
    'to': account_from.address,
    'gas': 21000,
    'maxFeePerGas': gas_price,
    'maxPriorityFeePerGas': max_priority_fee,
    'nonce': nonce,
    'chainId': 1
}

signed = w3.eth.account.sign_transaction(transaction, private_key)
w3.eth.send_raw_transaction(signed.rawTransaction)