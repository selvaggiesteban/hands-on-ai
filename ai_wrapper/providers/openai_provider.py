"""
OpenAI Provider - Proveedor para modelos de OpenAI (GPT-4, GPT-4o, o1)
"""

import asyncio
import time
import json
from typing import List, Optional, Dict, Any
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
        tools: Optional[List[Dict[str, Any]]] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AIResponse:
        """Genera respuesta usando OpenAI, con soporte para tool calling."""
        if not self.is_available:
            raise Exception(f"OpenAI no disponible: {self.last_error}")

        super().generate(messages=messages, tools=tools)
        start_time = time.time()

        openai_messages = []
        if system_prompt:
            openai_messages.append({"role": "system", "content": system_prompt})

        for msg in messages:
            message_dict = {"role": msg.role, "content": msg.content}
            if msg.role == "tool":
                message_dict["tool_call_id"] = msg.tool_call_id
            openai_messages.append(message_dict)
            
        try:
            request_params = {
                'model': self.model,
                'messages': openai_messages,
                'max_tokens': max_tokens,
                'temperature': temperature,
            }
            if tools:
                request_params['tools'] = tools
                request_params['tool_choice'] = "auto"

            response = await self.client.chat.completions.create(**request_params)

            latency_ms = int((time.time() - start_time) * 1000)
            choice = response.choices[0]
            message = choice.message

            tool_calls = None
            if message.tool_calls:
                tool_calls = [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": json.loads(tc.function.arguments),
                        },
                    }
                    for tc in message.tool_calls
                ]

            result = AIResponse(
                provider=self.name,
                model=self.model,
                timestamp=datetime.now().isoformat(),
                content=message.content,
                tool_calls=tool_calls,
                tokens_input=response.usage.prompt_tokens,
                tokens_output=response.usage.completion_tokens,
                tokens_total=response.usage.total_tokens,
                cost_usd=self.calculate_cost(response.usage.prompt_tokens, response.usage.completion_tokens),
                latency_ms=latency_ms,
                metadata={'finish_reason': choice.finish_reason, 'id': response.id}
            )

            self.update_stats(result)
            return result

        except Exception as e:
            self.last_error = str(e)
            self.logger.error("OpenAI API call failed", error=e, provider=self.name)
            raise

    async def validate_key(self) -> bool:
        """Valida la API key de OpenAI."""
        if not OPENAI_AVAILABLE: return False
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
