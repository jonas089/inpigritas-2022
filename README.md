# Inpigritas 2022 [Roadmap](https://github.com/jonas089/Inpigritas-2022/blob/master/ROADMAP.md)
Experimental python blockchain project. \
Improved version of Inpigritas-2020 ( see at the bottom of this file ) \

## Milestones
**07.02.2023**: Successfully synced a Transaction from the Pool ( flask API ) in a 2 node setup hosted locally \
**08.02.2023**: Introduction of "ictl" command line tool. Successfully synchronized 2900 Transactions in a single block. \
**16.03.2023**: Merged docker

## Run a local test-net
by [Carl Romedius](https://github.com/Rom3dius/)

To run a local Inpigritas network simply run docker-compose up. If you make any changes to the source code simply run \
```bash
docker build -t inpigritas:latest .
docker compose up
```
## Core features
1. Transfer class
2. Key-manager class
3. Blockchain and Block classes
4. Balance

## Transfer validation
Transaction data ( hash of tx ) is signed using an RSA private key and the signature is validated by peers. \
Balance/ Accounting logic is yet to be implemented. As of now, all Transactions are valid as long as the given signature is valid.

## API
Nodes communicate by calling endpoints of each others API instance. \
The API backend is programmed in Python-Flask. \
Synchronization and API are spun up through the multiprocessing python library. ( see run.py ) \
See below the blockchain API endpoint as an example:
![Inpigritas API](https://github.com/jonas089/Inpigritas-2022/blob/master/screenshots/flask.png)
This endpoint returns blocks from height 7 onwards, which enables synchronization between nodes.
## Genesis
Genesis Block is not included in validation process. \
Every node needs a copy of the genesis block to be able to sync with the network. \
=> Include many transfers in the Genesis Block for means of decentralization

## Scalability
Limited to pickle capabilities, 100% of historical chain is in memory. \
Change when network synchronization is stable and core functionality is built. \
TBD: migrate from pickle to a scalable database. \
Current preffered DB: postgres Python \
Also, potential Layer 2 ZK Rollup using Halo2 or Circom. \
Networking: Replace Flask with Sockets and build a Flask API on top.

## Implementation
Inpigritas is a blockchain transaction system that can validate actions from a Genesis Block onwards. \
Every trusted peer needs to hold a copy of the Genesis Block on startup. \
If a majority (n) of peers is hacked, the network is corrupt. \
Example: n = 2/3 of total nodes operating. \
Blocks are created locally on every node once time.time() == next_timestamp. \
Transactions are stored in a txpool and will be included in a future block (era + n) where n is a constant integer. \
Initial distribution of transferable assets happens in the Genesis Block.

## Limitations
Scalability and Speed are not super high as of today, memory overflow in Pickle implementation inevitable. Postgres or another scalable DB should be used to solve this in the future and allow for a potentially unlimited runtime of an Inpigritas Network. \
Inpigritas is a personal portfolio project but feel free to use it if you find any Implementations for this Python-Blockchain. \
Thanks to RSA signatures and Block creation/validation logic it can potentially offer moderate security to small systems / services. \
It is possible to track and prove an assets origin using Inpigritas or a variation of it. \
Use is at own Risk and this is not a production Blockchain!

## Screenshots
### Docker (Desktop) on MacOS
![cmd](https://github.com/jonas089/Inpigritas-2022/blob/master/screenshots/docker.png)
![docker overview](https://github.com/jonas089/Inpigritas-2022/blob/master/screenshots/docker-1.png)
![node details](https://github.com/jonas089/Inpigritas-2022/blob/master/screenshots/docker-2.png)
### Tests
![transactions](https://github.com/jonas089/Inpigritas-2022/blob/master/screenshots/tx-sync.png)

## History
I've been working on Inpigritas for years. The initial version was unmaintainable so I decided to create a new repo and re-factor the initial
[Prototype](https://github.com/jonas089/Inpigritas-2020-deprecated)
