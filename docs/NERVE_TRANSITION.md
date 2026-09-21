# Nerve transition

This document defines the source-repository transition from **Hermes-Jev** to **Nerve**.

Nerve is a provider-neutral supervisory layer for Hermes Agent. Hermes remains the primary reasoning agent; Nerve observes, verifies, redirects, and coordinates execution around it.

## Scope

The transition groups the existing and planned functionality into four subsystems:

- **Nerve Reflex** — typed System-1 decisions through Jev, Laya, and future compatible backends.
- **Nerve Core** — trajectory supervision, recovery control, and context/token governance.
- **Nerve Kanban** — Definition-of-Done verification and worker lifecycle supervision.
- **Nerve Remote** — durable delegation to independent Hermes workers over SSH.

```text
Nerve
├── Reflex
│   ├── Jev
│   ├── Laya
│   └── future compatible decision backends
├── Core
├── Kanban
└── Remote
```

## Provider-neutral Reflex layer

The implementation should introduce a common decision-backend interface so supervisory code does not depend directly on a Jev-specific response shape.

Normalized results should carry:

- typed answer;
- probabilities;
- confidence;
- backend/model provenance;
- latency;
- usage metadata where available;
- local/remote execution provenance.

### Jev

Existing supported Jev transports remain supported behind the generic Reflex interface.

### Laya

Laya is the first open-source/local Reflex backend. It supplies the typed primitives Nerve needs for supervision: `choice`, `score`, and `noul`, including probability/confidence output.

Laya-only operation must not require a Jev provider call.

Because local decision models have bounded context, Nerve should build a compact decision state from relevant evidence rather than forwarding an entire Hermes transcript. Relevant state may include:

- current goal;
- task/run identity;
- locked requirements;
- deterministic verification state;
- unresolved criteria;
- recent decision-significant evidence;
- repeated-failure fingerprints;
- current trajectory state;
- completion proposal.

Deterministic verification remains authoritative where applicable.

## Nerve Core

Nerve Core generalizes the existing asynchronous nervous-system behavior.

It should observe decision-significant events while avoiding unnecessary supervisory calls for routine state. Examples include significant failures, repeated equivalent failures, contradictions, stalled trajectories, completion proposals, verification results, and child-worker transitions.

The objective remains **continuation fidelity per context token**: preserve the smallest sufficient working set needed for Hermes to continue correctly while avoiding redundant work and unnecessary model turns.

## Nerve Kanban

Nerve Kanban should preserve and extend the current Kanban supervision work:

- exact task/run binding;
- locked Definition-of-Done requirements;
- deterministic criterion verification;
- semantic assessment of unresolved criteria;
- repeated-failure detection;
- premature-completion rejection;
- RETRY / REPLAN / ESCALATE / PASS control;
- parent/child completion isolation;
- durable terminal readiness;
- canonical native completion.

Target lifecycle:

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

A verified terminal state should not require another ordinary worker-model turn.

## Nerve Remote

Nerve incorporates the remote-worker functionality developed in Hermes Outpost rather than creating a second SSH transport.

The existing security boundaries should be preserved:

- administrator-configured host aliases only;
- normal OpenSSH host-key verification;
- no private-key/password collection;
- no forwarding of controller provider credentials;
- task/context over stdin;
- configured workspace containment;
- physical-path/symlink validation;
- allowlisted remote profile overrides;
- bounded runtime and turn budgets;
- durable job state;
- cancellation and result/session retrieval.

Remote workers remain independent Hermes processes with their own filesystem, profile, plugins, model, credentials, and session.

Hermes Outpost catalog retirement is tracked independently in NousResearch/hermes-agent#118471. This source transition does not own that catalog change.

## Execution-tree supervision

Supervision and completion authority must remain scoped to the correct session, task, run, worker, and parent.

A child completion must never implicitly authorize its parent.

## Public naming target

```text
Product:      Nerve
Plugin:       nerve
Repository:   hermes-nerve
```

Subsystems:

