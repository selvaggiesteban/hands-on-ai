import os
import pytest
import asyncio
from dotenv import load_dotenv
from typing import List, Dict, Any

from .base import Message
from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider
from .anthropic_provider import AnthropicProvider

# --- Mock Tools ---
def get_weather(location: str, unit: str = "celsius"):
    """Obtiene el clima actual para una ubicación."""
    if "london" in location.lower():
        return f"El clima en Londres es 10 grados {unit}."
    return f"No se pudo obtener el clima para {location}."

# --- Definición de Herramientas Estándar ---
mock_tools_definition: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Obtiene el clima actual para una ubicación específica.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "La ciudad y estado, ej. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]

def pytest_generate_tests(metafunc):
    load_dotenv()

    configured_providers = []

    if os.getenv("OPENAI_API_KEY"):
        model = os.getenv("AI_MODEL", "gpt-4o-mini")
        configured_providers.append(OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"), model=model))

    if os.getenv("GEMINI_API_KEY"):
        model = os.getenv("AI_MODEL", "gemini-1.5-flash-latest")
        configured_providers.append(GeminiProvider(api_key=os.getenv("GEMINI_API_KEY"), model=model))

    if os.getenv("ANTHROPIC_API_KEY"):
        model = os.getenv("AI_MODEL", "claude-3-5-sonnet-latest")
        configured_providers.append(AnthropicProvider(api_key=os.getenv("ANTHROPIC_API_KEY"), model=model))

    if "provider" in metafunc.fixturenames:
        if not configured_providers:
            pytest.skip("No se encontraron API keys configuradas. Saltando pruebas.")
        metafunc.parametrize("provider", configured_providers)


@pytest.mark.asyncio
async def test_tool_calling_for_provider(provider):
    """
    Test de integración para verificar la capacidad de tool calling de un proveedor.
    """
    if not provider.is_available:
        pytest.skip(f"Proveedor {provider.name} no disponible: {provider.last_error}")

    prompt = "Cual es el clima en Londres?"
    messages = [Message(role="user", content=prompt)]

    try:
        response = await provider.generate(
            messages=messages,
            tools=mock_tools_definition
        )

        assert response.content is None
        assert response.tool_calls is not None
        assert len(response.tool_calls) > 0
        
        tool_call = response.tool_calls[0]
        assert tool_call['type'] == 'function'
        assert tool_call['function']['name'] == 'get_weather'
        
        arguments = tool_call['function']['arguments']
        assert "location" in arguments
        assert "london" in arguments["location"].lower()

    except Exception as e:
        pytest.fail(f"La prueba para {provider.name} falló con una excepción: {e}")
