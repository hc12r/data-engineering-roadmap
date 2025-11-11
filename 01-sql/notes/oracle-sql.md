# **Oracle SQL Notes**

Oracle SQL extends standard SQL with powerful features, proprietary functions, and performance optimizations that support large-scale transactional and analytical workloads. This document provides an overview of Oracle-specific syntax, key functions, sequences, indexes, and performance considerations relevant to data engineers.

---

# **1. Oracle-Specific Syntax and Characteristics**

## **1.1 Dual Table**

Oracle uses `DUAL` as a special one-row table for expressions, functions, or system values.

```sql
SELECT SYSDATE FROM dual;
```

## **1.2 String Concatenation**

Oracle uses `||` rather than `+` for concatenation.

```sql
SELECT first_name || ' ' || last_name AS full_name
FROM employees;
```

## **1.3 Date Handling**

Oracle stores dates with both date and time components.

```sql
SELECT TO_DATE('2025-01-15', 'YYYY-MM-DD')
FROM dual;
```

To truncate time:

```sql
SELECT TRUNC(SYSDATE) FROM dual;
```

---

# **2. Oracle Functions**

## **2.1 NVL**

Replaces NULL with a provided value.

```sql
SELECT NVL(commission, 0) AS commission_value
FROM sales;
```

Equivalent to:

* `COALESCE` but only supports two arguments.

## **2.2 NVL2**

Extends NVL:

* If expression is NOT NULL → return value1
* Else → return value2

```sql
SELECT NVL2(commission, 'HAS BONUS', 'NO BONUS')
FROM sales;
```

## **2.3 DECODE**

Oracle-specific conditional logic, similar to a switch statement.

```sql
SELECT
    DECODE(status,
        'S', 'SUCCESS',
        'F', 'FAILED',
        'UNKNOWN') AS status_desc
FROM transactions;
```

Equivalent to a simplified `CASE` expression.

## **2.4 Oracle CASE Expression**

Standard SQL but widely used in Oracle transformations.

```sql
SELECT
    CASE
        WHEN amount > 1000 THEN 'HIGH'
        WHEN amount > 100 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS category
FROM transactions;
```

---

# **3. Sequences**

Sequences generate unique numeric values, often used for primary keys.

## **3.1 Creating a Sequence**

```sql
CREATE SEQUENCE transaction_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE;
```

## **3.2 Using a Sequence**

```sql
INSERT INTO transactions (id, customer_id, amount)
VALUES (transaction_seq.NEXTVAL, 10, 500);
```

Retrieve the most recently generated value within the same session:

```sql
SELECT transaction_seq.CURRVAL FROM dual;
```

## **3.3 Identity Columns**

Oracle 12c+ supports identity columns:

```sql
CREATE TABLE orders (
    id NUMBER GENERATED ALWAYS AS IDENTITY,
    customer_id NUMBER,
    amount NUMBER
);
```

---

# **4. Indexes in Oracle**

Indexes improve query performance by enabling faster lookup of rows.

## **4.1 B-tree Indexes (default)**

Best for high-cardinality columns.

```sql
CREATE INDEX idx_transactions_customer
ON transactions(customer_id);
```

## **4.2 Bitmap Indexes**

Optimized for low-cardinality columns (e.g., gender, status).

```sql
CREATE BITMAP INDEX idx_status
ON transactions(status);
```

Not recommended for OLTP workloads due to locking behavior.

## **4.3 Function-Based Indexes**

Indexing expressions improves performance of computed lookups.

```sql
CREATE INDEX idx_upper_name
ON customers(UPPER(customer_name));
```

Oracle requires `QUERY_REWRITE_ENABLED` for optimizer usage.

## **4.4 Index Monitoring**

Check if indexes are actually used:

```sql
ALTER INDEX idx_transactions_customer MONITORING USAGE;

SELECT * 
FROM v$object_usage
WHERE index_name = 'IDX_TRANSACTIONS_CUSTOMER';
```

---

# **5. Oracle Performance Considerations**

## **5.1 Explain Plan**

Inspect execution plans:

```sql
EXPLAIN PLAN FOR
SELECT * FROM transactions WHERE amount > 1000;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

## **5.2 Hints**

Oracle hints influence the optimizer.

```sql
SELECT /*+ INDEX(transactions idx_transactions_customer) */
    *
FROM transactions
WHERE customer_id = 10;
```

Use hints sparingly; rely on the optimizer when possible.

## **5.3 Parallel Query**

Accelerate large scans:

```sql
SELECT /*+ PARALLEL(4) */
    COUNT(*)
FROM large_table;
```

## **5.4 Analytic Functions**

Oracle supports advanced analytics:

```sql
SELECT
    customer_id,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id) AS total_amount
FROM transactions;
```

## **5.5 Materialized Views**

Used for caching results and improving performance.

```sql
CREATE MATERIALIZED VIEW mv_daily_totals
REFRESH FAST ON COMMIT AS
SELECT customer_id, SUM(amount) total_amount
FROM transactions
GROUP BY customer_id;
```

---

# **6. Oracle SQL in Data Engineering**

Oracle SQL is widely used in enterprise environments, making it essential for:

* ETL and batch processing
* CDC with Oracle GoldenGate
* Scripting and automation with PL/SQL
* Validating and reconciling transactional datasets
* Supporting analytics teams via materialized views and optimized queries

Oracle’s advanced indexing, analytic functions, and performance tuning capabilities allow data engineers to build efficient, high-volume pipelines.