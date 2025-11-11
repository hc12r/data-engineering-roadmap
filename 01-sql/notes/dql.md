# **Data Query Language (DQL)**

Data Query Language (DQL) is the subset of SQL used to retrieve data from relational databases. It focuses on reading, filtering, projecting, and combining data without modifying the underlying tables. DQL operations form the foundation of analytics, reporting, data validation, and pipeline development.

The primary DQL command is `SELECT`, supported by clauses that control which data is returned and how it is structured.

---

## **1. Purpose of DQL**

DQL is used to:

* Extract data for analysis or reporting
* Validate datasets before transformation
* Inspect source systems during data engineering work
* Support reconciliation processes by comparing datasets
* Feed downstream ETL or ELT pipelines

DQL commands do not alter database state; they operate in a read-only manner.

---

## **2. Core DQL Command: SELECT**

`SELECT` retrieves data from one or more tables or views. It supports:

* Column selection
* Expressions and functions
* Aliasing
* Derived fields
* Subqueries
* Joins and CTEs

**Example:**

```sql
SELECT customer_id, amount, status
FROM transactions;
```

---

## **3. Supporting Clauses**

DQL relies on several clauses to refine the result set.

### **3.1 FROM**

Specifies the table or tables to query.

```sql
SELECT *
FROM transactions;
```

### **3.2 WHERE**

Filters rows based on conditions.

```sql
SELECT *
FROM transactions
WHERE status = 'SUCCESS';
```

### **3.3 GROUP BY**

Aggregates rows based on shared column values.

```sql
SELECT customer_id, SUM(amount) AS total_amount
FROM transactions
GROUP BY customer_id;
```

### **3.4 HAVING**

Filters aggregated results.

```sql
SELECT customer_id, SUM(amount) AS total_amount
FROM transactions
GROUP BY customer_id
HAVING SUM(amount) > 1000;
```

### **3.5 ORDER BY**

Sorts results.

```sql
SELECT *
FROM transactions
ORDER BY timestamp DESC;
```

### **3.6 LIMIT / FETCH**

Restricts the number of returned rows.

```sql
SELECT *
FROM transactions
LIMIT 50;
```

---

## **4. DQL and Joins**

Join operations are part of DQL and enable combining data across tables.

Common join types include:

* INNER JOIN
* LEFT JOIN
* RIGHT JOIN
* FULL JOIN

**Example:**

```sql
SELECT t.transaction_id, c.customer_name
FROM transactions t
INNER JOIN customers c
    ON t.customer_id = c.id;
```

---

## **5. Subqueries and Derived Tables**

DQL supports embedding queries inside others.

```sql
SELECT *
FROM (
    SELECT customer_id, SUM(amount) AS total_amount
    FROM transactions
    GROUP BY customer_id
) AS aggregated
WHERE total_amount > 500;
```

Subqueries allow structuring multi-stage logic without modifying source tables.

---

## **6. DQL in Data Engineering**

Data engineers rely on DQL for:

* Source data profiling
* Data quality validation
* Reconciliation between systems
* Exploratory analysis before transformation
* Building intermediate views for pipelines
* Supporting analysts and data scientists with curated datasets

Because DQL is read-only, it is safe for exploration in production systems when proper limits and filters are applied.

---

## **7. Performance Considerations**

Although DQL does not modify data, inefficient queries can impact system performance.

Key principles:

* Use filters early (`WHERE` clauses)
* Select only required columns
* Avoid unnecessary sorting
* Inspect execution plans
* Index appropriately
* Limit result sets during exploration

Effective use of DQL improves pipeline reliability, reduces resource usage, and ensures faster delivery of insights.