```text
Nerve Reflex
Nerve Core
Nerve Kanban
Nerve Remote
```

The repository itself should not be renamed until the migration has passed the release gates below.

## API migration direction

Expected generic public tool names:

```text
nerve_decide
nerve_rank
nerve_verify
nerve_assess
nerve_context_curate
nerve_context_rehydrate
nerve_stats
nerve_event
nerve_remote_delegate
nerve_remote_status
nerve_remote_result
nerve_remote_cancel
```

Historical `jev_*` and Outpost `remote_worker_*` names require an explicit migration strategy. Avoid permanently duplicating the entire model-visible schema solely for compatibility.

## Configuration migration

Existing configuration under:

```text
plugins.entries.hermes-jev.settings
```

should migrate to:

```text
plugins.entries.nerve.settings
```

Applicable Outpost host configuration should migrate under a Nerve Remote namespace.

Migration must preserve applicable provider settings, context settings, local evidence/receipts, and remote host definitions.

## Privacy and provenance

Nerve must make the execution boundary clear:

- **Local Laya:** decision inference occurs locally once its runtime/model is available.
- **Remote Jev:** privacy-minimized decision state may be sent to the configured provider and may consume provider credits.
- **Remote Hermes:** delegated task/context is transmitted to an administrator-configured SSH host; controller provider credentials are not forwarded.

## Repository migration

Before final merge, review and update:

- `plugin.yaml`;
- package metadata;
- README and architecture docs;
- setup/provider/security docs;
- migration guide;
- configuration examples;
- telemetry/provenance naming;
- tests and fixtures;
- release workflow;
- package/archive names;
- repository links.

Historical changelog entries should retain historical names where appropriate.

## Release strategy

This source transition is intentionally separate from the Hermes community catalog.

Sequence:

1. Develop Nerve on this branch.
2. Preserve existing Jev behavior.
3. Add and evaluate Laya.
4. Integrate Nerve Remote.
5. Complete migration/rename testing.
6. Pass all release gates.
7. Merge the source PR.
8. Produce an immutable Nerve release commit/tag.
9. Rename the repository if approved by the release checklist.
10. Only then prepare a separate Hermes catalog update.

The existing Hermes-Jev catalog entry remains untouched during development and testing.

## Release gates

### Jev compatibility

- existing Jev regression coverage passes;
- supported Jev transport smoke tests pass;
- existing configuration migration is tested;
- context-governance regressions pass.

### Laya

- local runtime/model loads successfully;
- `choice`, `score`, and `noul` normalization is tested;
- probability/confidence normalization is tested;
- Laya-only mode performs no Jev decision calls;
- CPU behavior is tested;
- GPU path is smoke-tested;
- representative supervision decisions are replayed and compared.

### Kanban

- frozen lifecycle benchmark reproduces;
- deterministic Definition-of-Done checks pass;
- premature completion is rejected;
- parent/child completion isolation is verified;
- verified PASS reaches canonical `kanban_complete`;
- worker exits cleanly;
- no unnecessary post-PASS decision turn remains;
- no direct Kanban database completion bypass is used.

### Remote

- existing Outpost regression coverage is preserved;
- fake-SSH lifecycle passes;
- workspace containment and symlink rejection pass;
- cancellation and result retrieval pass;
- real remote Hermes smoke test passes.

### Plugin/release

- full project tests pass;
- compile checks pass;
- `git diff --check` passes;
- `hermes plugins validate --install-deps .` passes;
- `hermes plugins doctor . --ci` passes;
- declared capabilities match runtime registration;
- security scanner findings are reviewed;
- release CI passes at the final immutable release commit.

Final counts and live-test evidence should be recorded from the release candidate.

## Non-goals

Nerve is not:

- a replacement for Hermes' primary reasoning model;
- a second unrestricted autonomous planner;
- arbitrary remote shell access;
- a mechanism for forwarding controller credentials;
- semantic-model authority over failed deterministic checks;
- a claim that Laya and Jev behave identically.
