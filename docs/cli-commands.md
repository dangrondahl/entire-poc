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

## `entire explain`

Explain a session, commit, or checkpoint. Shows metadata, intent, outcome, and transcript.

```bash
entire explain --commit abc1234
entire explain --checkpoint a3b2c4d5e6f7
entire explain --full  # include full transcript
entire explain -s      # summary only
```

### Generating AI Summaries

Use `--generate` to produce an AI-written outcome summary. **This flag only works with `--checkpoint`, not `--commit`** — grab the checkpoint hash from the `Entire-Checkpoint` git trailer first.

```bash
# Get the checkpoint hash from the commit trailer
git show --format="%B" abc1234 | grep Entire-Checkpoint
# Entire-Checkpoint: a3b2c4d5e6f7

entire explain --checkpoint a3b2c4d5e6f7 --generate
entire explain --checkpoint a3b2c4d5e6f7 --generate --force  # regenerate existing summary
```

### Inside a Claude Code Session

Auto-summarize and `--generate` both fail silently when run inside an active Claude Code session — Entire cannot spawn a nested `claude` CLI process. The `Outcome` field will show `(not generated)` with no error.

**Workaround:** unset `CLAUDECODE` to bypass the nested session check:

```bash
env -u CLAUDECODE entire explain --checkpoint a3b2c4d5e6f7 --generate
```

Auto-summarize works normally when committing from a terminal where `CLAUDECODE` is not set.

## `entire hooks`

Manage Git hooks installed by Entire.

```bash
entire hooks opencode turn-end  # manually run a hook
```
