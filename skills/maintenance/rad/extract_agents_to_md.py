
import os
import sys
import re

# Add the project root to the python path to allow importing tools.agents.imported_subagents
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from tools.agents.imported_subagents import IMPORTED_SUBAGENTS, ImportedSubagentType, SubagentConfig

def get_category(agent_type_enum):
    name = agent_type_enum.name
    
    # Frontend_Mobile
    if name in ["FRONTEND_DEVELOPER", "MOBILE_DEVELOPER", "UI_DESIGNER", "ANGULAR_ARCHITECT", 
                "FLUTTER_EXPERT", "JAVASCRIPT_PRO", "NEXTJS_DEVELOPER", "REACT_SPECIALIST", 
                "SWIFT_EXPERT", "TYPESCRIPT_PRO", "VUE_EXPERT", "MOBILE_APP_DEVELOPER", 
                "UX_RESEARCHER", "ELECTRON_PRO"]:
        return "Frontend_Mobile"
        
    # Backend_API
    if name in ["API_DESIGNER", "BACKEND_DEVELOPER", "FULLSTACK_DEVELOPER", "GRAPHQL_ARCHITECT", 
                "MICROSERVICES_ARCHITECT", "WEBSOCKET_ENGINEER", "CSHARP_DEVELOPER", 
                "DJANGO_DEVELOPER", "DOTNET_CORE_EXPERT", "DOTNET_FRAMEWORK_4_8_EXPERT", 
                "ELIXIR_EXPERT", "GOLANG_PRO", "JAVA_ARCHITECT", "KOTLIN_SPECIALIST", 
                "LARAVEL_SPECIALIST", "PHP_PRO", "PYTHON_PRO", "RAILS_EXPERT", 
                "SPRING_BOOT_ENGINEER", "SQL_PRO", "POSTGRES_PRO", "WORDPRESS_MASTER"]:
        return "Backend_API"
        
    # DevOps_Cloud
    if name in ["AZURE_INFRA_ENGINEER", "CLOUD_ARCHITECT", "DATABASE_ADMINISTRATOR", 
                "DEPLOYMENT_ENGINEER", "DEVOPS_ENGINEER", "DEVOPS_INCIDENT_RESPONDER", 
                "INCIDENT_RESPONDER", "KUBERNETES_SPECIALIST", "NETWORK_ENGINEER", 
                "PLATFORM_ENGINEER", "SRE_ENGINEER", "TERRAFORM_ENGINEER", 
                "WINDOWS_INFRA_ADMIN", "BUILD_ENGINEER", "DEPENDENCY_MANAGER", 
                "GIT_WORKFLOW_MANAGER", "M365_ADMIN"]:
        return "DevOps_Cloud"
        
    # Security_Quality
    if name in ["ACCESSIBILITY_TESTER", "AD_SECURITY_REVIEWER", "ARCHITECT_REVIEWER", 
                "CHAOS_ENGINEER", "CODE_REVIEWER", "COMPLIANCE_AUDITOR", "DEBUGGER", 
                "ERROR_DETECTIVE", "PENETRATION_TESTER", "PERFORMANCE_ENGINEER", 
                "POWERSHELL_SECURITY_HARDENING", "QA_EXPERT", "SECURITY_AUDITOR", 
                "TEST_AUTOMATOR", "SECURITY_ENGINEER"]:
        return "Security_Quality"
        
    # Data_AI
    if name in ["AI_ENGINEER", "DATA_ANALYST", "DATA_ENGINEER", "DATA_SCIENTIST", 
                "DATABASE_OPTIMIZER", "LLM_ARCHITECT", "MACHINE_LEARNING_ENGINEER", 
                "ML_ENGINEER", "MLOPS_ENGINEER", "NLP_ENGINEER", "PROMPT_ENGINEER", 
                "QUANT_ANALYST", "DATA_RESEARCHER", "SEARCH_SPECIALIST", "TREND_ANALYST"]:
        return "Data_AI"
        
    # Automation_Tooling
    if name in ["CLI_DEVELOPER", "DOCUMENTATION_ENGINEER", "DX_OPTIMIZER", "MCP_DEVELOPER", 
                "POWERSHELL_MODULE_ARCHITECT", "POWERSHELL_UI_ARCHITECT", "TOOLING_ENGINEER", 
                "API_DOCUMENTER", "AGENT_INSTALLER", "AGENT_ORGANIZER", "CONTEXT_MANAGER", 
                "ERROR_COORDINATOR", "IT_OPS_ORCHESTRATOR", "KNOWLEDGE_SYNTHESIZER", 
                "MULTI_AGENT_COORDINATOR", "PERFORMANCE_MONITOR", "TASK_DISTRIBUTOR", 
                "WORKFLOW_ORCHESTRATOR"]:
        return "Automation_Tooling"
        
    # Management_Strategy
    if name in ["BUSINESS_ANALYST", "CONTENT_MARKETER", "CUSTOMER_SUCCESS_MANAGER", 
                "LEGAL_ADVISOR", "PRODUCT_MANAGER", "PROJECT_MANAGER", "SALES_ENGINEER", 
                "SCRUM_MASTER", "TECHNICAL_WRITER", "COMPETITIVE_ANALYST", 
                "MARKET_RESEARCHER", "RESEARCH_ANALYST", "RISK_MANAGER"]:
        return "Management_Strategy"
        
    # Specialized
    if name in ["BLOCKCHAIN_DEVELOPER", "EMBEDDED_SYSTEMS", "FINTECH_ENGINEER", 
                "GAME_DEVELOPER", "IOT_ENGINEER", "PAYMENT_INTEGRATION", 
                "REFACTORING_SPECIALIST", "SLACK_EXPERT", "LEGACY_MODERNIZER"]:
        return "Specialized"
        
    # Languages_Frameworks (Catch-all for language specific pros not covered above or generic)
    if name in ["CPP_PRO", "RUST_ENGINEER", "POWERSHELL_5_1_EXPERT", "POWERSHELL_7_EXPERT"]:
        return "Languages_Frameworks"

    # Fallback to Specialized if missed
    print(f"Warning: Agent {name} not explicitly mapped. Defaulting to Specialized.")
    return "Specialized"

def generate_markdown(agent_type, config):
    category = get_category(agent_type)
    file_name = f"{config.type}.md"
    file_path = os.path.join("agents", category, file_name)
    
    # Format capabilities and tools as YAML lists
    capabilities_yaml = "\n".join([f"  - {cap}" for cap in config.capabilities])
    tools_yaml = "\n".join([f"  - {tool}" for tool in config.tool_permissions])
    
    # Escape quotes in description if necessary
    description = config.description.replace('"', '\"')
    
    markdown_content = f"""
---
name: "{config.type}"
type: "{agent_type.name}"
description: "{description}"
capabilities:
{capabilities_yaml}
tools:
{tools_yaml}
---
# System Prompt

{config.system_prompt}
"""
    
    # Ensure directory exists (it should, but safety first)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    return file_path

def main():
    print("Starting extraction of agents to Markdown...")
    count = 0
    for agent_type, config in IMPORTED_SUBAGENTS.items():
        try:
            path = generate_markdown(agent_type, config)
            # print(f"Generated: {path}")
            count += 1
        except Exception as e:
            print(f"Error generating {agent_type.name}: {e}")
            
    print(f"Successfully generated {count} agent markdown files.")

if __name__ == "__main__":
    main()
