# Query Execution Estimator

A Python-based SQL query execution cost estimator that parses SQL queries, generates possible left-deep execution plans, estimates their costs using database statistics, and selects the lowest-cost plan.

## Overview

The project simulates a simplified database query optimizer. Given a SQL query and a database schema containing table statistics and indexes, it:

- Parses the SQL query into its components
- Estimates the effects of selections and joins
- Generates possible left-deep query execution plans
- Evaluates different join algorithms
- Considers available indexes and database statistics
- Accounts for sorting and projection costs
- Selects the execution plan with the lowest estimated cost
- Produces a textual explanation of the selected plan

The estimator uses a brute-force approach for plan generation, making it suitable for demonstrating the principles behind relational query optimization and cost-based query planning.

## Features

### SQL Parsing

The built-in SQL parser supports queries containing:

- `SELECT`
- `FROM`
- `WHERE`
- `ORDER BY`
- Table aliases
- Selection conditions
- Equality-based join conditions

Aliases such as `Students S` and `Students AS S` are resolved to their corresponding table names.

### Query Execution Plans

The optimizer generates left-deep execution trees by considering:

- Different table join orders
- Different join algorithms
- Selection operations
- Projection operations
- Sorting operations

For a query involving multiple tables, the optimizer evaluates possible combinations and chooses the plan with the lowest estimated cost.

### Join Algorithms

The following join algorithms are considered:

- Nested Loop Join
- Block Nested Loop Join
- Index Nested Loop Join
- Sort-Merge Join
- Hash Join

### Database Statistics

Execution costs are estimated using statistics such as:

- Number of rows
- Number of blocks
- Rows per block
- Number of distinct attribute values
- Attribute value ranges
- Available indexes
- Index type
- Index clustering
- B+ tree height
- Number of available buffer blocks

The schema and statistics are loaded from a JSON file.

### Index-Aware Optimization

The estimator considers available indexes when evaluating operations. It supports index statistics for:

- B+ tree indexes
- Hash indexes
- Clustered indexes
- Composite indexes

Selection operations can consider both individual and composite indexes when estimating their cost.

### Cost Estimation

Each operation maintains information about:

- Estimated number of output rows
- Estimated number of blocks
- Operation cost
- Total accumulated cost
- Sorting information
- Tables participating in the intermediate result

The final execution plan includes the cumulative estimated cost of all operations.

## Project Structure

```text
QueryExecutionEstimator/
│
├── execution_plans.py    # Generates and evaluates possible execution plans
├── loader.py             # Loads database schema and statistics from JSON
├── main.py               # Example entry point
├── models.py             # Data models for tables, attributes, indexes and results
├── operations.py         # Relational operations and cost estimation
├── parser.py             # SQL query parser
├── primer_ulaza.json     # Example database schema and statistics
├── tests.py              # Tests
├── LICENSE               # MIT License
└── README.md
```

## How It Works

The optimization process can be summarized as:

```text
SQL Query
    │
    ▼
SQL Parser
    │
    ▼
Parsed Query
    │
    ▼
Database Schema & Statistics
    │
    ▼
Generate Left-Deep Plans
    │
    ├── Different table orders
    └── Different join algorithms
    │
    ▼
Estimate Execution Costs
    │
    ├── Selection
    ├── Join
    ├── Sort
    └── Projection
    │
    ▼
Choose Lowest-Cost Plan
    │
    ▼
Execution Plan Explanation
```

For example, with four tables, the optimizer can consider up to `4! = 24` table orders and `5^3 = 125` combinations of join algorithms for each order.

## Requirements

- Python 3
- No external Python packages are required

## Usage

The example entry point is located in `main.py`.

The SQL query is defined in the source code:

```python
query = "SELECT ime, smer FROM Student ORDER BY Student.indeks"
```

The schema is loaded from the included JSON file:

```python
bufferBlocks, tables, schema = load_schema("primer_ulaza.json")
```

The query is then parsed and the best execution plan is selected:

```python
parser = SQLParser()
parsed_query = parser.parse(query)

best_plan = choose_best_plan(
    parsed_query=parsed_query,
    schema=tables,
    buffer_blocks=bufferBlocks
)
```

Finally, the selected plan and its estimated total cost are printed:

```python
print(best_plan.explain())
print("UKUPNA CENA:", best_plan.result.total_cost)
```

Run the example with:

```bash
python main.py
```

## Input Schema

The database schema is specified in JSON. Each table contains information such as:

```json
{
  "name": "Student",
  "rowCount": 1000,
  "blockCount": 50,
  "rowsPerBlock": 20,
  "attributes": [
    {
      "name": "indeks",
      "type": "int",
      "unique": true,
      "distinctValues": 1000
    }
  ],
  "indexes": []
}
```

Attribute statistics include the number of distinct values and can optionally contain minimum and maximum values.

Indexes contain information about their attributes, type, clustering, and tree height.

## Example Output

The selected execution plan is printed as a tree containing each relational operation, the algorithm used, the cost of that operation, and the accumulated cost.

Example structure:

```text
Projection(...)
 Algoritam: ...
 Cena operacije: ...
 Ukupna cena: ...

  Sort(...)
   Algoritam: ...
   Cena operacije: ...
   Ukupna cena: ...

    ...
```

If the input is already sorted on the requested attribute, the estimator can recognize that no additional sorting is required.

## Testing

Tests are provided in `tests.py`.

Run them with:

```bash
python tests.py
```

## Technologies

- Python
- SQL parsing
- Relational algebra
- Query optimization
- Cost-based execution planning
- Database statistics
- Index cost estimation
- Data structures and algorithms

## License

This project is licensed under the MIT License.
