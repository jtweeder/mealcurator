# Subscription State Machine

## Local states
- `free`
- `mini-chef_active`
- `super-chef_active`
- `past_due`
- `canceled`

## Transition examples
- Free -> Mini/Super on successful checkout + active subscription event.
- Active -> Past Due on payment failure event.
- Active/Past Due -> Canceled on delete/cancel event.
- Canceled -> Free entitlement at period end (or immediately per policy).

## Rules
- Stripe webhook events are source of truth for subscription status.
- Client redirects are not trusted for final entitlement updates.
- Keep `current_period_start/end` stored in UTC.
