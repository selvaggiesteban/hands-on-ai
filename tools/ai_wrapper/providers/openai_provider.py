"""
OpenAI Provider - Proveedor para modelos de OpenAI (GPT-4, GPT-4o, o1)
"""

import asyncio
import time
from typing import List, Optional, Dict
from datetime import datetime

try:
    import openai
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from .base import BaseProvider, AIResponse, Message


class OpenAIProvider(BaseProvider):
    """Proveedor de OpenAI."""

    # Precios por 1M tokens (Enero 2026)
    PRICING = {
        'gpt-4o': {'input': 2.50, 'output': 10.00},
        'gpt-4o-mini': {'input': 0.15, 'output': 0.60},
        'o1': {'input': 15.00, 'output': 60.00},
        'o1-mini': {'input': 3.00, 'output': 12.00},
        'gpt-4-turbo': {'input': 10.00, 'output': 30.00},
    }

    MODELS = ['gpt-4o', 'gpt-4o-mini', 'o1', 'o1-mini', 'gpt-4-turbo']

    def __init__(self, api_key: str, model: str = 'gpt-4o'):
        super().__init__(api_key, model)
        self.name = "openai"

        if not OPENAI_AVAILABLE:
            self.is_available = False
            self.last_error = "openai package not installed"
            return

        if not api_key:
            self.is_available = False
            self.last_error = "API key not provided"
            return

        self.client = AsyncOpenAI(api_key=api_key)
        self.is_available = True

    async def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AIResponse:
        """Genera respuesta usando OpenAI."""
        if not self.is_available:
            raise Exception(f"OpenAI no disponible: {self.last_error}")

        start_time = time.time()

        # Construir mensajes en formato OpenAI
        openai_messages = []

        if system_prompt:
            openai_messages.append({
                "role": "system",
                "content": system_prompt
            })

        for msg in messages:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                max_tokens=max_tokens,
                temperature=temperature
            )

            latency_ms = int((time.time() - start_time) * 1000)

            content = response.choices[0].message.content or ""
            tokens_input = response.usage.prompt_tokens
            tokens_output = response.usage.completion_tokens
            tokens_total = response.usage.total_tokens

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
                    'finish_reason': response.choices[0].finish_reason,
                    'id': response.id
                }
            )

            self.update_stats(result)
            return result

        except Exception as e:
            self.last_error = str(e)
            raise

    async def validate_key(self) -> bool:
        """Valida la API key de OpenAI."""
        if not OPENAI_AVAILABLE:
            return False
        try:
            await self.client.models.list()
            self.is_available = True
            return True
        except Exception as e:
            self.is_available = False
            self.last_error = str(e)
            return False

    def get_models(self) -> List[str]:
        """Retorna modelos disponibles de OpenAI."""
        return self.MODELS

    def calculate_cost(self, tokens_input: int, tokens_output: int) -> float:
        """Calcula costo en USD."""
        pricing = self.PRICING.get(self.model, self.PRICING['gpt-4o'])
        cost_input = (tokens_input / 1_000_000) * pricing['input']
        cost_output = (tokens_output / 1_000_000) * pricing['output']
        return round(cost_input + cost_output, 6)
