"""
Token Budget Manager - Gestión y optimización de tokens para operaciones AI
Tracks token usage and optimizes prompts to stay within budgets.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime


class TokenBudgetManager:
    """
    Gestor de presupuesto de tokens para operaciones AI.
    """

    def __init__(self, model: str = "gpt-4", budget_config_path: str = None):
        """
        Inicializa el gestor de tokens.

        Args:
            model: Modelo AI a utilizar
            budget_config_path: Ruta al archivo token-budget.json
        """
        self.model = model

        # Load budget configuration
        if budget_config_path and os.path.exists(budget_config_path):
            with open(budget_config_path, 'r', encoding='utf-8') as f:
                self.budget_config = json.load(f)
        else:
            self.budget_config = self._default_config()

        # Token counting (simple approximation)
        self.tokens_used = {
            'total': 0,
            'by_operation': {},
            'by_model': {}
        }

        # Budget tracking
        self.budgets = self.budget_config.get('operation_budgets', {})

    def _default_config(self) -> Dict:
        """Retorna configuración por defecto."""
        return {
            "operation_budgets": {
                "planning": {"max_tokens": 10000},
                "code_generation": {"max_tokens": 8000},
                "review": {"max_tokens": 5000}
            }
        }

    def count_tokens(self, text: str) -> int:
        """
        Cuenta tokens en un texto (aproximación simple).

        Args:
            text: Texto a contar

        Returns:
            Número estimado de tokens
        """
        # Simple approximation: ~4 characters per token
        return len(text) // 4

    def optimize_prompt(self, prompt: str, task_type: str) -> str:
        """
        Optimiza un prompt para que no exceda el presupuesto.

        Args:
            prompt: Prompt original
            task_type: Tipo de tarea

        Returns:
            Prompt optimizado
        """
        tokens = self.count_tokens(prompt)
        budget = self.budgets.get(task_type, {}).get('max_tokens', 5000)

        if tokens > budget:
            # Compress prompt
            compressed = self.extract_essential_context(prompt, budget)
            return compressed
        return prompt

    def extract_essential_context(self, prompt: str, target_tokens: int) -> str:
        """
        Extrae contexto esencial del prompt para reducir tokens.

        Args:
            prompt: Prompt original
            target_tokens: Tokens objetivo

        Returns:
            Contexto comprimido
        """
        current_tokens = self.count_tokens(prompt)

        if current_tokens <= target_tokens:
            return prompt

        # Strategy: Keep first and last parts, summarize middle
        lines = prompt.split('\n')
        target_lines = int(len(lines) * (target_tokens / current_tokens))

        # Keep structure
        keep_start = lines[:target_lines // 2]
        keep_end = lines[-(target_lines // 2):]

        compressed = '\n'.join(keep_start)
        compressed += '\n\n[... content summarized for brevity ...]\n\n'
        compressed += '\n'.join(keep_end)

        return compressed

    def track_usage(self, operation: str, tokens_input: int, tokens_output: int):
        """
        Registra el uso de tokens.

        Args:
            operation: Tipo de operación
            tokens_input: Tokens de input
            tokens_output: Tokens de output
        """
        total = tokens_input + tokens_output

        self.tokens_used['total'] += total

        if operation not in self.tokens_used['by_operation']:
            self.tokens_used['by_operation'][operation] = 0
        self.tokens_used['by_operation'][operation] += total

        if self.model not in self.tokens_used['by_model']:
            self.tokens_used['by_model'][self.model] = 0
        self.tokens_used['by_model'][self.model] += total

    def calculate_cost(self) -> Dict:
        """
        Calcula el costo de los tokens usados.

        Returns:
            Dict con costos por modelo y operación
        """
        costs = {
            'total_cost_usd': 0.0,
            'by_model': {},
            'by_operation': {}
        }

        # Get cost rates from config
        models = self.budget_config.get('models', {})

        for model_name, tokens in self.tokens_used['by_model'].items():
            model_config = models.get(model_name, {})
            cost_per_1k = model_config.get('cost_per_1k_input', 0.01)

            cost = (tokens / 1000) * cost_per_1k
            costs['by_model'][model_name] = cost
            costs['total_cost_usd'] += cost

        return costs

    def get_budget_status(self, operation: str) -> Dict:
        """
        Obtiene el estado del presupuesto para una operación.

        Args:
            operation: Tipo de operación

        Returns:
            Dict con estado del presupuesto
        """
        budget = self.budgets.get(operation, {}).get('max_tokens', 0)
        used = self.tokens_used['by_operation'].get(operation, 0)
        remaining = max(0, budget - used)

        return {
            'operation': operation,
            'budget': budget,
            'used': used,
            'remaining': remaining,
            'percentage_used': (used / budget * 100) if budget > 0 else 0,
            'within_budget': used <= budget
        }

    def generate_report(self) -> str:
        """
        Genera un reporte de uso de tokens.

        Returns:
            String con el reporte
        """
        report = "# Token Usage Report\n\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        report += "## Summary\n\n"
        report += f"Total tokens used: {self.tokens_used['total']:,}\n\n"

        report += "## By Operation\n\n"
        for operation, tokens in self.tokens_used['by_operation'].items():
            budget_status = self.get_budget_status(operation)
            report += f"- **{operation}**: {tokens:,} tokens "
            report += f"({budget_status['percentage_used']:.1f}% of budget)\n"

        report += "\n## By Model\n\n"
        for model, tokens in self.tokens_used['by_model'].items():
            report += f"- **{model}**: {tokens:,} tokens\n"

        report += "\n## Costs\n\n"
        costs = self.calculate_cost()
        report += f"Total estimated cost: ${costs['total_cost_usd']:.2f}\n\n"

        for model, cost in costs['by_model'].items():
            report += f"- **{model}**: ${cost:.2f}\n"

        return report

    def save_metrics(self, output_path: str = "./data/token_metrics.json"):
        """
        Guarda métricas de tokens en archivo.

        Args:
            output_path: Ruta del archivo de salida
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        metrics = {
            'timestamp': datetime.now().isoformat(),
            'model': self.model,
            'tokens_used': self.tokens_used,
            'costs': self.calculate_cost(),
            'budget_status': {
                op: self.get_budget_status(op)
                for op in self.tokens_used['by_operation'].keys()
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2)

        print(f"✓ Metrics saved to {output_path}")


def main():
    """Función principal para testing."""
    print("Token Budget Manager\n")

    manager = TokenBudgetManager()

    # Simulate some usage
    manager.track_usage('planning', 1500, 500)
    manager.track_usage('code_generation', 3000, 2000)
    manager.track_usage('review', 800, 200)

    # Generate report
    print(manager.generate_report())

    # Save metrics
    manager.save_metrics()


if __name__ == "__main__":
    main()
