# CAP Theorem

The **CAP theorem**, also known as **Brewer’s theorem**, states that a distributed data store can only guarantee **two** of the following **three** properties at any given time:

1. **Consistency (C)** – Every read receives the most recent write or an error.  
   - The system behaves as if there is only one up-to-date copy of the data.  
   - Example: Traditional relational databases often prioritize consistency.

2. **Availability (A)** – Every request receives a non-error response, even if it might not be the most recent data.  
   - The system remains operational and responsive under failure conditions.  
   - Example: DNS and some NoSQL systems emphasize availability.

3. **Partition Tolerance (P)** – The system continues to function even if there is a communication breakdown between nodes in the network.  
   - Network failures or latency do not cause the system to halt entirely.  
   - Example: Any distributed system deployed over a network must handle partitions.

---

## Trade-offs

In real-world distributed systems, **network partitions are inevitable**, which means that a system must choose between **Consistency** and **Availability** when a partition occurs.

| Combination | Description | Typical Systems |
|--------------|--------------|----------------|
| **CA (Consistency + Availability)** | Works well in single-node or tightly coupled clusters. Fails under network partition. | Traditional relational databases |
| **CP (Consistency + Partition Tolerance)** | Prioritizes consistency at the cost of availability during partition. | HBase, MongoDB (configurable), Zookeeper |
| **AP (Availability + Partition Tolerance)** | Remains available but may return stale data during partition. | Cassandra, DynamoDB, Couchbase |

---

## Practical Implications

- **Strong consistency** is preferred in financial transactions, banking, and accounting systems.  
- **High availability** is more important in user-facing applications like social media feeds or caching layers.  
- Many modern databases provide **tunable consistency**, allowing developers to configure the level of consistency vs. availability based on business needs.

---

## Summary

The CAP theorem helps guide architectural decisions when designing distributed data systems. It emphasizes that **perfect consistency, availability, and partition tolerance cannot coexist** — system architects must make trade-offs depending on the use case.