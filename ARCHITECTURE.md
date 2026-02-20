# QRAFT — QA Artifact Generation Pipeline — v1 Architecture

---

## 1. Project Intent

To reduce manual QA artifact workload by 60–80% by using AI agents to generate structured requirements analysis, risk models, and test plans from raw PRDs. Human testers retain ownership of validation, exploratory testing, and approval.

---

## 2. System Architecture

### Pipeline

```
PRD Input (markdown or plain text)
   ↓
Intake Agent        → plan_context block + structured requirements array
   ↓
Risk Agent          → risk-annotated, classified test plan array
   ↓
Review Agent        → complete Markdown test plan document
   ↓
Human Review & Approval
```

### Design Principles

- Linear pipeline. No branching, no orchestration, no retry logic.
- Each agent is a single prompted LLM call with strict JSON output — except Review Agent which outputs Markdown.
- No agent modifies upstream output.
- All artifacts are human-readable and independently approvable.
- `sample_output/` is preserved reference material — the runner writes to `output/` which is gitignored and not committed

---

## 3. Agent Definitions

### 3.1 Intake Agent

**Role:** Normalize and structure raw PRD content into discrete, testable requirements. Derive document-level plan context from the parsed requirement set.

**Does not:** Predict surfaces, assign risk, or apply test strategy.

**Input:** Raw PRD text

**Output:** A single JSON object containing a `plan_context` block and a `requirements` array.

```json
{
  "plan_context": {
    "purpose": "Validate the checkout flow against defined acceptance criteria across critical user journeys, integration points, and edge cases prior to release.",
    "in_scope": [
      "Guest and authenticated checkout flows",
      "Discount code application and validation",
      "Email confirmation delivery and SLA",
      "Order confirmation page rendering",
      "Cart-to-payment session state integrity"
    ],
    "out_of_scope": [
      "Account creation and login flows",
      "Payment gateway internals and PCI compliance testing",
      "Post-order fulfilment and shipping workflows",
      "Admin and back-office order management"
    ]
  },
  "requirements": [
    {
      "req_id": "REQ-001",
      "prd_ref": "Section 2.1",
      "description": "User receives email confirmation within 60s of checkout",
      "actors": ["Customer", "Email Service"],
      "testable": true,
      "ambiguity_flags": ["60s SLA undefined under load conditions"]
    }
  ]
}
```

**Field Rules**

| Field | Rule |
|---|---|
| `req_id` | Sequential, prefixed `REQ-` |
| `prd_ref` | Must trace to a section or line in source PRD |
| `testable` | `false` if requirement cannot be directly verified |
| `ambiguity_flags` | Empty array if none — never omitted |
| `plan_context.purpose` | One to two sentences derived from parsed requirements — not invented |
| `plan_context.in_scope` | Feature areas and integration points present in parsed requirements |
| `plan_context.out_of_scope` | Areas explicitly excluded in PRD or absent from all parsed requirements |

**Prompt Constraints**

```
Parse all requirements from the PRD and produce a single JSON object.

For each requirement:
- Assign a sequential req_id prefixed REQ-
- Trace prd_ref to a section or line in the source document
- Set testable to false if the requirement cannot be directly verified
- Populate ambiguity_flags with any unclear, undefined, or conflicting conditions
- Use an empty array for ambiguity_flags if none exist — never omit the field

After parsing all requirements, produce a plan_context block:
- purpose: one or two sentences summarising what this test plan validates and why
- in_scope: feature areas and integration points covered by parsed requirements
- out_of_scope: areas explicitly excluded in the PRD or not represented by any requirement

Do not invent scope boundaries. Derive them only from what is present
or explicitly absent in the PRD.
```

---

### 3.2 Risk Agent

**Role:** Apply testing strategy to each requirement. Assign risk, severity, and generate fully classified test cases.

**Does not:** Modify or re-interpret requirements.

**Input:** `requirements` array and `project_context` block from Intake Agent output

**Output:** Array of risk-annotated test plan objects

