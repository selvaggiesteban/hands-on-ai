---
category: "Authentication"
topic: "Authentication Standards"
---

# Authentication Standards

- Are passwords hashed using strong algorithms (e.g., Argon2, Bcrypt)? [YES/NO]
- Is Multi-Factor Authentication (MFA) supported or required for sensitive accounts? [YES/NO]
- Are session tokens securely generated and signed (e.g., JWT)? [YES/NO]
- Are cookies flagged as HttpOnly and Secure? [YES/NO]
- Is there a mechanism to revoke sessions or tokens? [YES/NO]
- Are excessive login attempts rate-limited to prevent brute-force attacks? [YES/NO]
