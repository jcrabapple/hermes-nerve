# Nerve transition

This document defines the source-repository transition from **Hermes-Jev** to **Nerve** and records the dev17 release-candidate authority model.

Nerve is a provider-neutral supervisory layer for Hermes Agent. Hermes remains the primary reasoning/orchestration authority. Nerve observes, verifies, forecasts, redirects, and coordinates execution around it; Reflex backends do **not** own irreversible task-stop authority.

## Current dev17 release scope

Dev17 ships the Nerve architecture under the existing `hermes-jev` plugin/repository identity so the proven runtime is not destabilized by a simultaneous rename. The public Nerve rename/migration remains a follow-up after the release candidate is proven.

Implemented in dev17:

- provider-neutral Reflex backend selection;
- hosted Jev compatibility;
- local/self-hosted Laya support;
- OpenJev integration and setup/matrix tooling;
- Nerve token-trajectory supervision;
- controller-owned verified completion;
- canonical orchestrator review handoff for budget escalation;
- Nerve Remote / Hermes Outpost-derived SSH worker implementation;
- deterministic DoD authority and parent/child completion isolation;
- crash-safe live model matrix telemetry.

OpenJev is **included but live-model untested** in dev17. Unit/interface/setup coverage is present, but real OpenJev inference and hosted-Jev vs OpenJev A/B validation require suitable GPU hardware and are tracked in issue #10.

## Architecture

```text
Nerve
├── Reflex
│   ├── Jev
│   ├── Laya
│   └── OpenJev
├── Core
├── Kanban
└── Remote
```

### Nerve Reflex

Reflex backends provide typed System-1 judgments and normalized provenance. Results carry typed answers, probabilities, confidence, backend/model identity, latency, usage metadata, and local/remote provenance where available.

Reflex is advisory for spending/lifecycle escalation. A model decision may grant a bounded policy-defined extension, but Reflex cannot permanently fail or block a task merely because its budget estimate was exceeded.

### Nerve Core

Nerve Core observes decision-significant events: repeated failures, stalls, contradictions, completion proposals, verification state, child-worker transitions, and token trajectory. Its objective is continuation fidelity per context token while preserving the smallest sufficient working set.

### Nerve Kanban

Correctness and spending policy are deliberately separated.

- Locked deterministic DoD remains authoritative for correctness.
- `DOD-BUDGET` is telemetry/execution policy, **not required correctness DoD**.
- Verified completion is controller-owned and does not require another ordinary worker-model turn.
- Parent/child completion authority remains isolated.
- No direct database completion bypass is allowed.

Target completion lifecycle:

```text
worker
  ↓
deterministic evidence
  ↓
semantic assessment where needed
  ↓
verified PASS
  ↓
COMPLETE_READY
  ↓
native kanban_complete
  ↓
worker exit
```

## Budget escalation authority

The first dev17 Jev/Laya live matrix exposed a policy trap: correct, test-green work could exceed required `DOD-BUDGET`, making successful completion impossible and eventually causing a model-owned Nerve kill. Dev17 RC2 removes that authority inversion.

The release policy is:

```text
0–65% of base target   CONTINUE
65%                    WATCH
80%                    Reflex forecast: would +25% likely finish? YES / NO / MAYBE
YES >= 0.60 confidence grant one +25% extension; no scope expansion
MAYBE                  canonical kanban_request_review immediately
NO                     checkpoint-only window; review by 90% of base target
extension exhausted    canonical kanban_request_review immediately
1.75x emergency fence  canonical review/pause, never Reflex-owned economic kill
```

The forecast question is explicitly about spending likelihood, not task authority:

> Given the locked DoD, verified evidence, current agent status, token use, and remaining work, would granting the proposed additional token budget likely let this worker finish the task correctly?

A confident `YES` may grant exactly one bounded extension. `NO`, `MAYBE`, extension exhaustion, or the emergency fence return authority through Hermes' native `kanban_request_review` path. The configured main LLM orchestrator/reviewer then chooses the canonical next action: complete, grant/replan additional work, request changes, or block/stop.

