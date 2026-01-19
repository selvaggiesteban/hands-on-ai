---
id: 01-configuration
title: "01 Configuration & Rules"
category: templates
subcategory: 
type: checklist
version: "2.1.0"
last_updated: "2026-01-16"
author: hands-on-ai
status: active
machine_readable: true
---

# STRICT WRITING PROTOCOL: SEO ARTICLE (DELIVERABLE 6)

## 1. FORMAT & TECHNICAL CONSTRAINTS
- **Output Format:** Pure Semantic HTML5 (`<article>`, `<h1>`, `<p>`, `<ul>`, `<table>`).
- **CSS:** **FORBIDDEN**. Do not use `<style>` blocks or `style="..."` attributes.
- **Classes/IDs:** **FORBIDDEN**. Rely solely on semantic HTML tags.
- **Images:** Use `<img src="..." alt="..." loading="lazy">`.

## 2. RESEARCH PHASE (MANDATORY BEFORE WRITING)
**CRITICAL: YOU MUST NOT INVENT DATA.**
1. **Sitemap/URLs:** Scan `sitemap.xml`, `routes` files, or project structure to identify VALID internal URLs.
2. **Contact Info:** Extract real address, phone, and **Google Business Profile (GBP)** URL.
3. **Prices/Services:** Search for `prices`, `tariffs`, or `services` files. **If no official data is found, DO NOT generate a price table.**

## 3. SEO & CONTENT RULES
- **Total Length:** Minimum 1500 words.
- **Paragraphs (CRITICAL):**
  - **Length:** Each paragraph must be between **100 and 200 words**.
  - **Keyword:** The *Main Keyword* must appear in **every single paragraph**.
  - **Emphasis:** The *Main Keyword* must be wrapped in `<strong>` tags every time it appears.
## 4. LINK ATTRIBUTES (GLOBAL RULE)
- **ALL LINKS (Internal & External) MUST HAVE:**
  - `rel="nofollow"`
  - `target="_blank"`
- **Internal Linking (HTTP VERIFICATION REQUIRED):**
  - **Rule:** You MUST verify that the URL returns a valid response (Status 200) or is explicitly listed in a Sitemap.
  - **Prohibition:** NEVER guess or infer URLs. If you cannot verify the link is alive, DO NOT generate the `<a>` tag.
  - **Action:** If verified + exact text match -> `<a href="[URL]" rel="nofollow" target="_blank">phrase</a>`.
  - **Fail-Safe:** If verification fails, leave as plain text.
- **External Linking:**
  - Mandatory link to the **Google Business Profile** (GBP).
  - **Anchor Text Rule:** The anchor text for the GBP link MUST be literally the title of the Google profile.
  - **Action:** `<a href="[GBP_URL]" rel="nofollow" target="_blank">[EXACT_GBP_TITLE]</a>`.
