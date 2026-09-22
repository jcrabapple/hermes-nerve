# Canonical 1,119-point Nerve vNext requirement inventory


## 1. Core architecture

1. Jev as Hermes’s decision engine, not merely an optional decision tool.
2. Hermes remains the reasoning engine.
3. Hermes remains the execution engine.
4. Jev becomes the decision/control plane.
5. Jev operates as an asynchronous tandem process.
6. Jev removed from the normal synchronous critical path.
7. Jev operates as a parallel supervisory process.
8. Jev operates as a decision auditor.
9. Jev operates as a decision corrector.
10. Jev operates as a high-confidence exception generator.
11. Jev supervision attached to selected Hermes turns.
12. Jev supervision can persist for the entire lifetime of a long-running autonomous turn.
13. A supervised turn may last seconds, minutes, or hours without changing the supervision model.
14. A turn may contain hundreds or thousands of Hermes events without creating equivalent Jev calls.
15. Hermes continues executing while Jev evaluates.
16. Jev’s ~500+ ms network latency treated as oversight latency, not worker latency.
17. No synchronous Jev micro-controller loop around ordinary Hermes actions.
18. No Jev → action → Jev → action requirement for every action.
19. Jev controls important forks while touching only a small fraction of individual Hermes operations.
20. Jev calls concentrated around decision epochs rather than tool-call epochs.
21. When appropriate, one Jev call can combine verification, next-state selection, uncertainty assessment, and completion assessment.
22. Existing nerve_assess primitive reused/expanded for multi-question control assessments.
23. New higher-level control assessment contract.
24. New higher-level decision epoch contract.
25. Decision supervision separate from ordinary assistant dialogue generation.

## 2. Turn-level Jev admission

26. Every user prompt receives a unique turn_id.
27. The same user prompt can be sent to Hermes and the Jev admission system in parallel.
28. Hermes starts processing immediately.
29. Hermes does not wait for Jev admission before beginning work.
30. Dedicated Jev Turn Arbiter.
31. Dedicated turn-admission contract.
32. Suggested contract namespace: hermes/jev-turn-admission/v1.
33. Admission contract explicitly non-recursive.
34. Admission Jev call cannot cause another admission Jev call.
35. Turn arbiter predicts whether a meaningful decision plane exists.
36. Turn arbiter predicts whether a decision plane is likely to emerge before the turn completes.
37. Turn arbiter does not merely classify chat versus work.
38. Turn arbiter evaluates likelihood of materially different actions.
39. Turn arbiter evaluates likelihood of materially different strategies.
40. Turn arbiter evaluates likelihood of recovery decisions.
41. Turn arbiter evaluates likelihood of completion judgments.
42. Turn arbiter evaluates likelihood of resource-allocation decisions.
43. Turn arbiter evaluates likelihood of consequential operations.
44. Turn arbiter evaluates likelihood of genuine routing choices.
45. Turn arbiter evaluates likelihood of meaningful human-escalation decisions.
46. Admission output includes OFF.
47. Admission output includes WATCH.
48. Admission output includes ON.
49. OFF means no active Jev nervous-system supervision.
50. WATCH means locally observe the event stream without routinely calling Jev.
51. WATCH can promote itself to active supervision when a material decision emerges.
52. ON immediately enables active Jev nervous-system supervision.
53. Admission decision logged even when result is OFF.
54. Admission confidence logged.
55. Admission probabilities logged.
56. Admission contract/version logged.
57. Admission latency logged.
58. Admission provider/model provenance logged.
59. Admission results become part of later calibration data.
60. False-negative turn admission measured.
61. False-positive turn admission measured.
62. WATCH mode specifically designed to mitigate admission false negatives.

## 3. Decision-plane model

63. Explicit internal concept of a decision plane.
64. Decision plane independent from whether the UI interaction looks conversational.
65. Decision plane independent from whether tools are being used.
66. Decision plane independent from whether the assistant is roleplaying.
67. Decision plane independent from whether the user calls something work.
68. Decision plane based primarily on accountability.
69. Accountable decision defined around whether the result matters beyond producing the next conversational turn.
70. Decision must belong to an active objective before becoming normally Jev-eligible.
71. Decision should have materially different alternatives.
72. Decision should be capable of changing trajectory, outcome, risk, cost, or completion state.
73. Immediate conversational wording choices excluded by default.
74. Fictional character choices excluded by default.
75. Pure stylistic decisions excluded by default.
76. Ordinary conversational responses excluded by default.
77. Material real-world/workflow decisions eligible.
78. Material training/director decisions eligible.
79. Material engineering decisions eligible.
80. Material operational decisions eligible.
81. Material resource decisions eligible.
82. Material recovery decisions eligible.
83. Material completion decisions eligible.

## 4. Interaction type separate from decision context

84. Separate interaction_type from Jev supervision state.
85. CONVERSATION interaction type.
86. ROLEPLAY interaction type.
87. RESEARCH interaction type.
88. CREATIVE interaction type.
89. OPERATIONAL interaction type.
90. Separate decision_context.
91. NONE decision context.
92. SIMULATION decision context.
93. ADVISORY decision context.
94. WORK decision context.
95. Potential EXTERNAL/consequential decision context.
96. Conversational-looking work can still receive decision supervision.
97. Operational-looking activity can still remain Jev-free if no meaningful decision exists.
98. Research generally stays outside Jev unless research results control subsequent work.
99. Brainstorming generally remains Jev-free.
100. Moving from brainstorming to implementation may create a decision plane.
101. Read-only activity does not automatically imply Jev supervision.
102. Tool usage does not automatically imply Jev supervision.
103. Mutation intent is a strong signal but not sufficient alone.
104. External-state changes are stronger Jev candidates.
105. Consequential external-state decisions receive elevated priority.

## 5. Roleplay handling

