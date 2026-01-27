
import os
import sys

sys.path.append(os.path.join(os.getcwd(), 'tools', 'ai_wrapper'))
from agent_loader import get_agent_loader

def count_agents():
    loader = get_agent_loader()
    agents = loader.list_agents()
    print(f"Total MD agents found: {len(agents)}")
    
    # Categorize
    categories = {}
    for name in agents:
        cat = name.split('/')[0] if '/' in name else 'root'
        categories[cat] = categories.get(cat, 0) + 1
        
    print("\nBreakdown by category:")
    for cat, count in categories.items():
        print(f"  {cat}: {count}")

if __name__ == "__main__":
    count_agents()

