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
    python tools/rag/knowledge_indexer.py --index
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

*   `orchestrator.py`: The main entry point and brain.
*   `tools/agents/`: 128+ Python-based specialized agents.
*   `tools/skills/`: 30+ capabilities (TDD, Debugging, Documentation).
*   `knowledge_base/`: Markdown rules and templates that guide the AI.
*   `data/chroma_db/`: Vector database (generated locally, do not commit).
*   `.planning/`: Persistent memory of ongoing tasks.

## 🛡️ Security

This framework includes a **Policy Enforcer** that intercepts file writes. It validates code against `project_meta/security/threat-model.yaml` before saving.

## 🤝 Contributing

See `CONTRIBUTING.md` (if available) or just open a PR.

---
*Powered by OpenAI, Anthropic, and Google Gemini models.*