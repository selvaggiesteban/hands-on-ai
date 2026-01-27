---
name: product-overview
description: Use when [describe the use case for this skill].
---

# EXECUTIVE SUMMARY TEMPLATE - [PROJECT NAME]

**[PROJECT TYPE / BRIEF DESCRIPTION]**
**Version:** 1.0
**Date:** [DATE]

---

## 🎯 OVERVIEW

[PROJECT NAME] is a [SYSTEM TYPE, e.g., SaaS, Mobile Application] designed for [PROJECT'S MAIN GOAL]. It combines [DISTINCTIVE FEATURE A] with [DISTINCTIVE FEATURE B] to create a market-leading user experience.

### Core User Epics & Stories
_[List the high-level user goals as Epics, and break them down into specific user stories. Include labels and Gherkin-like acceptance criteria for machine readability.]_

- **Epic: [High-level Goal, e.g., Account Management]**
  - *As a [User Role], I want to [Action] so that [Benefit].*
    - **Labels:** `area:frontend`, `module:auth`, `priority:high`
    - **Acceptance Criteria (Gherkin):**
      - `Given I am on the registration page,
        When I submit valid credentials,
        Then I should be redirected to the dashboard and receive a welcome email.`
      - `Given I am on the login page,
        When I enter invalid credentials,
        Then I should see an error message.`
  - *As a [User Role], I want to [Action] so that [Benefit].*
    - **Labels:** `area:backend`, `module:users`, `priority:medium`
    - **Acceptance Criteria (Gherkin):**
      - `Given I am logged in,
        When I navigate to my profile,
        Then I should see my personal information.`

- **Epic: [High-level Goal, e.g., Product Discovery]**
  - *As a [User Role], I want to [Action] so that [Benefit].*
    - **Labels:** `area:frontend`, `module:catalog`, `priority:high`
    - **Acceptance Criteria (Gherkin):**
      - `Given I am on the homepage,
        When I browse products,
        Then I should see a list of available products with their prices.`
  - *As a [User Role], I want to [Action] so that [Benefit].*
    - **Labels:** `area:backend`, `module:search`, `priority:medium`
    - **Acceptance Criteria (Gherkin):**
      - `Given I am on the product listing page,
        When I search for "[keyword]",
        Then I should see products matching the keyword.`

---

## 📋 KEY ARCHITECTURAL & BUSINESS DECISIONS

-   **Architecture**: A [**Monolithic / Microservices**] architecture will be used with [**Main Framework**] for [**Justification, e.g., rapid MVP development**].
-   **Database & Performance**: [**Database, e.g., PostgreSQL**] will ensure data integrity, while [**Caching Technology, e.g., Redis**] will be used for high-performance operations.
-   **[Critical Business Rule A]**: [Description of how this rule will be technically implemented or enforced].
-   **[Critical Business Rule B]**: [Description of how this rule will be technically implemented or enforced].
-   **[Key Data Policy]**: A [**e.g., soft-delete, anonymization**] policy will be implemented for [**Justification, e.g., preserving statistical integrity**].
-   **[Key Management Functionality]**: A [**e.g., "deep copy"**] function will be enabled to [**Justification, e.g., streamline new content creation**].

---

## 📊 ROLES & KEY FEATURES

| Role | Core Responsibility & Key Features |
|---|---|
| **[User Role A, e.g., Admin]** | [Description of key responsibilities and permissions]. |
| **[User Role B, e.g., Editor]** | [Description of key responsibilities and permissions]. |
| **[User Role C, e.g., Standard User]**| [Description of key responsibilities and permissions]. |
| **[User Role D, e.g., Guest]** | [Description of key responsibilities and permissions]. |

---

## 🚀 DEVELOPMENT ROADMAP (Release Plan)

The project will follow a phased release plan based on delivering user value.

-   **Release 1 (MVP - Est. [N] Weeks): [Release Goal, e.g., Core Account & Discovery Features]**
    - [ ] Story: *As a user, I want to register so that I can create an account.*
      - **Labels:** `area:auth`, `priority:high`
      - **Acceptance Criteria (Gherkin):**
        - `Given I am on the registration page,
          When I submit valid credentials,
          Then I should be redirected to the dashboard.`
    - [ ] Story: *As a user, I want to log in so that I can access my account.*
      - **Labels:** `area:auth`, `priority:high`
      - **Acceptance Criteria (Gherkin):**
        - `Given I am on the login page,
          When I enter valid credentials,
          Then I should be logged in.`
    - [ ] Story: *As a user, I want to browse products so that I can see what's available.*
      - **Labels:** `area:catalog`, `priority:medium`
      - **Acceptance Criteria (Gherkin):**
        - `Given I am on the homepage,
          When I view the product section,
          Then I should see a list of featured products.`

-   **Release 2 (Est. [N] Weeks): [Release Goal, e.g., First Transaction]**
    - [ ] Story: *As a user, I want to add a product to my cart so that I can purchase it.*
      - **Labels:** `area:cart`, `priority:high`
      - **Acceptance Criteria (Gherkin):**
        - `Given I am viewing a product,
          When I click "Add to Cart",
          Then the product should be added to my cart.`
    - [ ] Story: *As a user, I want to check out so that I can complete my purchase.*
      - **Labels:** `area:checkout`, `priority:high`
      - **Acceptance Criteria (Gherkin):**
        - `Given I have items in my cart,
          When I proceed to checkout and complete payment,
          Then my order should be placed.`

---

## ⚠️ PENDING DECISIONS

The following key business logic questions require final confirmation before implementation:
-   [Question 1 about Business Logic]
-   [Question 2 about Monetization or Access]
-   [Question 3 about User Flow]

**This updated plan provides a clear, comprehensive, and de-risked path to launching the project.**

*Document generated on [DATE]*
