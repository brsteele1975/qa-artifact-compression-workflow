# PRD — Guest Checkout Flow
**Sprint:** 24
**Author:** Product — Sarah Lin
**Status:** Ready for Engineering
**Scope:** Single feature — guest checkout path only

---

## 1. Problem Statement

Returning users can check out in under 2 minutes. Guest users currently cannot proceed without creating an account, resulting in a 34% cart abandonment rate at the account creation gate.

---

## 2. Goal

Allow users to complete a purchase without creating an account. Reduce abandonment at the account gate by 50% within 30 days of release.

---

## 3. Out of Scope

- Account creation flow
- Social login or SSO
- Saved payment methods for guest users
- Post-purchase account upgrade prompt (deferred to v2)

---

## 4. Requirements

### 4.1 Guest Checkout Entry
A user who is not logged in must be able to initiate checkout from the cart page without being redirected to the login or account creation page.

### 4.2 Email Capture
The guest checkout flow must collect the user's email address before the payment step. Email is required for order confirmation delivery.

### 4.3 Order Confirmation Email
Upon successful payment, the system must send an order confirmation email to the captured guest email address within 60 seconds. The email must include order ID, itemised receipt, and estimated delivery date.

### 4.4 Session Integrity
The guest session must persist across all checkout steps — cart, shipping, payment, and confirmation — without requiring authentication. If the session expires mid-checkout, the user must receive a recoverable error and not lose their cart.

### 4.5 Account Creation Prompt
After order confirmation is displayed, the system may present a single optional prompt inviting the guest user to create an account. This prompt must be dismissible and must not block access to the confirmation page.

---

## 5. Acceptance Criteria

- Guest user completes checkout without login prompt appearing at any step
- Email is captured before payment and validated as correctly formatted
- Confirmation email arrives within 60 seconds of payment success
- Session survives navigation across all four checkout steps
- Account creation prompt appears after confirmation and is fully dismissible

---

## 6. Dependencies

- Email Service: must support transactional send within SLA
- Cart Service: must support unauthenticated session tokens
- Payment Service: no changes required

---

## 7. Open Questions

None at time of writing. All acceptance criteria signed off by engineering lead and QA lead.