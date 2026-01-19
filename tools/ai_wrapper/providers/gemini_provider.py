"""
Gemini Provider - Proveedor para modelos de Google Gemini (Versión SDK v1+)
"""

import asyncio
import time
import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from .base import BaseProvider, AIResponse, Message

class GeminiProvider(BaseProvider):
    """Proveedor de Google Gemini usando el nuevo SDK google-genai."""

    PRICING = {
        'gemini-2.0-flash': {'input': 0.10, 'output': 0.40},
        'gemini-1.5-pro': {'input': 1.25, 'output': 5.00},
        'gemini-1.5-flash': {'input': 0.075, 'output': 0.30},
    }
    
    MODELS = ['gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-1.5-flash']

    def __init__(self, api_key: str, model: str = 'gemini-2.0-flash'):
        super().__init__(api_key, model)
        self.name = "gemini"

        if not GEMINI_AVAILABLE:
            self.is_available = False
            self.last_error = "google-genai package not installed"
            return
        if not api_key:
            self.is_available = False
            self.last_error = "API key not provided"
            return

        try:
            self.client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})
            self.is_available = True
        except Exception as e:
            self.is_available = False
            self.last_error = str(e)

    async def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AIResponse:
        """Genera respuesta usando el nuevo SDK de Gemini."""
        if not self.is_available:
            raise Exception(f"Gemini no disponible: {self.last_error}")

        # Registrar inicio (BaseProvider loggeará esto si se llama super)
        start_time = time.time()

        # Preparar herramientas
        gemini_tools = None
        if tools:
            # El nuevo SDK acepta una lista de funciones o objetos Tool
            # Convertimos el formato standard a lo que espera Gemini
            gemini_tools = [types.Tool(function_declarations=[
                types.FunctionDeclaration(
                    name=t['function']['name'],
                    description=t['function']['description'],
                    parameters=types.Schema(
                        type='OBJECT',
                        properties={k: types.Schema(type=v['type'].upper(), description=v.get('description', '')) 
                                   for k, v in t['function']['parameters']['properties'].items()},
                        required=t['function']['parameters'].get('required', [])
                    )
                ) for t in tools
            ])]

        # Construir contenidos
        contents = []
        for msg in messages:
            role = "user" if msg.role in ["user", "system", "tool"] else "model"
            contents.append(types.Content(role=role, parts=[types.Part(text=msg.content)]))

        # El system prompt se maneja en el config
        config = types.GenerateContentConfig(
            system_instruction=system_prompt if system_prompt else None,
            max_output_tokens=max_tokens,
            temperature=temperature,
            tools=gemini_tools
        )

        try:
            # Ejecución asíncrona
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model,
                contents=contents,
                config=config
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            content = None
            tool_calls = None

            if response.candidates and response.candidates[0].content.parts:
                part = response.candidates[0].content.parts[0]
                if part.function_call:
                    fc = part.function_call
                    tool_calls = [{
                        "id": f"call_{fc.name}_{int(time.time())}",
                        "type": "function",
                        "function": {
                            "name": fc.name,
                            "arguments": fc.args
                        }
                    }]
                else:
                    content = response.text

            usage = response.usage_metadata
            tokens_input = usage.prompt_token_count
            tokens_output = usage.candidates_token_count

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
                latency_ms=latency_ms
            )

            self.update_stats(result)
            return result

        except Exception as e:
            self.last_error = str(e)
            raise

    async def validate_key(self) -> bool:
        try:
            # Intento de listar modelos para validar key
            self.client.models.list()
            return True
        except:
            return False

    def get_models(self) -> List[str]:
        return self.MODELS

    def calculate_cost(self, tokens_input: int, tokens_output: int) -> float:
        pricing = self.PRICING.get(self.model, self.PRICING['gemini-1.5-flash'])
        return round((tokens_input / 1_000_000 * pricing['input']) + (tokens_output / 1_000_000 * pricing['output']), 6)