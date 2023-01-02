# Inpigritas 2022
Experimental python blockchain project. \
Improved version of Inpigritas-2020 ( see below ) \
Whilst developing core functionality, all data will be stored / read using pickle \
Database solution tbd.
## Inpigritas 2020 documentation for direct comparison and respective roadmap
[Inpigritas2020 Github](https://github.com/jonas089/Inpigritas-2020-deprecated)

## Core containts
1. Transfer class
2. Key-manager class
3. Blockchain and Block classes
4. Balance

## Transfer validation
TBD: pubkey => address => signature ( proof of identity ) \
1 account is bound to 1 address.

## API
Nodes communicate by calling endpoints of each others API instance. \
The API backend is programmed in Python-Flask. \
Synchronization and API are spun up through the multiprocessing python library. ( see run.py ) \

## Genesis
Genesis Block is not included in validation process. \
If Genesis account is hacked, Blockchain is corrupt. \
=> Broad distribution of Genesis data

## Scalability
Limited to pickle capabilities, 100% of historical chain is in memory. \
Change when network synchronization is stable and core functionality is built. \
TBD: migrate from pickle to a scalable database.

## Implementation
Inpigritas is a blockchain that can validate transfers and actions respectively from a Genesis Block. \
Every trusted peer needs to hold a copy of the Genesis Block on startup. \
If a majority (n) of peers is hacked, the network is corrupt. \
Example: n = 2/3 of total nodes operating. \
Blocks are created locally on every node once time.time() == next_timestamp. \
Transactions are stored in a txpool and will be included in a future block (era + n) where n is a constant integer. \
Initial distribution of transferable assets happens in the Genesis Block. \

## Limitations
Scalability and Speed are not super high, also, Inpigritas is currently not a programmable blockchain. \
Inpigritas is a personal portfolio project but feel free to use it if you find any Implementations for this Python-Blockchain. \
Thanks to RSA signatures and Block creation/validation logic it can potentially offer moderate security to small systems / services. \
It is possible to track and prove an assets origin using Inpigritas or a variation of it. \
Use is at own Risk and this is not a production Blockchain!
