# qa-artifact-compression-workflow
AI-driven QA artifact compression workflow

# QA Artifact Compression Workflow

AI-driven QA artifact compression workflow exploring how structured LLM agents can reduce manual QA artifact planning workload by 60–80% while keeping human testers in control of validation and exploratory testing.

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

---

### What This Is Not

- Not an autonomous QA system
- Not a CI/CD automation layer
- Not a replacement for exploratory testing
- Not a coverage auditing engine (v1)

---

## Status

v1 specification complete.  
Agent implementation in progress.

See `/docs/V1_SPEC.md` for full system design.