106. Explicit Actor Plane.
107. Explicit Director Plane.
108. Roleplay dialogue stays in Actor Plane.
109. Actor Plane dialogue does not become Jev decision events.
110. Imaginary in-character decisions do not automatically invoke Jev.
111. Roleplay transcript not continuously forwarded to Jev.
112. Roleplay objectives can maintain a separate Director Plane.
113. Director Plane may contain accountable real-world training objectives.
114. Director Plane decisions may be Jev-eligible.
115. Example director decisions include changing exercise difficulty.
116. Example director decisions include switching objection categories.
117. Example director decisions include repetition versus advancement.
118. Example director decisions include stopping for critique.
119. Simulation default Jev policy is off or observation-only.
120. Optional simulation policy director_only.
121. Roleplay decision scope distinguishable from fictional content.
122. Jev never decides what Hermes should literally say next merely because Hermes is speaking.
123. Jev supervises real decisions that occur around the roleplay when appropriate.

## 6. Decision scope metadata

124. Structured decision_scope.
125. conversation scope.
126. fiction scope.
127. simulation scope.
128. advisory scope.
129. work scope.
130. external scope.
131. Default drop policy for conversation scope.
132. Default drop policy for fiction scope.
133. Default drop or director-only policy for simulation scope.
134. Advisory scope generally quiet unless materially accountable.
135. Work scope normally Jev-eligible.
136. External/consequential scope high priority.
137. Decision scope included in event receipts.
138. Decision scope included in router state.
139. Decision scope usable as a router relevance feature.

## 7. Objective/work envelope

140. Persistent structured objective envelope.
141. Earlier Work Envelope generalized beyond literal work.
142. Objective ID.
143. Goal ID.
144. Goal description.
145. Turn ID.
146. Work/session ID where applicable.
147. Done criteria.
148. Current status.
149. Current strategy.
150. Active hypothesis.
151. Decision context.
152. Interaction type.
153. Jev supervision policy.
154. Jev admission result.
155. Jev admission confidence.
156. Allowed/priority event types.
157. Current risk/consequence state.
158. Current reversibility state.
159. Current completion evidence.
160. Active Jev decision/freshness state.

## 8. Structured event bus

161. Dedicated jev_event_bus.
162. Event bus generated by Hermes/runtime internals.
163. No dependence on parsing arbitrary assistant prose for decisions.
164. No scan-generated-text-and-guess-whether-a-decision-happened architecture.
165. Decision event generation independent from model voluntarily remembering to call Jev.
166. Runtime-generated structured events.
167. Automatic structured event emission.
168. Events associated with turn_id.
169. Events associated with objective/work IDs.
170. Events associated with decision IDs when applicable.
171. Events sequenced/versioned.
172. Event timestamps.
173. Event state provenance.
174. Events feed local router regardless of whether they reach remote Jev.
175. Full event stream can remain local.
176. Only selected consolidated events forwarded to Jev.

## 9. Event types discussed

177. DECISION event.
178. COMPLETION event.
179. FAILURE event.
180. TOOL_STARTED event.
181. TOOL_FINISHED event.
182. OBSERVATION event.
183. HYPOTHESIS event.
184. RETRY event.
185. PLAN_CHANGE event.
186. WORKER_SPAWN event.
187. CHECKPOINT event.
188. COMPLETION_CANDIDATE event.
189. RECOVERY event.
190. MUTATION_INTENT event.
191. CONSEQUENTIAL_ACTION event.
192. STRATEGY_CHANGE event.
193. REPEATED_FAILURE event.
194. HUMAN_ESCALATION event.
195. IRREVERSIBLE_ACTION event.
196. HIGH_MATERIALITY_DECISION event.
197. TURN_COMPLETE event.
198. Potential WORK_BEGIN/objective-start event.
199. Potential state-update events for router accumulation.
200. Potential Jev-challenge receipt events.

## 10. High-value Jev decision categories

201. STRATEGY category.
202. ROUTING category.
203. RECOVERY category.
204. COMPLETION category.
205. COMMIT category.
206. PRIORITIZATION category.
207. Resource allocation.
208. Worker selection.
209. Tool selection.
210. Tool-family selection.
211. Local-machine versus remote-worker selection.
212. Model/provider selection when materially consequential.
213. Retry versus replan.
214. Retry versus gather-more-evidence.
215. Retry versus escalation.
216. Replan versus escalation.
217. Rollback decisions.
218. Hypothesis selection.
219. Remediation-path selection.
220. Whether more evidence is required.
221. Whether human input is genuinely required.
222. Whether a task is actually complete.
223. Whether an expensive additional action is justified.
224. Which candidate merits deeper investigation.
225. Which project/work item receives resources next.
226. Which implementation approach should be pursued.
227. Which recovery branch should be pursued.

## 11. Hermes decision included in original event

228. Hermes’s proposed decision embedded in the original structured event.
229. No second request asking Hermes what decision did you make.
230. hermes_decision field.
231. Candidate choices included with the event.
232. Hermes reason summary optionally included.
233. Relevant evidence included.
234. Relevant state included.
235. Materiality included.
236. Reversibility included.
237. Objective included.
238. State version included.
239. Decision version included.
240. Jev evaluates the decision Hermes has already proposed.
241. Agreement can be detected without another Hermes round trip.
242. Disagreement can be detected without another Hermes round trip.

## 12. Example structured decision metadata to retain

243. event_id.
244. turn_id.
245. work_session_id/objective ID.
246. decision_id.
247. type.
248. scope.
249. goal.
250. state.
251. choices.
252. hermes_decision.
253. reason_summary.
254. materiality.
255. reversible.
256. state_version.
257. decision_version.
258. contract.
259. evidence.
260. current_strategy.
261. active_hypothesis.
262. consequence.
263. decision_context.

## 13. Jev response metadata

264. Original event_id.
265. Original turn_id.
266. Original state version.
267. Original decision version.
268. jev_decision.
269. Jev probabilities.
270. Jev confidence.
271. Agreement/disagreement disposition.
272. Jev model.
273. Jev provider.
274. Jev transport.
275. Jev request ID.
276. Jev latency.
277. Jev token usage.
278. Jev cost.
279. Jev contract.
280. Jev supervision recommendation where applicable.
281. Jev freshness/validity metadata.
282. Jev watch recommendations where applicable.

## 14. Confidence-gated challenge system

