# **Joins and Window Functions**

Joins and window functions are essential SQL concepts for combining, analyzing, and enriching datasets. They enable data engineers to build complex transformations, reconciliation logic, and analytical outputs without duplicating data or performing unnecessary preprocessing.

This document covers the fundamentals of join operations and the structure, purpose, and use cases of window functions, with detailed examples showing input and output tables.

---

# **1. Joins**

A join operation combines rows from two or more tables based on a related column. Joins are fundamental in relational databases, where data is normalized and spread across multiple tables.

## **1.1 INNER JOIN**

Returns rows where both tables have matching values. This is the most restrictive join, only including records that exist in both tables.

**Example:**

```sql
SELECT t.transaction_id, t.amount, c.customer_name
FROM transactions t
INNER JOIN customers c
    ON t.customer_id = c.customer_id;
```

**Input Tables:**

`customers` table:

| customer_id | customer_name | city        |
|-------------|---------------|-------------|
| 1           | Alice Smith   | New York    |
| 2           | Bob Jones     | London      |
| 3           | Carol White   | Paris       |

`transactions` table:

| transaction_id | customer_id | amount |
|----------------|-------------|--------|
| 101            | 1           | 250.00 |
| 102            | 2           | 180.50 |
| 103            | 1           | 420.00 |
| 104            | 5           | 99.99  |

**Output:**

| transaction_id | amount | customer_name |
|----------------|--------|---------------|
| 101            | 250.00 | Alice Smith   |
| 102            | 180.50 | Bob Jones     |
| 103            | 420.00 | Alice Smith   |

**Key Insight:** Transaction 104 (customer_id = 5) is excluded because there's no matching customer. Customer Carol White (id = 3) doesn't appear because she has no transactions.

**Use when:**
- Only matched records should be included
- You want to exclude orphaned records from either table
- Data quality requires both entities to exist

---

## **1.2 LEFT JOIN**

Returns all rows from the left table and the matched rows from the right table. Unmatched right-side values appear as NULL. This preserves the completeness of your primary dataset.

**Example:**

```sql
SELECT c.customer_id, c.customer_name, t.transaction_id, t.amount
FROM customers c
LEFT JOIN transactions t
    ON c.customer_id = t.customer_id;
```

**Input Tables:** (same as above)

**Output:**

| customer_id | customer_name | transaction_id | amount |
|-------------|---------------|----------------|--------|
| 1           | Alice Smith   | 101            | 250.00 |
| 1           | Alice Smith   | 103            | 420.00 |
| 2           | Bob Jones     | 102            | 180.50 |
| 3           | Carol White   | NULL           | NULL   |

**Key Insight:** Carol White appears with NULL transaction values because she has no transactions. This is crucial for identifying customers without activity.

**Use when:**
- You need a complete view of the left dataset, even if no match exists
- Identifying missing relationships (e.g., customers without orders)
- Preserving all records from a master or dimension table
- Building reports where zero values should be shown as NULL

---

## **1.3 RIGHT JOIN**

Opposite of LEFT JOIN. Returns all rows from the right table and matches from the left. In practice, RIGHT JOINs are less commonly used because they can be confusing to read.

**Best Practice:** Prefer rearranging the query and using a LEFT JOIN for clarity and consistency in your codebase.

---

## **1.4 FULL JOIN**

Returns rows when there is a match in either table. Shows all data, with NULLs where no match exists. This is the most comprehensive join, showing the complete picture of both datasets.

**Example:**

```sql
SELECT 
    COALESCE(c.customer_id, t.customer_id) AS customer_id,
    c.customer_name,
    t.transaction_id,
    t.amount
FROM customers c
FULL JOIN transactions t
    ON c.customer_id = t.customer_id;
```

**Input Tables:** (same as above)

**Output:**

