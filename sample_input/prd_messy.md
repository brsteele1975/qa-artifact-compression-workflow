# Product Requirements – Checkout V2

## Overview
We need to redo the checkout flow. The current one is bad and customers complain a lot.
The new version should be faster and easier. Design is still TBD but engineering can start on the backend stuff.

---

## Goals
Make checkout better. Reduce drop-off. Support guest users. Maybe add express checkout later (not this sprint probably).

---

## 2.1 Email Confirmation
After someone buys something they should get an email. It should be fast. The email needs to have the order details in it.
We haven't decided exactly what "fast" means yet but probably under a minute. Someone from the product team said 30 seconds but that hasn't been confirmed.

---

## 2.2 Guest Checkout
Users should be able to checkout without making an account. This is important.
Note: we still want to encourage account creation but not force it. The UX team has a modal design for this but it's not finalized.

---

## Discounts
Customers can apply a discount code at checkout. It should update the total before they pay.
What happens if someone enters two codes is TBD. Also we need to handle expired codes but no one has written the rules for that yet.

---

## Order Confirmation Page
Show the order details after purchase. Should work on mobile. Design has a comp but it keeps changing.
The comp shows: item name, quantity, price, total, estimated delivery. But estimated delivery might get cut, not confirmed.

---

## stuff we are NOT doing
- Rebuilding the login flow
- Touching the payment gateway
- Any of the post order fulfilment stuff
- Admin tools

---

## Open Questions
- Who owns the email service integration?
- Do we need to support international addresses in v1?
- What's the timeout threshold for the session?
- Is the discount engine a new service or an existing one?
