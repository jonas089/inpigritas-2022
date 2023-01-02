# Inpigritas 2022
Experimental python blockchain project. \
Whilst developing core functionality, all data will be stored / read using pickle \
Database solution tbd.
## Inpigritas 2020 documentation for direct comparison and respective roadmap
[Inpigritas2020 Github](https://github.com/jonas089/Inpigritas-2020-deprecated)

## Core overview
1. Transfer class
2. Key-manager class
3. Blockchain and Block classes
4. Balance

## Transfer validation
TBD: pubkey => address => signature ( proof of identity )

## Synchronization
Can Txpool sync fast enough? Will txs get lost? \
Transactions can get lost when a node is busy creating a Block and deletes the file from the txpool. \
How can this be prevented? -> Nodes should stop adding to the txpool when creating a block.

## Genesis
Genesis Block is not included in validation process. \
If Genesis account is hacked, Blockchain is corrupt. \
=> Broad distribution of Genesis funds

## Scalability
Limited to pickle capabilities, 100% of historical chain is in memory. \
Change when network synchronization is stable and core functionality is built.
