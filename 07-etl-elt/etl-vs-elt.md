# ETL vs ELT

- ETL: transform before loading into warehouse; common for legacy systems or when compute lives outside the warehouse.
- ELT: load first, transform in place using warehouse engines; leverages scalable MPP compute.
- Considerations: data volumes, latency, compliance, cost, skillset, tool ecosystem.
