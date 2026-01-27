---
name: condition-based-waiting
description: Use when writing async tests that depend on UI state changes or network events to prevent flakiness.
---

# Condition-Based Waiting

## Overview

Flaky tests often guess at timing with arbitrary delays. This creates race conditions where tests pass on fast machines but fail under load or in CI.

**Core principle:** Wait for the actual condition you care about, not a guess about how long it takes.

## When to Use