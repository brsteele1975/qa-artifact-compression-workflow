# QA Test Plan
**Artifact ID:** aqab-v1-raw_prd_notes  
**PRD Source:** raw_prd_notes.md  
**Generated:** 2026-02-19  
**Status:** Pending Human Review

---

## Purpose
This test plan validates the integration and functionality of discount code support during the checkout process.

---

## In Scope
- Discount code entry and validation
- Error messaging for invalid or inapplicable codes
- Real-time order total updates
- Mobile layout support for discount code entry

---

## Out of Scope
- Stacking multiple discount codes
- Confirmed handling of zero total orders

---

## Requirements & Test Cases

---

## REQ-001 — Customers can enter a discount code during checkout to receive a discount on their order.
**PRD Reference:** Feature Discussion Notes — Discount Code Support  
**Actors:** Customer  
**Testable:** true  
**Ambiguity Flags:** None

### Risk
**Description:** Failure to apply discount code could prevent customers from receiving expected discounts.  
**Severity:** high  
**Severity Basis:** This requirement is part of the primary user journey and revenue critical path.  
**Reasoning:** The requirement directly affects the primary user journey and is part of the revenue critical path, making it high severity.  
**Severity Locked:** false

### Test Cases

#### TC-001
| Field | Value |
|---|---|
| Objective | Verify that a discount code can be entered and applied during checkout. |
| Type | e2e |
| Surface | ui |
| Priority | P1 |
| Note | Ensure the discount is reflected in the order total. |

---

## REQ-002 — The discount code should be applied before payment but after shipping.
**PRD Reference:** Feature Discussion Notes — Discount Code Support  
**Actors:** Customer  
**Testable:** true  
**Ambiguity Flags:** Uncertainty about final placement in the checkout flow

### Risk
**Description:** Incorrect placement of discount code application could disrupt the checkout flow.  
**Severity:** medium  
**Severity Basis:** The requirement is part of the revenue critical path but has a workaround.  
**Reasoning:** The ambiguity about placement affects the revenue critical path, but the issue is not blocking if a workaround exists.  
**Severity Locked:** false

### Test Cases

#### TC-002
| Field | Value |
|---|---|
| Objective | Verify the discount code is applied after shipping but before payment. |
| Type | e2e |
| Surface | workflow |
| Priority | P2 |
| Note | Check the sequence of operations in the checkout flow. |

#### TC-003
| Field | Value |
|---|---|
| Objective | Explore potential issues with discount code placement in the checkout flow. |
| Type | exploratory |
| Surface | workflow |
| Priority | P2 |
| Note | Investigate any disruptions caused by the discount code placement. |

---

## REQ-003 — The discount engine validates the code and returns a discount value.
**PRD Reference:** Feature Discussion Notes — Discount Code Support  
**Actors:** System  
**Testable:** true  
**Ambiguity Flags:** Unclear if the discount value is a percentage, flat amount, or both

### Risk
**Description:** Ambiguity in discount value type could lead to incorrect discount calculations.  
**Severity:** medium  
**Severity Basis:** The ambiguity could affect the discount application, impacting the revenue critical path.  
**Reasoning:** The requirement's ambiguity affects the revenue critical path, but the issue is not blocking if a workaround exists.  
**Severity Locked:** false

### Test Cases

#### TC-004
| Field | Value |
|---|---|
| Objective | Verify the discount engine correctly validates codes and returns the correct discount value. |
| Type | integration |
| Surface | service |
| Priority | P2 |
| Note | Test both percentage and flat amount discount scenarios. |

#### TC-005
| Field | Value |
|---|---|
| Objective | Explore the handling of different discount value types by the discount engine. |
| Type | exploratory |
| Surface | service |
| Priority | P2 |
| Note | Investigate how the system handles different discount value types. |

---

## REQ-004 — Expired codes return a clear error message.
**PRD Reference:** Feature Discussion Notes — Discount Code Support  
**Actors:** Customer  
**Testable:** true  
**Ambiguity Flags:** None

### Risk
**Description:** Failure to return a clear error message for expired codes could confuse customers.  
**Severity:** high  
**Severity Basis:** Error messaging for invalid codes is a known high severity area.  
**Reasoning:** The requirement is in a known high severity area, affecting user experience and potentially the primary user journey.  
**Severity Locked:** false

### Test Cases