283. Low-confidence Jev answers do not interrupt Hermes.
284. Low-confidence Jev answers may still be logged.
285. Medium-confidence agreement normally log-only.
286. High-confidence agreement normally log-only.
287. High-confidence disagreement can generate a challenge.
288. Very-high-confidence/high-consequence disagreement can generate stronger intervention.
289. Agreement never needs to block Hermes.
290. Most Jev responses should produce no user-visible or worker-visible interruption.
291. Jev becomes a sparse exception channel.
292. Confidence thresholds empirically calibrated.
293. No permanent reliance on arbitrary example thresholds like .70/.85/.95.
294. Confidence interpreted together with consequence.
295. Confidence interpreted together with uncertainty.
296. Confidence interpreted together with staleness.
297. Confidence interpreted together with reversibility.
298. Challenge system records why a challenge was raised.

## 15. Jev challenge pipeline

299. Dedicated jev_challenge component.
300. Dedicated challenge queue.
301. Hermes challenge inbox.
302. Challenge associated with original decision/event.
303. Challenge delivered only when useful.
304. Challenge can arrive after Hermes has continued working.
305. Challenge validated against current state before application.
306. Challenge may modify current action when still actionable.
307. Challenge may modify next action when current action already occurred.
308. Challenge may be logged as stale.
309. Challenge may be advisory only.
310. Challenge may become precommit checkpoint for selected consequential actions.
311. Challenge acceptance logged.
312. Challenge rejection/override logged.
313. Override outcome logged.
314. Challenge usefulness later correlated with final outcomes.

## 16. Agreement/disagreement semantics

315. Hermes/Jev agreement logging.
316. Hermes/Jev disagreement logging.
317. No interruption for ordinary agreement.
318. High-confidence disagreement surfaced.
319. Final executed action logged.
320. Whether Hermes adopted Jev correction logged.
321. Whether Hermes correctly overrode Jev logged.
322. Whether Jev correctly overrode Hermes logged.
323. Outcome after agreement logged.
324. Outcome after disagreement logged.
325. Outcome after accepted challenge logged.
326. Outcome after rejected challenge logged.
327. Agreement rate metric.
328. Disagreement rate metric.
329. Useful-disagreement rate metric.
330. Jev disagreement precision metric.

## 17. Stale-response protection

331. State-versioned Jev requests.
332. Decision-versioned Jev requests.
333. State-versioned Jev responses.
334. Jev response validity check before action.
335. Current-state equality/compatibility check.
336. Stale Jev result detection.
337. Stale Jev results never blindly applied.
338. Stale results can remain telemetry.
339. Stale results can inform a subsequent decision.
340. State version can use semantic version IDs.
341. State version can use commit SHA.
342. State version can use tree hash.
343. State version can use test-run ID.
344. State version can use tool receipt ID.
345. State version can use other workflow-specific immutable identifiers.

## 18. Reversibility and irreversible-action handling

346. Explicit reversibility metadata.
347. Explicit committed/uncommitted state.
348. Jev disagreement before reversible uncommitted action may change the decision.
349. Jev disagreement after committed action does not blindly undo it.
350. Post-commit disagreement influences the next decision.
351. Consequential but not-yet-committed actions may use precommit supervision.
352. Irreversible actions receive elevated router priority.
353. External sends/deploys/deletes/pushes can receive elevated priority.
354. No automatic reverse-whatever-Hermes-just-did behavior.
355. Recovery after already-executed action treated as a new decision.

## 19. Supervision modes

356. SHADOW mode.
357. CORRECT_NEXT mode.
358. PRECOMMIT mode.
359. SHADOW logs Jev opinions without changing execution.
360. CORRECT_NEXT allows Jev to influence future action.
361. PRECOMMIT can briefly gate selected high-consequence boundaries.
362. Most operation remains asynchronous.
363. Synchronous behavior restricted to deliberately chosen consequential checkpoints.
364. Existing synchronous gating no longer primary architecture.

## 20. Local adaptive router

365. Dedicated local adaptive relevance engine.
366. Dedicated jev_supervisor.
367. Router consumes all structured Hermes events.
368. Router does not send all events remotely.
369. Router maintains compact local turn state.
370. Router accumulates state over time.
371. Router performs event compression.
372. Router performs novelty detection.
373. Router performs decision-change detection.
374. Router performs risk-change detection.
375. Router performs uncertainty-change detection.
376. Router performs evidence-change detection.
377. Router performs completion-pressure detection.
378. Router estimates whether another Jev call can plausibly change Hermes’s behavior.
379. Router treats Jev calls as a resource with expected value.
380. Router suppresses redundant Jev calls.
381. Router batches related events.
382. Router consolidates repetitive observations.
383. Router can remain local for hundreds of events.
384. Router forwards one state transition instead of raw event history when appropriate.

## 21. Router local state

385. Current goal.
386. Current objective.
387. Current strategy.
388. Active hypothesis.
389. Recent decisions.
390. Recent failures.
391. Recent retries.
392. Recent strategy changes.
393. Recent evidence.
394. Evidence novelty.
395. Confidence trend.
396. Tool/result novelty.
397. Contradictions.
398. Pending irreversible actions.
399. Pending consequential actions.
400. Completion evidence.
401. Current completion confidence/state.
402. Last Jev opinion.
403. Last Jev decision state.
404. Last Jev state version.
405. Last Jev trigger reason.
406. Last Jev challenge outcome.
407. Jev freshness.
408. Relevant event summary.
409. Event density.
410. Recent failure density.
411. Decision uncertainty.
412. Current reversibility.
413. Current materiality.
414. Current consequence level.

## 22. Adaptive Jev trigger signals

415. decision_delta.
416. evidence_delta.
417. risk_delta.
418. uncertainty_delta.
419. completion_pressure.
420. Strategy changes increase Jev pressure.
421. Unexpected results increase Jev pressure.
422. Hypothesis contradictions increase Jev pressure.
423. Repeated failures increase Jev pressure.
424. Falling Hermes confidence increases Jev pressure.
425. Multiple viable paths increase Jev pressure.
426. Approaching external mutation increases Jev pressure.
427. Increasing cost increases Jev pressure.
428. Increasing risk increases Jev pressure.
429. Approaching task completion increases Jev pressure.
430. Aging/stale Jev guidance increases Jev pressure.
431. Repetitive work decreases Jev pressure.
432. Stable state decreases Jev pressure.
433. Evidence confirming the current strategy decreases Jev pressure.
434. Redundant observations decrease Jev pressure.
435. Easily reversible actions decrease Jev pressure.
436. Recent Jev assessment of equivalent state decreases Jev pressure.
437. Materially new information can immediately increase pressure.
438. A single highly significant event can outweigh hundreds of mundane events.

