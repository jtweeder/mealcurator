# Stripe Catalog and Webhooks

## Stripe Catalog
- Create one Product with recurring Prices or multiple Products:
  - `mini-chef-monthly`
  - `super-chef-monthly`
- Keep a strict server-side `price_id -> tier` allowlist.

## Checkout/Portal
- Use hosted checkout session creation from server.
- Use Stripe billing portal for self-service subscription management.
- Never store card PAN/CVC in app.

## Webhooks to consume
- `checkout.session.completed`
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.paid`
- `invoice.payment_failed`

## Security
- Verify `Stripe-Signature` on every webhook.
- Store processed `event.id` for idempotency.
- Process webhooks in DB transaction; safe retry on failure.
