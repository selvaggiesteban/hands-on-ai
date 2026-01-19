"""
Multi-Model Processor - Procesamiento Multi-Modelo para Hands On AI
Implementa: rotación equitativa, ejecución paralela, merge inteligente, junta directiva.
"""

import asyncio
import os
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import deque

from .providers.base import BaseProvider, AIResponse, Message
from .providers.openai_provider import OpenAIProvider
from .providers.anthropic_provider import AnthropicProvider
from .providers.gemini_provider import GeminiProvider


@dataclass
class MultiModelConfig:
    """Configuración del procesador multi-modelo."""
    # Límites configurables
    max_requests_per_day: int = 1000
    max_tokens_per_day: int = 1_000_000
    max_cost_per_day_usd: float = 50.0

    # Modo de procesamiento
    parallel_execution: bool = True
    use_round_robin: bool = True
    use_board_evaluation: bool = True
    use_intelligent_merge: bool = True

    # Proveedores activos
    enabled_providers: List[str] = field(default_factory=lambda: ['openai', 'anthropic', 'gemini'])

    # Modelo evaluador para junta directiva
    board_evaluator_provider: str = 'anthropic'
    board_evaluator_model: str = 'claude-sonnet-4-5-20250929'


@dataclass
class ProcessingResult:
    """Resultado del procesamiento multi-modelo."""
    final_response: str
    selected_provider: str
    all_responses: List[AIResponse]
    board_evaluation: Optional[Dict] = None
    merge_info: Optional[Dict] = None
    total_cost_usd: float = 0.0
    total_tokens: int = 0
    total_latency_ms: int = 0
    processing_mode: str = "single"


class RoundRobinRotator:
    """Rotación equitativa entre proveedores."""

    def __init__(self, providers: List[str]):
        self.providers = deque(providers)
        self.rotation_count = 0

    def get_next(self) -> str:
        """Obtiene el siguiente proveedor en rotación."""
        if not self.providers:
            return None
        provider = self.providers[0]
        self.providers.rotate(-1)
        self.rotation_count += 1
        return provider

    def get_order(self) -> List[str]:
        """Retorna el orden actual de rotación."""
        return list(self.providers)

    def reset(self):
        """Reinicia la rotación."""
        self.rotation_count = 0


class UsageLimits:
    """Control de límites de uso."""

    def __init__(self, config: MultiModelConfig):
        self.config = config
        self.daily_requests = 0
        self.daily_tokens = 0
        self.daily_cost = 0.0
        self.last_reset = datetime.now().date()

    def check_and_reset(self):
        """Verifica si hay que resetear contadores diarios."""
        today = datetime.now().date()
        if today > self.last_reset:
            self.daily_requests = 0
            self.daily_tokens = 0
            self.daily_cost = 0.0
            self.last_reset = today

    def can_proceed(self) -> Tuple[bool, str]:
        """Verifica si se puede proceder con una solicitud."""
        self.check_and_reset()

        if self.daily_requests >= self.config.max_requests_per_day:
            return False, f"Límite de solicitudes diarias alcanzado ({self.config.max_requests_per_day})"

        if self.daily_tokens >= self.config.max_tokens_per_day:
            return False, f"Límite de tokens diarios alcanzado ({self.config.max_tokens_per_day})"

        if self.daily_cost >= self.config.max_cost_per_day_usd:
            return False, f"Límite de costo diario alcanzado (${self.config.max_cost_per_day_usd})"

        return True, "OK"

    def record_usage(self, tokens: int, cost: float):
        """Registra uso de una solicitud."""
        self.daily_requests += 1
        self.daily_tokens += tokens
        self.daily_cost += cost

    def get_status(self) -> Dict:
        """Retorna estado actual de límites."""
        self.check_and_reset()
        return {
            'daily_requests': f"{self.daily_requests}/{self.config.max_requests_per_day}",
            'daily_tokens': f"{self.daily_tokens}/{self.config.max_tokens_per_day}",
            'daily_cost_usd': f"${self.daily_cost:.4f}/${self.config.max_cost_per_day_usd}",
            'last_reset': str(self.last_reset)
        }


