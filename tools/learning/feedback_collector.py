"""
AI Feedback Loop - Aprende de cambios manuales al código generado
Continuous learning system.
"""

import json
import os
from typing import Dict, List
from datetime import datetime
import difflib


class AIFeedbackLoop:
    """
    Sistema de feedback loop para aprendizaje continuo.
    """

    def __init__(self, learning_db_path: str = "./data/learning_db.json"):
        self.learning_db_path = learning_db_path
        self.learning_examples = []

        # Load existing learning data
        if os.path.exists(learning_db_path):
            with open(learning_db_path, 'r', encoding='utf-8') as f:
                self.learning_examples = json.load(f)

    def collect_metrics(self, generated_code: str, human_changes: str, task: Dict) -> Dict:
        """
        Recolecta métricas y aprende de los cambios manuales.

        Args:
            generated_code: Código generado por AI
            human_changes: Código modificado por humano
            task: Tarea original

        Returns:
            Dict con análisis del feedback
        """
        diff = self.compute_diff(generated_code, human_changes)

        learning_example = {
            'timestamp': datetime.now().isoformat(),
            'task_type': task.get('type', 'unknown'),
            'task_id': task.get('id', 'unknown'),
            'ai_output': generated_code,
            'human_fix': human_changes,
            'diff': diff,
            'patterns_identified': self._identify_patterns(diff),
            'feedback_score': self._calculate_feedback_score(diff)
        }

        self.learning_examples.append(learning_example)
        self._save_learning_data()

        return learning_example

    def compute_diff(self, original: str, modified: str) -> Dict:
        """Calcula diff entre código original y modificado."""
        diff = list(difflib.unified_diff(
            original.splitlines(),
            modified.splitlines(),
            lineterm=''
        ))

        added_lines = [line for line in diff if line.startswith('+') and not line.startswith('+++')]
        removed_lines = [line for line in diff if line.startswith('-') and not line.startswith('---')]

        return {
            'total_changes': len(added_lines) + len(removed_lines),
            'added_lines': len(added_lines),
            'removed_lines': len(removed_lines),
            'diff_text': '\n'.join(diff)
        }

    def _identify_patterns(self, diff: Dict) -> List[str]:
        """Identifica patrones en los cambios."""
        patterns = []

        diff_text = diff.get('diff_text', '')

        # Common patterns
        if 'error' in diff_text.lower() or 'try' in diff_text.lower():
            patterns.append('error_handling_improvement')

        if 'validate' in diff_text.lower():
            patterns.append('validation_added')

        if 'test' in diff_text.lower():
            patterns.append('test_improvement')

        if 'comment' in diff_text or '//' in diff_text or '/*' in diff_text:
            patterns.append('documentation_improvement')

        return patterns

    def _calculate_feedback_score(self, diff: Dict) -> float:
        """
        Calcula score de feedback (0-1).
        Menor cambio = mejor score original.
        """
        total_changes = diff.get('total_changes', 0)

        if total_changes == 0:
            return 1.0
        elif total_changes < 5:
            return 0.9
        elif total_changes < 10:
            return 0.7
        elif total_changes < 20:
            return 0.5
        else:
            return 0.3

    def _save_learning_data(self):
        """Guarda datos de aprendizaje."""
        os.makedirs(os.path.dirname(self.learning_db_path), exist_ok=True)

        with open(self.learning_db_path, 'w', encoding='utf-8') as f:
            json.dump(self.learning_examples, f, indent=2, ensure_ascii=False)

    def get_insights(self) -> Dict:
        """Obtiene insights del feedback recolectado."""
        if not self.learning_examples:
            return {'message': 'No learning data available'}

        total_examples = len(self.learning_examples)
        avg_score = sum(ex['feedback_score'] for ex in self.learning_examples) / total_examples

        # Pattern frequency
        all_patterns = []
        for ex in self.learning_examples:
            all_patterns.extend(ex.get('patterns_identified', []))

        pattern_freq = {}
        for pattern in set(all_patterns):
            pattern_freq[pattern] = all_patterns.count(pattern)

        return {
            'total_examples': total_examples,
            'average_feedback_score': avg_score,
            'common_patterns': pattern_freq,
            'recommendation': 'Focus on improving' + str(list(pattern_freq.keys())[:3]) if pattern_freq else 'code generation'
        }


def main():
    print("AI Feedback Loop - Continuous Learning")


if __name__ == "__main__":
    main()
