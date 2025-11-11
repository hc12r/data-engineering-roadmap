# **Common Table Expressions (CTEs)**

A Common Table Expression (CTE) is a temporary, named result set defined within the execution scope of a single SQL statement. CTEs improve query readability, support modular design, and allow recursive operations.

CTEs are introduced using the `WITH` keyword and can reference themselves or other CTEs defined in the same block.

---

## **1. Purpose of CTEs**

CTEs are commonly used to:

* Simplify complex queries
* Improve readability compared to nested subqueries
* Break down transformations into logical steps
* Reuse intermediate results within the same query
* Enable recursive queries (hierarchical or sequential data)

For data engineering tasks, CTEs are essential when building reconciliation logic, validation layers, and multi-step transformations.

---

## **2. Basic Structure**

A simple CTE consists of a name, a column list (optional), and a query.

**Syntax:**

```sql
WITH cte_name AS (
    SELECT ...
)
SELECT *
FROM cte_name;
```

---

## **3. Example: Filtering and Aggregation**

This example uses a CTE to isolate successful transactions before aggregating totals.

```sql
WITH successful_tx AS (
    SELECT transaction_id, customer_id, amount
    FROM transactions
    WHERE status = 'SUCCESS'
)
SELECT customer_id, SUM(amount) AS total_amount
FROM successful_tx
GROUP BY customer_id;
```

The CTE improves readability by separating filtering logic from aggregation logic.

---

## **4. Multiple CTEs**

Multiple CTEs can be chained, allowing step-by-step transformations.

```sql
WITH filtered AS (
    SELECT *
    FROM transactions
    WHERE status = 'SUCCESS'
),
enhanced AS (
    SELECT customer_id, amount, amount * 0.02 AS fee
    FROM filtered
)
SELECT *
FROM enhanced;
```

CTEs execute in the order they are defined and can reference one another.

---

## **5. Recursive CTEs**

Recursive CTEs enable hierarchical or iterative queries. A recursive CTE has two parts:

* **Anchor member**: the initial result
* **Recursive member**: references the CTE itself

**Example:**

```sql
WITH RECURSIVE counter AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1
    FROM counter
    WHERE n < 10
)
SELECT *
FROM counter;
```

Recursive CTEs are particularly useful for:

* Tree structures (e.g., organizational charts)
* Ledger trails
* Sequential record generation
* Dependency resolution

---

## **6. Performance Considerations**

While CTEs improve readability, they do not always improve performance.
Key considerations:

* Some databases materialize CTE results, while others inline them
* For repeated use, CTEs may be more efficient than repeating subqueries
* For large datasets or complex pipelines, testing execution plans is required
* In Oracle and PostgreSQL, CTEs may prevent certain optimizations unless explicitly inlined

For performance-critical workloads, especially in data engineering pipelines, always check query plans and benchmark alternatives.

---

## **7. Practical Use in Data Engineering**

CTEs are frequently used to structure multi-step logic such as:

* Data cleansing and validation
* Transaction reconciliation
* Aggregation pipelines
* Feature engineering for analytics
* Multi-layered joins and transformations

Their ability to decompose transformations makes them a reliable tool when designing clear and maintainable SQL pipelines.