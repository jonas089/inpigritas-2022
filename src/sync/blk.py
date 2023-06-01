import sys
import os
module_path = os.path.abspath('../src')
sys.path.insert(0, module_path)
from core.blockchain import Block
from cli.lib import ApiClient
from core.transfer import Transfer

'''
    Sync blocks with a list of peers
    :param: instance
    :type instance: Blockchain
    :param: peers
    :type instance: str[]
    :return: ()
    :rtype: ()
'''
def sync_proto(instance, peers):
    for peer in peers:
        cli = ApiClient(peer['HOST'], peer['PORT'])
        try:
            peer_height = int(cli.get_height())
            if peer_height > instance.height():
                peer_chain = cli.get_blockchain(instance.height())
                for block in peer_chain:
                    b = Block(block['index'], block['timestamp'], block['next_timestamp'], block['block_hash'], block['next_hash'], block['prev_hash'], block['transfers'])
                    for tx in b.transfers:
                        instance.update()
                        tx_obj = Transfer(tx['sender'], tx['recipient'], tx['amount'], tx['timestamp'], tx['transaction_hash'], tx['signature'], tx['public_key'], None, None)
                        if tx_obj.validate(c) == False:
                            print('[Error]: Invalid transaction found in Block => Peer skipped: ', peer)
                            time.sleep(60)
                                            #False: don't allow blocks that are in the future.
                    if instance.validate(b, False) == True:
                        print('[Info]: Block valid')
                        instance.add_external_finalized_block(b.finalize())
                    else:
                        print('[Error]: Block did not pass validaton => Peer skipped: ', peer)
                        continue
            else:
                print('[Info]: Nothing to sync')
        except Exception as connerr:
            print('[Warning]: Connection lost: ', peer)
            print("[Error]: ", connerr)
