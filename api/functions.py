from api.blockscan_api import BlockscanConnector

def get_from_block(blockscanner: BlockscanConnector, refund_contract_address: str, refund_wallet_address: str):
    txs_account = blockscanner.get_normal_transactions(
        address=refund_wallet_address)
    from_block = 0
    for tx in txs_account:
        if tx["functionName"][0:6] == "refund":
            from_block = int(tx['blockNumber'])
            break
    txs_contract = blockscanner.get_normal_transactions(
        address=refund_contract_address)
    for tx in txs_contract:
        if from_block > int(tx['blockNumber']):
            break
        if tx["functionName"][0:6] == "refund":
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
