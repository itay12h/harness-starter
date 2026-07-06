# Architecture (reference module)

> Pulled in on demand — not loaded every message. Keep the day-to-day rules in
> `CLAUDE.md`; put the deeper "how it fits together" here so that file stays lean.

Replace this with your project's real map:

- **Entry points** — where a request or command starts.
- **Main modules** — what each is responsible for, with file paths.
- **Data** — the store, the schema, migrations.
- **External services** — APIs, queues, MCP servers.
- **Gotchas** — the non-obvious things that have bitten people (timezones,
  retries, auth edge cases). Each one is a rule you earned.
