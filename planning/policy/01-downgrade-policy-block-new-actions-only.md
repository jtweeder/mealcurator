# Downgrade Policy: Block New Actions Only

## Policy
- On downgrade, do not delete user content automatically.
- If user is above new tier limits:
  - allow read/list/open existing items
  - allow delete/archive/select what to keep
  - block creation of new over-limit actions

## UX
- Show clear notice: over limit after downgrade.
- Provide direct links to cleanup screens.
- Resume create actions automatically after user is within limit.