```json
[
  {
    "req_id": "REQ-001",
    "risk": "Provider latency under peak load may breach SLA",
    "severity": "high",
    "severity_basis": "Affects core user journey — failure breaks post-purchase trust signal",
    "severity_locked": false,
    "test_cases": [
      {
        "tc_id": "TC-001",
        "req_id": "REQ-001",
        "objective": "Verify confirmation email is delivered within 60s under normal load",
        "type": "integration",
        "surface": "service",
        "priority": "P1",
        "human_note": "Use timestamped send and receive logs to validate SLA"
      },
      {
        "tc_id": "TC-002",
        "req_id": "REQ-001",
        "objective": "Verify confirmation email is delivered within 60s under peak load",
        "type": "non_functional",
        "surface": "service",
        "priority": "P1",
        "human_note": "Simulate 10x normal order volume; confirm SLA holds"
      },
      {
        "tc_id": "TC-003",
        "req_id": "REQ-001",
        "objective": "Explore failure states when email provider is degraded or unresponsive",
        "type": "exploratory",
        "surface": "workflow",
        "priority": "P2",
        "human_note": "SLA boundary undefined — tester to document observed behaviour and define failure threshold"
      }
    ]
  }
]
```

**Classification Rules**

| Field | Allowed Values |
|---|---|
| `type` | `unit` `integration` `e2e` `exploratory` `non_functional` |
| `surface` | `ui` `api` `service` `workflow` |

Both fields are required on every test case. A test case missing either field is malformed output.

**Severity Heuristics**

| Severity | Condition |
|---|---|
| `high` | Affects data integrity, security, payment, core user journey, or post-purchase communication critical to the user completing their goal |
| `medium` | Affects secondary features, performance thresholds, or UX degradation |
| `low` | Cosmetic, edge-case only, or easily recoverable |

When ambiguous, assign one level higher and explain reasoning in `severity_basis`.

**Exploratory Generation Rule**

Exploratory test cases are generated only when at least one is true:
- `risk` is present on the requirement
- `ambiguity_flags` is non-empty

Never generated by default for clean requirements.

**Prompt Constraints**

```
For each requirement in the input array, produce a risk entry.

Assign severity using the following heuristics:
- high:   affects data integrity, security, payment, or core user journey
- medium: affects secondary features, performance thresholds, or UX degradation
- low:    cosmetic, edge-case only, or easily recoverable

When ambiguous, assign one level higher and explain in severity_basis.

For every test case you generate:
- type must be one of: unit, integration, e2e, exploratory, non_functional
- surface must be one of: ui, api, service, workflow
- Both fields are required. Do not omit either. Do not invent values outside these lists.
- If classification is ambiguous, default to exploratory / workflow and flag in human_note.

Only generate exploratory test cases when at least one of the following is true:
- The requirement has an associated risk entry
- The intake artifact contains one or more ambiguity_flags for that requirement

Do not generate exploratory test cases for clean, unambiguous requirements.
```

---

### 3.3 Review Agent

**Role:** Render Intake Agent and Risk Agent output into a single structured Markdown test plan document ready for human review. No reasoning. No inference.

**Input:** Full Intake Agent output (`plan_context` + `requirements`) and Risk Agent output (risk and test case array)

**Output:** A single Markdown document containing Purpose, In Scope, Out of Scope, and all requirements with associated risks and fully classified test cases, followed by a human review decision block.

**Output Template**

```markdown
# QRAFT Test Plan
**Artifact ID:** {artifact_id}
**PRD Source:** {prd_source}
**Generated:** {date}
**Status:** Pending Human Review

---

## Purpose
{plan_context.purpose}

---

## In Scope
{plan_context.in_scope as list}

---

## Out of Scope
{plan_context.out_of_scope as list}

---

## Requirements & Test Cases

---

## {req_id} — {description}
**PRD Reference:** {prd_ref}
**Actors:** {actors}
**Testable:** {testable}
**Ambiguity Flags:** {ambiguity_flags or "None"}

### Risk
**Description:** {risk or "None identified"}
**Severity:** {severity or "—"}
**Severity Basis:** {severity_basis or "—"}
**Severity Locked:** {severity_locked or "—"}

### Test Cases

#### {tc_id}
| Field     | Value |
|-----------|-------|
| Objective | {objective} |
| Type      | {type} |
| Surface   | {surface} |
| Priority  | {priority} |
| Note      | {human_note} |

---

## Review Decision

**Reviewer:**
**Date:**

| Item | Response |
|---|---|
| Plan Status | [ ] Accept [ ] Reject [ ] Request Updates |
| Severity Overrides | List any REQ-IDs where severity is being changed and new value |
| Ambiguities Resolved | List any ambiguity flags resolved, escalated, or accepted as-is |
| Requirements Rejected | List any REQ-IDs removed from scope with reason |
| Notes | |
```

