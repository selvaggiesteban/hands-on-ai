# Proveedores de IA
# Imports lazy para evitar errores de dependencias (pydantic/openai)
from .base import BaseProvider, AIResponse, Message

# Los proveedores se importan bajo demanda para evitar errores
def get_openai_provider():
    """Import lazy de OpenAIProvider."""
    try:
        from .openai_provider import OpenAIProvider
        return OpenAIProvider
    except Exception as e:
        return None

def get_anthropic_provider():
    """Import lazy de AnthropicProvider."""
    try:
        from .anthropic_provider import AnthropicProvider
        return AnthropicProvider
    except Exception as e:
        return None

def get_gemini_provider():
    """Import lazy de GeminiProvider."""
    try:
        from .gemini_provider import GeminiProvider
        return GeminiProvider
    except Exception as e:
        return None

__all__ = ['BaseProvider', 'AIResponse', 'Message',
           'get_openai_provider', 'get_anthropic_provider', 'get_gemini_provider']
