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

## Session 4 — Kosli Attestation of Entire Checkpoints

- Entire's shadow branch (`entire/checkpoints/v1`) is pushed to GitHub, making checkpoint data available in CI
- Checkpoint metadata at `<cp[:2]>/<cp[2:]>/0/metadata.json` contains: session_id, agent, files_touched, token_usage, initial_attribution
- `prompt.txt` contains all session messages separated by `---`; last message = direct trigger for the commit
- Created custom Kosli attestation type `entire-attribution` with JSON schema and jq governance rule
- Governance rule (v3): NON-COMPLIANT when `agent_percentage > 90` AND `human_modified == 0` AND sensitive file touched
- Intent is recorded as audit data but not used in compliance evaluation — intent quality is hard to measure quantitatively
- `--build-url` is not a valid flag for `kosli attest custom`; use `--origin-url` instead

## Questions to Explore

- How does attribution work with back-and-forth edits?
- What happens if a session is interrupted mid-commit?
- Can we search across historical checkpoints?
- Does auto-summarize work correctly when committing outside of a Claude Code session?
- Could Entire surface a warning when `claude` CLI cannot be spawned at commit time?
