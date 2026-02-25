# Tool Audit via Entire Transcript

Observations from exploring how to audit AI agent tool usage using Entire's `full.jsonl` transcript.

## What the transcript contains

Each checkpoint has a `full.jsonl` on the shadow branch (`entire/checkpoints/v1`) containing every tool call made during the session. Each record has:
- `type: "assistant"` with `content` blocks of `type: "tool_use"`
- `name`: the tool (e.g. `Bash`, `Read`, `Write`, `mcp__kosli-docs__SearchKosliDocumentation`)
- `input`: the arguments passed to the tool

This gives a complete, ordered record of every action the agent took.

## What we built

A `parse_tool_audit.py` script and `entire-tool-audit` Kosli attestation type that:
1. Parses `full.jsonl` and counts calls per tool
2. Reads `.claude/settings.json` from the repo to get the deny rules
3. Checks each tool call against the deny rules and reports violations
4. Records `settings_hash` (SHA256 of `.claude/settings.json`) for integrity
5. Tracks `unsandboxed_bash_count` (Bash calls with `dangerouslyDisableSandbox: true`)

## The threat model this catches

The attack: a developer removes a deny rule from `.claude/settings.json` before starting a Claude Code session, giving the agent broader permissions. They then revert `settings.json` before committing — so the repo looks clean, but the transcript records what the agent actually did.

CI catches it by:
1. Checking out the repo (which has the deny rule)
2. Fetching the checkpoint transcript from the shadow branch
3. Finding tool calls in the transcript that match the deny rules
4. Posting a NON-COMPLIANT attestation

## What deny rules can and cannot be overridden

- `settings.local.json` allows you to ADD to the allow list, but **cannot override deny rules** from `settings.json`
- The only way to bypass a deny rule is to remove it from `settings.json` directly before session start
- Mid-session changes to `settings.json` have no effect — settings are loaded once at session start

## Important limitation: checkpoint persistence timing

Entire only fully persists checkpoint data to the shadow branch for **the first commit of a session**. Subsequent commits in the same session don't have their checkpoint data written to the shadow branch until the session ends (or possibly never within an active Claude Code session).

This means:
- The end-to-end tool audit only works reliably for the **first commit of a fresh session**
- Commits made mid-session (like the commits in this exploration) will have `Entire-Checkpoint` trailers in git but no corresponding data on the shadow branch
- CI will log "Checkpoint metadata not found on shadow branch — skipping" for these commits

The right demo scenario is always a fresh session where the deny rule is in the committed `settings.json` before the session starts.

## jq rule

The attestation type `entire-tool-audit` uses `.violations_count == 0` as its compliance rule. Any deny-rule violation in the transcript produces a NON-COMPLIANT trail in Kosli.
