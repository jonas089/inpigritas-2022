from core.transfer import Transfer
from cli.lib import ApiClient

'''
    Sync transaction pool for current block with a list of peers
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
        local_pool = instance.txpool()
        try:
            peer_height = int(cli.get_height())
            if peer_height == instance.height():
                peer_pool = cli.get_pool()
                if len(peer_pool) > len(local_pool):
                    for tx in peer_pool:
                        if not instance.is_duplicate_in_pool(tx):
                            instance.update()
                            tx_obj = Transfer(tx['sender'], tx['recipient'], tx['amount'], tx['timestamp'], tx['transaction_hash'], tx['signature'], tx['public_key'], None, None)
                            tx_obj.add_to_pool(instance.height())
                            #print("[Info]: Tx valid -> ", tx_obj.validate(instance))
                            #print("[Success]: Tx synced!")
                elif len(local_pool) == 0 and len(peer_pool) == 0:
                    print("[Info]: no transaction found.")
                else:
                    print("[Success]: Tx sync complete!")
                    print("[Info]: Local pool length: {llp}, Peer pool lengt: {ppl}".format(llp=str(len(local_pool)), ppl=str(len(peer_pool))))
        except Exception as connerr:
            print('[Warning]: Connection lost: ', peer)
            print("[Error]: ", connerr)
