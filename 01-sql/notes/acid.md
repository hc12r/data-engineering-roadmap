# **ACID Properties**

ACID is a foundational concept in relational database systems that ensures reliable, predictable, and consistent behavior when executing transactions. Each letter represents a property that guarantees data integrity even under failure conditions, concurrency, or system interruptions.

## **1. Atomicity**

Atomicity ensures that a transaction is treated as a single, indivisible unit of work. All operations within the transaction must succeed, or none of them are applied.
If any step fails, the database must roll back to its previous consistent state.

**Key characteristics:**

* All-or-nothing execution
* Rollback on failure
* Prevents partial updates

Example: If you transfer money from account A to account B, both the debit from A and the credit to B must happen. If the process fails after the debit but before the credit, the entire transaction is rolled back, and the database returns to its original state. 

## **2. Consistency**

Consistency ensures that a transaction can only bring the database from one valid state to another valid state according to defined rules, constraints, and data integrity requirements.

**Key characteristics:**

* Enforces constraints, triggers, and rules
* Maintains referential integrity
* Prevents invalid or contradictory data

Example: If a rule states that a bank account balance cannot be negative, a transaction that would result in a negative balance will fail, and the database will not be left in an inconsistent state. 

## **3. Isolation**

Isolation ensures that concurrent transactions do not interfere with each other.
Each transaction should behave as if it is executed independently, even when multiple transactions run at the same time.

**Key characteristics:**

* Prevents dirty reads, non-repeatable reads, and phantom reads
* Controlled by isolation levels (READ COMMITTED, SERIALIZABLE, and others)
* Reduces data anomalies in concurrent environments

Example: when multiple users are reading and writing from the same table all at once, isolation of their transactions ensures that the concurrent transactions don't interfere with or affect one another. Each request can occur as though they were occurring one by one, even though they're actually occurring simultaneously *.

\* link: https://www.databricks.com/glossary/acid-transactions

## **4. Durability**

Durability guarantees that once a transaction is committed, its effects are permanently recorded, even in the case of power failures, crashes, or unexpected shutdowns.

**Key characteristics:**

* Data persistence after commit
* Typically implemented through logs and persistent storage
* Ensures long-term reliability of committed data

Example: After a successful transaction has been committed, the changes are saved to non-volatile memory, and the system is designed to restore this state even if it crashes immediately afterward. 

---

## **ACID in Practice**

ACID compliance is critical for systems where correctness and data integrity are non-negotiable, such as financial services, mobile money processing, reconciliation workflows, and operational databases.

Relational databases like Oracle, PostgreSQL, SQL Server, and MySQL use transaction logs, locks, checkpoints, and write-ahead logging to enforce ACID guarantees.
