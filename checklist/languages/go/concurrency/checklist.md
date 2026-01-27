---
category: "Go"
topic: "Concurrency"
---

# Concurrency

- Are goroutines synchronized using 'sync.WaitGroup' or channels? [YES/NO]
- Is the 'sync/atomic' package used for simple counters or flags? [YES/NO]
- Is 'sync.Mutex' or 'sync.RWMutex' used to protect shared mutable state? [YES/NO]
- Is the race detector ('-race') enabled during testing? [YES/NO]
- Are goroutines leaked (ensure they exit)? [YES/NO]
- Is the 'errgroup' package used for managing groups of goroutines? [YES/NO]
