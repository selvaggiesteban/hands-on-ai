---
name: sql
description: Use when designing schemas, optimizing complex queries, or managing relational data in PostgreSQL, MySQL, or SQL Server.
---

# SQL Database Skill

This skill provides expert capabilities in relational database development (PostgreSQL, MySQL, SQL Server), focusing on query performance and data integrity.

## Capabilities

- **Advanced Querying**: CTEs, Window functions, Recursive queries, Complex joins
- **Performance Optimization**: Execution plan analysis, Indexing strategies, Query rewriting
- **Schema Design**: Normalization/Denormalization, Constraints, Partitioning
- **Maintenance**: Statistics updates, Vacuum/Maintenance plans, Deadlock prevention

## Process

1.  **Context Assessment**: Review database schema, platform, and performance SLAs.
2.  **Analysis**: Analyze execution plans and identify bottlenecks (scans, locks).
3.  **Implementation**: Write efficient SQL, create optimal indexes, and refactor schema if needed.
4.  **Optimization**: Tune query parameters and server configurations.
5.  **Verification**: Verify performance gains and ensure data integrity constraints.

## Best Practices

- Avoid `SELECT *` and use explicit column lists.
- Use window functions for complex analytics instead of self-joins.
- Design covering indexes for critical queries.
- Normalize schemas to 3NF unless performance dictates denormalization.
