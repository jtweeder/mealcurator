# Schema and Migration Plan

## Proposed models
- `CustomerSubscription` (user, tier, stripe_customer_id, stripe_subscription_id, stripe_price_id, status, current_period_start/end)
- `UsageCounter` (user, feature_key, period_start, period_end, used, limit)
- `WebhookEvent` (provider, event_id unique, processed_at, payload_hash)

## Migration strategy
1. Add tables nullable/non-breaking.
2. Backfill all existing users to `free`.
3. Deploy webhook processing with enforcement off.
4. Enable enforcement after validation.

## Integrity
- Unique constraints on provider event id.
- Index `(user, feature_key, period_start)` for usage lookups.
