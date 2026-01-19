"""
Review Agent - Code review automático
Analiza código generado para calidad, performance y mejores prácticas.
"""

import json
from typing import Dict, List, Any
from datetime import datetime


class ReviewAgent:
    """
    Agente especializado en code review automático.
    """

    def __init__(self, ai_config: Dict):
        """
        Inicializa el agente de review.

        Args:
            ai_config: Configuración de AI
        """
        self.ai_config = ai_config
        self.quality_gates = {}

    def review_code(self, code: str, language: str, context: Dict = None) -> Dict:
        """
        Revisa código y proporciona feedback.

        Args:
            code: Código a revisar
            language: Lenguaje del código
            context: Contexto adicional

        Returns:
            Dict con resultado del review
        """
        review_result = {
            'timestamp': datetime.now().isoformat(),
            'language': language,
            'status': 'completed',
            'score': 0,
            'issues': [],
            'suggestions': [],
            'approved': False
        }

        # Run checks
        review_result['issues'].extend(self._check_code_quality(code, language))
        review_result['issues'].extend(self._check_security_patterns(code))
        review_result['issues'].extend(self._check_performance(code))
        review_result['suggestions'].extend(self._generate_suggestions(code, language))

        # Calculate score
        review_result['score'] = self._calculate_score(review_result['issues'])
        review_result['approved'] = review_result['score'] >= 0.8

        return review_result

    def _check_code_quality(self, code: str, language: str) -> List[Dict]:
        """Verifica calidad del código."""
        issues = []

        # Check for TODO/FIXME comments
        if 'TODO' in code or 'FIXME' in code:
            issues.append({
                'severity': 'low',
                'category': 'code_quality',
                'message': 'Contains TODO/FIXME comments',
                'line': None
            })

        # Check for console.log (if JavaScript/TypeScript)
        if language in ['javascript', 'typescript', 'typescriptreact', 'javascriptreact'] and 'console.log' in code:
            issues.append({
                'severity': 'medium',
                'category': 'code_quality',
                'message': 'Contains console.log statements - use proper logging',
                'line': None
            })

        # CRITICAL: TypeScript 'any' type check
        if language in ['typescript', 'typescriptreact'] and ': any' in code:
            issues.append({
                'severity': 'high',
                'category': 'type_safety',
                'message': 'Usage of "any" type is forbidden. Define explicit interfaces.',
                'line': None
            })

        # Next.js Server Actions check (basic heuristic)
        if language in ['typescript', 'typescriptreact', 'javascript', 'javascriptreact']:
            if 'use server' in code and 'export default function' in code:
                 issues.append({
                    'severity': 'medium',
                    'category': 'architecture',
                    'message': 'Potential mix of UI component and Server Actions. Verify "use server" is in a separate file or restricted scope.',
                    'line': None
                })

        return issues

    def _check_security_patterns(self, code: str) -> List[Dict]:
        """Verifica patrones de seguridad."""
        issues = []

        # Check for common security issues
        dangerous_patterns = [
            ('eval(', 'high', 'Use of eval() is dangerous'),
            ('exec(', 'high', 'Use of exec() is dangerous'),
            ('innerHTML', 'medium', 'innerHTML can lead to XSS - use textContent or sanitize'),
        ]

        for pattern, severity, message in dangerous_patterns:
            if pattern in code:
                issues.append({
                    'severity': severity,
                    'category': 'security',
                    'message': message,
                    'line': None
                })

        return issues

    def _check_performance(self, code: str) -> List[Dict]:
        """Verifica performance."""
        issues = []

        # Simple performance checks
        if code.count('for') > 3:
            issues.append({
                'severity': 'low',
                'category': 'performance',
                'message': 'Multiple nested loops detected - consider optimization',
                'line': None
            })

        return issues

    def _generate_suggestions(self, code: str, language: str) -> List[str]:
        """Genera sugerencias de mejora."""
        suggestions = []

        suggestions.append("Consider adding JSDoc/docstring comments")
        suggestions.append("Ensure proper error handling")
        suggestions.append("Add input validation")

        return suggestions

    def _calculate_score(self, issues: List[Dict]) -> float:
        """Calcula score basado en issues."""
        if not issues:
            return 1.0

        severity_weights = {
            'critical': 0.3,
            'high': 0.15,
            'medium': 0.05,
            'low': 0.02
        }

        total_deduction = sum(
            severity_weights.get(issue['severity'], 0.02)
            for issue in issues
        )

        return max(0.0, 1.0 - total_deduction)


def main():
    print("Review Agent - Automated Code Review")


if __name__ == "__main__":
    main()
