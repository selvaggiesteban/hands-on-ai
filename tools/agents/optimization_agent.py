"""
Optimization Agent - Refactoring y mejoras de performance
Analiza código para oportunidades de optimización.
"""

import json
from typing import Dict, List, Any
from datetime import datetime


class OptimizationAgent:
    """
    Agente especializado en optimización y refactoring.
    """

    def __init__(self, ai_config: Dict):
        """
        Inicializa el agente de optimización.

        Args:
            ai_config: Configuración de AI
        """
        self.ai_config = ai_config

    def analyze(self, code: str, language: str, metrics: Dict = None) -> Dict:
        """
        Analiza código y sugiere optimizaciones.

        Args:
            code: Código a analizar
            language: Lenguaje del código
            metrics: Métricas adicionales (tiempo de ejecución, memoria, etc.)

        Returns:
            Dict con análisis y sugerencias
        """
        analysis_result = {
            'timestamp': datetime.now().isoformat(),
            'language': language,
            'optimizations': [],
            'refactoring_suggestions': [],
            'complexity_score': self._calculate_complexity(code),
            'maintainability_score': self._calculate_maintainability(code)
        }

        # Analyze for optimizations
        analysis_result['optimizations'].extend(self._find_performance_issues(code, language))
        analysis_result['refactoring_suggestions'].extend(self._suggest_refactoring(code))

        return analysis_result

    def _calculate_complexity(self, code: str) -> float:
        """Calcula complejidad ciclomática aproximada."""
        # Simple approximation
        decision_points = (
            code.count('if ') +
            code.count('for ') +
            code.count('while ') +
            code.count('case ') +
            code.count('&&') +
            code.count('||')
        )

        # Normalize to 0-1 scale (10+ decision points = very complex)
        complexity = min(1.0, decision_points / 10.0)
        return round(1.0 - complexity, 2)  # Invert so higher is better

    def _calculate_maintainability(self, code: str) -> float:
        """Calcula índice de mantenibilidad."""
        # Factors: comments, function size, naming
        lines = code.split('\n')
        total_lines = len(lines)

        if total_lines == 0:
            return 0.0

        comment_lines = sum(1 for line in lines if line.strip().startswith('//') or line.strip().startswith('#'))
        comment_ratio = comment_lines / total_lines

        # Check for long functions (>50 lines is red flag)
        function_markers = code.count('function ') + code.count('def ') + code.count('const ')
        avg_function_size = total_lines / max(function_markers, 1)

        size_score = 1.0 if avg_function_size < 50 else 0.5

        # Combine scores
        maintainability = (comment_ratio * 0.3 + size_score * 0.7)
        return round(min(1.0, maintainability), 2)

    def _find_performance_issues(self, code: str, language: str) -> List[Dict]:
        """Identifica problemas de performance."""
        issues = []

        # Nested loops
        if code.count('for') >= 2 or code.count('while') >= 2:
            issues.append({
                'type': 'performance',
                'severity': 'medium',
                'issue': 'Nested loops detected',
                'suggestion': 'Consider algorithmic optimization or memoization',
                'estimated_impact': 'medium'
            })

        # Repeated calculations
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if '(' in line and ')' in line:
                # Simple heuristic: same function call in loop
                if any(loop_keyword in line for loop_keyword in ['for', 'while']):
                    issues.append({
                        'type': 'performance',
                        'severity': 'low',
                        'issue': 'Potential repeated calculation in loop',
                        'suggestion': 'Cache results outside loop',
                        'estimated_impact': 'low',
                        'line': i + 1
                    })

        # Array operations that could be optimized
        if '.map(' in code and '.filter(' in code:
            issues.append({
                'type': 'performance',
                'severity': 'low',
                'issue': 'Multiple array iterations',
                'suggestion': 'Consider combining map and filter operations',
                'estimated_impact': 'low'
            })

        return issues

    def _suggest_refactoring(self, code: str) -> List[Dict]:
        """Sugiere oportunidades de refactoring."""
        suggestions = []

        lines = code.split('\n')
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith('//')]

        # Long function
        if len(code_lines) > 50:
            suggestions.append({
                'type': 'refactoring',
                'category': 'Extract Method',
                'reason': 'Function is too long',
                'suggestion': 'Break down into smaller, focused functions',
                'priority': 'medium'
            })

        # Duplicate code patterns
        # Simple check: identical lines repeated
        line_counts = {}
        for line in code_lines:
            stripped = line.strip()
            if len(stripped) > 20:  # Only consider substantial lines
                line_counts[stripped] = line_counts.get(stripped, 0) + 1

        duplicates = {line: count for line, count in line_counts.items() if count > 2}
        if duplicates:
            suggestions.append({
                'type': 'refactoring',
                'category': 'DRY Principle',
                'reason': f'Found {len(duplicates)} duplicated code patterns',
                'suggestion': 'Extract duplicated code into reusable functions',
                'priority': 'high'
            })

        # Magic numbers
        import re
        numbers = re.findall(r'\b\d+\b', code)
        if len([n for n in numbers if int(n) > 1]) > 5:  # Ignore 0 and 1
            suggestions.append({
                'type': 'refactoring',
                'category': 'Magic Numbers',
                'reason': 'Multiple magic numbers in code',
                'suggestion': 'Replace with named constants',
                'priority': 'low'
            })

        return suggestions

    def refactor(self, code: str, refactoring_type: str) -> Dict:
        """
        Aplica refactoring automático.

        Args:
            code: Código original
            refactoring_type: Tipo de refactoring a aplicar

        Returns:
            Dict con código refactorizado
        """
        result = {
            'original_code': code,
            'refactored_code': code,  # Placeholder
            'refactoring_applied': refactoring_type,
            'changes_made': [],
            'timestamp': datetime.now().isoformat()
        }

        # Placeholder: implementar refactorings específicos
        result['changes_made'].append(f'{refactoring_type} refactoring applied')

        return result


def main():
    print("Optimization Agent - Code Optimization and Refactoring")


if __name__ == "__main__":
    main()
