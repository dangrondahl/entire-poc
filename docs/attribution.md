# Attribution

Entire tracks how much of each commit came from the agent vs the human developer.

## How It Works

Attribution is calculated by tracking changes at two points:

1. **Before each agent run** — Entire captures what you changed since the last checkpoint
2. **At commit time** — Entire sums up all edits and compares agent vs human contributions

## Git Trailer

Attribution is stored as a Git commit trailer:

```
feat: Add user authentication

Entire-Checkpoint: a3b2c4d5e6f7
Entire-Attribution: 73% agent (146/200 lines)
```

## Interleaved Edits

A typical session looks like:

1. You write some code
2. Agent runs, adds more code → checkpoint created
3. You edit the agent's code and add your own
4. Agent runs again → another checkpoint
5. You make final tweaks
6. You commit

Entire untangles these interleaved contributions for an accurate breakdown.
