import os
import asyncio
from dotenv import load_dotenv
from typing import List, Dict, Any

# Cargar variables de entorno y configurar sys.path
load_dotenv()

from tools.ai_wrapper.providers.base import Message
from tools.ai_wrapper.providers.openai_provider import OpenAIProvider
from tools.ai_wrapper.providers.gemini_provider import GeminiProvider
from tools.ai_wrapper.providers.anthropic_provider import AnthropicProvider

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

async def run_test_for_provider(provider):
    """Ejecuta la prueba de tool calling para un proveedor específico."""
    print(f"--- Iniciando Prueba para: {provider.name} ({provider.model}) ---")
    
    if not provider.is_available:
        print(f"⏭️  OMITIDO: Proveedor {provider.name} no disponible: {provider.last_error}")
        return {"provider": provider.name, "status": "SKIPPED", "reason": provider.last_error}

    prompt = "Cual es el clima en Londres?"
    messages = [Message(role="user", content=prompt)]

    try:
        response = await provider.generate(
            messages=messages,
            tools=mock_tools_definition
        )

        assert response.content is None, "Se recibió contenido en lugar de una tool call."
        assert response.tool_calls is not None, "La respuesta no contiene tool calls."
        assert len(response.tool_calls) > 0, "La lista de tool calls está vacía."
        
        tool_call = response.tool_calls[0]
        assert tool_call['type'] == 'function', f"Tipo de tool call incorrecto: {tool_call['type']}"
        assert tool_call['function']['name'] == 'get_weather', f"Función incorrecta: {tool_call['function']['name']}"
        
        arguments = tool_call['function']['arguments']
        assert "location" in arguments, "Falta el argumento 'location'."
        assert "london" in arguments["location"].lower(), f"Argumento 'location' incorrecto: {arguments['location']}"
        
        print(f"✅ PASSED: {provider.name}")
        return {"provider": provider.name, "status": "PASSED"}

    except Exception as e:
        print(f"❌ FAILED: {provider.name} falló con una excepción: {e}")
        return {"provider": provider.name, "status": "FAILED", "reason": str(e)}

async def main():
    """Función principal para ejecutar todas las pruebas."""
    configured_providers = []

    if os.getenv("OPENAI_API_KEY"):
        model = os.getenv("AI_MODEL", "gpt-4o-mini")
        configured_providers.append(OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"), model=model))

    if os.getenv("GEMINI_API_KEY"):
        # Asegurarse de que GOOGLE_API_KEY esté seteada para la librería de Gemini
        if 'GOOGLE_API_KEY' not in os.environ:
            os.environ['GOOGLE_API_KEY'] = os.getenv("GEMINI_API_KEY")
        model = os.getenv("AI_MODEL", "gemini-1.5-flash-latest")
        configured_providers.append(GeminiProvider(api_key=os.getenv("GEMINI_API_KEY"), model=model))

    if os.getenv("ANTHROPIC_API_KEY"):
        model = os.getenv("AI_MODEL", "claude-3-5-sonnet-latest")
        configured_providers.append(AnthropicProvider(api_key=os.getenv("ANTHROPIC_API_KEY"), model=model))

    if not configured_providers:
        print("No se encontraron API keys configuradas. Abortando pruebas.")
        return

    results = await asyncio.gather(*(run_test_for_provider(p) for p in configured_providers))
    
    # Aquí podrías generar un informe con los resultados si lo deseas
    print("\n--- Resumen de Resultados ---")
    for res in results:
        print(f"- {res['provider']}: {res['status']}")

if __name__ == "__main__":
    asyncio.run(main())
