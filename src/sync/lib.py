import sys
import os
module_path = os.path.abspath('../src')
sys.path.insert(0, module_path)
from cli.lib import ApiClient

'''
    * check if synchronised or behind peer(s)
'''

def is_synced(instance, peers):
    for peer in peers:
        cli = ApiClient(peer['HOST'], peer['PORT'])
        try:
            peer_height = int(cli.get_height())
            if peer_height > instance.height():
                return False
        except Exception as connerr:
            print(connerr)
            print('[Warning]: Connection lost: ', peer)
    return True
