import etherscan_api
import os
import time
import datetime
import pandas as pd
import numpy as np
import sys
current_dir = os.getcwd()
sys.path.insert(1, os.path.abspath(os.path.join(current_dir, '../../')))


def conv_dt_rev(dt_int):
    """
    convert datetime format
    """
    return datetime.datetime(1970, 1, 1, 0, 0, 0)+datetime.timedelta(seconds=int(dt_int)/1e0)


eth = etherscan_api.EtherscanConnector()

contract = '0x24B10a62385C2d04F3f04Dd55297ADD7b4502530' # compass evm
txs = eth.get_normal_transactions(address=contract)
methodid = '0xeadf4af7'


def get_refundlist(fromtime='2022-08-25 15:00:00', totime='2022-08-26 09:00:00'):
    fromtime_ = pd.to_datetime(fromtime)
    totime_ = pd.to_datetime(totime)

    refund_list = {}

    try:
        for tx in txs:
            if tx['txreceipt_status'] == '1' and tx['methodId'] == methodid:
                time_ = conv_dt_rev(tx['timeStamp'])
                if time_ > fromtime_ and time_ <= totime_:
                    sender_ = tx['from']
                    if sender_ not in refund_list.keys():
                        refund_list[sender_] = int(
                            tx['gasUsed']) * int(tx['gasPrice'])
                    else:
                        refund_list[sender_] += int(tx['gasUsed']) * \
                            int(tx['gasPrice'])
                    # print(tx['blockNumber'], time_, sender_, refund_list[sender_])
                elif time_ < fromtime_:
                    break
    except Exception as e:
        print(e)

    return refund_list


def get_refundlist_byblock(contract, methodid, fromblock, toblock):

    refund_list = {}
    txs = eth.get_normal_transactions(address=contract)

    try:
        for tx in txs:
            if tx['txreceipt_status'] == '1' and tx['methodId'] == methodid:
                blockid_ = int(tx['blockNumber'])
                if blockid_ >= fromblock and blockid_ <= toblock:
                    sender_ = tx['from']
                    if sender_ not in refund_list.keys():
                        refund_list[sender_] = int(
                            tx['gasUsed']) * int(tx['gasPrice'])
                    else:
                        refund_list[sender_] += int(tx['gasUsed']) * \
                            int(tx['gasPrice'])
                    # print(tx['blockNumber'], time_, sender_, refund_list[sender_])
                elif blockid_ < fromtblock:
                    break
    except Exception as e:
        print(e)

    return refund_list


def get_refundlist_old(fromtime='2022-08-25 15:00:00', totime='2022-08-26 09:00:00', eth_lowercap=0.1, refund_cap=0.15):
    fromtime_ = pd.to_datetime(fromtime)
    totime_ = pd.to_datetime(totime)

    refund_list = {}
    sender_list = []
    try:
        for tx in txs:
            if tx['txreceipt_status'] == '1' and tx['methodId'] == methodid:
                time_ = conv_dt_rev(tx['timeStamp'])
                if time_ > fromtime_ and time_ <= totime_:
                    sender_ = tx['from']
                    if not sender_ in sender_list:
                        balance_ = float(eth.get_account_eth(sender_))/1e18
                        print(tx['blockNumber'], time_, sender_, balance_)
                        sender_list.append(sender_)

                        if balance_ < eth_lowercap:
                            refund_list[sender_] = refund_cap - balance_

                elif time_ < fromtime_:
                    break
    except Exception as e:
        print(e)

    return refund_list


if __name__ == '__main__':
    print(get_refundlist())