---

## 4. Shared Field Contracts

| Field | Format | Scope |
|---|---|---|
| `req_id` | `REQ-###` | Intake Agent, Risk Agent, Review Agent |
| `tc_id` | `TC-###` | Risk Agent, Review Agent |
| `prd_ref` | Section or line reference | Intake Agent |
| `plan_context` | Top-level block | Intake Agent output only |
| `severity_locked` | Boolean, default `false` | Risk Agent — human-editable at review |
| `ambiguity_flags` | Array, never omitted | Intake Agent |
| `type` | Enum — see classification rules | Risk Agent |
| `surface` | Enum — see classification rules | Risk Agent |

---

## 5. Agent Handoff Contracts

| From | To | Payload |
|---|---|---|
| Intake Agent | Risk Agent | `requirements` array + `project_context` block |
| Intake Agent | Review Agent | Full output — `plan_context` + `requirements` array |
| Risk Agent | Review Agent | Full risk and test case array |

---

## 6. Human Review Gate

Humans receive the Review Agent Markdown document and are responsible for:

- Accepting, rejecting, or requesting updates to the full plan
- Confirming or overriding severity assignments and setting `severity_locked: true`
- Resolving ambiguity flags before sign-off
- Executing and validating all exploratory test cases personally
- Rejecting any requirement they consider out of scope or untestable

Agents do not auto-promote, auto-approve, or proceed without human action.

---

## 7. v1 Success Criteria

- PRD in → Markdown test plan out with no manual construction
- Every test case traces to a requirement and a PRD section
- All ambiguities surfaced and flagged — never silently resolved
- `type` and `surface` present on every generated test case
- Purpose, In Scope, and Out of Scope derived from parsed PRD content — not manually authored
- Exploratory cases appear only where risk or ambiguity exists
- Human reviewer can accept, reject, or request updates on the full plan

---

## 8. v1 Exclusions

The following are explicitly out of scope for v1:

- Orchestration or state machine logic
- Coverage auditing
- Artifact versioning
- Feedback loops or agent self-correction
- Function-calling or tool-use contracts
- CI/CD integration
- Retry or validation layers

---

## 9. Known Failure Modes

| Failure | Risk | Mitigation |
|---|---|---|
| Ambiguous PRD input | Malformed or untraceable requirements | Intake Agent flags ambiguity; human resolves before Risk Agent runs |
| Hallucinated scope boundaries | Inaccurate In Scope or Out of Scope sections | Prompt constrains derivation to parsed content only — no invention |
| Severity miscalibration | Wrong priority on test execution | `severity_basis` exposed for human review; `severity_locked` enforces confirmation |
| Classification outside allowed values | Schema violation | Prompt constraint enforced; Review Agent renders raw values — violations are visible |
| Requirement hallucination | False coverage | `prd_ref` required on every requirement |
| Exploratory overgeneration | Noise in test plan | Exploratory gated on risk or ambiguity flag only |
| Unstructured input has no section references | `prd_ref` defaults to document title on all requirements, reducing traceability | Flag in `ambiguity_flags`; human reviewer must manually trace requirements to source |

---

## 10. Phased Evolution

| Phase | Name | Status | Input | Output | Human Gate |
|-------|------|--------|-------|--------|------------|
| 1 | Test Plan Generation | Complete | PRD (Markdown) | Structured test plan (.md) | Required before Phase 3 |
| 2 | Test Data Generation | Planned | Accepted test plan | Test data specification (.md) | Required before Phase 3 |
| 3a | Cypress Script Agent | Planned | Test plan + test data | Cypress test scripts | Required before Phase 5 |
| 3b | Playwright Script Agent | Planned | Test plan + test data | Playwright test scripts | Required before Phase 5 |
| 3c | Postman Script Agent | Planned | Test plan + test data | Postman collection (.json) | Required before Phase 5 |
| 3d | k6 Script Agent | Planned | Test plan + test data | k6 performance scripts | Required before Phase 5 |
| 4 | Coverage Summary | Planned | All Phase 3 outputs | Summary report (.md) | Required before Phase 5 |
| 5a | PR Description Agent | Planned | Accepted artifacts | PR description (.md) | Team discretion |
| 5b | PR Review Agent | Planned | PR diff + test plan | Risk assessment (.md) | Team discretion |