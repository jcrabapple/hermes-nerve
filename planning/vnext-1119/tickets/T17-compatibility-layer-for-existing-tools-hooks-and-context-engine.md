# T17: Compatibility layer for existing tools, hooks, and context engine

**Phase:** Phase 6 — compatibility

**Blocked by:** T16

**Status:** ready-for-agent

## What to build

Preserve existing Jev tools/hooks/context surfaces while placing the new nervous system above them and keeping context shadow-first with rehydration capabilities intact.

## Public seam(s)

Compatibility adapter for existing tool registry/hooks/context engine.

## TDD focus

All seven existing tools and both hooks still register; existing context fallback works; anchor/rehydrate remains available.

## Acceptance criteria

- [ ] All source requirements **668–700** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 668 | jev_decide. | `T17-R0668` |
| 669 | jev_rank. | `T17-R0669` |
| 670 | jev_verify. | `T17-R0670` |
| 671 | jev_assess. | `T17-R0671` |
| 672 | jev_context_curate. | `T17-R0672` |
| 673 | jev_context_rehydrate. | `T17-R0673` |
| 674 | jev_stats. | `T17-R0674` |
| 675 | Existing tools remain available manually. | `T17-R0675` |
| 676 | New nervous-system architecture sits above these primitives. | `T17-R0676` |
| 677 | Existing direct tool APIs remain useful for explicit debugging/testing. | `T17-R0677` |
| 678 | pre_tool_call hook. | `T17-R0678` |
| 679 | post_tool_call hook. | `T17-R0679` |
| 680 | Optional Jev ContextEngine. | `T17-R0680` |
| 681 | Context engine not automatically selected. | `T17-R0681` |
| 682 | Existing built-in Hermes compressor fallback retained. | `T17-R0682` |
| 683 | Context system remains shadow-first until proven. | `T17-R0683` |
| 684 | Context should become subordinate to decision usefulness, not maximum compression. | `T17-R0684` |
| 685 | Decision-state context accumulator. | `T17-R0685` |
| 686 | Current goal retention. | `T17-R0686` |
| 687 | Current strategy retention. | `T17-R0687` |
| 688 | Active hypothesis retention. | `T17-R0688` |
| 689 | Important failure retention. | `T17-R0689` |
| 690 | Contradiction retention. | `T17-R0690` |
| 691 | Relevant completion evidence retention. | `T17-R0691` |
| 692 | Last Jev opinion retention. | `T17-R0692` |
| 693 | Event-state compression before remote Jev call. | `T17-R0693` |
| 694 | Existing anchoring capability retained. | `T17-R0694` |
| 695 | Existing local rehydration capability retained. | `T17-R0695` |
| 696 | Sanitized evidence rehydration retained. | `T17-R0696` |
| 697 | Context pressure experimentation remains future validation target. | `T17-R0697` |
| 698 | Actual shadow-plan pressure testing still needed. | `T17-R0698` |
| 699 | End-to-end ANCHOR → rehydrate → successful continuation remains a valuable validation scenario. | `T17-R0699` |
| 700 | Context optimization explicitly not the first priority of the decision-engine redesign. | `T17-R0700` |
