---
category: "Go"
topic: "Defer and Panic"
---

# Defer and Panic

- Is 'defer' used for resource cleanup (e.g., file closing, mutex unlocking)? [YES/NO]
- Is 'recover()' used only in specific goroutines where panics are expected? [YES/NO]
- Is 'panic' avoided in libraries (return errors instead)? [YES/NO]
- Are deferred function arguments evaluated immediately? [YES/NO]
- Is the order of execution (LIFO) for multiple defers considered? [YES/NO]
- Is 'defer' avoided in tight loops if performance is critical? [YES/NO]
