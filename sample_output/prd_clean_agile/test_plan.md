# QA Test Plan
**Artifact ID:** aqab-v1-prd_clean_agile  
**PRD Source:** prd_clean_agile.md  
**Generated:** 2026-02-19  
**Status:** Pending Human Review

---

## Purpose
Validate the guest checkout flow to ensure users can complete purchases without creating an account, reducing cart abandonment.

---

## In Scope
- Guest checkout initiation
- Email capture for guest users
- Order confirmation email delivery
- Session integrity across checkout steps
- Optional account creation prompt post-purchase

---

## Out of Scope
- Account creation flow
- Social login or SSO
- Saved payment methods for guest users
- Post-purchase account upgrade prompt

---

## Requirements & Test Cases

---

## REQ-001 — A user who is not logged in must be able to initiate checkout from the cart page without being redirected to the login or account creation page.
**PRD Reference:** 4.1  
**Actors:** Guest User  
**Testable:** true  
**Ambiguity Flags:** None

### Risk
**Description:** Guest users may be incorrectly redirected to login or account creation, blocking checkout.  
**Severity:** high  
**Severity Basis:** This requirement affects the primary user journey and revenue-critical guest checkout flow.  
**Reasoning:** The requirement is part of the primary user journey and revenue-critical path, making any redirection issues high severity.  
**Severity Locked:** false

### Test Cases

#### TC-001
| Field | Value |
|---|---|
| Objective | Verify that guest users can initiate checkout without redirection to login or account creation. |
| Type | e2e |
| Surface | ui |
| Priority | P1 |
| Note | Ensure the user remains on the checkout path without any login prompts. |

---

## REQ-002 — The guest checkout flow must collect the user's email address before the payment step. Email is required for order confirmation delivery.
**PRD Reference:** 4.2  
**Actors:** Guest User  
**Testable:** true  
**Ambiguity Flags:** None

### Risk
**Description:** Failure to collect email could prevent order confirmation delivery.  
**Severity:** high  
**Severity Basis:** Email capture is critical for order confirmation, part of the revenue-critical path.  
**Reasoning:** The requirement is part of the revenue-critical path for email capture and confirmation.  
**Severity Locked:** false

### Test Cases

#### TC-002
| Field | Value |
|---|---|
| Objective | Ensure the guest checkout flow collects the user's email before the payment step. |
| Type | e2e |
| Surface | workflow |
| Priority | P1 |
| Note | Check that the email field is mandatory and correctly positioned in the flow. |

---

## REQ-003 — Upon successful payment, the system must send an order confirmation email to the captured guest email address within 60 seconds. The email must include order ID, itemised receipt, and estimated delivery date.
**PRD Reference:** 4.3  
**Actors:** System  
**Testable:** true  
**Ambiguity Flags:** None

### Risk
**Description:** Order confirmation email may not be sent or may lack required details.  
**Severity:** high  
**Severity Basis:** Order confirmation email delivery is a known high severity area.  
**Reasoning:** The requirement touches a known high severity area of order confirmation email delivery.  
**Severity Locked:** false

### Test Cases

#### TC-003
| Field | Value |
|---|---|
| Objective | Verify the system sends an order confirmation email with all required details within 60 seconds. |
| Type | integration |
| Surface | service |
| Priority | P1 |
| Note | Check email content for order ID, itemised receipt, and estimated delivery date. |

---

## REQ-004 — The guest session must persist across all checkout steps — cart, shipping, payment, and confirmation — without requiring authentication. If the session expires mid-checkout, the user must receive a recoverable error and not lose their cart.
**PRD Reference:** 4.4  
**Actors:** Guest User  
**Testable:** true  
**Ambiguity Flags:** None

### Risk
**Description:** Session expiration could cause loss of cart contents during checkout.  
**Severity:** high  
**Severity Basis:** Session integrity across checkout steps is a known high severity area.  
**Reasoning:** The requirement affects session integrity, a known high severity area, and is part of the primary user journey.  
**Severity Locked:** false

### Test Cases

#### TC-004
| Field | Value |
|---|---|
| Objective | Ensure guest session persists across all checkout steps without requiring authentication. |
| Type | e2e |
| Surface | workflow |
| Priority | P1 |
| Note | Simulate session expiration and verify cart recovery process. |

---

## REQ-005 — After order confirmation is displayed, the system may present a single optional prompt inviting the guest user to create an account. This prompt must be dismissible and must not block access to the confirmation page.
**PRD Reference:** 4.5  
**Actors:** Guest User  
**Testable:** true  
**Ambiguity Flags:** None

### Risk
**Description:** Optional prompt may block access to the confirmation page.  
**Severity:** medium  
**Severity Basis:** The prompt is not part of the critical path but could degrade UX if not dismissible.  
**Reasoning:** The requirement affects UX but does not block the primary user journey or revenue-critical path.  
**Severity Locked:** false

### Test Cases

#### TC-005
| Field | Value |
|---|---|
| Objective | Verify the optional prompt is dismissible and does not block access to the confirmation page. |
| Type | exploratory |
| Surface | ui |
| Priority | P2 |
| Note | Ensure the prompt can be easily dismissed and does not interfere with user flow. |

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