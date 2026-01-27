---
name: endpoint-responses
description: Use when [describe the use case for this skill].
---

﻿---
name: endpoint-responses
description: Use when specifying the response structure and data types returned by an API endpoint.
---

#### Responses

**Success (200)**:

```json
{
  "status": "success",
  "data": {
    {{response_structure}}
  }
}
```

**Error (4xx/5xx)**:

```json
{
  "status": "error",
  "error": {
    "code": "{{error_code}}",
    "message": "{{error_message}}"
  }
}
```

