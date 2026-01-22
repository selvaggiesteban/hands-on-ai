import os
import yaml
from typing import Dict, Any, Optional

class AgentLoader:
    """
    Loads agent definitions from Markdown files with YAML frontmatter.
    """
    
    def __init__(self, agents_root: str = None):
        if agents_root:
            self.agents_root = agents_root
        else:
            # Default to agents relative to this file
            self.agents_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../agents'))
            
        self.agent_cache = {}

    def list_agents(self) -> Dict[str, str]:
        """
        Lists all available agents discovered in the agents directory.
        
        Returns:
            Dict mapping agent names to their file paths (relative to agents root).
        """
        agents = {}
        for root, dirs, files in os.walk(self.agents_root):
            for file in files:
                if file.endswith(".md"):
                    # Calculate relative path for category/name structure
                    rel_dir = os.path.relpath(root, self.agents_root)
                    if rel_dir == ".":
                        name = file.replace(".md", "")
                    else:
                        name = f"{rel_dir}/{file.replace('.md', '')}".replace("\\", "/")
                    
                    agents[name] = os.path.join(root, file)
        return agents

    def load_agent(self, agent_name: str) -> Dict[str, Any]:
        """
        Loads an agent by name.
        
        Args:
            agent_name: Name of the agent (e.g., 'coding', 'Core/coding_agent', 'api-designer')
            
        Returns:
            Dict containing agent configuration and prompt
        """
        if agent_name in self.agent_cache:
            return self.agent_cache[agent_name]
            
        agent_path = self._find_agent_file(agent_name)
        if not agent_path:
            raise FileNotFoundError(f"Agent '{agent_name}' not found in {self.agents_root}")
            
        agent_config = self._parse_agent_file(agent_path)
        self.agent_cache[agent_name] = agent_config
        return agent_config

    def _find_agent_file(self, agent_name: str) -> Optional[str]:
        """Finds the .md file for the agent."""
        
        # 1. Check if direct path provided (e.g. Core/coding_agent)
        if '/' in agent_name or '\\' in agent_name:
            if not agent_name.endswith('.md'):
                agent_name += '.md'
            path = os.path.join(self.agents_root, agent_name)
            if os.path.exists(path):
                return path
                
        # 2. Search recursively for filename
        search_name = agent_name
        if not search_name.endswith('.md'):
            search_name += '.md'
            
        for root, dirs, files in os.walk(self.agents_root):
            if search_name in files:
                return os.path.join(root, search_name)
                
        # 3. Try partial matching (e.g. 'coding' -> 'coding_agent.md')
        if not agent_name.endswith('_agent'):
            alt_name = f"{agent_name}_agent.md"
            for root, dirs, files in os.walk(self.agents_root):
                if alt_name in files:
                    return os.path.join(root, alt_name)
        
        return None

    def _parse_agent_file(self, file_path: str) -> Dict[str, Any]:
        """Parses the Markdown file with YAML frontmatter."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Split frontmatter
        parts = content.split('---')
        if len(parts) < 3:
            # Fallback for files without valid frontmatter
            return {
                "name": os.path.basename(file_path).replace('.md', ''),
                "system_prompt": content,
                "capabilities": [],
                "tools": []
            }
            
        yaml_content = parts[1]
        # The rest is the body/prompt
        # Note: join remaining parts in case '---' appears in the body
        markdown_body = '---'.join(parts[2:]).strip()
        
        # Remove "# System Prompt" header if present
        markdown_body = markdown_body.replace('# System Prompt', '').strip()
        
        try:
            config = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML for {file_path}: {e}")
            config = {}
            
        config['system_prompt'] = markdown_body
        config['file_path'] = file_path
        
        return config

# Singleton instance
_loader = None

def get_agent_loader(root_path: str = None) -> AgentLoader:
    global _loader
    if _loader is None:
        _loader = AgentLoader(root_path)
    return _loader