## 23. Decision-delta logic

439. Detect same strategy/same trajectory.
440. Detect meaningful strategy transition.
441. Detect implementation-path changes.
442. Detect hypothesis switching.
443. Detect abandonment of current approach.
444. Detect newly introduced alternatives.
445. Detect closing/eliminating alternatives.
446. Detect when Hermes is merely continuing an already-selected strategy.
447. Continuing a stable strategy does not automatically re-call Jev.
448. Major trajectory shift strongly triggers Jev consideration.

## 24. Evidence-delta logic

449. Detect genuinely new information.
450. Detect redundant evidence.
451. Detect confirming evidence.
452. Detect contradictory evidence.
453. Detect evidence disproving active hypothesis.
454. Detect evidence substantially changing likelihoods.
455. Detect evidence sufficient to move from investigation to remediation.
456. Detect evidence sufficient to move from remediation to verification.
457. Detect evidence sufficient to consider completion.
458. Condense multiple evidence events before Jev.
459. Prefer state transition summaries over raw logs.

## 25. Risk-delta logic

460. Read-only introspection low risk.
461. Local reversible edits moderate risk.
462. Service restarts elevated risk.
463. Git push elevated risk.
464. Deployment elevated risk.
465. Message/send actions elevated risk.
466. Deletes elevated risk.
467. Purchases or irreversible external state elevated risk.
468. Risk trajectory used in Jev call-worthiness calculation.
469. Risk escalation can bypass ordinary batching.

## 26. Uncertainty-delta logic

470. Detect one obvious continuation path.
471. Detect multiple plausible paths.
472. Detect unresolved competing hypotheses.
473. Detect low-confidence Hermes decision.
474. Detect ambiguity requiring evidence.
475. Detect ambiguity requiring human input.
476. Increased uncertainty increases Jev call value.
477. Reduced uncertainty suppresses unnecessary Jev calls.

## 27. Completion pressure

478. Detect transition from active work toward I think this is done.
479. Detect COMPLETION_CANDIDATE.
480. Completion events receive high Jev priority.
481. Completion review can bypass sparse polling.
482. Jev checks whether observed evidence satisfies done criteria.
483. Jev can return DONE.
484. Jev can return NOT_DONE.
485. Jev can return NEEDS_VERIFICATION.
486. Completion assessment can map to PASS/RETRY/REPLAN/ESCALATE.
487. Premature completion detection.
488. False PASS treated as a critical metric.
489. Completion decisions tied to explicit objective done criteria.

## 28. Decision leases / Jev freshness

490. Jev decisions can remain valid across multiple Hermes actions.
491. Decision lease concept.
492. Lease allows Hermes to act autonomously under an already-selected strategy.
493. Lease remains valid while decision state stays materially equivalent.
494. Lease invalidated when active hypothesis is disproven.
495. Lease invalidated by material failure.
496. Lease invalidated by major strategy change.
497. Lease invalidated when destructive/consequential action boundary appears.
498. Lease invalidated when enough evidence exists to advance state.
499. Lease invalidated when relevant state version changes materially.
500. Lease reduces repeated Jev calls.
501. Router checks Jev freshness before calling again.
502. Hysteresis based on meaningful state change rather than time alone.

## 29. Hysteresis

503. Post-Jev-call hysteresis.
504. Repeated equivalent observations do not immediately trigger another call.
505. Confirming evidence alone normally does not trigger.
506. Same-hypothesis file reads normally do not trigger.
507. Unexpected failure can break hysteresis.
508. Contradictory evidence can break hysteresis.
509. Strategy transition can break hysteresis.
510. Completion candidate can break hysteresis.
511. High-risk boundary can break hysteresis.
512. Hysteresis prevents Jev call storms.

## 30. Event batching

513. Event batching under high-volume execution.
514. Repeated observations grouped.
515. Repeated tool results summarized.
516. Repeated failures summarized.
517. Intermediate hypothesis evolution summarized.
518. State transition summary sent instead of dozens of raw events.
519. Batch may contain event count.
520. Batch may contain tool-call count.
521. Batch may contain failure count.
522. Batch may contain new-hypothesis count.
523. Batch may contain strategy-change count.
524. Batch may contain current decision.
525. Batch may contain current evidence delta.
526. Batch may contain router trigger reasons.
527. Batch may contain accumulated relevant state.
528. Batch maintains provenance back to underlying events.

## 31. Adaptive polling/sparse mode

529. Polling/batching mode retained as a concept.
530. Polling is not based primarily on fixed every N events.
531. Polling triggered by workload/state characteristics.
532. Adaptive sparse mode.
533. Adaptive intensive mode.
534. Event pressure can change Jev granularity.
535. Decision materiality independently changes Jev priority.
536. High event density can decrease ordinary Jev frequency.
537. High decision consequence can increase Jev priority even under high density.
538. Ordinary low-value events can be accumulated locally.
539. Important decisions bypass polling.
540. Completion candidates bypass polling.
541. Consequential actions bypass polling.
542. Strategy changes bypass polling when sufficiently material.
543. Repeated failures bypass polling.
544. Human escalation decisions bypass polling.
545. Irreversible actions bypass polling.
546. High-materiality decisions bypass polling.

## 32. Jev-controlled supervision intensity

547. Jev may recommend its own future supervision intensity.
548. Jev may return supervision mode.
549. Example SPARSE supervision mode.
550. Example INTENSIVE supervision mode.
551. Jev may recommend which event classes to watch.
552. Jev may recommend looser observation when trajectory is stable.
553. Jev may recommend tighter observation when trajectory is unstable.
554. Jev may recommend a future polling cadence as a hint.
555. Poll cadence remains subordinate to local critical-event overrides.
556. Jev does not get called solely to decide whether each individual event warrants Jev.

## 33. Expected-value routing

