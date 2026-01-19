import os
import pytest
import asyncio
from dotenv import load_dotenv
from typing import List, Dict, Any

# Cargar variables de entorno desde .env
load_dotenv()

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

# --- Proveedores para Probar ---
providers = []
if os.getenv("OPENAI_API_KEY"):
    providers.append(OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"), model=os.getenv("AI_MODEL", "gpt-4o-mini")))
if os.getenv("GEMINI_API_KEY"):
    providers.append(GeminiProvider(api_key=os.getenv("GEMINI_API_KEY"), model=os.getenv("AI_MODEL", "gemini-1.5-flash")))
if os.getenv("ANTHROPIC_API_KEY"):
    providers.append(AnthropicProvider(api_key=os.getenv("ANTHROPIC_API_KEY"), model=os.getenv("AI_MODEL", "claude-3-5-sonnet-latest")))

@pytest.mark.parametrize("provider", providers)
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

        # Verificar logs (se imprimen en la salida de pytest)
        print(f"\n--- Logs for {provider.name} ---")
        print(f"Response object: {response.to_dict()}")
        print("--- End Logs ---")

        # Asertos
        assert response.content is None, f"Se esperaba una llamada a herramienta, pero se recibió contenido: {response.content}"
        assert response.tool_calls is not None, "La respuesta no contiene llamadas a herramientas."
        assert len(response.tool_calls) > 0, "La lista de llamadas a herramientas está vacía."
        
        tool_call = response.tool_calls[0]
        assert tool_call['type'] == 'function', f"El tipo de llamada esperado era 'function', se obtuvo '{tool_call['type']}'"
        assert tool_call['function']['name'] == 'get_weather', f"Se esperaba la función 'get_weather', se obtuvo '{tool_call['function']['name']}'"
        
        arguments = tool_call['function']['arguments']
        assert "location" in arguments, "El argumento 'location' no se encontró en la llamada a la herramienta."
        assert "london" in arguments["location"].lower(), f"Se esperaba 'london' en la ubicación, se obtuvo '{arguments['location']}'"

    except Exception as e:
        pytest.fail(f"La prueba de tool calling para {provider.name} falló con una excepción: {e}")
