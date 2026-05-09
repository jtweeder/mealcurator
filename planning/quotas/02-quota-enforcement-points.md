# Quota Enforcement Points

## Free tier meal plan cap
- Enforce before create/update actions that increase active plans.
- Target existing plan creation/edit flows in `cooks/views.py`.

## AI monthly limit
- Enforce before OpenAI generation call in `stewpot/views.py`.
- Fail with user-friendly message and remaining/reset metadata.

## Requirements
- Enforce in server-side view/service layer.
- Keep checks atomic to avoid race overages.
