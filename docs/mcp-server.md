# Entire MCP Server

Entire ships with an MCP (Model Context Protocol) server that exposes the knowledge base to your AI agent.

## What It Provides

- `SearchEntire` tool — semantic search across Entire documentation
- Returns titles, links, and relevant content snippets

## Usage in Claude Code

The MCP server is automatically available when Entire is enabled. Example query:

```
SearchEntire("how do checkpoints work")
```

## Example Results

Searches return structured results with:
- `Title` — document section heading
- `Link` — direct URL to the docs page
- `Content` — relevant excerpt
