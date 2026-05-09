# Rollout, Observability, and Support

## Rollout phases
1. Schema + backfill
2. Webhooks on, enforcement off (observe-only)
3. Small cohort enforcement
4. Full rollout

## Observability
- Metrics: checkout success, webhook failures, quota blocks, entitlement mismatches
- Alerts: repeated webhook failure, processing lag, high block rate spikes

## Support runbook
- Replay webhook safely via idempotency keys
- Manual entitlement reconcile from Stripe to local records
- Customer-facing downgrade and quota guidance scripts
