---
description: An authenticated handler that trusts a client-supplied user_id and role, and logs the raw payload including passwords, must trigger security-review with blocking authorization findings.
tags: [smoke, review, security]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Security review please. This handler lets a logged-in user update a profile:

```python
@app.route("/api/profile", methods=["PUT"])
@login_required
def update_profile():
    data = request.get_json()
    user = User.query.get(data["user_id"])
    user.email = data["email"]
    user.role = data.get("role", user.role)
    db.session.commit()
    logger.info("profile updated: %s", data)
    return jsonify(ok=True)
```

Clients also send `password` in the same payload when changing it.
