# Project Wiki — maintained, current as of today

This page is kept current by hand. Superseded material is removed rather than
archived here, so everything below reflects the present state.

## core — datastore

Canonical state lives in SQLite, one file per vault (ADR-0007, day 40). This
replaced an earlier Postgres decision once the local-first requirement landed.

## core — constraints

- Every read of a canonical object verifies its UUID after opening the handle.
- No network I/O in the core.

## core — deploy target

**Unresolved.** The team is split and has not converged:

- Position A: the deploy target is staging, because production deploys go through
  the release train and anything else breaks the rollback guarantee.
- Position B: the deploy target is production, because the release train adds a day
  of latency for no benefit now that the canary covers the same risk.

Do not treat either as settled.

## core — known gotchas

A vault root with a trailing separator produced doubled separators during index
rebuild. The FTS insert accepted them silently and queries then returned nothing for
those objects, with no error anywhere. Normalize the root before walking.

## edge — constraints

- The edge service must retain request logs for ninety days.
- The edge service runs behind the shared gateway and inherits its TLS termination.
