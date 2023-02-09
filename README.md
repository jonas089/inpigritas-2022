# Inpigritas 2022
Experimental python blockchain project. \
Will be used for R&D Work \
Whilst developing core functionality, all data is stored / read using pickle \
Database solution tbd.

## Milestones
**07.02.2022**: Successfully synced a Transaction from the Pool ( flask API ) in a 2 node setup hosted locally \
**08.02.2022**: Introduction of "ictl" command line tool. Successfully synchronized 2900 Transactions in a single block.

## ictl - run an Inpigritas-network locally

Tested on: MacOS
1. See requirements.txt in root directory of the repo to install all python3 dependencies.
2. **setup.sh** => create 2 copies of the Inpigritas core, named cli_1 and cli_2
3. **start.sh** => run cli_1 and cli_2 in a single cmd tab. Blocks will be created according to chainspec.py in "artifacts/cli-1" and "artifacts/cli-2" chainspecs have to be the same for both clients, except for the ports they run at / sync with respectively.

## Core containts
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
Synchronization and API are spun up through the multiprocessing python library. ( see run.py )

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
Inpigritas is a blockchain that can validate transfers and actions from a Genesis Block onwards. \
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

## History
I've been working on Inpigritas for years. The initial version was unmaintainable so I decided to create a new repo and re-factor the initial
[Prototype](https://github.com/jonas089/Inpigritas-2020-deprecated)
