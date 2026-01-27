---
category: "Go"
topic: "Mutexes"
---

# Mutexes

- Is the mutex locked and unlocked in the same scope (using defer)? [YES/NO]
- Is 'RWMutex' used when there are many readers and few writers? [YES/NO]
- Are mutexes embedded in structs properly (not copied by value)? [YES/NO]
- Is the scope of the lock kept as small as possible? [YES/NO]
- Are deadlocks avoided by acquiring locks in a consistent order? [YES/NO]
- Is 'sync.Map' considered for specific concurrent map use cases? [YES/NO]
