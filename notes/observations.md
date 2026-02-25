# Observations

## Session 1 — Initial Setup

- Entire hooks install cleanly into `.git/hooks`
- `entire status` correctly shows enabled state
- MCP server responds to search queries

## Session 2 — Testing Commit Trailers

- Testing whether `Entire-Checkpoint` trailer is added to commits in `manual-commit` mode
- Strategy: make a small change, commit, inspect the commit message for trailers
- Confirmed: trailer is added automatically via git hooks

## Session 3 — Testing Auto-Summarize

- Enabled `strategy_options.summarize.enabled` in `.entire/settings.json`
- Auto-summarize silently fails when committing inside a Claude Code session — Entire cannot spawn a nested `claude` CLI process
- No error is surfaced at commit time; `Outcome` just shows `(not generated)`
- Workaround: run `entire explain --checkpoint <id> --generate` with `CLAUDECODE` unset: `env -u CLAUDECODE entire explain --checkpoint <id> --generate`
- Auto-summarize should work normally when committing from a terminal outside of Claude Code
- `entire explain` `Outcome` field includes: Intent, Outcome, Learnings (Repository/Code/Workflow), Friction, and Open Items

## Questions to Explore

- How does attribution work with back-and-forth edits?
- What happens if a session is interrupted mid-commit?
- Can we search across historical checkpoints?
- Does auto-summarize work correctly when committing outside of a Claude Code session?
- Could Entire surface a warning when `claude` CLI cannot be spawned at commit time?
