import os

# --- KNOWLEDGE BASE (Absolute Truths 2026) ---

KNOWLEDGE_BASE = {
    "web_development_and_technology": {
        "intro": "The Web Development and Technology department is the bedrock of the agency's infrastructure. It operates on the principle of 'Architecture as a Service' (AaaS).",
        "standards": [
            "Strict adherence to SOLID principles and Clean Architecture is mandatory.",
            "All services must implement the Twelve-Factor App methodology.",
            "Zero Trust Architecture (ZTA) must be the default for all internal and external communication.",
            "Database schemas must follow the Third Normal Form (3NF) unless performance-driven denormalization is architecturally approved.",
            "API documentation must follow the OpenAPI 3.1 specification and be automatically generated."
        ],
        "kpis": ["DORA Metrics (Deployment Frequency, Lead Time, MTTR, Change Failure Rate)", "Performance: Core Web Vitals (LCP < 2s, CLS < 0.1)"]
    },
    "security_infrastructure_and_support": {
        "intro": "Security is not a phase; it is the environment. This department enforces the agency's 'Fortress' protocol.",
        "standards": [
            "OWASP Top 10 mitigation is the minimum requirement for all deployments.",
            "All infrastructure must be managed via version-controlled IaC (Terraform/HCL).",
            "Continuous Security Monitoring (CSM) must be active 24/7/365.",
            "Disaster Recovery (DR) RPO/RTO must be verified monthly via simulated failures.",
            "Secrets must never touch the filesystem; use Vault or specialized Cloud KMS."
        ],
        "kpis": ["Time to Detection (TTD)", "Vulnerability Patch Cycle < 24h for Criticals"]
    },
    "seo_and_content": {
        "intro": "SEO in 2026 is driven by SGE (Search Generative Experience) and E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness).",
        "standards": [
            "Semantic HTML5 is the foundation of technical SEO; no exceptions.",
            "Content must satisfy both user intent and Large Language Model (LLM) indexing requirements.",
            "Structured Data (Schema.org) must be implemented using JSON-LD for every entity.",
            "Entity-based SEO over keyword density: focus on Knowledge Graph integration.",
            "Automated link-building must strictly adhere to white-hat 'Authority-First' protocols."
        ],
        "kpis": ["Organic Visibility Index", "SGE Citation Share", "Entity Dominance Score"]
    },
    "advanced_content_and_ai": {
        "intro": "AI is the engine of efficiency. This department pioneers 'Human-in-the-loop' (HITL) automation.",
        "standards": [
            "Prompt Engineering must follow the 'Context-Task-Constraint' (CTC) framework.",
            "All AI-generated output must undergo automated bias and hallucination auditing.",
            "Model selection is based on Token-Cost-Latency optimization (TCLo).",
            "Multi-agent orchestration requires state-machine validation to prevent infinite loops.",
            "AI Ethics: All synthetic content must be watermarked per agency policy."
        ],
        "kpis": ["Token Efficiency Ratio", "Human Edit Rate < 15%", "Inference Accuracy"]
    }
}

# Generic fallback for unmapped roles to maintain high quality
GENERIC_TECHNICAL = [
    "Follow the 'Automation First' doctrine for all repetitive tasks.",
    "Documentation must be versioned alongside the code or process it describes.",
    "All decisions must be backed by data or documented in an ADR (Architecture Decision Record).",
    "Maintain a growth mindset: audit and update the tech stack every 6 months.",
    "Quality is everyone's responsibility; the 'Definition of Done' is absolute."
]

def generate_absolute_truth(role_name, category_key):
    # Fetch data
    data = KNOWLEDGE_BASE.get(category_key, {
        "intro": f"The {category_key.replace('_', ' ')} department ensures operational excellence in its domain.",
        "standards": GENERIC_TECHNICAL,
        "kpis": ["Process Efficiency", "Deliverable Accuracy"]
    })
    
    lines = [
        f"# Authority Profile: {role_name.upper()}",
        f"Domain: {category_key.upper()} | Role Status: CORE | Authority Level: SENIOR",
        "=" * 80,
        "",
        "## 1. Executive Summary",
        data["intro"],
        f"The {role_name} acts as the primary authority on implementation and quality standards within this domain.",
        "",
        "## 2. Universal Engineering Standards",
        "All work produced must adhere to the following non-negotiable standards:",
    ]
    
    for s in data["standards"]:
        lines.append(f"- [MANDATE]: {s}")
    
    lines.append("")
    lines.append("## 3. Operational Protocols (SOPs)")
    protocols = [
        "Inception: Define clear objectives and success metrics before execution.",
        "Implementation: Use strictly modular, testable, and reusable components.",
        "Validation: Automated testing and peer review are prerequisites for finalization.",
        "Deployment: Continuous Integration (CI) is the only path to production.",
        "Observation: Post-deployment monitoring is mandatory for 72 hours."
    ]
    for p in protocols:
        lines.append(f"- PROTOCOL: {p}")
        
    lines.append("")
    lines.append("## 4. Key Performance Indicators (KPIs)")
    lines.append("Success for this role is measured by these objective metrics:")
    for kpi in data["kpis"]:
        lines.append(f"- KPI: {kpi}")
        
    lines.append("")
    lines.append("## 5. 2026 Tech Stack & Tooling")
    lines.append("This role is expected to maintain mastery over the following ecosystem:")
    stack = ["Git/GitHub Enterprise", "Containerization (Docker/Kubernetes)", "AI Orchestration Frameworks", "Automated Quality Gates"]
    for tool in stack:
        lines.append(f"- {tool}")

    lines.append("")
    lines.append("---")
    lines.append("END OF AUTHORITY DOCUMENT. NON-COMPLIANCE REQUIRES CTO EXCEPTION.")
    
    return "\n".join(lines)

def main():
    root_dirs = ["agents", "skills"]
    
    for root in root_dirs:
        if not os.path.exists(root): continue
        
        for category in os.listdir(root):
            cat_path = os.path.join(root, category)
            if not os.path.isdir(cat_path): continue
            
            for profile in os.listdir(cat_path):
                profile_path = os.path.join(cat_path, profile)
                if not os.path.isdir(profile_path): continue
                
                # Filename depends on root (agent.md or skill.md)
                filename = "agent.md" if root == "agents" else "skill.md"
                file_path = os.path.join(profile_path, filename)
                
                # Check if it's a profile or a nested folder (like tech_stack_languages)
                if os.path.isdir(profile_path):
                    # Handle nested (like tech_stack_languages)
                    if profile == "tech_stack_languages":
                        for lang in os.listdir(profile_path):
                            lang_path = os.path.join(profile_path, lang)
                            if os.path.isdir(lang_path):
                                f_path = os.path.join(lang_path, filename)
                                print(f"Regenerating: {f_path}")
                                content = generate_absolute_truth(lang, category)
                                with open(f_path, "w", encoding="utf-8") as f:
                                    f.write(content)
                    else:
                        print(f"Regenerating: {file_path}")
                        content = generate_absolute_truth(profile, category)
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(content)

if __name__ == "__main__":
    main()