| customer_id | customer_name | transaction_id | amount |
|-------------|---------------|----------------|--------|
| 1           | Alice Smith   | 101            | 250.00 |
| 1           | Alice Smith   | 103            | 420.00 |
| 2           | Bob Jones     | 102            | 180.50 |
| 3           | Carol White   | NULL           | NULL   |
| 5           | NULL          | 104            | 99.99  |

**Key Insight:** Both Carol White (no transactions) and the orphaned transaction 104 (no customer) appear. This is perfect for data quality audits and reconciliation.

**Use when:**
- Performing reconciliation or comparing two datasets for completeness
- Identifying orphaned records in either table
- Data quality audits requiring full visibility
- Merging data from two independent sources

---

## **1.5 CROSS JOIN**

Returns the Cartesian product of both tables. Every row from the first table is combined with every row from the second table.

**Example:**

```sql
SELECT c.currency_code, co.country_name
FROM currencies c
CROSS JOIN countries co;
```

**Input Tables:**

`currencies` table:

| currency_code |
|---------------|
| USD           |
| EUR           |

`countries` table:

| country_name |
|--------------|
| USA          |
| France       |
| Japan        |

**Output:**

| currency_code | country_name |
|---------------|--------------|
| USD           | USA          |
| USD           | France       |
| USD           | Japan        |
| EUR           | USA          |
| EUR           | France       |
| EUR           | Japan        |

**Key Insight:** With 2 currencies and 3 countries, we get 6 rows (2 × 3). This grows exponentially with larger tables.

**Use when:**
- Generating all possible combinations for scenario planning
- Creating calendar tables with date ranges
- Testing data generation
- Setting up configuration matrices

**Warning:** Rarely used in production transformations due to exponential growth. Be cautious with large tables.

---

## **1.6 Practical Applications in Data Engineering**

- **Combining dimension and fact tables:** INNER JOIN facts to dimensions for complete context
- **Building enriched datasets for analytics:** LEFT JOIN to preserve all fact records
- **Reconciling transaction logs across different systems:** FULL JOIN to find discrepancies
- **Validating data integrity between sources:** Find orphaned records
- **Feature engineering for model inputs:** Create derived attributes through joins
- **Historical tracking:** Join snapshot tables with SCDs (Slowly Changing Dimensions)

---

# **2. Window Functions**

Window functions perform calculations across a set of rows related to the current row, without collapsing the result set as aggregates do. They operate over a "window" defined by the `OVER` clause.

The key distinction: **GROUP BY reduces rows, window functions preserve them while adding analytical context.**

Window functions are critical for analytical pipelines, ranking, deduplication, time series calculations, and reconciliation workflows.

---

## **2.1 Structure of a Window Function**

**General syntax:**

```sql
function_name(expression) OVER (
    [PARTITION BY column]
    [ORDER BY column]
    [frame_clause]
)
```

