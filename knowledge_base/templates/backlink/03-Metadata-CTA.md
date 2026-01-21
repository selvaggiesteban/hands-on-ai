---
id: 03-metadata-cta
title: "03 Metadata and CTA"
category: templates
subcategory: 
type: checklist
version: "2.1.0"
last_updated: "2026-01-16"
author: hands-on-ai
status: active
machine_readable: true
---

# GENERATE: CONCLUSION, CTA & METADATA

## 1. CONCLUSION & CTA
1. **Conclusion:** Start with `<h2>Conclusion</h2>` followed by closing paragraphs (standard length/keyword rules apply).
2. **CTA Section:** Create a `<section>` (NO CSS, NO STYLES):
   - Encouraging text.
   - Link: `<a href="[CONTACT_URL]" rel="nofollow" target="_blank">Solicitar Presupuesto</a>` (Use verified URL).
   - GBP Link: `<a href="[GBP_URL]" rel="nofollow" target="_blank">[EXACT_GBP_TITLE]</a>` (Use the exact Google Business Profile title as anchor).

## 2. METADATA BLOCK (HTML COMMENT)
Append this block at the very end of the file as an HTML comment `<!-- ... -->`:
- **Slug:** Suggested permanent URL (e.g., `/guia-quitar-manchas/`).
- **Meta Title:** < 60 chars.
- **Meta Description:** < 160 chars.
- **Image Alts:** List of suggested alt texts for hypothetical images.
