"""
Anthropic Provider - Proveedor para modelos de Anthropic (Claude)
"""

import asyncio
import time
import json
from typing import List, Optional, Dict, Any
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
        'claude-3-5-sonnet-20240620': {'input': 3.00, 'output': 15.00},
        'claude-3-opus-20240229': {'input': 15.00, 'output': 75.00},
        'claude-3-haiku-20240307': {'input': 0.25, 'output': 1.25},
    }

    MODELS = ['claude-3-5-sonnet-20240620', 'claude-3-opus-20240229', 'claude-3-haiku-20240307']

    def __init__(self, api_key: str, model: str = 'claude-3-5-sonnet-20240620'):
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
        tools: Optional[List[Dict[str, Any]]] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AIResponse:
        """Genera respuesta usando Anthropic Claude, con soporte para tool calling."""
        if not self.is_available:
            raise Exception(f"Anthropic no disponible: {self.last_error}")
        
        super().generate(messages=messages, tools=tools)
        start_time = time.time()

        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({"role": msg.role, "content": msg.content})

        try:
            request_params = {
                'model': self.model,
                'messages': anthropic_messages,
                'max_tokens': max_tokens,
                'temperature': temperature,
            }
            if system_prompt:
                request_params['system'] = system_prompt
            if tools:
                request_params['tools'] = tools
                request_params['tool_choice'] = {"type": "auto"}

            response = await self.client.messages.create(**request_params)
            latency_ms = int((time.time() - start_time) * 1000)

            content = None
            tool_calls = None
            
            if response.stop_reason == "tool_use":
                tool_calls = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool_calls.append({
                            "id": block.id,
                            "type": "function",
                            "function": {
                                "name": block.name,
                                "arguments": block.input,
                            }
                        })
            elif response.content:
                content = response.content[0].text

            result = AIResponse(
                provider=self.name,
                model=self.model,
                timestamp=datetime.now().isoformat(),
                content=content,
                tool_calls=tool_calls,
                tokens_input=response.usage.input_tokens,
                tokens_output=response.usage.output_tokens,
                tokens_total=response.usage.input_tokens + response.usage.output_tokens,
                cost_usd=self.calculate_cost(response.usage.input_tokens, response.usage.output_tokens),
                latency_ms=latency_ms,
                metadata={'stop_reason': response.stop_reason, 'id': response.id}
            )

            self.update_stats(result)
            return result

        except Exception as e:
            self.last_error = str(e)
            self.logger.error("Anthropic API call failed", error=e, provider=self.name)
            raise

    async def validate_key(self) -> bool:
        """Valida la API key de Anthropic."""
        if not ANTHROPIC_AVAILABLE: return False
        try:
            await self.client.messages.create(
                model=self.model, messages=[{"role": "user", "content": "test"}], max_tokens=1
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
        pricing = self.PRICING.get(self.model, self.PRICING['claude-3-5-sonnet-20240620'])
        cost_input = (tokens_input / 1_000_000) * pricing['input']
        cost_output = (tokens_output / 1_000_000) * pricing['output']
        return round(cost_input + cost_output, 6)
