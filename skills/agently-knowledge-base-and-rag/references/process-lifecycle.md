# Process Lifecycle

Use this page when the issue is real-world reuse rather than one demo query.

## 1. Build Once, Reuse Many Times

If the corpus is stable, initialize the knowledge base once per process and reuse it across turns or requests.

This is the common pattern for:

- API services
- auto-loop agents
- long-lived workers

## 2. Avoid Rebuilding On Every Turn

Rebuilding the collection inside each request path is usually the wrong default for production-style services.

Prefer:

- one long-lived collection object
- one stable embedding agent
- request-time query only

## 3. Persistence Boundary

If long-lived storage or shared deployment behavior matters, pass the collection the right Chroma client or configuration explicitly instead of relying on a throwaway in-process default.
