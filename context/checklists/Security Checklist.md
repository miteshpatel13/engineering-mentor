# Security Checklist

- [ ] Authentication reviewed
- [ ] Authorization reviewed
- [ ] Every client-supplied identifier (body, params, query, realtime/socket payload, job payload) is verified against the caller's tenant before use
- [ ] Revoking access invalidates cached authorization immediately
- [ ] Missing secrets/config fail closed at startup; secrets compared in constant time
- [ ] Input validation reviewed
- [ ] Injection risks reviewed
- [ ] Secrets protected
- [ ] Sensitive data exposure reviewed
- [ ] Logs reviewed for sensitive information
- [ ] File handling reviewed where applicable
- [ ] Dependency risk considered
- [ ] Abuse/rate limiting considered
