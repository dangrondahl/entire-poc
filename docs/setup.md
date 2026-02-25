# Setup Guide

## Prerequisites

- Git repository initialized
- Entire CLI installed (`brew install entire` or see [installation docs](https://docs.entire.io/cli/installation))

## Enable Entire in a Repo

```bash
cd your-project
entire enable
```

## Verify Installation

```bash
entire status
```

Expected output:
```
● Enabled · manual-commit · branch main
```

## Git Hooks

Entire installs Git hooks automatically. Verify with:

```bash
ls .git/hooks
```
