"""
Planning Metrics Dashboard - Métricas de salud del planning
Monitors planning completeness, consistency and actionability.
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime


class PlanningMetrics:
    """
    Calcula métricas de salud del planning.
    """

    def __init__(self, plan_path: str, product_path: str):
        self.plan_path = plan_path
        self.product_path = product_path

        # Load documents
        with open(plan_path, 'r', encoding='utf-8') as f:
            self.plan = json.load(f)

        with open(product_path, 'r', encoding='utf-8') as f:
            self.product = json.load(f)

    def calculate_health_score(self) -> Dict:
        """
        Calcula el health score del planning.

        Returns:
            Dict con scores detallados
        """
        health_score = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': 0.0,
            'scores': {
                'completeness': self.check_all_fields_filled(),
                'consistency': self.validate_cross_references(),
                'actionability': self.count_automatable_tasks(),
                'ai_readiness': self.check_structured_data_quality(),
                'token_efficiency': self.estimate_token_usage()
            }
        }

        # Calculate overall score
        scores = health_score['scores']
        health_score['overall_score'] = sum(scores.values()) / len(scores)

        # Add recommendations
        health_score['recommendations'] = self._generate_recommendations(scores)

        return health_score

    def check_all_fields_filled(self) -> float:
        """Verifica que todos los campos requeridos estén llenos."""
        required_fields = [
            ('plan', ['title', 'metadata', 'sections']),
            ('product', ['title', 'overview', 'coreUserEpicsAndStories'])
        ]

        total_fields = 0
        filled_fields = 0

        for doc_type, fields in required_fields:
            doc = self.plan if doc_type == 'plan' else self.product

            for field in fields:
                total_fields += 1
                if field in doc and doc[field]:
                    filled_fields += 1

        return filled_fields / total_fields if total_fields > 0 else 0.0

    def validate_cross_references(self) -> float:
        """Valida consistencia entre documentos."""
        consistency_score = 1.0

        # Check if tech stack is consistent
        plan_tech = self.plan.get('metadata', {}).get('techStack', '')
        product_tech = self.product.get('metadata', {}).get('projectType', '')

        # Basic consistency checks
        if not plan_tech or not product_tech:
            consistency_score -= 0.2

        # Check if epics have stories
        epics = self.product.get('coreUserEpicsAndStories', {}).get('epics', [])
        for epic in epics:
            if not epic.get('stories', []):
                consistency_score -= 0.1

        return max(0.0, consistency_score)

    def count_automatable_tasks(self) -> float:
        """Cuenta tareas que pueden automatizarse."""
        total_stories = 0
        automatable_stories = 0

        epics = self.product.get('coreUserEpicsAndStories', {}).get('epics', [])

        for epic in epics:
            stories = epic.get('stories', [])
            total_stories += len(stories)

            for story in stories:
                # Story is automatable if it has labels and acceptance criteria
                if story.get('labels') and story.get('acceptanceCriteria'):
                    automatable_stories += 1

        return automatable_stories / total_stories if total_stories > 0 else 0.0

    def check_structured_data_quality(self) -> float:
        """Verifica calidad de datos estructurados para AI."""
        quality_score = 1.0

        # Check if AI optimization config exists
        if 'ai_optimization' not in self.plan:
            quality_score -= 0.3

        if 'ai_optimization' not in self.product:
            quality_score -= 0.2

        # Check if stories have proper labels
        epics = self.product.get('coreUserEpicsAndStories', {}).get('epics', [])
        stories_with_labels = 0
        total_stories = 0

        for epic in epics:
            stories = epic.get('stories', [])
            total_stories += len(stories)
            stories_with_labels += sum(1 for s in stories if s.get('labels'))

        if total_stories > 0:
            label_ratio = stories_with_labels / total_stories
            quality_score *= label_ratio

        return max(0.0, quality_score)

    def estimate_token_usage(self) -> float:
        """Estima eficiencia de tokens."""
        # Simple estimation: smaller planning documents are more efficient
        plan_size = len(json.dumps(self.plan))
        product_size = len(json.dumps(self.product))

        total_size = plan_size + product_size

        # Optimal range: 50KB - 200KB
        if total_size < 50000:
            return 0.7  # Too sparse
        elif total_size < 200000:
            return 1.0  # Optimal
        elif total_size < 500000:
            return 0.8  # Acceptable
        else:
            return 0.5  # Too large, needs optimization

    def _generate_recommendations(self, scores: Dict) -> List[str]:
        """Genera recomendaciones basadas en scores."""
        recommendations = []

        if scores['completeness'] < 0.8:
            recommendations.append("Fill in missing fields in planning documents")

        if scores['consistency'] < 0.8:
            recommendations.append("Improve consistency between plan and product overview")

        if scores['actionability'] < 0.7:
            recommendations.append("Add labels and acceptance criteria to more user stories")

        if scores['ai_readiness'] < 0.7:
            recommendations.append("Add AI optimization configuration to planning documents")

        if scores['token_efficiency'] < 0.7:
            recommendations.append("Optimize planning documents for better token efficiency")

        return recommendations

    def generate_report(self) -> str:
        """Genera reporte de métricas."""
        health = self.calculate_health_score()

        report = "# Planning Health Report\n\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        report += f"## Overall Health Score: {health['overall_score']:.1%}\n\n"

        report += "## Detailed Scores\n\n"
        for metric, score in health['scores'].items():
            report += f"- **{metric}**: {score:.1%}\n"

        report += "\n## Recommendations\n\n"
        for i, rec in enumerate(health['recommendations'], 1):
            report += f"{i}. {rec}\n"

        return report


def main():
    """Función principal para testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Planning Metrics Dashboard')
    parser.add_argument('--plan', default='src/project_meta/planning/plan.json')
    parser.add_argument('--product', default='src/project_meta/product_overview/product-overview.json')

    args = parser.parse_args()

    metrics = PlanningMetrics(args.plan, args.product)
    print(metrics.generate_report())


if __name__ == "__main__":
    main()
