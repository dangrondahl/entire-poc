# Open Questions

## Attribution Edge Cases

- What if the agent and human both modify the same line?
- How does attribution handle file renames or moves?
- Does whitespace-only edits count toward human attribution?

## Session Lifecycle

- What triggers a session to end automatically?
- Can multiple agents contribute to the same session?
- How are nested sessions (sub-agents) attributed?

## Search & Retrieval

- Can the MCP server search across checkpoint transcripts, not just docs?
- Is search semantic (vector) or keyword-based?
