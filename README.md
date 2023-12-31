# Python Blockchain Transaction network "Inpigritas" - Portfolio Project by Jonas Pauli

Inpigritas is an experimental mini-project representing an MVP blockchain transaction network with noticable compromises.

2023 review: Due to a lack of a consensus protocol, **Inpigritas can never achieve perfect synchronisation**. 

Refactoring [here](https://github.com/jonas089/Inpigritas-2022/tree/concept)

# High-level XMind map 
![Inpigritas intro](https://github.com/jonas089/Inpigritas-2022/blob/master/high-level-mindmap.png)

## Implementation
Inpigritas is a blockchain transaction system that can validate actions from a Genesis Block onwards.

Every trusted peer needs to hold a copy of the Genesis Block on startup.

If a majority (n) of peers is hacked, the network is corrupt.

Example: n = 2/3 of total nodes operating.

Blocks are created locally on every node once time.time() == next_timestamp.

Transactions are stored in a txpool and will be included in a future block (era + n) where n is a constant integer.

Initial distribution of transferable assets happens in the Genesis Block.

## Run a local test-net
credit to [Carl Romedius](https://github.com/Rom3dius/) for helping with the Docker image setup.

To run a local Inpigritas network, start your docker cli and run the latest inpigritas image:
```bash
docker build -t inpigritas:latest .
docker compose up
```
This will start 2 Inpigritas nodes (node1, node2) locally on your machine, you can reach them through their ports (8080, 8081 respectively) and query the *Status* and *Read* routes of the API.

## Transfer validation
Transaction data ( hash of tx ) is signed using an RSA private key.

Nodes verify signatures and block hashes before syncing to an extent (Inpigritas is not sound and this is still a prototype).

Balance/ Accounting logic is yet to be implemented and the default Genesis Block holds no transactions.

## API
Nodes communicate by querying flask API routes.
 
A Node's synchronization and API processes are spawned simultaneously. (see run.py)

### The flask API enables users to query the entire chain (so long as it fits in device memory)**
![Inpigritas API](https://github.com/jonas089/Inpigritas-2022/blob/master/screenshots/flask.png)
(views blocks from height N onwards).

## Genesis
The Genesis Block is not included in validation process.

Every node needs a copy of the genesis block to be able to sync with the network.

The Genesis Block can hold transactions to initialize transferable balances (unimplemented).

## Scalability
Limited to pickle capabilities, 100% of historical chain is in memory.

It'd be beneficial to chunk blockchain data and use a scalable database when network synchronization is stable and core functionality is sound.

For R&D purposes a rollup system could be built on top of this network, to enable efficient real-world testing.

## Limitations
Scalability and Speed are not super high as of today, memory overflow in Pickle implementation inevitable. 

Inpigritas is a personal portfolio project but feel free to use it if you discover a use-case for it.

It is possible to track and prove an assets origin using Inpigritas or a variation of it.

Any integrations or use is/are at own Risk since Inpigritas is not intended to be used as production software!

## Screenshots
### Docker (Desktop) on MacOS
![docker preview](https://github.com/jonas089/Inpigritas-2022/blob/master/screenshots/docker-1.png)
![transactions](https://github.com/jonas089/Inpigritas-2022/blob/master/screenshots/tx-sync.png)

## Milestones
**07.02.2023**: Successfully synced a Transaction from the Pool ( flask API ) in a 2 node setup hosted locally 

**08.02.2023**: Introduction of "ictl" command line tool. Successfully synchronized 2900 Transactions in a single block.

**16.03.2023**: Merged docker

## History
The initial version was unmaintainable so I decided to create a new repo and re-factor the initial
[Prototype](https://github.com/jonas089/Inpigritas-2020-deprecated)
