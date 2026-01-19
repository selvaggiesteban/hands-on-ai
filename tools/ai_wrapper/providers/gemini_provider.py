"""
Gemini Provider - Proveedor para modelos de Google Gemini
"""

import asyncio
import time
from typing import List, Optional, Dict
from datetime import datetime

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from .base import BaseProvider, AIResponse, Message


class GeminiProvider(BaseProvider):
    """Proveedor de Google Gemini."""

    # Precios por 1M tokens (Enero 2026)
    PRICING = {
        'gemini-3-pro': {'input': 1.25, 'output': 5.00},
        'gemini-3-flash': {'input': 0.075, 'output': 0.30},
        'gemini-2.5-pro': {'input': 1.25, 'output': 5.00},
        'gemini-2.5-flash': {'input': 0.075, 'output': 0.30},
        'gemini-2.5-flash-lite': {'input': 0.0375, 'output': 0.15},
        'gemini-2.0-flash': {'input': 0.075, 'output': 0.30},
    }

    MODELS = [
        'gemini-3-pro',
        'gemini-3-flash',
        'gemini-2.5-pro',
        'gemini-2.5-flash',
        'gemini-2.5-flash-lite',
        'gemini-2.0-flash'
    ]

    def __init__(self, api_key: str, model: str = 'gemini-2.5-flash'):
        super().__init__(api_key, model)
        self.name = "gemini"

        if not GEMINI_AVAILABLE:
            self.is_available = False
            self.last_error = "google-generativeai package not installed"
            return

        if not api_key:
            self.is_available = False
            self.last_error = "API key not provided"
            return

        genai.configure(api_key=api_key)
        self.genai_model = genai.GenerativeModel(model)
        self.is_available = True

    async def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AIResponse:
        """Genera respuesta usando Google Gemini."""
        if not self.is_available:
            raise Exception(f"Gemini no disponible: {self.last_error}")

        start_time = time.time()

        # Construir historial y prompt
        history = []
        current_prompt = ""

        for msg in messages:
            if msg.role == 'user':
                if current_prompt:
                    history.append({'role': 'user', 'parts': [current_prompt]})
                    current_prompt = ""
                current_prompt = msg.content
            elif msg.role == 'assistant':
                if current_prompt:
                    history.append({'role': 'user', 'parts': [current_prompt]})
                    current_prompt = ""
                history.append({'role': 'model', 'parts': [msg.content]})

        # Agregar system prompt al inicio si existe
        if system_prompt and current_prompt:
            current_prompt = f"{system_prompt}\n\n{current_prompt}"
        elif system_prompt:
            current_prompt = system_prompt

        try:
            # Gemini usa API síncrona, ejecutar en thread
            loop = asyncio.get_event_loop()

            def sync_generate():
                chat = self.genai_model.start_chat(history=history)
                generation_config = genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
                return chat.send_message(
                    current_prompt,
                    generation_config=generation_config
                )

            response = await loop.run_in_executor(None, sync_generate)

            latency_ms = int((time.time() - start_time) * 1000)

            content = response.text if response.text else ""

            # Gemini no siempre reporta tokens exactos
            # Estimación básica: 1 token ~ 4 caracteres
            tokens_input = len(current_prompt) // 4 + sum(len(str(h)) for h in history) // 4
            tokens_output = len(content) // 4
            tokens_total = tokens_input + tokens_output

            # Usar usage_metadata si está disponible
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                if hasattr(response.usage_metadata, 'prompt_token_count'):
                    tokens_input = response.usage_metadata.prompt_token_count
                if hasattr(response.usage_metadata, 'candidates_token_count'):
                    tokens_output = response.usage_metadata.candidates_token_count
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
                metadata={}
            )

            self.update_stats(result)
            return result

        except Exception as e:
            self.last_error = str(e)
            raise

    async def validate_key(self) -> bool:
        """Valida la API key de Gemini."""
        if not GEMINI_AVAILABLE:
            return False
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
        pricing = self.PRICING.get(self.model, self.PRICING['gemini-2.5-flash'])
        cost_input = (tokens_input / 1_000_000) * pricing['input']
        cost_output = (tokens_output / 1_000_000) * pricing['output']
        return round(cost_input + cost_output, 6)
