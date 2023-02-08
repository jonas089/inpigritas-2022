import pickle
with open('./cli_2/data/blockchain.dat', 'rb') as cli2:
    print(pickle.load(cli2))
with open('./cli_1/data/blockchain.dat', 'rb') as cli1:
    print(pickle.load(cli1))
