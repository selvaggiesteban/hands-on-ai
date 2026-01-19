"""
Anthropic Provider - Proveedor para modelos de Anthropic (Claude)
"""

import asyncio
import time
from typing import List, Optional, Dict
from datetime import datetime

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from .base import BaseProvider, AIResponse, Message


class AnthropicProvider(BaseProvider):
    """Proveedor de Anthropic Claude."""

    # Precios por 1M tokens (Enero 2026)
    PRICING = {
        'claude-opus-4-5-20251101': {'input': 15.00, 'output': 75.00},
        'claude-sonnet-4-5-20250929': {'input': 3.00, 'output': 15.00},
        'claude-haiku-4-5-20251001': {'input': 0.25, 'output': 1.25},
        'claude-3-5-sonnet-latest': {'input': 3.00, 'output': 15.00},
    }

    MODELS = [
        'claude-opus-4-5-20251101',
        'claude-sonnet-4-5-20250929',
        'claude-haiku-4-5-20251001',
        'claude-3-5-sonnet-latest'
    ]

    def __init__(self, api_key: str, model: str = 'claude-sonnet-4-5-20250929'):
        super().__init__(api_key, model)
        self.name = "anthropic"

        if not ANTHROPIC_AVAILABLE:
            self.is_available = False
            self.last_error = "anthropic package not installed"
            return

        if not api_key:
            self.is_available = False
            self.last_error = "API key not provided"
            return

        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.is_available = True

    async def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AIResponse:
        """Genera respuesta usando Anthropic Claude."""
        if not self.is_available:
            raise Exception(f"Anthropic no disponible: {self.last_error}")

        start_time = time.time()

        # Construir mensajes en formato Anthropic
        anthropic_messages = []

        for msg in messages:
            anthropic_messages.append({
                "role": msg.role if msg.role != 'system' else 'user',
                "content": msg.content
            })

        try:
            kwargs = {
                'model': self.model,
                'messages': anthropic_messages,
                'max_tokens': max_tokens,
            }

            # Claude no soporta temperature para o1-like models
            if 'opus' not in self.model:
                kwargs['temperature'] = temperature

            if system_prompt:
                kwargs['system'] = system_prompt

            response = await self.client.messages.create(**kwargs)

            latency_ms = int((time.time() - start_time) * 1000)

            content = response.content[0].text if response.content else ""
            tokens_input = response.usage.input_tokens
            tokens_output = response.usage.output_tokens
            tokens_total = tokens_input + tokens_output

            cost = self.calculate_cost(tokens_input, tokens_output)

            result = AIResponse(
                content=content,
                provider=self.name,
                model=self.model,
                tokens_input=tokens_input,
                tokens_output=tokens_output,
                tokens_total=tokens_total,
                cost_usd=cost,
                latency_ms=latency_ms,
                timestamp=datetime.now().isoformat(),
                metadata={
                    'stop_reason': response.stop_reason,
                    'id': response.id
                }
            )

            self.update_stats(result)
            return result

        except Exception as e:
            self.last_error = str(e)
            raise

    async def validate_key(self) -> bool:
        """Valida la API key de Anthropic."""
        if not ANTHROPIC_AVAILABLE:
            return False
        try:
            # Anthropic no tiene endpoint de validación simple
            # Intentamos una llamada mínima
            await self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            self.is_available = True
            return True
        except Exception as e:
            self.is_available = False
            self.last_error = str(e)
            return False

    def get_models(self) -> List[str]:
        """Retorna modelos disponibles de Anthropic."""
        return self.MODELS

    def calculate_cost(self, tokens_input: int, tokens_output: int) -> float:
        """Calcula costo en USD."""
        pricing = self.PRICING.get(self.model, self.PRICING['claude-sonnet-4-5-20250929'])
        cost_input = (tokens_input / 1_000_000) * pricing['input']
        cost_output = (tokens_output / 1_000_000) * pricing['output']
        return round(cost_input + cost_output, 6)
