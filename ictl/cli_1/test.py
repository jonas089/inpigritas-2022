from core.transfer import Transfer
from core.blockchain import Block, Blockchain
from core.accounts import Keys
import time, os
from chainspec import BLOCKTIME
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description='AMPS')
parser.add_argument('amount')
args = parser.parse_args()
# TBD: remove this function from api.py and move it in a helper file.
def tx_chain_info():
    b = Blockchain()
    b.update()
    h = b.chain[-1]
    l = len(b.chain)
    return (h, l)
# Conditions that have to be met:
# * time.time > last_block_time
# * effective_height = current_height + n, n!=0
# 4. Send a Transaction that is to be included in Block #1
test_nonce = 0
n = int(args.amount)
progress_bar = tqdm(total=n)
progress_bar.set_description("Creating Transfers locally: ")
for i in range(0, n):
    _Keys = Keys()
    info = tx_chain_info()
    if not time.time() < int(info[0]['next_timestamp']) and not time.time() > int(info[0]['timestamp']):
        print("[Warning]: wait for chain to sync or block to be created.")

    else:

        r = 'recipient' + str(test_nonce)
        tx = Transfer('sender', r, 10, None, None, None, None, 1, _Keys)
        tx.new()
        effective_height = info[1] + 2
        tx.add_to_pool(effective_height)
    test_nonce += 1
    progress_bar.update(1)
