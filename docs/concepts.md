# Core Concepts

## Checkpoints

A checkpoint is a snapshot of your work at a specific moment. Think of it as a save point.

- 12-character hex ID (e.g., `8a513f56ed70`)
- Created automatically when you or the agent commit
- Stores the full agent transcript alongside the code

## Sessions

A session is a continuous AI coding interaction. It begins when the agent starts and ends when you're done.

## Attribution

Entire tracks what percentage of changes were agent-written vs human-written, recorded as a Git trailer:

```
Entire-Attribution: 73% agent (146/200 lines)
```

See [Attribution](attribution.md) for a detailed breakdown of how this is calculated.

## CLI

See [CLI Commands](cli-commands.md) for a full reference.
