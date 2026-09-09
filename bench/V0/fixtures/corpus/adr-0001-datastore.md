# ADR-0001 — Canonical state lives in Postgres

Status: Accepted (day 3)
Project: core

## Context

We evaluated three options for the canonical store over two weeks. The team ran
load tests against each, wrote throwaway prototypes, and argued about it at length
in three separate meetings. The discussion is preserved here because the reasoning
matters more than the outcome.

Postgres gave us mature tooling, a real query planner, well-understood operational
characteristics, and a migration story the team already knew. The row-level locking
behaviour matched our write pattern. Connection pooling was a solved problem.

SQLite was considered and rejected at this stage: the team was concerned about
concurrent writer limits and about operational visibility.

A document store was rejected because our access pattern is relational.

## Decision

Canonical state lives in Postgres. All services connect through the shared pool.

## Consequences

Every service needs pool configuration. Local development requires a running
Postgres instance. Schema changes go through the migration tool.
