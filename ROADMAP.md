# Roadmap and TBDs
Some ideas to improve and re-structure this project over time
## Transactions
1. Transaction-height should not be mutable. When a transaction is broadcasted, it's height should be
at least instance.height() + n = h(t)
until h(t) is reached, the transaction should have been broadcasted to all active nodes.
create & save => broadcast => validate => save => add to block h(t)
Majority of active nodes have to agree over the state of the chain => need 3 instances to form majority
## Classes
1. change some functions to just attributes. height() is an example for this.
2. improve structure of client.py
