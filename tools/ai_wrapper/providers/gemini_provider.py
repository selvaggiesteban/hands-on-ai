"""
Gemini Provider - Proveedor para modelos de Google Gemini
"""

import asyncio
import time
import json
from typing import List, Optional, Dict, Any
from datetime import datetime

try:
    import google.generativeai as genai
    from google.generativeai.types import FunctionCall
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from .base import BaseProvider, AIResponse, Message


class GeminiProvider(BaseProvider):
    """Proveedor de Google Gemini."""

    # Precios por 1M tokens (Enero 2026)
    PRICING = {
        'gemini-1.5-pro-latest': {'input': 3.50, 'output': 10.50},
        'gemini-1.5-flash-latest': {'input': 0.35, 'output': 1.05},
    }

    MODELS = ['gemini-1.5-pro-latest', 'gemini-1.5-flash-latest']

    def __init__(self, api_key: str, model: str = 'gemini-1.5-flash-latest'):
        super().__init__(api_key, model)
        self.name = "gemini"

        if not GEMINI_AVAILABLE:
            self.is_available = False
            self.last_error = "google-genai package not installed or configured"
            return

        if not api_key:
            self.is_available = False
            self.last_error = "API key not provided"
            return

        genai.configure(api_key=api_key)
        self.is_available = True

    async def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AIResponse:
        """Genera respuesta usando Google Gemini, con soporte para tool calling."""
        if not self.is_available:
            raise Exception(f"Gemini no disponible: {self.last_error}")

        super().generate(messages=messages, tools=tools)
        start_time = time.time()
        
        genai_model = genai.GenerativeModel(
            model_name=self.model,
            system_instruction=system_prompt
        )

        history = []
        for msg in messages:
            role = "user" if msg.role == "user" else "model"
            history.append({'role': role, 'parts': [msg.content]})

        try:
            loop = asyncio.get_event_loop()

            def sync_generate():
                chat = genai_model.start_chat(history=history)
                generation_config = genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
                
                # Gemini espera el último mensaje del usuario por separado
                last_user_message = history.pop()
                
                return chat.send_message(
                    last_user_message['parts'],
                    generation_config=generation_config,
                    tools=tools if tools else None
                )

            response = await loop.run_in_executor(None, sync_generate)
            latency_ms = int((time.time() - start_time) * 1000)

            content = None
            tool_calls = None
            
            # Procesar la respuesta para tool calls o contenido de texto
            part = response.parts[0]
            if part.function_call:
                fc = part.function_call
                tool_calls = [{
                    "id": f"call_{fc.name}_{int(time.time())}", # Gemini no provee ID, se genera uno
                    "type": "function",
                    "function": {
                        "name": fc.name,
                        "arguments": dict(fc.args),
                    }
                }]
            else:
                content = response.text

            tokens_input = response.usage_metadata.prompt_token_count
            tokens_output = response.usage_metadata.candidates_token_count

            result = AIResponse(
                provider=self.name,
                model=self.model,
                timestamp=datetime.now().isoformat(),
                content=content,
                tool_calls=tool_calls,
                tokens_input=tokens_input,
                tokens_output=tokens_output,
                tokens_total=tokens_input + tokens_output,
                cost_usd=self.calculate_cost(tokens_input, tokens_output),
                latency_ms=latency_ms,
                metadata={'finish_reason': response.candidates[0].finish_reason.name}
            )

            self.update_stats(result)
            return result

        except Exception as e:
            self.last_error = str(e)
            self.logger.error("Gemini API call failed", error=e, provider=self.name)
            raise

    async def validate_key(self) -> bool:
        """Valida la API key de Gemini."""
        if not GEMINI_AVAILABLE: return False
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: list(genai.list_models()))
            self.is_available = True
            return True
        except Exception as e:
            self.is_available = False
            self.last_error = str(e)
            return False

    def get_models(self) -> List[str]:
        """Retorna modelos disponibles de Gemini."""
        return self.MODELS

    def calculate_cost(self, tokens_input: int, tokens_output: int) -> float:
        """Calcula costo en USD."""
        pricing = self.PRICING.get(self.model, self.PRICING['gemini-1.5-flash-latest'])
        cost_input = (tokens_input / 1_000_000) * pricing['input']
        cost_output = (tokens_output / 1_000_000) * pricing['output']
        return round(cost_input + cost_output, 6)
