"""
Planning Agent - Lee documentos de planning y genera tareas ejecutables
Analiza product-overview.json y plan.json para generar tareas granulares.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime


class PlanningAgent:
    """
    Agente especializado en análisis de planning documents y generación de tareas.
    """

    def __init__(self, product_overview: Dict, plan: Dict, ai_config: Dict):
        """
        Inicializa el agente de planning.

        Args:
            product_overview: Diccionario del product-overview.json
            plan: Diccionario del plan.json
            ai_config: Configuración de AI
        """
        self.product_overview = product_overview
        self.plan = plan
        self.ai_config = ai_config

        # Extract key information
        self.epics = self._extract_epics()
        self.stories = self._extract_stories()
        self.roadmap = self._extract_roadmap()
        self.tech_stack = self._extract_tech_stack()

    def _extract_epics(self) -> List[Dict]:
        """Extrae los epics del product overview."""
        return self.product_overview.get('coreUserEpicsAndStories', {}).get('epics', [])

    def _extract_stories(self) -> List[Dict]:
        """Extrae todas las user stories de todos los epics."""
        stories = []
        for epic in self.epics:
            epic_title = epic.get('title', 'Unknown Epic')
            for story in epic.get('stories', []):
                story_with_epic = story.copy()
                story_with_epic['epic'] = epic_title
                stories.append(story_with_epic)
        return stories

    def _extract_roadmap(self) -> List[Dict]:
        """Extrae el development roadmap."""
        return self.product_overview.get('developmentRoadmap', {}).get('phases', [])

    def _extract_tech_stack(self) -> Dict:
        """Extrae el tech stack del plan."""
        return self.plan.get('metadata', {}).get('techStack', 'Not specified')

    def generate_tasks(self, scope: str = "full", filter_labels: Optional[List[str]] = None) -> List[Dict]:
        """
        Genera tareas ejecutables desde user stories.

        Args:
            scope: Alcance (full/mvp/release)
            filter_labels: Filtrar por etiquetas específicas (ej: ['area:backend'])

        Returns:
            Lista de tareas con metadata
        """
        tasks = []

        if scope == "full":
            # Todas las user stories
            stories_to_process = self.stories
        elif scope == "mvp":
            # Solo el primer release
            stories_to_process = self._get_mvp_stories()
        else:
            stories_to_process = self.stories

        # Apply label filtering
        if filter_labels:
            stories_to_process = [
                s for s in stories_to_process
                if any(label in s.get('labels', []) for label in filter_labels)
            ]

        # Convert stories to tasks
        for story in stories_to_process:
            task = self._story_to_task(story)
            tasks.append(task)

        return tasks

    def _get_mvp_stories(self) -> List[Dict]:
        """Obtiene las user stories del MVP (primer release)."""
        mvp_stories = []

        if self.roadmap and len(self.roadmap) > 0:
            first_release = self.roadmap[0]
            mvp_stories_data = first_release.get('stories', [])

            # Match these stories with full story data
            for mvp_story_data in mvp_stories_data:
                mvp_story_text = mvp_story_data.get('story', '')
                # Find full story data
                for full_story in self.stories:
                    if full_story.get('story', '') == mvp_story_text:
                        mvp_stories.append(full_story)
                        break

        return mvp_stories if mvp_stories else self.stories[:3]  # Fallback

    def _story_to_task(self, story: Dict) -> Dict:
        """
        Convierte una user story en una tarea ejecutable.

        Args:
            story: User story dict

        Returns:
            Task dict con metadata completa
        """
        labels = story.get('labels', [])

        # Determine task type and module from labels
        task_type = self._determine_task_type(labels)
        module = self._determine_module(labels)
        priority = self._extract_priority(labels)
        area = self._extract_area(labels)

        task = {
            'id': self._generate_task_id(story),
            'type': task_type,
            'story': story.get('story', ''),
            'epic': story.get('epic', 'Unknown'),
            'module': module,
            'area': area,
            'priority': priority,
            'labels': labels,
            'acceptance_criteria': story.get('acceptanceCriteria', []),
            'created_at': datetime.now().isoformat(),
            'status': 'pending',

            # Technical breakdown
            'estimated_subtasks': self._estimate_subtasks(story, labels),
            'required_agents': self._determine_required_agents(labels),
            'dependencies': [],  # TODO: analyze dependencies

            # Context for AI generation
            'context': {
                'tech_stack': self.tech_stack,
                'security_policies': self.plan.get('security_policies', {}),
                'quality_gates': self.plan.get('quality_gates', {})
            }
        }

        return task

    def _generate_task_id(self, story: Dict) -> str:
        """Genera un ID único para la tarea."""
        # Extract a few keywords from story
        story_text = story.get('story', 'task')
        words = story_text.split()[:3]
        keywords = '-'.join([w.lower().strip('*.,') for w in words])

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"task-{keywords[:30]}-{timestamp}"

    def _determine_task_type(self, labels: List[str]) -> str:
        """Determina el tipo de tarea desde las etiquetas."""
        for label in labels:
            if 'area:' in label:
                area = label.split(':')[1]
                if area in ['frontend', 'ui']:
                    return 'frontend_development'
                elif area in ['backend', 'api']:
                    return 'backend_development'
                elif area in ['database', 'db']:
                    return 'database_development'
                elif area in ['devops', 'infra']:
                    return 'infrastructure'
        return 'feature_development'

    def _determine_module(self, labels: List[str]) -> str:
        """Determina el módulo desde las etiquetas."""
        for label in labels:
            if 'module:' in label:
                return label.split(':')[1]
        return 'general'

    def _extract_priority(self, labels: List[str]) -> str:
        """Extrae la prioridad desde las etiquetas."""
        for label in labels:
            if 'priority:' in label:
                return label.split(':')[1]
        return 'medium'

    def _extract_area(self, labels: List[str]) -> str:
        """Extrae el área desde las etiquetas."""
        for label in labels:
            if 'area:' in label:
                return label.split(':')[1]
        return 'general'

    def _estimate_subtasks(self, story: Dict, labels: List[str]) -> List[str]:
        """
        Estima las subtareas necesarias para completar la user story.
        """
        subtasks = []
        acceptance_criteria = story.get('acceptanceCriteria', [])

        # Basic subtasks for any story
        subtasks.append("Analyze requirements and technical approach")

        # Frontend tasks
        if any('area:frontend' in label for label in labels):
            subtasks.append("Design UI components")
            subtasks.append("Implement frontend logic")
            subtasks.append("Add client-side validation")

        # Backend tasks
        if any('area:backend' in label for label in labels):
            subtasks.append("Design API endpoints")
            subtasks.append("Implement business logic")
            subtasks.append("Add input validation and error handling")
            subtasks.append("Implement data persistence")

        # Database tasks
        if any('module:' in label and 'db' in label.lower() for label in labels):
            subtasks.append("Design database schema")
            subtasks.append("Create migrations")
            subtasks.append("Add database indexes")

        # Testing (always)
        subtasks.append("Write unit tests")
        subtasks.append("Write integration tests")

        # Documentation (always)
        subtasks.append("Update documentation")

        return subtasks

    def _determine_required_agents(self, labels: List[str]) -> List[str]:
        """
        Determina qué agentes son necesarios para ejecutar esta tarea.
        """
        required_agents = ['coding']  # Siempre necesario

        # Always need these
        required_agents.extend(['review', 'security'])

        # Optional based on labels
        if any('area:backend' in label for label in labels):
            required_agents.append('optimization')

        # Documentation for complex features
        required_agents.append('documentation')

        return list(set(required_agents))  # Remove duplicates

    def decompose_epic(self, epic_title: str) -> Dict:
        """
        Descompone un epic en tareas granulares.

        Args:
            epic_title: Título del epic a descomponer

        Returns:
            Dict con el epic y sus tareas descompuestas
        """
        # Find the epic
        epic_data = None
        for epic in self.epics:
            if epic.get('title', '').lower() == epic_title.lower():
                epic_data = epic
                break

        if not epic_data:
            return {'error': f"Epic '{epic_title}' not found"}

        # Generate tasks for all stories in epic
        tasks = []
        for story in epic_data.get('stories', []):
            story_with_epic = story.copy()
            story_with_epic['epic'] = epic_title
            task = self._story_to_task(story_with_epic)
            tasks.append(task)

        return {
            'epic': epic_title,
            'total_stories': len(epic_data.get('stories', [])),
            'total_tasks': len(tasks),
            'tasks': tasks
        }

    def generate_github_issues(self, tasks: List[Dict], output_format: str = "json") -> Any:
        """
        Genera GitHub issues desde las tareas.

        Args:
            tasks: Lista de tareas
            output_format: Formato de salida (json/markdown)

        Returns:
            Issues en el formato solicitado
        """
        issues = []

        for task in tasks:
            issue = {
                'title': f"[{task['module']}] {task['story'][:60]}...",
                'body': self._generate_issue_body(task),
                'labels': task['labels'] + [f"type:{task['type']}", f"priority:{task['priority']}"],
                'assignees': [],
                'milestone': None
            }
            issues.append(issue)

        if output_format == "json":
            return issues
        elif output_format == "markdown":
            return self._issues_to_markdown(issues)
        else:
            return issues

    def _generate_issue_body(self, task: Dict) -> str:
        """Genera el body del GitHub issue."""
        body = f"## User Story\n\n{task['story']}\n\n"
        body += f"## Epic\n\n{task['epic']}\n\n"
        body += f"## Acceptance Criteria\n\n"

        for criteria in task['acceptance_criteria']:
            body += f"- [ ] {criteria}\n"

        body += f"\n## Estimated Subtasks\n\n"
        for subtask in task['estimated_subtasks']:
            body += f"- [ ] {subtask}\n"

        body += f"\n## Technical Context\n\n"
        body += f"- **Tech Stack**: {task['context']['tech_stack']}\n"
        body += f"- **Priority**: {task['priority']}\n"
        body += f"- **Module**: {task['module']}\n"
        body += f"- **Required Agents**: {', '.join(task['required_agents'])}\n"

        return body

    def _issues_to_markdown(self, issues: List[Dict]) -> str:
        """Convierte issues a formato Markdown."""
        md = "# GitHub Issues\n\n"

        for idx, issue in enumerate(issues, 1):
            md += f"## Issue #{idx}: {issue['title']}\n\n"
            md += f"**Labels**: {', '.join(issue['labels'])}\n\n"
            md += issue['body']
            md += "\n\n---\n\n"

        return md


def main():
    """Función principal para testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Planning Agent - Task Generation')
    parser.add_argument('--product', default='project_meta/product_overview/product-overview.json',
                       help='Path to product-overview.json')
    parser.add_argument('--plan', default='project_meta/planning/plan.json',
                       help='Path to plan.json')
    parser.add_argument('--scope', default='full', choices=['full', 'mvp'],
                       help='Scope of task generation')
    parser.add_argument('--output', default='tasks.json',
                       help='Output file for generated tasks')

    args = parser.parse_args()

    # Load planning documents
    with open(args.product, 'r', encoding='utf-8') as f:
        product_overview = json.load(f)

    with open(args.plan, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    # Initialize agent
    agent = PlanningAgent(product_overview, plan, {})

    # Generate tasks
    tasks = agent.generate_tasks(scope=args.scope)

    # Save to file
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

    print(f"✓ Generated {len(tasks)} tasks")
    print(f"✓ Saved to {args.output}")


if __name__ == "__main__":
    main()
