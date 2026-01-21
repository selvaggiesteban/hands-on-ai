---
id: 02-article-body
title: "02 Article Body Structure"
category: templates
subcategory: 
type: checklist
version: "2.1.0"
last_updated: "2026-01-16"
author: hands-on-ai
status: active
machine_readable: true
---

# GENERATE: ARTICLE BODY

Follow this sequence to build the article body in strict HTML5.

## 1. MAIN TITLE (H1)
- Generate a single `<h1>` tag containing the SEO-optimized title.
- Must include **Main Keyword**.

## 2. INTRODUCTION
- Write multiple `<p>` paragraphs.
- **Constraints:** 100-200 words each, **Main Keyword** in `<strong>` tags in every paragraph.
- **Links:** Verify URL technically (HTTP 200 check) or via Sitemap. If alive + Exact Match -> Link with `rel="nofollow" target="_blank"`. Else -> Plain text.

## 3. CORE CONTENT (GUIDE STEPS) - REPEAT 4 TIMES
For each of the 4 main sections (H2):
1. Create an `<h2>` subtitle relevant to the step.
2. Write content in `<p>` tags (100-200 words, **keyword** bolded).
3. **SPECIAL INSTRUCTION FOR SECTION 3:**
   - **IF** verified pricing data exists in project files: Generate an HTML `<table>` with the data.
   - **IF NOT**: Continue with text only. **DO NOT INVENT PRICES.**

## 4. FAQ SECTION (H3)
1. Create a header `<h2>Preguntas Frecuentes</h2>`.
2. Generate **5 Questions** using `<h3>` tags.
3. Answer each with `<p>` tags obeying the length (100-200w) and keyword (`<strong>`) rules.
