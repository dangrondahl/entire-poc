# CLI Commands

## `entire status`

Show current Entire state for the repo.

```bash
entire status
# ● Enabled · manual-commit · branch main
```

## `entire doctor`

Scan for stuck or problematic sessions and offer to fix them.

A session is considered stuck if:
- It is in `ACTIVE` or `ACTIVE_COMMITTED` phase with no interaction for over 1 hour
- It is in `ENDED` phase with uncondensed checkpoint data on a shadow branch

```bash
entire doctor
entire doctor --force  # fix all without prompting
```

## `entire hooks`

Manage Git hooks installed by Entire.

```bash
entire hooks opencode turn-end  # manually run a hook
```
