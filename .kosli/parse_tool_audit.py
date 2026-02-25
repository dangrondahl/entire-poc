#!/usr/bin/env python3
"""
Parse an Entire full.jsonl transcript and produce a tool audit attestation JSON.

Usage:
    python3 parse_tool_audit.py <full.jsonl> <settings.json> <checkpoint> <commit> <output.json>
"""

import json, re, sys, hashlib
from collections import Counter
from fnmatch import fnmatch


def parse_deny_rules(settings_path):
    """
    Parse deny rules from .claude/settings.json.
    Rule format: "ToolName(glob_pattern)" e.g. "Read(./.entire/metadata/**)"
    Returns list of {"tool": str, "pattern": str}
    """
    try:
        with open(settings_path) as f:
            settings = json.load(f)
        rules = []
        for rule in settings.get("permissions", {}).get("deny", []):
            m = re.match(r'^(\w+)\((.+)\)$', rule.strip())
            if m:
                rules.append({"tool": m.group(1), "pattern": m.group(2), "raw": rule})
        return rules
    except Exception:
        return []


def glob_match(pattern, path):
    """Match a path against a glob pattern, normalising ./ prefix."""
    pattern = pattern.lstrip("./")
    path = path.lstrip("./")
    return fnmatch(path, pattern) or fnmatch(path, pattern.replace("**", "*"))


def parse_transcript(jsonl_path, deny_rules):
    tool_calls = []
    violations = []
    unsandboxed = []

    with open(jsonl_path) as f:
        for line in f:
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("type") != "assistant":
                continue
            for block in rec.get("message", {}).get("content", []):
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                tool = block.get("name", "")
                inp  = block.get("input", {})
                tool_calls.append(tool)

                # Check deny rules
                for rule in deny_rules:
                    if tool == rule["tool"]:
                        path = inp.get("file_path", inp.get("path", ""))
                        if path and glob_match(rule["pattern"], path):
                            violations.append({
                                "rule": rule["raw"],
                                "tool": tool,
                                "path": path,
                            })

                # Flag unsandboxed Bash
                if tool == "Bash" and inp.get("dangerouslyDisableSandbox"):
                    unsandboxed.append(inp.get("command", "")[:120])

    return tool_calls, violations, unsandboxed


def main():
    jsonl_path, settings_path, checkpoint, commit, output_path = sys.argv[1:6]

    # Hash the settings file
    try:
        content = open(settings_path, "rb").read()
        settings_hash = "sha256:" + hashlib.sha256(content).hexdigest()
    except Exception:
        settings_hash = None

    deny_rules = parse_deny_rules(settings_path)
    tool_calls, violations, unsandboxed = parse_transcript(jsonl_path, deny_rules)

    counts = Counter(tool_calls)
    attestation = {
        "checkpoint": checkpoint,
        "commit": commit,
        "settings_hash": settings_hash,
        "deny_rules_evaluated": [r["raw"] for r in deny_rules],
        "tool_usage": dict(counts.most_common()),
        "tools_used": list(counts.keys()),
        "total_tool_calls": len(tool_calls),
        "unsandboxed_bash_count": len(unsandboxed),
        "deny_rule_violations": violations,
        "violations_count": len(violations),
    }

    with open(output_path, "w") as f:
        json.dump(attestation, f, indent=2)

    print(json.dumps(attestation, indent=2))


if __name__ == "__main__":
    main()