#### TC-006
| Field | Value |
|---|---|
| Objective | Verify that expired codes return a clear error message. |
| Type | unit |
| Surface | api |
| Priority | P1 |
| Note | Ensure the error message is user-friendly and informative. |

---

## REQ-005 — Codes that do not apply to items in the cart return a user-facing message.
**PRD Reference:** Feature Discussion Notes — Discount Code Support  
**Actors:** Customer  
**Testable:** true  
**Ambiguity Flags:** None

### Risk
**Description:** Failure to return a message for non-applicable codes could lead to user confusion.  
**Severity:** medium  
**Severity Basis:** The requirement affects user experience but does not block the primary user journey.  
**Reasoning:** The requirement impacts user experience but is not part of the primary user journey or a known high severity area.  
**Severity Locked:** false

### Test Cases

#### TC-007
| Field | Value |
|---|---|
| Objective | Verify that codes not applicable to cart items return a user-facing message. |
| Type | unit |
| Surface | api |
| Priority | P2 |
| Note | Check the clarity and helpfulness of the message. |

---

## REQ-006 — Only one discount code can be applied per order.
**PRD Reference:** Feature Discussion Notes — Discount Code Support  
**Actors:** Customer  
**Testable:** true  
**Ambiguity Flags:** None

### Risk
**Description:** Allowing multiple discount codes could lead to incorrect discount calculations.  
**Severity:** medium  
**Severity Basis:** The requirement affects discount application but is not part of the primary user journey.  
**Reasoning:** The requirement impacts discount calculations but is not in a known high severity area or the primary user journey.  
**Severity Locked:** false

### Test Cases

#### TC-008
| Field | Value |
|---|---|
| Objective | Verify that only one discount code can be applied per order. |
| Type | unit |
| Surface | api |
| Priority | P2 |
| Note | Test scenarios with multiple codes to ensure only one is applied. |

---

## REQ-007 — Order total updates in real time when a discount code is applied, without a page reload.
**PRD Reference:** Feature Discussion Notes — Discount Code Support  
**Actors:** Customer  
**Testable:** true  
**Ambiguity Flags:** None

### Risk
**Description:** Failure to update order total in real time could lead to incorrect user expectations.  
**Severity:** high  
**Severity Basis:** Real-time order total updates are a known high severity area.  
**Reasoning:** The requirement is in a known high severity area, affecting user experience and potentially the primary user journey.  
**Severity Locked:** false

### Test Cases

#### TC-009
| Field | Value |
|---|---|
| Objective | Verify that the order total updates in real time when a discount code is applied. |
| Type | integration |
| Surface | ui |
| Priority | P1 |
| Note | Ensure no page reload is required for the update. |

---

## REQ-008 — The discount field must work on the mobile layout of the cart page.
**PRD Reference:** Feature Discussion Notes — Discount Code Support  
**Actors:** Customer  
**Testable:** true  
**Ambiguity Flags:** None

### Risk
**Description:** Failure of the discount field on mobile could hinder mobile user experience.  
**Severity:** medium  
**Severity Basis:** The requirement affects mobile user experience but is not part of the primary user journey.  
**Reasoning:** The requirement impacts mobile user experience but is not in a known high severity area or the primary user journey.  
**Severity Locked:** false

### Test Cases

#### TC-010
| Field | Value |
|---|---|
| Objective | Verify that the discount field functions correctly on the mobile layout. |
| Type | e2e |
| Surface | ui |
| Priority | P2 |
| Note | Test on various mobile devices and screen sizes. |

---

## REQ-009 — Handling of orders with a total of zero after applying a discount code is not confirmed.
**PRD Reference:** Feature Discussion Notes — Discount Code Support  
**Actors:** System  
**Testable:** false  
**Ambiguity Flags:** Uncertainty about whether to run zero total orders through the payment flow

### Risk
**Description:** Uncertainty about handling zero total orders could lead to incorrect order processing.  
**Severity:** medium  
**Severity Basis:** The ambiguity could affect order processing, impacting the revenue critical path.  
**Reasoning:** The requirement's ambiguity affects the revenue critical path, but the issue is not blocking if a workaround exists.  
**Severity Locked:** false

### Test Cases

#### TC-011
| Field | Value |
|---|---|
| Objective | Explore the handling of orders with a total of zero after applying a discount code. |
| Type | exploratory |
| Surface | workflow |
| Priority | P2 |
| Note | Investigate how zero total orders are processed in the system. |

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