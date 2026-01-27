---
category: "JavaScript"
topic: "Promises"
---

# Promises

- Are new Promises created only when necessary (avoiding the Promise constructor anti-pattern)? [YES/NO]
- Is .then() chaining kept flat to maintain readability? [YES/NO]
- Are errors propagated correctly through the promise chain? [YES/NO]
- Is Promise.allSettled() used when all results are needed regardless of success/failure? [YES/NO]
- Is Promise.race() used appropriately for timeout or first-responder logic? [YES/NO]
- Are promises cleaned up (e.g., cancelling timers) if they are no longer needed? [YES/NO]
