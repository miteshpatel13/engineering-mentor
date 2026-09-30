#!/usr/bin/env bash
set -euo pipefail
mkdir -p accounts billing db/views tests
cat > accounts/models.py <<'EOF'
class User(Model):
    id = BigAutoField(primary_key=True)
    email = TextField(unique=True)
    name = TextField()
EOF
cat > accounts/serializers.py <<'EOF'
def serialize_user(user):
    return {"id": user.id, "email": user.email, "name": user.name}
EOF
cat > billing/invoice_pdf.py <<'EOF'
def render_header(invoice):
    return f"Bill to: {invoice.user.name} <{invoice.user.email}>"
EOF
cat > db/views/v_customers.sql <<'EOF'
CREATE VIEW reporting.v_customers AS
SELECT u.id, u.name AS customer_name, u.email FROM users u;
EOF
cat > tests/test_serializers.py <<'EOF'
def test_serialize_user(user):
    assert serialize_user(user)["name"] == user.name
EOF
