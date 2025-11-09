# CAP Theorem

The CAP theorem states that in a distributed system you can only guarantee two of the following three properties at any given time:

- Consistency: Every read receives the most recent write or an error.
- Availability: Every request receives a (non-error) response, without guarantee that it contains the most recent write.
- Partition Tolerance: The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes.

Common trade-offs:
- CA (rare in practice in distributed systems because partitions happen)
- CP (e.g., systems prioritizing consistency like HBase, ZooKeeper)
- AP (e.g., systems prioritizing availability like Dynamo-style stores, Cassandra)
