# Test Strategy: Billing and Quotas

## Unit tests
- Tier entitlement resolution
- UTC month window calculation
- Quota consume/idempotency helpers

## Integration tests
- Webhook signature validation
- Webhook idempotent processing
- Checkout -> entitlement activation flow

## Behavior tests
- Free plan cap at 30 active plans
- Mini/Super AI monthly limits
- Downgrade over-limit: block new only; allow delete/read
