---
category: "Go"
topic: "Channels"
---

# Channels

- Are channels properly closed by the sender? [YES/NO]
- Is the 'range' loop used to receive values until the channel is closed? [YES/NO]
- Are buffered channels used only when necessary to prevent blocking? [YES/NO]
- Is 'select' used for handling multiple channel operations? [YES/NO]
- Are nil channels handled correctly (they block forever)? [YES/NO]
- Is the 'context' package used to propagate cancellation signals to channel operations? [YES/NO]
