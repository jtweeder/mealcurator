# Planning Index

This folder stores implementation planning docs for tiered subscriptions.

## Scope
- Tiers: `free`, `mini-chef`, `super-chef`
- Billing provider: Stripe (hosted checkout)
- Usage reset: UTC monthly window
- Downgrade behavior: block **new** actions only; allow read/delete/selection

## Documents
- billing/01-product-tiers-and-entitlements.md
- billing/02-stripe-catalog-and-webhooks.md
- billing/03-subscription-state-machine.md
- quotas/01-utc-monthly-quota-spec.md
- quotas/02-quota-enforcement-points.md
- policy/01-downgrade-policy-block-new-actions-only.md
- data/01-schema-and-migration-plan.md
- tests/01-test-strategy-billing-and-quotas.md
- ops/01-rollout-observability-and-support.md

## Suggested implementation order
1. Product tiers + UTC quota rules
2. Downgrade policy
3. Stripe catalog + webhook contract
4. Subscription state machine
5. Schema + migrations
6. Enforcement points in app
7. Tests
8. Rollout + support runbook
