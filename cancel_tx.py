import os
from web3 import Web3
from eth_account import Account

node = os.environ['NODE']
w3 = Web3(Web3.HTTPProvider(node))
print('check EVM node connected: ', w3.isConnected())
private_key = os.environ['PRIVATE_KEY']
account_from = Account.from_key(private_key)

nonce = w3.eth.get_transaction_count(account_from.address)
gas_price = int(w3.eth.gas_price * 1.1)
transaction = {
    'to': account_from.address,
    'gas': 21000,
    'gasPrice': gas_price,
    'nonce': nonce,
    'chainId': 1
}

signed = w3.eth.account.sign_transaction(transaction, private_key)
w3.eth.send_raw_transaction(signed.rawTransaction)