**Components:**
- **PARTITION BY**: Splits data into independent groups (like GROUP BY, but doesn't collapse rows)
- **ORDER BY**: Defines the sequence for ordered calculations (ranking, LAG/LEAD)
- **OVER**: Specifies the window boundaries and scope
- **frame_clause**: Optional - defines which rows to include (ROWS/RANGE BETWEEN)

---

# **3. Types of Window Functions**

## **3.1 Ranking Functions**

### **ROW_NUMBER()**

Assigns a unique sequential integer to each row within each partition, starting at 1. No ties—every row gets a unique number.

**Example:**

```sql
SELECT
    customer_id,
    transaction_id,
    amount,
    timestamp,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY timestamp DESC
    ) AS rn
FROM transactions;
```

**Input Table:**

`transactions` table:

| customer_id | transaction_id | amount | timestamp           |
|-------------|----------------|--------|---------------------|
| 1           | 101            | 250.00 | 2025-01-15 10:30:00 |
| 1           | 103            | 420.00 | 2025-01-20 14:15:00 |
| 1           | 105            | 180.00 | 2025-01-18 09:00:00 |
| 2           | 102            | 180.50 | 2025-01-16 11:20:00 |
| 2           | 104            | 99.99  | 2025-01-19 16:45:00 |

**Output:**

| customer_id | transaction_id | amount | timestamp           | rn |
|-------------|----------------|--------|---------------------|----|
| 1           | 103            | 420.00 | 2025-01-20 14:15:00 | 1  |
| 1           | 105            | 180.00 | 2025-01-18 09:00:00 | 2  |
| 1           | 101            | 250.00 | 2025-01-15 10:30:00 | 3  |
| 2           | 104            | 99.99  | 2025-01-19 16:45:00 | 1  |
| 2           | 102            | 180.50 | 2025-01-16 11:20:00 | 2  |

**Key Insight:** Each partition (customer) gets its own numbering sequence. Row number 1 represents the most recent transaction per customer.

**Use when:**
- Identifying the latest/first record per group
- Removing duplicates (WHERE rn = 1)
- Selecting top N entries per category
- Creating sequence numbers within groups

---

### **RANK() and DENSE_RANK()**

Both assign ranks based on ORDER BY values, but handle ties differently:
- **RANK()**: Leaves gaps after ties (1, 2, 2, 4)
- **DENSE_RANK()**: No gaps in ranking (1, 2, 2, 3)

**Example:**

```sql
SELECT
    product_name,
    sales_amount,
    RANK() OVER (ORDER BY sales_amount DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY sales_amount DESC) AS dense_rank
FROM product_sales;
```

**Input Table:**

`product_sales` table:

| product_name | sales_amount |
|--------------|--------------|
| Laptop       | 5000         |
| Phone        | 3000         |
| Tablet       | 3000         |
| Monitor      | 1500         |

**Output:**

| product_name | sales_amount | rank | dense_rank |
|--------------|--------------|------|------------|
| Laptop       | 5000         | 1    | 1          |
| Phone        | 3000         | 2    | 2          |
| Tablet       | 3000         | 2    | 2          |
| Monitor      | 1500         | 4    | 3          |

**Key Insight:** RANK() skips to 4 after the tie, while DENSE_RANK() continues to 3.

**Use when:**
- Competitive rankings where ties share positions
- Identifying top performers with natural ranking gaps (RANK)
- Continuous ranking sequences (DENSE_RANK)

---

## **3.2 Aggregate Window Functions**

Perform aggregate operations without grouping the rows. Each row retains its identity while gaining aggregate context.

Examples: `SUM()`, `AVG()`, `COUNT()`, `MIN()`, `MAX()`

**Example:**

```sql
SELECT
    customer_id,
    transaction_id,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id) AS total_per_customer,
    AVG(amount) OVER (PARTITION BY customer_id) AS avg_per_customer,
    COUNT(*) OVER (PARTITION BY customer_id) AS transaction_count
FROM transactions;
```

**Input Table:**

`transactions` table:

| customer_id | transaction_id | amount |
|-------------|----------------|--------|
| 1           | 101            | 250.00 |
| 1           | 103            | 420.00 |
| 1           | 105            | 180.00 |
| 2           | 102            | 180.50 |
| 2           | 104            | 99.99  |

**Output:**

| customer_id | transaction_id | amount | total_per_customer | avg_per_customer | transaction_count |
|-------------|----------------|--------|--------------------|------------------|-------------------|
| 1           | 101            | 250.00 | 850.00             | 283.33           | 3                 |
| 1           | 103            | 420.00 | 850.00             | 283.33           | 3                 |
| 1           | 105            | 180.00 | 850.00             | 283.33           | 3                 |
| 2           | 102            | 180.50 | 280.49             | 140.25           | 2                 |
| 2           | 104            | 99.99  | 280.49             | 140.25           | 2                 |

**Key Insight:** All transactions remain visible, but each includes the aggregate metrics for their customer. This allows comparison of individual transactions against group totals.

**Use when:**
- You need aggregated values alongside detailed records
- Calculating percentage of total (amount / total_per_customer)
- Comparing individual values to group averages
- Building analytical features without losing granularity

---

## **3.3 Value Functions**

### **LAG() and LEAD()**

Access the previous or next row within a partition, based on the ORDER BY clause.

- **LAG(column, offset, default)**: Looks backward
- **LEAD(column, offset, default)**: Looks forward

**Example:**

```sql
SELECT
    transaction_date,
    amount,
    LAG(amount, 1) OVER (ORDER BY transaction_date) AS previous_amount,
    LEAD(amount, 1) OVER (ORDER BY transaction_date) AS next_amount,
    amount - LAG(amount, 1) OVER (ORDER BY transaction_date) AS change_from_previous
FROM daily_transactions;
```

**Input Table:**

`daily_transactions` table:

| transaction_date | amount |
|------------------|--------|
| 2025-01-15       | 250.00 |
| 2025-01-16       | 320.00 |
| 2025-01-17       | 180.00 |
| 2025-01-18       | 420.00 |

**Output:**

| transaction_date | amount | previous_amount | next_amount | change_from_previous |
|------------------|--------|-----------------|-------------|----------------------|
| 2025-01-15       | 250.00 | NULL            | 320.00      | NULL                 |
| 2025-01-16       | 320.00 | 250.00          | 180.00      | 70.00                |
| 2025-01-17       | 180.00 | 320.00          | 420.00      | -140.00              |
| 2025-01-18       | 420.00 | 180.00          | NULL        | 240.00               |

**Key Insight:** LAG and LEAD enable row-to-row comparisons without self-joins. The first row has no previous value, and the last row has no next value.

**Use when:**
- Analyzing time series data
- Detecting anomalies or significant changes
- Computing differences between consecutive transactions
- Identifying trends (increasing/decreasing patterns)
- Calculating growth rates

---

## **3.4 Window Frame Clauses**

Define the precise range of rows considered for the calculation. Frames allow you to create sliding windows for moving calculations.

**Syntax:**
```sql
ROWS BETWEEN <start> AND <end>
```

**Common frame specifications:**
- `UNBOUNDED PRECEDING`: From the start of the partition
- `N PRECEDING`: N rows before current row
- `CURRENT ROW`: The current row
- `N FOLLOWING`: N rows after current row
- `UNBOUNDED FOLLOWING`: To the end of the partition

**Example: 3-Day Moving Average**

```sql
SELECT
    transaction_date,
    amount,
    AVG(amount) OVER (
        ORDER BY transaction_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3day
FROM daily_transactions;
```

**Input Table:**

`daily_transactions` table:

| transaction_date | amount |
|------------------|--------|
| 2025-01-15       | 100.00 |
| 2025-01-16       | 200.00 |
| 2025-01-17       | 300.00 |
| 2025-01-18       | 400.00 |
| 2025-01-19       | 500.00 |

**Output:**

| transaction_date | amount | moving_avg_3day |
|------------------|--------|-----------------|
| 2025-01-15       | 100.00 | 100.00          |
| 2025-01-16       | 200.00 | 150.00          |
| 2025-01-17       | 300.00 | 200.00          |
| 2025-01-18       | 400.00 | 300.00          |
| 2025-01-19       | 500.00 | 400.00          |

**Key Insight:** The moving average considers the current row and 2 preceding rows. First row: only itself (100/1). Second row: (100+200)/2 = 150. Third onward: 3 values averaged.

**Use when:**
- Computing moving averages or rolling sums
- Smoothing time series data
- Creating cumulative totals
- Analyzing trends over sliding windows

---

# **4. Window Functions vs GROUP BY**

**Critical Distinction:**

**GROUP BY aggregation:**
```sql
SELECT customer_id, SUM(amount) AS total
FROM transactions
GROUP BY customer_id;
```

Output: 1 row per customer (collapsed)

| customer_id | total  |
|-------------|--------|
| 1           | 850.00 |
| 2           | 280.49 |

**Window function:**
```sql
SELECT customer_id, transaction_id, amount,
    SUM(amount) OVER (PARTITION BY customer_id) AS total
FROM transactions;
```

Output: All original rows preserved with aggregate added

| customer_id | transaction_id | amount | total  |
|-------------|----------------|--------|--------|
| 1           | 101            | 250.00 | 850.00 |
| 1           | 103            | 420.00 | 850.00 |
| 1           | 105            | 180.00 | 850.00 |
| 2           | 102            | 180.50 | 280.49 |
| 2           | 104            | 99.99  | 280.49 |

**When to use which:**
- **GROUP BY**: When you only need aggregated results
- **Window Functions**: When you need both detail and aggregates simultaneously

This distinction makes window functions preferable for complex analytical logic where context matters.

---

# **5. Practical Use Cases for Data Engineers**

**Deduplication and record ranking:**
```sql
-- Keep only the latest version of each record
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) AS rn
    FROM staging_table
)
SELECT * FROM ranked WHERE rn = 1;
```

**Detecting changes in transaction streams:**
```sql
-- Flag when amount changes by more than 50%
SELECT *,
    CASE 
        WHEN ABS(amount - LAG(amount) OVER (ORDER BY timestamp)) / 
             LAG(amount) OVER (ORDER BY timestamp) > 0.5 
        THEN 'ANOMALY' 
        ELSE 'NORMAL' 
    END AS status
FROM transactions;
```

**Time-based aggregations:**
```sql
-- 7-day rolling revenue
SELECT date, revenue,
    SUM(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_7d
FROM daily_revenue;
```

**Customer behavior analysis:**
```sql
-- Days since last purchase
SELECT customer_id, purchase_date,
    purchase_date - LAG(purchase_date) OVER (PARTITION BY customer_id ORDER BY purchase_date) AS days_since_last
FROM purchases;
```

**Identifying mismatches in reconciliation processes:**
```sql
-- Compare transaction counts between systems
SELECT date,
    COUNT(*) OVER (PARTITION BY date) AS system_a_count,
    SUM(COUNT(*)) OVER (ORDER BY date) AS cumulative_count
FROM system_a_transactions;
```

**Building features for machine learning workflows:**
```sql
-- Create recency, frequency, monetary features
SELECT customer_id,
    MAX(transaction_date) OVER (PARTITION BY customer_id) AS last_purchase,
    COUNT(*) OVER (PARTITION BY customer_id) AS purchase_frequency,
    AVG(amount) OVER (PARTITION BY customer_id) AS avg_transaction_value
FROM transactions;
```

---

# **6. Performance Considerations**

**Optimization tips:**
1. **Indexes matter**: Ensure columns in PARTITION BY and ORDER BY are indexed
2. **Limit partitions**: Fewer, larger partitions perform better than many tiny ones
3. **Frame clauses**: Specific frame clauses are faster than unbounded windows
4. **Materialize results**: For reused window calculations, compute once and store
5. **Partition pruning**: Filter data before applying window functions when possible

**Common pitfalls:**
- Multiple window functions with different OVER clauses force separate scans
- Unbounded frames on large partitions can consume significant memory
- Complex expressions in ORDER BY slow down sorting operations

---

# **7. Summary**

**Joins** combine datasets horizontally, enabling data enrichment and relationship mapping:
- INNER: Strict matching
- LEFT: Preserve left table
- FULL: Complete picture
- CROSS: All combinations

**Window Functions** add analytical context without collapsing rows:
- Ranking: Identify top/bottom records
- Aggregates: Compare individual vs group metrics
- Value functions: Row-to-row comparisons
- Frames: Sliding window calculations

Together, these tools form the foundation of sophisticated SQL analytics and data transformation pipelines.