# Fehrest benchmarks

Two benchmark generations live here. They are not versions of each other — they ask
different questions, and the first one is closed.

| | [V0](./V0/) | [R1](./R1/) |
|---|---|---|
| Question | Does an arm's **context** contain what is needed? | Can a fresh agent **continue the work** correctly? |
| Corpus | Static, 7 documents | Longitudinal, multiple scenarios evolving across checkpoints |
| Maintenance | Hand-authored to be perfect, **cost not measured** | Prospective, task-blind, **cost measured** |
| Model execution | None | Required before any thesis claim |
| Status | **SEALED — `INCONCLUSIVE`, non-confirmatory** | See [R1/STATUS.md](./R1/STATUS.md) |

## `PRODUCT_THESIS_STATUS`

`NOT_EVALUATED`.

That has been the status since the beginning and neither directory changes it yet. V0
did not test the thesis and said so in advance. R1 is designed to test it, and until a
model actually executes, a benchmark design is not a result.

## Reading order

1. [V0/ARCHIVE.md](./V0/ARCHIVE.md) — why the first pilot is `INCONCLUSIVE`, and the
   two design defects that make R1 necessary: a metric on which the empty arm scores
   like the treatment, and `MAINTENANCE_COST: NOT_MEASURED`.
2. [R1/PROTOCOL.md](./R1/PROTOCOL.md) — the longitudinal design.
3. [R1/PREREGISTRATION.md](./R1/PREREGISTRATION.md) — what was fixed before results, and
   its digest.
4. [R1/PILOT.md](./R1/PILOT.md) — the instrument pilot, including the three defects it
   caught before preregistration.
5. [R1/STATUS.md](./R1/STATUS.md) — why no model ran, and what an external executor
   must do.

## Rules that hold across both

- **No Fehrest capability may be added in response to a benchmark result.** Not graph,
  not vectors, not automatic memory, not reranking, not MCP, not UI.
- **No baseline may be weakened** because it came close.
- **A loss is reported as a loss.** The experiment is only worth running if it can
  conclude that a maintained wiki is enough.