class MultiModelProcessor:
    """
    Procesador Multi-Modelo Principal.
    Coordina múltiples proveedores de IA con rotación, paralelismo, merge y evaluación.
    """

    def __init__(self, config: MultiModelConfig = None):
        self.config = config or MultiModelConfig()
        self.providers: Dict[str, BaseProvider] = {}
        self.rotator = RoundRobinRotator(self.config.enabled_providers)
        self.limits = UsageLimits(self.config)

        # Cargar API keys desde .env o variables de entorno
        self._load_providers()

    def _load_providers(self):
        """Carga proveedores desde variables de entorno."""
        # Buscar .env en hands-on-ai-master
        root_dir = Path(__file__).parent.parent.parent
        env_file = root_dir / '.env'

        env_vars = {}
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()

        # OpenAI
        openai_key = env_vars.get('OPENAI_API_KEY') or os.environ.get('OPENAI_API_KEY')
        if openai_key and 'openai' in self.config.enabled_providers:
            openai_model = env_vars.get('OPENAI_MODEL', 'gpt-4o')
            self.providers['openai'] = OpenAIProvider(openai_key, openai_model)

        # Anthropic
        anthropic_key = env_vars.get('ANTHROPIC_API_KEY') or os.environ.get('ANTHROPIC_API_KEY')
        if anthropic_key and 'anthropic' in self.config.enabled_providers:
            anthropic_model = env_vars.get('ANTHROPIC_MODEL', 'claude-sonnet-4-5-20250929')
            self.providers['anthropic'] = AnthropicProvider(anthropic_key, anthropic_model)

        # Gemini
        gemini_key = env_vars.get('GEMINI_API_KEY') or env_vars.get('AI_API_KEY') or os.environ.get('GEMINI_API_KEY')
        if gemini_key and 'gemini' in self.config.enabled_providers:
            gemini_model = env_vars.get('GEMINI_MODEL') or env_vars.get('AI_MODEL', 'gemini-2.5-flash')
            self.providers['gemini'] = GeminiProvider(gemini_key, gemini_model)

        # Actualizar rotador con proveedores disponibles
        available = [name for name, prov in self.providers.items() if prov.is_available]
        self.rotator = RoundRobinRotator(available)

    def get_available_providers(self) -> List[str]:
        """Retorna lista de proveedores disponibles."""
        return [name for name, prov in self.providers.items() if prov.is_available]

    async def process_single(
        self,
        prompt: str = None,
        messages: List[Message] = None,
        system_prompt: Optional[str] = None,
        provider: Optional[str] = None
    ) -> AIResponse:
        """Procesa con un solo proveedor (usando round-robin si no se especifica)."""
        can_proceed, msg = self.limits.can_proceed()
        if not can_proceed:
            raise Exception(f"Límite alcanzado: {msg}")

        # Construir mensajes
        final_messages = []
        if messages:
            final_messages = messages
        elif prompt:
            final_messages = [Message(role='user', content=prompt)]
        else:
            raise ValueError("Se requiere 'prompt' o 'messages'")

        # Seleccionar proveedor
        if provider and provider in self.providers:
            selected = provider
        elif self.config.use_round_robin:
            selected = self.rotator.get_next()
        else:
            selected = self.get_available_providers()[0] if self.get_available_providers() else None

        if not selected or selected not in self.providers:
            # Intentar fallback si el rotador falló pero hay proveedores cargados
            available = self.get_available_providers()
            if available:
                selected = available[0]
            else:
                raise Exception("No hay proveedores disponibles (verifique API Key)")

        prov = self.providers[selected]
        response = await prov.generate(final_messages, system_prompt)

        self.limits.record_usage(response.tokens_total, response.cost_usd)
        return response

    async def process_parallel(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> List[AIResponse]:
        """Ejecuta el prompt en todos los proveedores en paralelo."""
        can_proceed, msg = self.limits.can_proceed()
        if not can_proceed:
            raise Exception(f"Límite alcanzado: {msg}")

        messages = [Message(role='user', content=prompt)]
        available = self.get_available_providers()

        if not available:
            raise Exception("No hay proveedores disponibles")

        # Ejecutar en paralelo
        tasks = []
        for prov_name in available:
            prov = self.providers[prov_name]
            tasks.append(self._safe_generate(prov, messages, system_prompt))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filtrar respuestas exitosas
        responses = []
        for result in results:
            if isinstance(result, AIResponse):
                responses.append(result)
                self.limits.record_usage(result.tokens_total, result.cost_usd)

        return responses

    async def _safe_generate(
        self,
        provider: BaseProvider,
        messages: List[Message],
        system_prompt: Optional[str]
    ) -> AIResponse:
        """Genera respuesta con manejo de errores."""
        try:
            return await provider.generate(messages, system_prompt)
        except Exception as e:
            # Retornar respuesta de error
            return AIResponse(
                content=f"ERROR: {str(e)}",
                provider=provider.name,
                model=provider.model,
                tokens_input=0,
                tokens_output=0,
                tokens_total=0,
                cost_usd=0,
                latency_ms=0,
                timestamp=datetime.now().isoformat(),
                metadata={'error': str(e)}
            )

    async def intelligent_merge(self, responses: List[AIResponse]) -> Dict:
        """
        Merge inteligente: combina lo mejor de cada respuesta.
        Analiza estructura, completitud y calidad.
        """
        if not responses:
            return {'merged_content': '', 'method': 'none'}

        if len(responses) == 1:
            return {
                'merged_content': responses[0].content,
                'method': 'single',
                'source': responses[0].provider
            }

        # Filtrar respuestas válidas (sin errores)
        valid_responses = [r for r in responses if not r.content.startswith('ERROR:')]

        if not valid_responses:
            return {'merged_content': responses[0].content, 'method': 'fallback'}

        # Criterios de selección automática
        scores = []
        for r in valid_responses:
            score = 0
            content = r.content

            # Longitud razonable (ni muy corta ni excesivamente larga)
            length = len(content)
            if 100 < length < 10000:
                score += 10
            elif length >= 10000:
                score += 5

            # Contiene código (para generación de código)
            if '```' in content or 'def ' in content or 'function ' in content or 'class ' in content:
                score += 15

            # Estructura (tiene secciones, listas)
            if '\n\n' in content:
                score += 5
            if '- ' in content or '* ' in content or '1.' in content:
                score += 5

            # Menor costo (preferir eficiencia)
            score += max(0, 10 - int(r.cost_usd * 100))

            # Menor latencia
            score += max(0, 10 - int(r.latency_ms / 1000))

            scores.append((score, r))

        # Ordenar por score
        scores.sort(key=lambda x: x[0], reverse=True)
        best = scores[0][1]

        return {
            'merged_content': best.content,
            'method': 'auto_select',
            'selected_provider': best.provider,
            'scores': {r.provider: s for s, r in scores}
        }

    async def board_evaluation(
        self,
        prompt: str,
        responses: List[AIResponse],
        system_prompt: Optional[str] = None
    ) -> Dict:
        """
        Junta Directiva: un modelo evalúa las respuestas de los otros.
        Retorna evaluación y recomendación.
        """
        if len(responses) < 2:
            return {
                'recommendation': responses[0].provider if responses else None,
                'reason': 'Solo una respuesta disponible'
            }

        # Preparar prompt de evaluación
        eval_prompt = f"""Eres un evaluador experto de código y respuestas de IA.
El usuario hizo esta solicitud:
---
{prompt}
---

Recibimos estas respuestas de diferentes modelos de IA:

"""
        for i, r in enumerate(responses):
            if not r.content.startswith('ERROR:'):
                eval_prompt += f"""
=== Respuesta {i+1} (Proveedor: {r.provider}, Modelo: {r.model}) ===
{r.content[:2000]}{'...[truncado]' if len(r.content) > 2000 else ''}
"""

        eval_prompt += """
---
Evalúa cada respuesta considerando:
1. Correctitud técnica
2. Completitud
3. Claridad
4. Mejores prácticas

Responde en JSON con este formato exacto:
{
  "evaluations": [
    {"provider": "nombre", "score": 1-10, "strengths": ["..."], "weaknesses": ["..."]}
  ],
  "recommendation": "nombre_del_mejor_proveedor",
  "reason": "explicación breve"
}
"""

        # Usar el evaluador configurado
        evaluator_name = self.config.board_evaluator_provider
        if evaluator_name not in self.providers or not self.providers[evaluator_name].is_available:
            # Fallback: usar cualquier proveedor disponible
            available = self.get_available_providers()
            evaluator_name = available[0] if available else None

        if not evaluator_name:
            return {'recommendation': responses[0].provider, 'reason': 'No hay evaluador disponible'}

        try:
            evaluator = self.providers[evaluator_name]
            eval_response = await evaluator.generate(
                [Message(role='user', content=eval_prompt)],
                system_prompt="Eres un evaluador técnico experto. Responde solo en JSON válido."
            )

            # Parsear respuesta JSON
            content = eval_response.content
            # Buscar JSON en la respuesta
            start = content.find('{')
            end = content.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = content[start:end]
                evaluation = json.loads(json_str)
                evaluation['evaluator'] = evaluator_name
                evaluation['cost_usd'] = eval_response.cost_usd
                return evaluation

        except Exception as e:
            pass

        # Fallback si falla la evaluación
        return {
            'recommendation': responses[0].provider,
            'reason': f'Evaluación falló, usando primera respuesta'
        }

    async def process_multi_model(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> ProcessingResult:
        """
        Procesamiento Multi-Modelo Completo.
        Ejecuta paralelo + merge inteligente + junta directiva.
        """
        # 1. Ejecución paralela
        responses = await self.process_parallel(prompt, system_prompt)

        if not responses:
            raise Exception("Ningún proveedor generó respuesta")

        total_cost = sum(r.cost_usd for r in responses)
        total_tokens = sum(r.tokens_total for r in responses)
        total_latency = max(r.latency_ms for r in responses)  # Paralelo = max latency

        # 2. Merge inteligente
        merge_result = None
        if self.config.use_intelligent_merge:
            merge_result = await self.intelligent_merge(responses)

        # 3. Junta directiva
        board_result = None
        if self.config.use_board_evaluation and len(responses) > 1:
            board_result = await self.board_evaluation(prompt, responses, system_prompt)
            if board_result:
                total_cost += board_result.get('cost_usd', 0)

        # 4. Selección final
        if board_result and 'recommendation' in board_result:
            selected_provider = board_result['recommendation']
            # Buscar respuesta del proveedor recomendado
            final_response = next(
                (r.content for r in responses if r.provider == selected_provider),
                merge_result.get('merged_content', responses[0].content) if merge_result else responses[0].content
            )
        elif merge_result:
            final_response = merge_result.get('merged_content', responses[0].content)
            selected_provider = merge_result.get('selected_provider', responses[0].provider)
        else:
            final_response = responses[0].content
            selected_provider = responses[0].provider

        return ProcessingResult(
            final_response=final_response,
            selected_provider=selected_provider,
            all_responses=responses,
            board_evaluation=board_result,
            merge_info=merge_result,
            total_cost_usd=total_cost,
            total_tokens=total_tokens,
            total_latency_ms=total_latency,
            processing_mode="multi_model"
        )

    def get_status(self) -> Dict:
        """Retorna estado completo del procesador."""
        return {
            'providers': {
                name: prov.get_stats() for name, prov in self.providers.items()
            },
            'available_providers': self.get_available_providers(),
            'rotation_order': self.rotator.get_order(),
            'rotation_count': self.rotator.rotation_count,
            'limits': self.limits.get_status(),
            'config': {
                'parallel_execution': self.config.parallel_execution,
                'use_round_robin': self.config.use_round_robin,
                'use_board_evaluation': self.config.use_board_evaluation,
                'use_intelligent_merge': self.config.use_intelligent_merge
            }
        }
