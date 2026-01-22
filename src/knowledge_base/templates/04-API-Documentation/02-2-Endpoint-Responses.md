
---
id: 02-2-endpoint-responses
title: "02 2 Endpoint Responses"
category: templates
subcategory: 
type: checklist
version: "1.0.0"
last_updated: "2026-01-14"
author: hands-on-ai
status: active
machine_readable: true
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

