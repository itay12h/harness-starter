# Auth (reference module)

> Pulled in on demand — how authentication and authorization work here. Replace
> with your project's real details.

- **Scheme** — sessions / JWT / OAuth? Where the token lives and how it's signed.
- **Who can do what** — the roles, and the exact checks that enforce them.
- **The edges** — token expiry, refresh, logout, password reset.
- **Never** — log tokens, commit secrets, or trust a client-supplied user id.
  (The `security_guard` hook already blocks `.env` access; this is the rest.)
