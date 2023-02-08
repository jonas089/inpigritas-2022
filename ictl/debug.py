import pickle
with open('./cli_2/data/blockchain.dat', 'rb') as cli2:
    #print(pickle.load(cli2))
    r = pickle.load(cli2)
    print(len(r[3]['transfers']))
    print(r[3]['transfers'][500])
with open('./cli_1/data/blockchain.dat', 'rb') as cli1:
    r = pickle.load(cli1)
    print(len(r[3]['transfers']))
