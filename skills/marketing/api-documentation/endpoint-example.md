---
name: endpoint-example
description: Use when [describe the use case for this skill].
---

﻿---
name: endpoint-example
description: Use when providing a concrete usage example of a marketing API endpoint, including requests and responses.
---

#### Complete example

**Request**:

```bash
curl -X {{METHOD}} \
  -H "Authorization: Bearer {{token}}" \
  -H "Content-Type: application/json" \
  -d '{{json_body}}' \
  {{base_url}}/{{endpoint}}
```

**Response**:

```json
{{complete_response_example}}
```

[Repeat for each detected endpoint]

