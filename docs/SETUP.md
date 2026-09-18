# Hermes-Jev v0.2.1.1 setup

## Install

Install the plugin with the normal Hermes plugin flow, then validate registration:

```bash
hermes plugins doctor hermes-jev --ci
```

Expected public surface: 8 tools, 7 hook names, and the optional `jev` ContextEngine.

## Provider

OpenRouter (live-tested historically in v0.1.x):

```bash
export OPENROUTER_API_KEY='...'
hermes config set plugins.entries.hermes-jev.settings.jev_provider openrouter --force
hermes config set plugins.entries.hermes-jev.settings.jev_model typesafe/jev-1.13 --force
```

Direct TypeSafe (wire-tested in v0.2.1.1):

```bash
export TYPESAFE_API_KEY='...'
hermes config set plugins.entries.hermes-jev.settings.jev_provider typesafe --force
hermes config set plugins.entries.hermes-jev.settings.typesafe_model jev-latest --force
```

Only the selected provider's credential is required.

## Nervous system defaults

```bash
hermes config set plugins.entries.hermes-jev.settings.nervous_enabled true --force
hermes config set plugins.entries.hermes-jev.settings.nervous_turn_admission true --force
hermes config set plugins.entries.hermes-jev.settings.nervous_mode correct_next --force
hermes config set plugins.entries.hermes-jev.settings.nervous_challenge_confidence 0.86 --force
hermes config set plugins.entries.hermes-jev.settings.nervous_call_threshold 0.58 --force
```

The old synchronous pre-tool gate remains `off` by default. It is compatibility/special-purpose behavior, not the recommended v0.2 decision architecture.

## Manual structured events

Hermes/runtime integrations may call `jev_nervous_event` to expose explicit accountable decisions. The event can include choices and `hermes_decision`, or a control-state event such as `RECOVERY`, `STRATEGY_CHANGE`, or `COMPLETION_CANDIDATE`.

## Telemetry

Inside Hermes:

```text
Call jev_stats and return the nervous section.
```

Local files are profile-scoped under `$HERMES_HOME/jev/`, including nervous-event and decision-outcome JSONL ledgers.
