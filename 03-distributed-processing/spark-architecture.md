# Spark Architecture

Apache Spark is a distributed data processing framework designed for large-scale data analysis, streaming, and machine learning.
It provides high performance through in-memory computation and an optimized execution engine.

---

## 1. Core Components

### **Driver**

* The **Driver** is the central controller of a Spark application.
* It runs the **main()** function of your code and is responsible for:

  * Creating the **SparkSession** or **SparkContext**.
  * Defining the logical execution plan (DAG).
  * Scheduling tasks on worker nodes.
  * Collecting results from executors.

If the driver fails, the entire Spark application stops.

---

### **Executors**

* **Executors** are processes launched on worker nodes that execute tasks assigned by the driver.
* Each executor:

  * Runs multiple tasks in parallel.
  * Stores data in memory or disk for caching.
  * Reports back results and metrics to the driver.

Executors exist only for the lifetime of the Spark application.

---

### **Cluster Manager**

The cluster manager allocates resources (CPU, memory) across Spark applications.

Common cluster managers:

* **Standalone** – Simple built-in manager for small or test environments.
* **YARN** – Common in Hadoop ecosystems.
* **Kubernetes** – Popular for containerized workloads.
* **Mesos** – A general-purpose resource manager (less common today).

---

## 2. Spark’s Execution Model

When a Spark job is submitted:

1. The **driver** builds a **logical plan** from your DataFrame or RDD transformations.
2. The plan is optimized into a **physical plan** by the **Catalyst optimizer**.
3. The **DAG scheduler** breaks the job into **stages**, each containing multiple **tasks**.
4. The **Task scheduler** sends tasks to executors for execution.
5. Results are collected, cached, or written to storage.

---

## 3. RDD vs DataFrame

| Feature               | RDD                          | DataFrame                              |
| --------------------- | ---------------------------- | -------------------------------------- |
| **Abstraction level** | Low-level, object-oriented   | High-level, tabular (similar to SQL)   |
| **Optimization**      | No query optimization        | Optimized by Catalyst                  |
| **Performance**       | Manual tuning required       | Automatically optimized                |
| **Type safety**       | Type-safe (in Scala)         | Schema-based but less strict in Python |
| **Best for**          | Complex data transformations | Aggregations, joins, analytics         |

> **Recommendation:** Use **DataFrames** for most workloads — they are faster, more expressive, and easier to maintain.

---

## 4. DAG Scheduler

The **Directed Acyclic Graph (DAG) scheduler** converts the logical execution plan into stages and tasks.

* Each **stage** is a set of parallel tasks that can be executed without shuffle.
* When data needs to be redistributed (e.g., join or groupBy), a **shuffle** occurs, marking a boundary between stages.
* The scheduler ensures tasks are executed in the correct order while optimizing for locality and resource efficiency.

---

## 5. Shuffle

**Shuffle** is the process of redistributing data across partitions — a key but expensive operation.

* Triggered by operations like **join**, **groupBy**, **reduceByKey**, or **distinct**.
* Causes data to be written to disk and sent across the network.
* Optimization tips:

  * Repartition strategically before shuffles.
  * Use **broadcast joins** for small lookup tables.
  * Avoid unnecessary wide transformations.

---

## 6. Summary Diagram (Conceptual)

```
+-----------------+        +-------------------+
|     Driver      | <----> |   Cluster Manager |
|  (Creates DAG)  |        | (Allocates Nodes) |
+--------+--------+        +---------+---------+
         |                           |
         | Schedules Tasks           |
         v                           v
+-----------------+        +-----------------+
|   Executor 1    |  ...   |   Executor N    |
| (Runs Tasks)    |        | (Runs Tasks)    |
| (Caches Data)   |        | (Reports Back)  |
+-----------------+        +-----------------+
```

---

## 7. Key Takeaways

* Spark follows a **master–worker** model (Driver + Executors).
* The **Catalyst optimizer** and **DAG scheduler** improve performance automatically.
* **DataFrames** are preferred for declarative and optimized data processing.
* Reducing **shuffles** and managing **partitions** are critical for performance.
