from core.accounts import Keys
from core.transfer import Transfer
from tqdm import tqdm
import requests
print("Running the tx-tests.")
test_nonce = 0
#n = int(args.amount)
n = 1
progress_bar = tqdm(total=n)
progress_bar.set_description("Creating Transfers locally: ")
for i in range(0, n):
    _Keys = Keys()

    r = 'recipient' + str(test_nonce)
    tx = Transfer('sender', r, 10, None, None, None, None, 1, _Keys)
    tx.new()
    _tx = tx.finalize()


    x = requests.post("http://127.0.0.1:8080/propose/tx", json=_tx)
    print(x.text)

    test_nonce += 1
    progress_bar.update(1)
