# Feature Store Concepts

- Purpose: centralize, version, and serve features for ML training and inference.
- Key components: feature definitions, transformation pipelines, storage (offline/online), lineage & governance.
- Patterns:
  - Offline store (e.g., data lake/warehouse) for training datasets.
  - Online store (e.g., Redis, DynamoDB) for low-latency inference features.
  - Materialization jobs to keep online features fresh (TTL, backfills).
- Considerations: time-travel correctness, point-in-time joins, feature quality monitoring, ownership model.
- Tools: Feast, Tecton, Databricks Feature Store, custom implementations on Spark + lakehouse.