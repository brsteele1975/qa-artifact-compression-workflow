# QA Test Plan
**Artifact ID:** aqab-v1-prd_messy  
**PRD Source:** prd_messy.md  
**Generated:** 2026-02-19  
**Status:** Pending Human Review

---

## Purpose
To validate the new checkout flow, ensuring it is faster, easier, and supports guest users while addressing key customer complaints.

---

## In Scope
- Email Confirmation
- Guest Checkout
- Discount Code Application
- Order Confirmation Page

---

## Out of Scope
- Rebuilding the login flow
- Touching the payment gateway
- Any of the post order fulfilment stuff
- Admin tools

---

## Requirements & Test Cases

---

## REQ-001 — After a purchase, an email confirmation with order details should be sent quickly.
**PRD Reference:** 2.1 Email Confirmation  
**Actors:** Customer  
**Testable:** true  
**Ambiguity Flags:** Definition of 'fast' is unclear, possibly under a minute or 30 seconds.

### Risk
**Description:** Email confirmation may be delayed, affecting customer satisfaction.  
**Severity:** high  
**Severity Basis:** Email confirmation is a known high severity area and critical for post-purchase communication.  
**Reasoning:** The requirement affects the Email Confirmation area, which is known to be high severity, and is critical for the primary user journey.  
**Severity Locked:** false

### Test Cases

#### TC-001
| Field | Value |
|---|---|
| Objective | Verify that email confirmation is sent within the expected time frame. |
| Type | integration |
| Surface | service |
| Priority | P1 |
| Note | Ensure to test with different email providers to check delivery speed. |

#### TC-002
| Field | Value |
|---|---|
| Objective | Explore the impact of delayed email confirmations on user experience. |
| Type | exploratory |
| Surface | workflow |
| Priority | P1 |
| Note | Investigate scenarios where email delivery is delayed beyond the expected time. |

---

## REQ-002 — Users should be able to checkout without creating an account.
**PRD Reference:** 2.2 Guest Checkout  
**Actors:** Guest User  
**Testable:** true  
**Ambiguity Flags:** UX design for encouraging account creation is not finalized.

### Risk
**Description:** Potential friction in guest checkout due to unclear UX design.  
**Severity:** high  
**Severity Basis:** Guest Checkout is a known high severity area and part of the primary user journey.  
**Reasoning:** The requirement is part of the Guest Checkout, a known high severity area, and directly affects the primary user journey.  
**Severity Locked:** false

### Test Cases

#### TC-003
| Field | Value |
|---|---|
| Objective | Verify that users can complete checkout without creating an account. |
| Type | e2e |
| Surface | ui |
| Priority | P1 |
| Note | Focus on the flow from adding items to cart to completing purchase as a guest. |

#### TC-004
| Field | Value |
|---|---|
| Objective | Explore the UX design for encouraging account creation during guest checkout. |
| Type | exploratory |
| Surface | workflow |
| Priority | P2 |
| Note | Evaluate different design approaches for account creation prompts. |

---

## REQ-003 — Customers can apply a discount code at checkout, updating the total before payment.
**PRD Reference:** Discounts  
**Actors:** Customer  
**Testable:** true  
**Ambiguity Flags:** Handling of multiple discount codes is TBD., Rules for expired codes are not defined.

### Risk
**Description:** Incorrect handling of discount codes could lead to revenue loss.  
**Severity:** medium  
**Severity Basis:** Discount code application is part of a revenue-critical path.  
**Reasoning:** The requirement is part of the revenue-critical path for discount code application, affecting the checkout flow.  
**Severity Locked:** false

### Test Cases

#### TC-005
| Field | Value |
|---|---|
| Objective | Verify that a single discount code can be applied and updates the total correctly. |
| Type | integration |
| Surface | api |
| Priority | P1 |
| Note | Test with valid, invalid, and expired codes. |

#### TC-006
| Field | Value |
|---|---|
| Objective | Explore the handling of multiple discount codes during checkout. |
| Type | exploratory |
| Surface | workflow |
| Priority | P2 |
| Note | Investigate how the system behaves with multiple codes applied. |

---

## REQ-004 — Show order details after purchase, compatible with mobile.
**PRD Reference:** Order Confirmation Page  
**Actors:** Customer  
**Testable:** true  
**Ambiguity Flags:** Design comp is changing., Inclusion of estimated delivery is not confirmed.

### Risk
**Description:** Order details may not display correctly on mobile, affecting user satisfaction.  
**Severity:** high  
**Severity Basis:** Order Confirmation Page is a known high severity area and critical for post-purchase communication.  
**Reasoning:** The requirement affects the Order Confirmation Page, a known high severity area, and is critical for the primary user journey.  
**Severity Locked:** false

### Test Cases

#### TC-007
| Field | Value |
|---|---|
| Objective | Verify that order details are displayed correctly on mobile devices. |
| Type | e2e |
| Surface | ui |
| Priority | P1 |
| Note | Test across different mobile devices and screen sizes. |

#### TC-008
| Field | Value |
|---|---|
| Objective | Explore the impact of design changes on the order confirmation page. |
| Type | exploratory |
| Surface | workflow |
| Priority | P2 |
| Note | Assess how design changes affect the display of order details. |

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