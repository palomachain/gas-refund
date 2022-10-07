import bscscan_api
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


bsc = bscscan_api.BscscanConnector()

# this is the compass contract
contract = '0xB3c4641D309c21766AC00B3524D246Ee73bf5475'
txs = bsc.get_normal_transactions(address=contract)
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


if __name__ == '__main__':
    print(get_refundlist(fromtime='2022-08-25 15:00:00', totime='2022-10-26 09:00:00'))
