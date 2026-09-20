# MySQL Quick Reference
 
Core syntax for everyday querying and schema work — SELECT, joins, aggregates, writes, DDL, and the functions and patterns you reach for most, including window functions, CTEs, indexing, and transactions.
 
## Table of contents
 
- [Sample schema](#sample-schema)
- [Basic SELECT](#basic-select)
- [Filtering rows](#filtering-rows)
- [Sorting & limiting](#sorting--limiting)
- [Joins](#joins)
- [Grouping & aggregates](#grouping--aggregates)
- [Insert, update, delete](#insert-update-delete)
- [Create & alter tables](#create--alter-tables)
- [Common data types](#common-data-types)
- [Frequently used functions](#frequently-used-functions)
- [Window functions](#window-functions)
- [Common table expressions](#common-table-expressions)
- [Subquery patterns](#subquery-patterns)
- [Indexes & EXPLAIN](#indexes--explain)
- [Transactions & locking](#transactions--locking)
- [JSON columns](#json-columns)
- [Good habits](#good-habits)
## Sample schema
 
The tables every example below queries against — a small shop database.
 
**customers**
 
| Column | Type | Notes |
|---|---|---|
| `id` | `INT AUTO_INCREMENT` | PK |
| `first_name` | `VARCHAR(50)` | |
| `last_name` | `VARCHAR(50)` | |
| `email` | `VARCHAR(100)` | unique |
| `country` | `CHAR(2)` | |
| `created_at` | `DATETIME` | |
 
**orders**
 
| Column | Type | Notes |
|---|---|---|
| `id` | `INT AUTO_INCREMENT` | PK |
| `customer_id` | `INT` | FK → customers.id |
| `status` | `VARCHAR(20)` | |
| `total` | `DECIMAL(10,2)` | |
| `order_date` | `DATE` | |
| `created_at` | `DATETIME` | |
| `shipped_at` | `DATETIME` | nullable |
 
**employees**
 
| Column | Type | Notes |
|---|---|---|
| `id` | `INT AUTO_INCREMENT` | PK |
| `name` | `VARCHAR(100)` | |
| `manager_id` | `INT` | FK → employees.id, nullable |
| `department_id` | `INT` | |
| `salary` | `DECIMAL(10,2)` | |
 
**products**
 
| Column | Type | Notes |
|---|---|---|
| `id` | `INT AUTO_INCREMENT` | PK |
| `name` | `VARCHAR(100)` | |
| `attributes` | `JSON` | e.g. brand, color |
 
**inventory**
 
| Column | Type | Notes |
|---|---|---|
| `sku` | `VARCHAR(20)` | PK |
| `qty` | `INT UNSIGNED` | |
 
**accounts**
 
| Column | Type | Notes |
|---|---|---|
| `id` | `INT AUTO_INCREMENT` | PK |
| `balance` | `DECIMAL(10,2)` | |
 
Create the core three:
 
```sql
CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(100) UNIQUE,
  country CHAR(2),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
 
CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  total DECIMAL(10,2) NOT NULL,
  order_date DATE NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  shipped_at DATETIME NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);
 
CREATE TABLE employees (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  manager_id INT NULL,
  department_id INT NOT NULL,
  salary DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (manager_id) REFERENCES employees(id)
);
```
 
## Basic SELECT
 
```sql
-- All columns
SELECT * FROM customers;
 
-- Specific columns, renamed
SELECT id, first_name AS name, email
FROM customers;
 
-- Only distinct values
SELECT DISTINCT country FROM customers;
```
 
## Filtering rows
 
```sql
-- Comparisons
SELECT * FROM orders
WHERE status = 'shipped' AND total > 100;
 
-- Pattern, range, set, null
WHERE email LIKE '%@gmail.com'
WHERE total BETWEEN 10 AND 50
WHERE country IN ('US', 'CA', 'UK')
WHERE shipped_at IS NULL
```
 
## Sorting & limiting
 
```sql
SELECT * FROM orders
ORDER BY created_at DESC, total ASC
LIMIT 20 OFFSET 40;
 
-- Shorthand pagination: offset, row count
LIMIT 40, 20
```
 
## Joins
 
```sql
-- Inner join (only matches)
SELECT o.id, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id;
 
-- Left join (keep unmatched left rows)
SELECT c.name, o.id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;  -- customers with no orders
 
-- Self join
SELECT e.name, m.name AS manager
FROM employees e
JOIN employees m ON e.manager_id = m.id;
```
 
## Grouping & aggregates
 
```sql
SELECT customer_id, COUNT(*) AS orders, SUM(total) AS spent
FROM orders
GROUP BY customer_id
HAVING SUM(total) > 500
ORDER BY spent DESC;
 
-- Aggregate functions
COUNT(*), SUM(col), AVG(col), MIN(col), MAX(col)
```
 
## Insert, update, delete
 
```sql
-- Insert one or many rows
INSERT INTO customers (first_name, email)
VALUES ('Ada', 'ada@example.com'),
       ('Grace', 'grace@example.com');
 
-- Upsert
INSERT INTO stock (sku, qty)
VALUES ('A100', 5)
ON DUPLICATE KEY UPDATE qty = qty + 5;
 
-- Update & delete
UPDATE orders SET status = 'shipped' WHERE id = 42;
DELETE FROM orders WHERE status = 'cancelled';
```
 
## Create & alter tables
 
```sql
CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  email VARCHAR(100) UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
 
-- Alter & drop
ALTER TABLE customers ADD COLUMN phone VARCHAR(20);
ALTER TABLE customers MODIFY email VARCHAR(150);
ALTER TABLE customers DROP COLUMN phone;
DROP TABLE IF EXISTS temp_customers;
```
 
## Common data types
 
| Category | Types | Notes |
|---|---|---|
| Integers | `TINYINT` `INT` `BIGINT` | Add `UNSIGNED` to disallow negatives |
| Decimals | `DECIMAL(10,2)` `FLOAT` `DOUBLE` | Use `DECIMAL` for money — exact precision |
| Text | `VARCHAR(n)` `TEXT` `CHAR(n)` | `VARCHAR` needs a max length |
| Date & time | `DATE` `DATETIME` `TIMESTAMP` | `TIMESTAMP` is timezone-aware, range-limited to 2038 |
| Boolean | `BOOLEAN` | Stored as `TINYINT(1)` under the hood |
| Enumerated | `ENUM('a','b','c')` | Fixed list of allowed string values |
| Structured | `JSON` | Query with `JSON_EXTRACT` / `->` `->>` |
 
## Frequently used functions
 
```sql
-- String
CONCAT(first, ' ', last)
UPPER(name), LOWER(name)
TRIM(name)
SUBSTRING(name, 1, 3)
LENGTH(name)
REPLACE(name, '-', ' ')
 
-- Date & time
NOW(), CURDATE()
DATE_FORMAT(created_at, '%Y-%m-%d')
DATEDIFF(end_date, start_date)
DATE_ADD(created_at, INTERVAL 7 DAY)
 
-- Numeric & conditional
ROUND(price, 2), CEIL(x), FLOOR(x)
IFNULL(phone, 'n/a')
CASE WHEN total > 100 THEN 'big' ELSE 'small' END
```
 
## Window functions
 
Calculations across a set of rows related to the current one, without collapsing them like `GROUP BY` does.
 
```sql
-- Ranking within groups
SELECT employee_id, department_id, salary,
  RANK() OVER (
    PARTITION BY department_id
    ORDER BY salary DESC
  ) AS dept_rank
FROM employees;
 
-- Running total & row comparison
SELECT order_date, total,
  SUM(total) OVER (ORDER BY order_date) AS running_total,
  LAG(total) OVER (ORDER BY order_date) AS prev_total
FROM orders;
```
 
Other common ones: `ROW_NUMBER()`, `DENSE_RANK()`, `LEAD()`, `NTILE(n)`, and framed aggregates like `AVG(x) OVER (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`.
 
## Common table expressions
 
Named, reusable subqueries that keep multi-step logic readable.
 
```sql
-- Basic CTE
WITH big_spenders AS (
  SELECT customer_id, SUM(total) AS spent
  FROM orders
  GROUP BY customer_id
  HAVING SUM(total) > 1000
)
SELECT c.name, b.spent
FROM big_spenders b
JOIN customers c ON c.id = b.customer_id;
 
-- Recursive CTE
WITH RECURSIVE org_chart AS (
  SELECT id, manager_id, 1 AS depth
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.manager_id, o.depth + 1
  FROM employees e
  JOIN org_chart o ON e.manager_id = o.id
)
SELECT * FROM org_chart;
```
 
## Subquery patterns
 
When to reach for EXISTS, IN, or a correlated subquery.
 
```sql
-- EXISTS: stops at first match, often faster on large sets
SELECT * FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
 
-- IN: fine for small, static, or pre-computed lists
SELECT * FROM customers
WHERE id IN (SELECT customer_id FROM vip_list);
 
-- Correlated subquery
SELECT o.id, o.total,
  (SELECT AVG(total) FROM orders o2
   WHERE o2.customer_id = o.customer_id) AS customer_avg
FROM orders o;
```
 
## Indexes & EXPLAIN
 
```sql
-- Reading a query plan
EXPLAIN FORMAT=JSON
SELECT * FROM orders WHERE customer_id = 42;
-- watch: type (const/ref/range/ALL), key used, rows examined
 
-- Composite & covering indexes
CREATE INDEX idx_orders_cust_date
  ON orders (customer_id, created_at);
-- leftmost-prefix rule: this index helps queries filtering on
-- customer_id alone, or customer_id + created_at — not created_at alone
```
 
A function or implicit cast on an indexed column (`WHERE YEAR(created_at) = 2026`) usually blocks index use — rewrite as a range instead.
 
## Transactions & locking
 
```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- or ROLLBACK on error
 
-- Row locking
SELECT * FROM inventory WHERE sku = 'A100' FOR UPDATE;
-- blocks other transactions from locking/updating this row until commit
 
SET SESSION transaction_isolation = 'READ-COMMITTED';
-- default is REPEATABLE-READ; lower isolation trades consistency for less locking
```
 
## JSON columns
 
```sql
SELECT id, attributes->'$.color' AS color
FROM products
WHERE attributes->>'$.brand' = 'Acme';
 
UPDATE products
SET attributes = JSON_SET(attributes, '$.color', 'red')
WHERE id = 7;
```
 
`->` extracts as JSON, `->>` extracts and unquotes. Index a hot path with a generated column:
 
```sql
ALTER TABLE products
  ADD brand VARCHAR(50) GENERATED ALWAYS AS (attributes->>'$.brand') STORED,
  ADD INDEX (brand);
```
 
## Good habits
 
- **Quoting identifiers** — Use backticks for table or column names that clash with reserved words: `` `order` ``, `` `select` ``.
- **Comments** — `-- a line comment` or `/* a block comment */`.
- **NULL isn't a value** — Compare with `IS NULL` / `IS NOT NULL`, never `= NULL`.
- **Prefer explicit columns** — `SELECT *` is fine for exploring, but name columns in application code.
- **Index what you filter and join on** — `CREATE INDEX idx_orders_customer ON orders (customer_id);`
- **Transactions for multi-step writes** — `START TRANSACTION;` … `COMMIT;` or `ROLLBACK;`
- **Batch writes, don't loop them** — One multi-row `INSERT` beats thousands of single-row round trips.
- **Watch the query plan, not just the result** — `EXPLAIN ANALYZE` shows actual execution time and row counts, not just the plan.
- **Beware implicit type coercion** — Comparing a string column to a number can silently skip an index or misbehave — keep types matched.
 