557. Explicit concept of expected value of a Jev call.
558. Estimate probability Jev will produce a useful disagreement.
559. Weight by consequence of current decision.
560. Weight by uncertainty.
561. Weight by novelty.
562. Weight by materiality.
563. Weight by risk.
564. Weight by Jev freshness.
565. Subtract provider cost.
566. Subtract latency cost.
567. Subtract stale-answer risk.
568. Subtract redundant-call penalty.
569. Invoke Jev when expected benefit is sufficiently positive.
570. No requirement that expected-value logic literally use a single hand-coded equation.
571. Design philosophy centered on could another Jev opinion materially matter now?

## 34. No hard-coded event-count dependence

572. No primary call Jev every 10 events behavior.
573. No primary call Jev after 25 events behavior.
574. No primary call Jev after 100 tool calls behavior.
575. Event counts may remain as contextual signals.
576. Event counts may remain as diagnostics.
577. Event counts may remain as emergency ceilings.
578. Hard maximum/provider budget only as a safety valve.
579. Adaptive state relevance remains primary call trigger.

## 35. Router materiality model

580. Continuous materiality signal.
581. Earlier 0–5 materiality idea retained as a conceptual feature if useful.
582. Materiality not used as a single permanent hard-coded threshold.
583. Trivial operational details very low materiality.
584. Meaningful but reversible details low/moderate materiality.
585. Strategy-changing choices high materiality.
586. External/irreversible choices high materiality.
587. Completion high materiality.
588. Materiality combined with uncertainty and consequence.
589. Materiality included in telemetry.

## 36. Critical Jev control states

590. CONTINUE.
591. RETRY.
592. REPLAN.
593. ESCALATE.
594. DONE.
595. GATHER_EVIDENCE.
596. ASK_HUMAN.
597. Potential ROLLBACK.
598. Potential INSPECT.
599. Potential strategy-specific bounded labels.
600. PASS.
601. FAIL.
602. PARTIAL.
603. UNKNOWN.
604. NOT_DONE.
605. NEEDS_VERIFICATION.

## 37. Recovery control

606. Recovery decision events.
607. Retry vs replan.
608. Retry vs gather evidence.
609. Retry vs rollback.
610. Retry vs human escalation.
611. Replan vs escalation.
612. Repeated retry detection.
613. Repeated failure detection.
614. Jev intervention on looping behavior.
615. Failure events high-value compared with ordinary successful tool calls.
616. Recovery outcomes logged.

## 38. Ambiguity handling

617. Explicit enough information? judgment.
618. Evidence sufficiency assessment.
619. Human escalation when genuinely required.
620. Avoid automatic human escalation for ordinary uncertainty.
621. Bounded ASK_HUMAN option.
622. Bounded GATHER_EVIDENCE option.
623. Jev can detect when Hermes is choosing prematurely.
624. Jev can detect when a decision should wait for more evidence.

## 39. Resource/routing decisions

625. Worker selection.
626. Tool selection.
627. Tool-family selection.
628. Environment selection.
629. Local versus remote compute.
630. CPU versus GPU where material.
631. j2 versus win4060 style routing.
632. Cheap versus expensive path selection.
633. Candidate prioritization.
634. Hypothesis prioritization.
635. File/remediation candidate ranking.
636. Queue/work-item prioritization.
637. Jev ranking used only where bounded candidate sets exist.

## 40. Structured multi-question assessment

638. Batch related control questions into one Jev call.
639. Previous-step success assessment.
640. Next-action selection.
641. Evidence-sufficiency assessment.
642. Completion assessment.
643. Confidence assessment.
644. Potential supervision-intensity recommendation.
645. Potential watch-category recommendation.
646. Avoid separate network round trips for each sub-question.

## 41. Useful-work filtering

647. Known read-only introspection not automatically Jev-assessed.
648. File reading generally local.
649. Grep/search generally local.
650. Git status generally local.
651. Status inspection generally local.
652. Test execution generally local unless the test result creates a decision fork.
653. Routine evidence gathering generally local.
654. Repetitive same-hypothesis diagnostics generally local.
655. Jev invoked on the decision produced by evidence, not the mere act of collecting evidence.
656. Tool calls treated as signals, not definitions of work.
657. Mutating tool calls treated as stronger signals.
658. External mutations treated as stronger signals.
659. Decision plane determines ultimate eligibility.

## 42. Existing selective gate retained but demoted

660. Existing selective pre_tool_call gating can remain.
661. Existing gate_scope=selective behavior retained.
662. Known read-only bypass retained.
663. Existing gate no longer treated as primary Jev architecture.
664. Automatic gating remains off by default.
665. Synchronous gating reserved for narrow precommit/high-consequence use.
666. gate_scope=all remains compatibility/explicit mode rather than recommended operation.
667. Legacy gate telemetry retained.

## 43. Existing tools retained

668. nerve_decide.
669. nerve_rank.
670. nerve_verify.
671. nerve_assess.
672. nerve_context_curate.
673. nerve_context_rehydrate.
674. nerve_stats.
675. Existing tools remain available manually.
676. New nervous-system architecture sits above these primitives.
677. Existing direct tool APIs remain useful for explicit debugging/testing.

## 44. Existing hooks/context surfaces retained

678. pre_tool_call hook.
679. post_tool_call hook.
680. Optional Jev ContextEngine.
681. Context engine not automatically selected.
682. Existing built-in Hermes compressor fallback retained.
683. Context system remains shadow-first until proven.

## 45. Context features discussed for eventual integration

684. Context should become subordinate to decision usefulness, not maximum compression.
685. Decision-state context accumulator.
686. Current goal retention.
687. Current strategy retention.
688. Active hypothesis retention.
689. Important failure retention.
690. Contradiction retention.
691. Relevant completion evidence retention.
692. Last Jev opinion retention.
693. Event-state compression before remote Jev call.
694. Existing anchoring capability retained.
695. Existing local rehydration capability retained.
696. Sanitized evidence rehydration retained.
697. Context pressure experimentation remains future validation target.
698. Actual shadow-plan pressure testing still needed.
699. End-to-end ANCHOR → rehydrate → successful continuation remains a valuable validation scenario.
700. Context optimization explicitly not the first priority of the decision-engine redesign.

## 46. Local classifier evolution

