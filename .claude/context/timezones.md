# Timezones (reference module)

> A classic source of silent bugs. Kept here because it bit someone — the exact
> kind of "earned" rule that belongs in a reference module, not in your head.

- **Store** every timestamp in UTC.
- **Convert** to the user's zone only at the edges (display and input).
- **Never** rely on the server's local time.
- **Test** around DST boundaries and midnight — that's where it breaks.