Nerve does not dispatch `kanban_block` for economic reasons.

## Nerve Remote

Nerve incorporates the remote-worker functionality developed in Hermes Outpost rather than inventing another SSH transport. Preserve:

- administrator-configured host aliases;
- normal OpenSSH host-key verification;
- no private-key/password collection;
- no forwarding controller provider credentials;
- stdin task/context transport;
- workspace containment and physical-path/symlink validation;
- allowlisted remote profile overrides;
- bounded runtime/turn budgets;
- durable job state;
- cancellation and result/session retrieval.

Remote workers remain independent Hermes processes with their own filesystem, profile, plugins, model, credentials, and session.

The dev17 release-validation path has re-proven `j2 -> win4060` BatchMode OpenSSH, local forwarding, real Laya inference through the tunnel, and clean tunnel teardown. Broader Remote lifecycle regression coverage remains part of the release gate.

## Privacy and provenance

- **Local Laya:** typed-decision inference occurs on the configured local/SSH-reached service.
- **Remote Jev:** privacy-minimized decision state may be sent to the configured provider and may consume provider credits.
- **OpenJev:** self-hosted integration is available; live model validation is pending issue #10.
- **Remote Hermes:** delegated task/context is transmitted only to an administrator-configured SSH host; controller provider credentials are not forwarded.

## Public naming target

After source/runtime migration is proven:

```text
Product:      Nerve
Plugin:       nerve
Repository:   hermes-nerve
```

Expected future generic public tools remain `nerve_*`. Historical `jev_*` and `remote_worker_*` surfaces require an explicit compatibility/migration strategy; dev17 intentionally does not combine this rename with the runtime release.

## Release gates for dev17 / PR #9

### Jev compatibility

- existing Jev regression coverage passes;
- hosted Jev remains a supported Reflex backend;
- context-governance and controller-completion regressions pass.

### Laya

- real checkpoint loads;
- CUDA path is smoke-tested;
- typed probability/confidence normalization passes;
- Laya-only operation performs no Jev decision-provider call;
- real inference through the packaged sidecar passes;
- real inference through the OpenSSH forward passes;
- hosted-Jev vs Laya matrix is rerun on the final orchestrator-authority RC.

### OpenJev

- integration/unit/interface/setup coverage ships in dev17;
- GPU guard fails closed on undersized hardware;
- real-model inference and hosted-Jev vs OpenJev A/B are explicitly **not yet tested** and are tracked by issue #10.

### Kanban / Nerve

- deterministic DoD checks pass;
- budget cannot invalidate otherwise-correct work;
- premature completion is rejected;
- parent/child completion isolation is verified;
- verified PASS reaches canonical `kanban_complete`;
- no unnecessary post-PASS model turn remains;
- Nerve budget escalation routes to `kanban_request_review`, not `kanban_block`;
- `YES` grants only one bounded extension;
- `NO`/`MAYBE`/extension exhaustion return authority to the main orchestrator;
- no direct Kanban database completion bypass is used.

### Remote

- applicable Outpost regression coverage passes;
- fake-SSH lifecycle passes;
- workspace containment and symlink rejection pass;
- cancellation and result retrieval pass;
- real SSH transport smoke passes.

### Plugin/release

- release verifier passes;
- focused dev17 regression suite passes;
- compile checks pass;
- `git diff --check` passes;
- `hermes plugins validate --install-deps .` passes on final PR SHA;
- `hermes plugins doctor . --ci` passes on final PR SHA;
- declared capabilities match runtime registration;
- security findings are reviewed;
- GitHub CI passes on the exact final immutable PR SHA.

## Repository/catalog sequence

1. Finish and validate dev17 / PR #9.
2. Merge the tested source implementation.
3. Produce an immutable release commit/tag.
4. Keep OpenJev live-validation gap visible through issue #10.
5. Rename repository/plugin to Nerve only after migration testing.
6. Handle any Hermes community-catalog update separately after the source release is proven.

The community catalog is intentionally not modified by this source PR.
