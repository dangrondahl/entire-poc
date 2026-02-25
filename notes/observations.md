# Observations

## Session 1 — Initial Setup

- Entire hooks install cleanly into `.git/hooks`
- `entire status` correctly shows enabled state
- MCP server responds to search queries

## Session 2 — Testing Commit Trailers

- Testing whether `Entire-Checkpoint` trailer is added to commits in `manual-commit` mode
- Strategy: make a small change, commit, inspect the commit message for trailers

## Questions to Explore

- How does attribution work with back-and-forth edits?
- What happens if a session is interrupted mid-commit?
- Can we search across historical checkpoints?
