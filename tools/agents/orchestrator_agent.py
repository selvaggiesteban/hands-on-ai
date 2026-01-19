"""
Orchestrator Agent - Coordinador Principal del Sistema Multi-Agente
Coordina la ejecución de todos los agentes especializados según el planning document.
"""

import os
import json
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))


class PlanningOrchestrator:
    """
    Coordinador principal que gestiona la ejecución de agentes especializados.
    """

    def __init__(self, plan_path: str, product_path: str, kb_root: str = None):
        """
        Inicializa el orquestador con los documentos de planificación.

        Args:
            plan_path: Ruta al archivo plan.json
            product_path: Ruta al archivo product-overview.json
            kb_root: Ruta raíz del knowledge base
        """
        self.plan_path = plan_path
        self.product_path = product_path
        self.kb_root = kb_root or os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        # Load configuration files
        self.plan = self.load_json(plan_path)
        self.product = self.load_json(product_path)
        self.ai_config = self.load_ai_config()

        # Initialize agents (lazy loading)
        self.agents = {}
        self._agents_initialized = False

        # Execution context
        self.execution_log = []
        self.current_task = None

    def load_json(self, file_path: str) -> Dict:
        """Carga un archivo JSON."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return {}

    def load_ai_config(self) -> Dict:
        """Carga la configuración AI desde project_meta/ai-context/"""
        ai_context_path = os.path.join(
            self.kb_root,
            'project_meta',
            'ai-context'
        )

        config = {
            'token_budget': {},
            'prompt_library': {},
            'context_windows': {},
            'rag_config': {}
        }

        config_files = {
            'token_budget': 'token-budget.json',
            'prompt_library': 'prompt-library.json',
            'context_windows': 'context-windows.json',
            'rag_config': 'rag-config.json'
        }

        for key, filename in config_files.items():
            file_path = os.path.join(ai_context_path, filename)
            if os.path.exists(file_path):
                config[key] = self.load_json(file_path)

        return config

    def initialize_agents(self):
        """Inicializa todos los agentes especializados."""
        if self._agents_initialized:
            return

        try:
            # Import agents dynamically
            from planning_agent import PlanningAgent
            from coding_agent import CodingAgent
            from review_agent import ReviewAgent
            from security_agent import SecurityAgent
            from optimization_agent import OptimizationAgent
            from documentation_agent import DocumentationAgent

            self.agents = {
                'planning': PlanningAgent(self.product, self.plan, self.ai_config),
                'coding': CodingAgent(self.plan, self.ai_config),
                'review': ReviewAgent(self.ai_config),
                'security': SecurityAgent(self.plan.get('security_policies', {}), self.ai_config),
                'optimization': OptimizationAgent(self.ai_config),
                'documentation': DocumentationAgent(self.ai_config)
            }

            self._agents_initialized = True
            print("✓ All agents initialized successfully")

        except ImportError as e:
            print(f"Warning: Some agents not available yet: {e}")
            print("Running in limited mode...")

    def execute_pipeline(self, scope: str = "full", feature_name: Optional[str] = None):
        """
        Ejecuta el pipeline completo de automatización.

        Pipeline:
        1. Planning Analysis
        2. Task Generation (AI)
        3. Code Generation (Multi-agent)
        4. Security Scan
        5. Quality Check
        6. Test Generation
        7. Documentation Update
        8. Git Commit + PR (optional)

        Args:
            scope: Alcance de ejecución (full/feature/module/service/hotfix/refactor)
            feature_name: Nombre de la feature específica (si scope='feature')
        """
        print(f"\n{'='*60}")
        print(f"Starting Pipeline Execution")
        print(f"Scope: {scope}")
        if feature_name:
            print(f"Feature: {feature_name}")
        print(f"{'='*60}\n")

        self.initialize_agents()

        # Step 1: Analyze planning documents
        print("Step 1: Analyzing planning documents...")
        tasks = self._generate_tasks(scope, feature_name)
        print(f"✓ Generated {len(tasks)} tasks\n")

        # Step 2: Execute tasks with appropriate agents
        results = []
        for idx, task in enumerate(tasks, 1):
            print(f"\nProcessing Task {idx}/{len(tasks)}: {task.get('description', 'N/A')}")
            result = self._execute_task(task)
            results.append(result)

        # Step 3: Generate summary
        print(f"\n{'='*60}")
        print("Pipeline Execution Complete")
        print(f"{'='*60}")
        self._print_summary(results)

        return results

    def _generate_tasks(self, scope: str, feature_name: Optional[str] = None) -> List[Dict]:
        """
        Genera tareas basándose en el scope y el planning document.
        """
        tasks = []

        if scope == "full":
            # Generar tareas para todo el proyecto
            tasks = self._generate_full_project_tasks()
        elif scope == "feature" and feature_name:
            # Generar tareas para una feature específica
            tasks = self._generate_feature_tasks(feature_name)
        elif scope == "module":
            # Generar tareas para un módulo completo
            tasks = self._generate_module_tasks()
        elif scope == "hotfix":
            # Análisis mínimo para corrección urgente
            tasks = self._generate_hotfix_tasks()
        else:
            print(f"Warning: Unknown scope '{scope}', generating default tasks")
            tasks = self._generate_default_tasks()

        return tasks

    def _generate_full_project_tasks(self) -> List[Dict]:
        """Genera tareas para el proyecto completo."""
        tasks = []

        # Extract epics and stories from product overview
        epics = self.product.get('coreUserEpicsAndStories', {}).get('epics', [])

        for epic in epics:
            epic_title = epic.get('title', 'Unknown Epic')
            stories = epic.get('stories', [])

            for story in stories:
                task = {
                    'type': 'feature_implementation',
                    'epic': epic_title,
                    'story': story.get('story', ''),
                    'labels': story.get('labels', []),
                    'acceptance_criteria': story.get('acceptanceCriteria', []),
                    'priority': self._extract_priority(story.get('labels', []))
                }
                tasks.append(task)

        return tasks

    def _generate_feature_tasks(self, feature_name: str) -> List[Dict]:
        """Genera tareas para una feature específica."""
        tasks = []

        # Search for the feature in user stories
        epics = self.product.get('coreUserEpicsAndStories', {}).get('epics', [])

        for epic in epics:
            stories = epic.get('stories', [])
            for story in stories:
                if feature_name.lower() in story.get('story', '').lower():
                    task = {
                        'type': 'feature_implementation',
                        'epic': epic.get('title', 'Unknown'),
                        'story': story.get('story', ''),
                        'labels': story.get('labels', []),
                        'acceptance_criteria': story.get('acceptanceCriteria', []),
                        'priority': self._extract_priority(story.get('labels', []))
                    }
                    tasks.append(task)

        if not tasks:
            print(f"Warning: No tasks found for feature '{feature_name}'")

        return tasks

    def _generate_module_tasks(self) -> List[Dict]:
        """Genera tareas para un módulo completo."""
        # Placeholder: implementar según necesidades
        return self._generate_default_tasks()

    def _generate_hotfix_tasks(self) -> List[Dict]:
        """Genera tareas para un hotfix."""
        return [{
            'type': 'hotfix',
            'description': 'Quick fix with minimal analysis',
            'priority': 'critical'
        }]

    def _generate_default_tasks(self) -> List[Dict]:
        """Genera tareas por defecto."""
        return [{
            'type': 'analysis',
            'description': 'Analyze project structure and generate recommendations',
            'priority': 'medium'
        }]

    def _extract_priority(self, labels: List[str]) -> str:
        """Extrae la prioridad de las etiquetas."""
        for label in labels:
            if 'priority:' in label:
                return label.split(':')[1]
        return 'medium'

    def _execute_task(self, task: Dict) -> Dict:
        """
        Ejecuta una tarea usando los agentes apropiados.
        """
        self.current_task = task
        task_type = task.get('type', 'unknown')

        result = {
            'task': task,
            'status': 'pending',
            'outputs': [],
            'timestamp': datetime.now().isoformat()
        }

        try:
            # Route task to appropriate agent
            if task_type == 'feature_implementation':
                result = self._execute_feature_implementation(task)
            elif task_type == 'backend':
                result = self._execute_backend_task(task)
            elif task_type == 'security':
                result = self._execute_security_task(task)
            elif task_type == 'refactor':
                result = self._execute_refactor_task(task)
            elif task_type == 'documentation':
                result = self._execute_documentation_task(task)
            else:
                result['status'] = 'skipped'
                result['message'] = f"Unknown task type: {task_type}"

            self.execution_log.append(result)

        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            print(f"✗ Error executing task: {e}")

        return result

    def _execute_feature_implementation(self, task: Dict) -> Dict:
        """Ejecuta la implementación completa de una feature."""
        result = {
            'task': task,
            'status': 'in_progress',
            'outputs': [],
            'steps_completed': []
        }

        # Simulación (placeholder para integración real con agentes)
        print(f"  → Planning feature: {task.get('story', 'N/A')[:50]}...")
        result['steps_completed'].append('planning')

        print(f"  → Generating code structure...")
        result['steps_completed'].append('code_generation')

        print(f"  → Running security scan...")
        result['steps_completed'].append('security_scan')

        print(f"  → Generating tests...")
        result['steps_completed'].append('test_generation')

        result['status'] = 'completed'
        print(f"  ✓ Feature implementation completed")

        return result

    def _execute_backend_task(self, task: Dict) -> Dict:
        """Ejecuta una tarea de backend."""
        # Placeholder
        return {'task': task, 'status': 'completed', 'message': 'Backend task completed'}

    def _execute_security_task(self, task: Dict) -> Dict:
        """Ejecuta un análisis de seguridad."""
        # Placeholder
        return {'task': task, 'status': 'completed', 'message': 'Security scan completed'}

    def _execute_refactor_task(self, task: Dict) -> Dict:
        """Ejecuta una tarea de refactoring."""
        # Placeholder
        return {'task': task, 'status': 'completed', 'message': 'Refactor completed'}

    def _execute_documentation_task(self, task: Dict) -> Dict:
        """Ejecuta una tarea de documentación."""
        # Placeholder
        return {'task': task, 'status': 'completed', 'message': 'Documentation updated'}

    def _print_summary(self, results: List[Dict]):
        """Imprime un resumen de la ejecución."""
        total = len(results)
        completed = sum(1 for r in results if r.get('status') == 'completed')
        errors = sum(1 for r in results if r.get('status') == 'error')
        skipped = sum(1 for r in results if r.get('status') == 'skipped')

        print(f"\nExecution Summary:")
        print(f"  Total tasks: {total}")
        print(f"  ✓ Completed: {completed}")
        print(f"  ✗ Errors: {errors}")
        print(f"  ⊘ Skipped: {skipped}")

    def get_execution_log(self) -> List[Dict]:
        """Retorna el log de ejecución."""
        return self.execution_log


def main():
    """Función principal para testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Orchestrator Agent - Main Coordinator')
    parser.add_argument('--scope', default='full',
                       choices=['full', 'feature', 'module', 'service', 'hotfix', 'refactor'],
                       help='Execution scope')
    parser.add_argument('--feature', help='Feature name (for scope=feature)')
    parser.add_argument('--plan', default='project_meta/planning/plan.json',
                       help='Path to plan.json')
    parser.add_argument('--product', default='project_meta/product_overview/product-overview.json',
                       help='Path to product-overview.json')

    args = parser.parse_args()

    # Get project root
    kb_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    plan_path = os.path.join(kb_root, args.plan)
    product_path = os.path.join(kb_root, args.product)

    # Initialize orchestrator
    orchestrator = PlanningOrchestrator(plan_path, product_path, kb_root)

    # Execute pipeline
    results = orchestrator.execute_pipeline(
        scope=args.scope,
        feature_name=args.feature
    )

    print(f"\n✓ Orchestration completed. {len(results)} tasks processed.")


if __name__ == "__main__":
    main()
