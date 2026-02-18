# Feature Discussion Notes — Discount Code Support
**Date:** February 14 2026
**Attendees:** Jordan (PM), Priya (Engineering), Matt (QA), Lisa (Design)
**Type:** Informal feature scoping call — notes not reviewed or approved

---

These are rough notes from the call. Jordan will clean them up into a proper PRD next week.

---

So basically we want customers to be able to type in a discount code during checkout and have it knock money off their order. Pretty standard stuff. The big question is where it lives in the flow — before or after they enter shipping? Priya thinks it should be before payment but after shipping because the discount might affect shipping cost too (we do free shipping over $50). Lisa said the design already has it on the cart page but that might need to change.

The discount engine — Priya confirmed this is an existing internal service, not new build. She said there's an endpoint for it already but it's not documented. She'll dig up the docs or write something up. The endpoint validates the code and returns a discount value. We don't know yet if it returns a percentage or a flat amount or both. Probably both.

Expired codes need to return a clear error message. Someone (can't remember who) mentioned we also need to handle codes that are valid but don't apply to the items in the cart — like a code only for shoes but someone's buying a hat. That scenario needs a user-facing message too.

Nobody wants to support stacking codes right now. Jordan said definitely not in v1. One code per order max.

What about the order total display? When the code is applied it should update in real time without a page reload. Priya said that's fine, it's just a recalculation on the frontend hitting the same endpoint.

Mobile — Lisa reminded everyone that the cart page has a separate mobile layout and the discount field needs to work there too. She'll flag it in the design file.

Edge case someone raised at the end: what if the discount code brings the order total to zero? Do we still run it through the payment flow? Probably not but nobody has a confirmed answer.

---

**Action Items (from Jordan's memory, not official)**
- Priya to find discount engine API docs
- Lisa to update cart design for code placement
- Jordan to write up proper PRD
- QA (Matt) flagged he needs the edge case rules before he can write test cases