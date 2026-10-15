---
id: security-review-21-rule-coverage-socket-payload-tenant-and-revocation-cache
category: rule-coverage
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Realtime Handler Trusts the Payload's Company, and Revocation Waits for a TTL

## Input Material

> A multi-tenant app authenticates socket connections with a JWT in the handshake and stores `socket.data.companyId`. The `deleteNotification` event handler runs `UPDATE notification SET isDelete = 1 WHERE id IN (:...ids)` with `ids` from the payload. The `messageList` handler loads messages for `payload.roomId` and `payload.companyId`. Separately, removing a sales person from a company deletes their membership row; the auth guard caches "is this user active in this company" in Redis for 10 minutes and nothing deletes that key on removal. A batch endpoint `POST /products/toggle` updates `WHERE productId IN (:...ids)` and, after a recent fix, filters to the caller's company but silently updates only the owned subset when some IDs are foreign.

## Pass Criteria

- Flags the socket handlers under Rules → Tenant Scoping of Client-Supplied Identifiers: no tenant predicate on the delete, and the company taken from the payload instead of `socket.data`.
- Flags the batch toggle for acting on the owned subset instead of rejecting the request when any ID is foreign.
- Flags the removal under Rules → Revocation and Cached Authorization: access continues for up to the TTL.
- Recommends an inventory sweep of request-supplied IDs rather than three point fixes, and does not recommend a global role guard as the fix.

## Fail Signals

- Treating the authenticated handshake as sufficient authorization for the payload IDs.
- Accepting TTL expiry as an adequate revocation mechanism.
