# QRAFT — QA Artifact Generation Pipeline

AI-driven QA artifact generation pipeline exploring how structured LLM agents can reduce manual QA artifact planning workload by 60–80% while keeping human testers in control of validation and exploratory testing.

---

## Why This Exists

Manual QA teams spend significant time:

- Interpreting PRDs
- Drafting structured requirements
- Writing and formatting test plans
- Maintaining traceability between requirements and tests

This project experiments with compressing that effort into a deterministic AI workflow so testers can focus on:

- Risk validation
- Exploratory testing
- Critical thinking
- Product quality judgment

The goal is not to replace QA professionals, but to elevate them by removing repetitive artifact construction work.

---

## Scope (v1)

### What It Is

A structured AI workflow that:

- Parses a PRD into discrete, testable requirements  
- Identifies risk and assigns severity  
- Generates classified test cases (unit, integration, e2e, exploratory, non-functional)  
- Produces a sprint-scoped Markdown test plan for human review  

It is a deterministic artifact generation pipeline, not an autonomous testing system.


Constraints:

- Linear pipeline (no orchestration engine)
- Single LLM call per agent
- Strict JSON output contracts
- Markdown artifact generation for review
- Human approval required at all times

### Sample Output

The `sample_output/` folder contains reference outputs generated during 
development across three input types — a clean agile PRD, a messy PRD, 
and raw meeting notes. These are preserved as examples of what the 
pipeline produces and are never overwritten by the runner.

---

### What This Is Not

- Not an autonomous QA system
- Not a CI/CD automation layer
- Not a replacement for exploratory testing
- Not a coverage auditing engine (v1)

---
## How This System Improves

The workflow is designed to get better through use. During initial testing, severity
heuristics were updated to better define the boundaries of the core user
journey — specifically to include post-purchase communication as a high
severity concern.

The pattern for iteration is simple:
- Human reviewer identifies a consistent gap in agent output
- The agent prompt is updated to encode the fix
- The system is re-run to confirm the correction holds

Reviewers are not just approving output — they are actively improving the
system through their judgment.

---

## Status

Phase 1 complete. Test plan generation from PRDs is fully implemented and validated against multiple input types.

QRAFT is a multi-phase pipeline. Phase 1 is the foundation — subsequent phases cover test data generation, test script generation (Cypress, Playwright, Postman, k6), coverage summary reporting, and PR artifact generation. See `ARCHITECTURE.md` for the full pipeline design and roadmap.