701. Begin with local deterministic/state-delta logic.
702. Do not put another full remote LLM in front of Jev.
703. Optional future tiny local classifier.
704. Classifier estimates P(useful Jev disagreement | state delta).
705. Classifier should execute locally.
706. Classifier should be low latency.
707. Classifier should be cheap.
708. Classifier should use accumulated historical telemetry.
709. Classifier should learn which event patterns merit Jev.
710. Rules + state delta + tiny classifier hybrid architecture.
711. Classifier does not replace turn-level Jev admission unless proven useful.

## 47. Adaptive learning from outcomes

712. Router learns from Jev agreement/disagreement history.
713. Router learns from challenge usefulness.
714. Router learns from accepted Jev corrections.
715. Router learns from rejected Jev corrections.
716. Router learns from final task outcome.
717. Router learns event classes with low Jev value.
718. Router learns event classes with high Jev value.
719. Router reduces calls for consistently low-value patterns.
720. Router increases sensitivity for high-value patterns.
721. Completion supervision can become aggressive if it frequently catches errors.
722. Recovery supervision can become aggressive if it frequently catches bad retries.
723. Calibration by event type.
724. Calibration by objective type.
725. Calibration by consequence class.
726. Calibration by Hermes model.
727. Calibration by Jev model/provider if relevant.
728. Calibration by confidence bucket.

## 48. Decision outcome dataset

729. Store Hermes decision.
730. Store Jev decision.
731. Store agreement boolean.
732. Store Jev confidence.
733. Store Jev probability distribution.
734. Store final action.
735. Store whether Jev changed the action.
736. Store observed outcome.
737. Store whether outcome was successful.
738. Store whether Hermes override was correct.
739. Store whether Jev correction was correct.
740. Store state delta.
741. Store router trigger reason.
742. Store objective type.
743. Store decision type.
744. Store materiality.
745. Store reversibility.
746. Store consequence.
747. Store latency.
748. Store provider cost.
749. Store stale/not-stale classification.
750. Store challenge disposition.

## 49. Telemetry metrics

751. Total turns.
752. OFF turns.
753. WATCH turns.
754. ON turns.
755. WATCH→ON promotions.
756. Total raw events.
757. Events consumed locally.
758. Events suppressed.
759. Events batched.
760. Events forwarded to Jev.
761. Provider-call avoidance count.
762. Jev calls per turn.
763. Jev calls per 100 Hermes events.
764. Jev calls per meaningful decision.
765. Meaningful decision count.
766. Jev decisions followed.
767. Jev decisions overridden.
768. Agreements.
769. Disagreements.
770. High-confidence disagreements.
771. Challenges issued.
772. Challenges accepted.
773. Challenges rejected.
774. Stale challenges.
775. Useful disagreements.
776. Useless disagreements.
777. False-positive challenges.
778. False-negative supervision events where measurable.
779. Retry count.
780. Replan count.
781. Escalate count.
782. Gather-evidence count.
783. Completion assessments.
784. False PASS.
785. False REPLAN.
786. Premature-DONE catches.
787. Rehydrations.
788. Decision-lease reuse.
789. Decision-lease invalidations.
790. Average Jev latency.
791. P50 Jev latency.
792. P95 Jev latency.
793. Jev token usage.
794. Jev provider cost.
795. Estimated avoided Jev calls.
796. Estimated avoided provider cost.
797. Avoided synchronous wait time.
798. Final task success.
799. Decision correction success.
800. Router precision.
801. Router recall where ground truth can be approximated.
802. Challenge precision.
803. Confidence calibration.

## 50. Metrics explicitly prioritized in the thread

804. False PASS as a critical metric.
805. Final task success as ultimate metric.
806. Useful decision disagreement over raw Jev call count.
807. Avoid number of Jev calls as the primary success measure.
808. Measure whether Jev actually changed the trajectory usefully.
809. Measure whether Jev catches premature completion.
810. Measure whether Jev catches pointless retry loops.
811. Measure whether Jev improves routing.
812. Measure how often Hermes correctly overrides Jev.
813. Measure how often Jev correctly overrides Hermes.
814. Measure decision-added latency.
815. Measure avoided tool/model calls.
816. Measure avoided Jev calls.

## 51. Receipts

817. Immutable-ish structured decision receipts.
818. Turn-admission receipt.
819. Router-trigger receipt.
820. Jev-request receipt.
821. Agreement receipt.
822. Challenge receipt.
823. Challenge-resolution receipt.
824. Stale-response receipt.
825. Decision-lease receipt.
826. Completion receipt.
827. Recovery receipt.
828. Final-turn supervision summary.
829. Choices preserved.
830. Hermes selected value preserved.
831. Jev selected value preserved.
832. Probabilities preserved.
833. Confidence preserved.
834. Decision contract preserved.
835. Resulting Hermes action preserved.
836. Observed outcome preserved.
837. Provider provenance preserved.
838. State/version provenance preserved.

## 52. nerve_stats expansion

839. Turn admission section.
840. Nervous-system section.
841. Event-router section.
842. Router trigger reasons.
843. Router suppression reasons.
844. Batch statistics.
845. Challenge statistics.
846. Agreement statistics.
847. Disagreement statistics.
848. Staleness statistics.
849. Decision-lease statistics.
850. Completion statistics.
851. Recovery statistics.
852. Supervision-mode statistics.
853. WATCH→ON transition statistics.
854. Provider usage statistics.
855. Cost statistics.
856. Latency statistics.
857. Avoided-call estimates.
858. Confidence calibration buckets.
859. Recent high-confidence disagreements.
860. Recent stale responses.
861. Recent challenge outcomes.
862. Local-only nerve_stats behavior retained.

## 53. Provider architecture retained

863. OpenRouter Jev transport retained.
864. Direct TypeSafe transport retained.
865. Provider selection without changing Hermes-visible decision contracts.
866. Only credential for selected provider required.
867. OpenRouter credential path.
868. TypeSafe credential path.
869. OpenRouter model configuration retained.
870. Direct TypeSafe model configuration retained.
871. Transport provenance included in responses.
872. Request IDs preserved.
873. Provider token usage preserved when available.
874. Provider cost preserved when available.
875. Provider latency preserved.
876. Provider errors incorporated into supervision telemetry.
877. Provider failures do not silently authorize consequential execution.

## 54. Direct TypeSafe validation work

