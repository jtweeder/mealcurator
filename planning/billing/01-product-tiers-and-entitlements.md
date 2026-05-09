# Product Tiers and Entitlements

## Tiers
- **free**
  - Meal plans: max 30 active
  - AI generation: no paid AI entitlement
- **mini-chef**
  - AI generation: enabled
  - Monthly AI limit: configurable (UTC month)
- **super-chef**
  - AI generation: enabled
  - Monthly AI limit: higher configurable amount (UTC month)
  - Weekly planning features: enabled

## Notes
- Limits must be enforced server-side only.
- UI can show limits, but UI is not authorization.
- Keep tier values in code constants + DB-backed entitlement records.
