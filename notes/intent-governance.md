# Intent Governance

Observations from exploring how to evaluate and govern AI-generated code changes using intent as a signal.

## What "intent" is in Entire

The `prompt.txt` in a checkpoint contains all user messages in the session, separated by `---` lines. The **last message** is the most relevant as intent — it's the direct trigger for the work that produced the commit. Earlier messages are session context.

`entire explain` surfaces the first message of the checkpoint scope as "Intent", not the last message and not the session start.

## Why intent is hard to use as a compliance gate

- **It's natural language** — quality is semantic, not syntactic. Character count is a poor proxy: `"Fix XSS in login"` is 18 chars and specific; a 90-char sentence can be meaningless.
- **It can be vague or misleading** — accidentally or deliberately. `"Clean up auth code"` could mean anything.
- **It's not the same as understanding** — a developer can write a well-formed prompt without understanding the implications of what the agent produces.
- **It can be gamed** — a detailed-sounding intent doesn't guarantee the change is safe.

## What intent is good for

Intent is valuable as an **audit artifact**, not a compliance gate. An auditor reviewing a high-autonomy change to a sensitive file months later can answer: *"Did the developer know what they were asking for?"* — but that judgment requires human cognition, not a jq rule.

## Quantitative proxies we considered

| Signal | What it measures | Gap |
|---|---|---|
| `agent_percentage` | How much the agent wrote | Doesn't capture whether human reviewed it |
| `human_modified` | Human directly edited agent output | Prompting for corrections also counts as review |
| `human_removed` | Human deleted agent code | Stronger review signal, but still physical action |
| `api_call_count` | Rounds of back-and-forth | High count ≠ understanding; could be cosmetic changes |
| `files_touched` sensitivity | Risk scope of the change | Pattern matching, not semantic |

All behavioral proxies measure **actions**, not **cognition**. None reliably answers *"did the human understand and approve what was committed?"*

## What would be a direct signal

An **explicit human attestation** — a deliberate approval step separate from file editing and prompting. Conceptually similar to a PR review approval: a human saying "I reviewed this" as a first-class event, not inferred from indirect signals.

## Conclusion

The right model for Entire + Kosli:

1. **Record everything as evidence** — intent, attribution, files, token usage, transcript attachment. Structured, queryable, tamper-evident.
2. **No automated pass/fail on intent or behavioral proxies** — these signals are too ambiguous for reliable automated governance.
3. **Reserve compliance gates for objective facts** — e.g. a PR review attestation exists, a specific approver signed off.
4. **Use the audit trail for human review** — when a high-autonomy change to a sensitive area needs scrutiny, the Kosli evidence vault provides the full context.
