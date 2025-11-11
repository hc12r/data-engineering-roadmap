# **Normalization**

Normalization is the process of organizing data in relational databases to reduce redundancy, improve data integrity, and ensure consistent updates. It is achieved by structuring tables according to logical rules known as normal forms. Each normal form adds constraints that reduce anomalies in insert, update, and delete operations.

This document covers 1NF, 2NF, 3NF, and BCNF, followed by practical guidance on when to denormalize for analytics and performance.

---

# **1. First Normal Form (1NF)**

A table is in 1NF when:

1. All values are atomic (no repeating groups, arrays, or composite values).
2. Every record is unique.
3. There are no repeating columns.

### **Example (Not in 1NF)**

| order_id | customer_id | items                 |
| -------- | ----------- | --------------------- |
| 1        | 10          | "Pen, Notebook"       |
| 2        | 11          | "Paper, Pencil, Glue" |

`items` contains multiple values in one field.

### **Corrected (1NF)**

| order_id | customer_id | item     |
| -------- | ----------- | -------- |
| 1        | 10          | Pen      |
| 1        | 10          | Notebook |
| 2        | 11          | Paper    |
| 2        | 11          | Pencil   |
| 2        | 11          | Glue     |

---

# **2. Second Normal Form (2NF)**

A table is in 2NF when:

1. It is already in 1NF.
2. All non-key attributes depend on the *entire* primary key (applies only to composite keys).

### **Example (Not in 2NF)**

Composite primary key: `(order_id, item_id)`

| order_id | item_id | item_name | customer_name |
| -------- | ------- | --------- | ------------- |
| 1        | 1       | Pen       | Ana           |
| 1        | 2       | Notebook  | Ana           |

`customer_name` depends on `order_id` only, not the whole key.

### **Corrected (2NF)**

Split into two tables:

**orders**

| order_id | customer_name |
| -------- | ------------- |
| 1        | Ana           |

**order_items**

| order_id | item_id | item_name |
| -------- | ------- | --------- |
| 1        | 1       | Pen       |
| 1        | 2       | Notebook  |

---

# **3. Third Normal Form (3NF)**

A table is in 3NF when:

1. It is already in 2NF.
2. There are no transitive dependencies (non-key attributes must not depend on other non-key attributes).

### **Example (Not in 3NF)**

| customer_id | customer_name | city   | country    |
| ----------- | ------------- | ------ | ---------- |
| 10          | Ana           | Maputo | Mozambique |
| 11          | Carlos        | Beira  | Mozambique |

`country` depends on `city`, not directly on the key.

### **Corrected (3NF)**

**customers**

| customer_id | customer_name | city_id |
| ----------- | ------------- | ------- |
| 10          | Ana           | 1       |
| 11          | Carlos        | 2       |

**cities**

| city_id | city   | country    |
| ------- | ------ | ---------- |
| 1       | Maputo | Mozambique |
| 2       | Beira  | Mozambique |

---

# **4. Boyce–Codd Normal Form (BCNF)**

BCNF is a stronger version of 3NF.
A table is in BCNF when:

* For every functional dependency X → Y, X is a superkey.

BCNF fixes anomalies that 3NF does not guarantee to solve, especially when alternative candidate keys exist.

### **Example (Not in BCNF)**

| course | instructor |
| ------ | ---------- |
| SQL101 | Ana        |
| DS201  | Ana        |
| DS201  | Carlos     |

Assume:

* A course is always taught in one classroom.
* An instructor is assigned to only one classroom.
* But instructors may teach multiple courses.

Functional dependencies:

* `course → instructor`
* `instructor → classroom`

`instructor` is not a key, so the second dependency violates BCNF.

### **Corrected**

Split into:

**courses**

| course | instructor |
| ------ | ---------- |
| SQL101 | Ana        |
| DS201  | Carlos     |

**instructors**

| instructor | classroom |
| ---------- | --------- |
| Ana        | A1        |
| Carlos     | B1        |

---

# **5. When Denormalization Is Necessary**

While normalization improves integrity, it may reduce performance in analytical workloads where frequent joins over large tables can be expensive.
Data engineers often denormalize intentionally in:

## **5.1 Data Warehouses**

* Star schemas (fact + dimension tables)
* Snowflake schemas with partial denormalization
* Pre-aggregated summary tables

## **5.2 Performance Optimization**

* Reducing join complexity
* Improving query latency in BI dashboards
* Supporting real-time analytics

## **5.3 FinTech Use Cases**

* Reconciliation pipelines requiring quick comparisons
* Frequently accessed customer or transaction attributes
* Precomputed balances and metrics for faster retrieval

## **5.4 Guidelines**

Denormalize when:

* Read performance matters more than write performance
* Joins dominate query cost
* Data is immutable (facts) or updated in batches
* You can enforce integrity using ETL pipelines or quality checks

Normalize when:

* Strong integrity constraints are required
* Data changes frequently
* You must avoid anomalies or inconsistencies