
---
id: 02-3-endpoint-example
title: "02 3 Endpoint Example"
category: templates
subcategory: 
type: checklist
version: "1.0.0"
last_updated: "2026-01-14"
author: hands-on-ai
status: active
machine_readable: true
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

