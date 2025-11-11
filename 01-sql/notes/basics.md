# **SQL Basics**

Structured Query Language (SQL) is the standard language used to manage and query relational databases. This section introduces core elements required to read, filter, aggregate, and structure data effectively.

SQL fundamentals are essential for data engineering tasks such as data extraction, transformation, validation, and reconciliation.

---

## **1. Data Types**

Relational databases provide a set of data types used to define column structure and ensure consistency. Although specific types vary between systems, the following categories are common:

### **Numeric**

* `INT`, `BIGINT`, `SMALLINT`
* `DECIMAL(p, s)`, `NUMERIC`
* `FLOAT`, `DOUBLE`

### **Text**

* `CHAR(n)`
* `VARCHAR(n)`
* `TEXT`

### **Date and Time**

* `DATE`
* `TIME`
* `TIMESTAMP`
* `INTERVAL`

### **Boolean**

* `BOOLEAN` or equivalent representation

### **Binary**

* `BLOB`, `VARBINARY`

Correct selection of data types influences performance, storage usage, and data accuracy.

---

## **2. SELECT**

`SELECT` retrieves data from one or more tables. It supports column selection, expressions, aliases, and derived fields.

**Example:**

```sql
SELECT id, customer_name, amount
FROM transactions;
```

---

## **3. WHERE**

`WHERE` filters rows based on conditions. It supports logical operators, comparisons, pattern matching, and functions.

**Example:**

```sql
SELECT *
FROM transactions
WHERE amount > 1000 AND status = 'SUCCESS';
```

---

## **4. GROUP BY**

`GROUP BY` aggregates rows that share the same values in specified columns. It must be used with aggregate functions.

Common aggregate functions:

* `COUNT()`
* `SUM()`
* `AVG()`
* `MIN()`
* `MAX()`

**Example:**

```sql
SELECT customer_id, SUM(amount) AS total_spent
FROM transactions
GROUP BY customer_id;
```

---

## **5. ORDER BY**

`ORDER BY` sorts the result set by one or more columns, either ascending (`ASC`) or descending (`DESC`).

**Example:**

```sql
SELECT customer_id, amount
FROM transactions
ORDER BY amount DESC;
```

---

## **6. LIMIT**

`LIMIT` restricts the number of returned rows.
Useful for previewing datasets or optimizing performance during analysis.

**Example:**

```sql
SELECT *
FROM transactions
ORDER BY timestamp DESC
LIMIT 100;
```

Some database systems use `TOP` or `FETCH FIRST` instead of `LIMIT`.

---

## **Practical Importance for Data Engineers**

These SQL basics form the foundation for:

* Extracting source data
* Profiling and validating datasets
* Building aggregations for reporting
* Performing reconciliation checks
* Preparing datasets for downstream pipelines

Understanding these operations is essential before working with advanced features such as window functions, CTEs, or optimization strategies.