878. Direct TypeSafe transport remains wire-verified.
879. Add first genuine direct-account live smoke when credentials are available.
880. Distinguish wire-contract verification from live-account verification.
881. Do not claim direct live validation before it exists.
882. Keep OpenRouter path as known live-tested reference.
883. Compare direct TypeSafe and OpenRouter latency if live access becomes available.
884. Compare cost where applicable.
885. Compare response/probability behavior where appropriate.

## 55. Latency constraints

886. Explicit architectural assumption: Jev ping cannot reliably get below roughly 500 ms in current setup.
887. Avoid adding that latency to ordinary tool work.
888. Avoid synchronous per-tool Jev calls.
889. Avoid synchronous per-observation Jev calls.
890. Avoid synchronous per-decision microchecks where asynchronous supervision suffices.
891. Reserve synchronous waiting for deliberately selected precommit boundaries.
892. Measure network latency separately from worker wall-clock penalty.
893. Design every new Jev feature around asynchronous operation where possible.

## 56. Long-running autonomous-worker support

894. Supervision persists across very long turns.
895. Supervision persists across hundreds of tool calls.
896. Supervision persists across worker spawns.
897. Supervision persists across strategy changes.
898. Supervision persists until explicit turn completion.
899. Long-running sessions shift toward more compressed event representation.
900. High event volume does not disable critical-event Jev checks.
901. High event volume can reduce low-value Jev call frequency.
902. Long-run state summaries replace full raw history.
903. Jev receives decision state, not 30,000-token conversation history.
904. Jev input optimized toward hundreds of relevant tokens where possible.

## 57. Event-stream privacy/compactness principles

905. Jev receives structured relevant state instead of the complete transcript.
906. Raw conversation transcript not automatically forwarded to nervous-system Jev.
907. Raw roleplay transcript not automatically forwarded.
908. Raw tool transcript not automatically forwarded.
909. Relevant evidence condensed.
910. Relevant state condensed.
911. Decision alternatives explicitly represented.
912. Hermes proposal explicitly represented.
913. Event provenance retained despite compression.

## 58. Turn lifecycle

914. Prompt received.
915. turn_id created.
916. Hermes starts work immediately.
917. Prompt simultaneously evaluated by turn arbiter.
918. Arbiter returns OFF/WATCH/ON.
919. Local event bus runs.
920. Local router accumulates state.
921. ON mode permits active Jev calls.
922. WATCH mode waits for a decision-plane wake condition.
923. OFF mode logs admission result and remains quiet.
924. Material decision can create Jev assessment.
925. Jev result can log agreement.
926. Jev result can generate challenge.
927. Router continues accumulating state.
928. Supervision persists through autonomous execution.
929. Completion candidate receives high-priority review where supervised.
930. TURN_COMPLETE ends turn-scoped nervous system.
931. Final supervision summary emitted.

## 59. WATCH wake triggers

932. Structured DECISION.
933. MUTATION_INTENT.
934. RECOVERY.
935. COMPLETION_CANDIDATE.
936. Consequential operation intent.
937. Strategy change.
938. Repeated failure.
939. High uncertainty.
940. Human escalation candidate.
941. Irreversible-action candidate.
942. Other adaptive-router indication that a real decision plane has emerged.

## 60. Useful Jev call definition

943. Jev call should have a reasonable chance of changing Hermes’s next meaningful action.
944. Jev call should have a reasonable chance of preventing an error.
945. Jev call should have a reasonable chance of catching false completion.
946. Jev call should have a reasonable chance of improving recovery.
947. Jev call should have a reasonable chance of improving routing.
948. Jev call should have a reasonable chance of identifying need for more evidence.
949. Calls that merely reconfirm obvious harmless behavior should be suppressed.
950. Calls whose answer cannot influence any still-actionable state should normally be suppressed.

## 61. Anti-bureaucracy behavior

951. Do not Jev-check every ls.
952. Do not Jev-check every file read.
953. Do not Jev-check every grep.
954. Do not Jev-check every status command.
955. Do not Jev-check every successful test.
956. Do not Jev-check every harmless tool call.
957. Do not turn Jev into an ALLOW-everything latency tax.
958. Do not optimize for maximizing percentage of actions reviewed.
959. Do not equate more Jev calls with better control.
960. Do not use Jev as a conversational shadow for ordinary dialogue.

## 62. Synchronous loop ideas explicitly superseded

961. Do not make route → act → verify → route a mandatory synchronous network loop.
962. Do not require Jev verification after every meaningful Hermes unit if it would block execution.
963. Do not independently call Jev for verification and then again for next-action selection when one assessment can batch them.
964. Do not make Hermes wait 500+ ms at every fork unless that fork is deliberately precommit/consequential.
965. Preserve the conceptual control states from that design while moving them into the asynchronous nervous system.

## 63. Raw-chat separation explicitly refined

966. Do not completely forbid Jev from seeing the user prompt.
967. The turn arbiter may see the original prompt once.
968. The nervous system should not continuously consume raw chat.
969. After admission, structured decision state becomes the primary Jev input.
970. Casual prompts should normally terminate after the admission decision.
971. Chat can still contain work.
972. Work can still look like chat.
973. Roleplay can still contain accountable director-level work.
974. Therefore Jev activation must follow decision-plane/accountability semantics, not UI surface.

## 64. Decision admission inside an active turn

975. Local router acts as second-level admission after turn-level Jev admission.
976. Turn admission answers could this turn need Jev?
977. Local router answers does Jev matter right now?
978. Jev itself not invoked for every local router decision.
979. Local router designed to be far cheaper than remote Jev.
980. Local router stateful across the turn.
981. Local router decision based on state deltas rather than raw event count.
982. Critical-event bypass always available.

## 65. Potential future local intelligence

983. Lightweight local statistical model.
984. Lightweight classifier.
985. No need for full conversational intelligence.
986. Input primarily router-state features.
987. Output useful-disagreement probability.
988. Potential confidence calibration.
989. Potential event-type calibration.
990. Potential per-objective calibration.
991. Potential model-specific calibration.
992. Potential online/offline tuning from collected receipts.

## 66. Goal-oriented verification

