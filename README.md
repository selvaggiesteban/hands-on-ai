# Hands-On AI: Autonomous Development Framework (v2.1)

**Hands-On AI** is a unified orchestration system that combines multiple LLMs, specialized sub-agents, and persistent memory (RAG) to automate software engineering tasks. It evolves beyond simple chat to perform complex, multi-step development workflows autonomously.

## 🚀 Key Capabilities (v2.1 Unified)

*   **🧠 Unified Brain:** One interface (`/chat`) seamlessly switches between quick answers and deep autonomous work using the **Enhanced Multi-Agent System**.
*   **🤖 128+ Specialized Agents:** Includes experts like `React Specialist`, `Security Auditor`, `Rust Engineer`, and `SEO Analyst` (migrated from Anthropic's library).
*   **📚 RAG Memory:** Indexes your codebase, external documentation, and conversation history into a local vector database (`ChromaDB`) for context-aware responses.
*   **🛡️ Security First:** Enforces `threat-model.yaml` policies automatically. If an agent tries to write insecure code (e.g., hardcoded secrets), the system blocks it.
*   **⚡ Skills System:** Agents automatically "learn" new skills (e.g., "Create PowerPoint", "Debug SQL") based on your request context.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/hands-on-ai.git
    cd hands-on-ai
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Copy `.env.example` to `.env` and add your API keys (OpenAI, Anthropic, or Gemini).
    ```bash
    cp .env.example .env
    ```

4.  **Initialize the Brain (Index Knowledge):**
    This populates the RAG database with the included knowledge base and agents.
    ```bash
    python skills/rag/knowledge_indexer.py --index
    ```

## 🎮 Usage

Start the Orchestrator:
```bash
python orchestrator.py
```

**Just chat naturally.** The system decides the best course of action:

*   **Ask:** "What is the security policy for API tokens?" -> *Uses RAG to answer from `threat-model.yaml`.*
*   **Task:** "Create a login page with React." -> *Activates `Frontend Developer` agent, loads `react-best-practices` skill, and generates code.*
*   **Command:** "/audit" -> *Runs a full security scan on your project.*

## 📂 Project Structure

```
./
│   ├── LICENSE
│   ├── orchestrator.py                 # Main entry point and brain
│   ├── README.md                       # This file
│   ├── requirements.txt                # Python dependencies
│   ├── robots.txt                      # Crawler configuration
│   ├── sitemap.xml                     # Site map for indexing
│   ├── .github/                        # CI/CD workflows
│   ├── integrations/                   # Core system integration logic
│   │   ├── enhanced_multi_agent_system.py # The advanced agent engine
│   ├── knowledge_base/                 # Static knowledge and rules
│   │   ├── setup/                      # Project setup guides (Rules.md)
│   │   ├── skills/                     # Documentation for skills
│   │   ├── technologies/               # Tech stack documentation
│   │   ├── templates/                  # Document templates
│   ├── project_meta/                   # Project-specific metadata
│   │   ├── ai-context/                 # Prompts and token budgets
│   │   ├── planning/                   # Current project plan (plan.json)
│   │   ├── security/                   # Threat model (threat-model.yaml)
│   ├── src/                            # Source code of the target application
│   ├── tests/                          # System tests
│   ├── agents/                         # Multi-agent definitions (Markdown)
│   │   ├── Core/                       # Coding, Planning, etc.
│   │   ├── Backend_API/                # 128+ specialized agents
│   ├── ai_wrapper/                     # Multi-model AI abstraction layer
│   ├── skills/                         # Executable tools and skills
│   │   ├── rag/                        # Knowledge indexing logic
│   │   ├── security/                   # Policy enforcement logic
│   │   ├── imported_skills.py          # Registry of all skills
│   ├── data/                           # Runtime data (ignored by git)
│   │   ├── chroma_db/                  # Local vector database
│   ├── .planning/                      # Persistent task memory
```

## 🛡️ Security

This framework includes a **Policy Enforcer** that intercepts file writes. It validates code against `project_meta/security/threat-model.yaml` before saving.

## 🤝 Contributing

See `CONTRIBUTING.md` (if available) or just open a PR.

---
*Powered by OpenAI, Anthropic, and Google Gemini models.*
