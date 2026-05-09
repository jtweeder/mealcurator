# UTC Monthly Quota Spec

## Window
- Quota period is calendar month in UTC.
- Reset at `00:00:00 UTC` on first day of month.

## Counters
- Track usage per user, feature key, period start/end.
- Suggested feature key: `ai_recipe_generation`.

## Consumption
- Consume quota only after successful generation request is accepted.
- Use atomic increment with row lock/transaction.

## Edge cases
- Retry behavior: do not double-charge on duplicate requests.
- Late webhooks: entitlement change should not retroactively rewrite prior usage.