993. Verification tied to explicit goal.
994. Verification tied to observed evidence.
995. Verification tied to done criteria.
996. Verification not based solely on Hermes saying work is complete.
997. Completion evidence bundled into Jev assessment.
998. PASS only when required state is actually supported.
999. RETRY for execution failure with still-valid strategy.
1000. REPLAN when current approach is inadequate.
1001. ESCALATE when genuine external/human dependency exists.
1002. GATHER_EVIDENCE when state is insufficient.
1003. Avoid completion without relevant evidence.

## 67. Decision engine authority model

1004. Jev authoritative enough that high-confidence disagreements can alter trajectory.
1005. Hermes not required to blindly follow every Jev output.
1006. Hermes overrides explicitly recorded.
1007. Jev corrections explicitly recorded.
1008. Staleness can override Jev authority.
1009. Reversibility can affect Jev authority.
1010. Consequence can affect Jev authority.
1011. Confidence can affect Jev authority.
1012. Precommit mode can temporarily increase Jev authority.
1013. Shadow mode deliberately reduces Jev authority.
1014. Correct-next mode gives Jev future-state authority without unsafe retroactive undo.

## 68. Testing scenarios explicitly implied/discussed

1015. Real bug diagnosis task.
1016. Failing-test repair task.
1017. Service-failure diagnosis task.
1018. Multiple-plausible-root-causes task.
1019. Local versus remote-worker routing task.
1020. Retry-versus-replan task.
1021. Premature completion trap.
1022. Repeated failure loop.
1023. High-confidence Hermes/Jev disagreement.
1024. Low-confidence Jev disagreement.
1025. Jev agreement.
1026. Stale Jev response.
1027. State changed before challenge arrives.
1028. Reversible action corrected after challenge.
1029. Irreversible action already completed before challenge.
1030. Precommit consequential action.
1031. Casual chat admission.
1032. Ordinary explanation admission.
1033. Pure fictional roleplay admission.
1034. Roleplay with real training objective.
1035. Research-only turn.
1036. Research that becomes real execution mid-turn.
1037. WATCH→ON promotion.
1038. Two-hour/high-event-count autonomous turn.
1039. Hundreds of low-value tool calls with few real decisions.
1040. Event batching.
1041. Event compression.
1042. Adaptive router suppression.
1043. Router hysteresis.
1044. Router trigger after hypothesis contradiction.
1045. Direct TypeSafe live smoke.
1046. OpenRouter live regression.
1047. Context pressure/shadow planning.
1048. Anchor→rehydrate continuation.

## 69. Recommended default posture

1049. Turn arbiter enabled.
1050. Nervous system asynchronous.
1051. Most casual turns OFF.
1052. Ambiguous potentially operational turns WATCH.
1053. Clearly autonomous/material work turns ON.
1054. Local adaptive router enabled.
1055. Confidence-gated challenges enabled.
1056. Agreement log-only by default.
1057. Low-confidence disagreement log-only by default.
1058. High-confidence disagreement eligible for challenge.
1059. PRECOMMIT restricted to consequential boundaries.
1060. Legacy automatic gate remains off by default.
1061. Context mutation remains shadow-first initially.
1062. Built-in Hermes context fallback retained.
1063. Provider call budget safety valve enabled.
1064. Adaptive relevance remains primary call-limiting mechanism.

## 70. Existing release engineering issues worth fixing in the next release

1065. Canonical release tree should match the pinned published repository.
1066. Handoff ZIP should not silently differ from the pinned source tree.
1067. Clearly distinguish full development test suite from compact admission/release suite.
1068. Clearly document intended test runner.
1069. unittest remains the known intended runner for the examined v0.1.5.5 tree.
1070. Avoid confusing pytest collection failures being mistaken for functional failures.
1071. Include GUIDE.md in canonical handoff/package where expected.
1072. Include SETUP.md in canonical handoff/package where expected.
1073. Include PROVIDER_SETUP.md in canonical handoff/package where expected.
1074. Preserve exact release checksums.
1075. Preserve exact pinned commit reference.
1076. Keep PR/release documentation aligned with actual packaged contents.
1077. Report test counts accurately by suite.
1078. Keep provider-validation claims precise.
1079. Keep direct-TypeSafe wire-tested distinct from live-tested.

## 71. Architecture components that emerged from the thread

1080. jev_turn_arbiter.
1081. jev_event_bus.
1082. jev_supervisor.
1083. Adaptive local relevance router.
1084. Local turn-state accumulator.
1085. Event compressor.
1086. Novelty detector.
1087. Decision-delta detector.
1088. Evidence-delta detector.
1089. Risk-delta detector.
1090. Uncertainty-delta detector.
1091. Completion-pressure detector.
1092. Jev freshness/decision-lease manager.
1093. Jev asynchronous provider worker.
1094. Jev challenge queue.
1095. Hermes challenge inbox.
1096. Challenge-state validator.
1097. Agreement/disagreement logger.
1098. Nervous-system receipt store.
1099. Outcome correlation layer.
1100. Router calibration dataset.
1101. Optional future local classifier.

## 72. Overall final design principles

1102. Jev supervises decisions, not tokens.
1103. Jev supervises decisions, not every tool call.
1104. Jev supervises accountable objectives, not whatever happens to look like work.
1105. Jev can inspect the prompt once to decide whether supervision is useful.
1106. The nervous system sees structured state rather than raw conversation wherever possible.
1107. Hermes never waits for Jev unless a deliberately chosen precommit boundary requires it.
1108. Most Jev agreements stay silent.
1109. Most low-confidence Jev results stay silent.
1110. High-confidence meaningful disagreement is the scarce signal.
1111. State change, not event count, determines when Jev should look again.
1112. Novelty, uncertainty, consequence, risk, and completion pressure determine Jev value.
1113. High-volume work should make the system smarter and more compressed, not simply more expensive.
1114. One significant contradiction can matter more than hundreds of mundane tool events.
1115. Jev’s previous opinion remains usable until the decision state materially changes.
1116. Stale Jev answers never blindly mutate newer state.
1117. Completed irreversible actions are not blindly reversed because of a late Jev disagreement.
1118. The final optimization target is useful intervention per Jev call, not Jev-call volume.
1119. The ultimate metric is whether Jev makes Hermes complete real work more reliably.
