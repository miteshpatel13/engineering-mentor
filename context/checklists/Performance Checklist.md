# Performance Checklist

- [ ] Performance target defined
- [ ] Current behavior measured where relevant
- [ ] Database queries reviewed
- [ ] N+1 risk checked
- [ ] Index usage checked
- [ ] External calls reviewed
- [ ] Every external call has a timeout and runs without holding a DB connection or transaction
- [ ] Concurrent fan-out is bounded below the connection-pool size
- [ ] Connection-pool total across instances (incl. deploy surge) fits the DB connection limit
- [ ] Payload size considered
- [ ] Concurrency considered
- [ ] Caching considered only when justified
- [ ] Post-change measurement planned
