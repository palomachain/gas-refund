from api.blockscan_api import BlockscanConnector
from web3 import Web3


def get_from_block(blockscanner: BlockscanConnector, refund_contract_address: str, refund_wallet_address: str):
    txs_account = blockscanner.get_normal_transactions(
        address=refund_wallet_address)
    from_block = 0
    for tx in txs_account:
        if tx["methodId"] == "0xc091c435":
            from_block = int(tx['blockNumber'])
            break
    txs_contract = blockscanner.get_normal_transactions(
        address=refund_contract_address)
    for tx in txs_contract:
        if from_block > int(tx['blockNumber']):
            break
        if tx["methodId"][0:6] == "0xc091c435":
            if from_block < int(tx['blockNumber']):
                from_block = int(tx['blockNumber'])
            break
    return from_block + 1


def get_refund_list(blockscanner: BlockscanConnector, compass_evm: str, from_block: int):
    txs = blockscanner.get_normal_transactions(
        address=compass_evm, start_block=from_block)
    refund_list = {}
    try:
        for tx in txs:
            if tx['txreceipt_status'] == '1':
                sender_ = tx['from']
                if sender_ not in refund_list.keys():
                    refund_list[sender_] = int(
                        tx['gasUsed']) * int(tx['gasPrice'])
                else:
                    refund_list[sender_] += int(tx['gasUsed']) * \
                        int(tx['gasPrice'])
    except Exception as e:
        print(e)

    return refund_list


def get_refund_list_optimism(w3: Web3, blockscanner: BlockscanConnector, compass_evm: str, from_block: int):
    txs = blockscanner.get_normal_transactions(
        address=compass_evm, start_block=from_block)
    refund_list = {}
    tx_hashes = []
    try:
        for tx in txs:
            if tx['txreceipt_status'] == '1':
                tx_hashes.append(tx['hash'])
        for tx_hash in tx_hashes:
            res = w3.eth.get_transaction_receipt(tx_hash)
            sender_ = str(res['from'])
            if sender_ not in refund_list.keys():
                refund_list[sender_] = int(res['gasUsed']) * int(res['effectiveGasPrice']) + int(res['l1Fee'], base=16)
            else:
                refund_list[sender_] += int(res['gasUsed']) * int(res['effectiveGasPrice']) + int(res['l1Fee'], base=16)
    except Exception as e:
        print(e)
    return refund_list
