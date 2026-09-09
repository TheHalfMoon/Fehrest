# ADR-0007 — Canonical state moves to SQLite

Status: Accepted (day 40)
Project: core
Supersedes: ADR-0001

## Decision

Canonical state moves to SQLite, one file per vault.

## Why the reversal

The local-first requirement landed after ADR-0001 and changed the problem. A
server-dependent store cannot satisfy it.
