---
name: defense-in-depth
description: Use when designing test strategies that require multiple layers of verification to avoid false positives.
---

# Defense in Depth

## Overview
One check is never enough. Systems fail in complex ways.

## Strategy
Layer your assertions:
1.  **State Check:** Is the data correct?
2.  **UI Check:** Is it visible?
3.  **Network Check:** Did the request fire?