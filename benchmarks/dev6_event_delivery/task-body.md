# Task: Repair the event delivery pipeline

Work only in the provided Git repository. The `delivery` package has interacting defects in retry/idempotency semantics, failed-attempt accounting, dead-letter thresholds, retry-queue uniqueness, exponential backoff, and batch continuation. Some source comments are intentionally misleading: verify behavior rather than trusting comments.

Before editing, run the full existing suite once and use it as evidence. Fix root causes, not test symptoms. After each logical defect cluster, run the narrowest relevant test(s); before completion, run the full suite.

Do not edit `tests/test_delivery.py`. Add `tests/test_delivery_regression.py` with at least five focused regression tests for distinct root causes you fixed. Do not add dependencies or use the network. Preserve the public signatures of `Event`, `DeliveryStore`, `Dispatcher`, and `retry_delay`.

## Definition of Done

1. `python3 -m pytest tests/ -q` exits 0 with zero failures, skips, or xfails.
2. `tests/test_delivery_regression.py` exists and contains at least five focused regression tests covering distinct fixed defects.
3. `tests/test_delivery.py` is byte-identical to the starting revision and must not be edited.
4. No new dependencies are added; dependency manifests remain unchanged.
5. All changes are committed with a descriptive commit and a clean git status.
6. Public signatures of `Event`, `DeliveryStore`, `Dispatcher`, and `retry_delay` remain compatible with the starting revision.
7. Transient handler failures must not cause permanent event loss or duplicate successful delivery; retry and dead-letter behavior must remain idempotent across repeated dispatch attempts.
8. The final completion summary provides concise evidence for each DoD item, including the exact test command and result.