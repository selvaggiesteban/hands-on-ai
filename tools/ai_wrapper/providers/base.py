"""
Base Provider - Clase base para todos los proveedores de IA
Define el contrato que deben implementar todos los proveedores.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AIResponse:
    """Respuesta estandarizada de cualquier proveedor de IA."""
    content: str
    provider: str
    model: str
    tokens_input: int
    tokens_output: int
    tokens_total: int
    cost_usd: float
    latency_ms: int
    timestamp: str
    metadata: Dict[str, Any] = None

    def to_dict(self) -> Dict:
        return {
            'content': self.content,
            'provider': self.provider,
            'model': self.model,
            'tokens': {
                'input': self.tokens_input,
                'output': self.tokens_output,
                'total': self.tokens_total
            },
            'cost_usd': self.cost_usd,
            'latency_ms': self.latency_ms,
            'timestamp': self.timestamp,
            'metadata': self.metadata or {}
        }


@dataclass
class Message:
    """Mensaje en una conversación."""
    role: str  # 'user', 'assistant', 'system'
    content: str


class BaseProvider(ABC):
    """
    Clase base abstracta para proveedores de IA.
    Todos los proveedores deben implementar estos métodos.
    """

    def __init__(self, api_key: str, model: str = None):
        self.api_key = api_key
        self.model = model
        self.name = "base"
        self.is_available = False
        self.last_error = None
        self.request_count = 0
        self.total_tokens = 0
        self.total_cost = 0.0

    @abstractmethod
    async def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> AIResponse:
        """
        Genera una respuesta a partir de los mensajes.

        Args:
            messages: Lista de mensajes de la conversación
            system_prompt: Prompt del sistema (opcional)
            max_tokens: Máximo de tokens en la respuesta
            temperature: Temperatura para la generación

        Returns:
            AIResponse con la respuesta generada
        """
        pass

    @abstractmethod
    async def validate_key(self) -> bool:
        """Valida que la API key sea correcta."""
        pass

    @abstractmethod
    def get_models(self) -> List[str]:
        """Retorna lista de modelos disponibles."""
        pass

    @abstractmethod
    def calculate_cost(self, tokens_input: int, tokens_output: int) -> float:
        """Calcula el costo en USD de una llamada."""
        pass

    def update_stats(self, response: AIResponse):
        """Actualiza estadísticas del proveedor."""
        self.request_count += 1
        self.total_tokens += response.tokens_total
        self.total_cost += response.cost_usd

    def get_stats(self) -> Dict:
        """Retorna estadísticas del proveedor."""
        return {
            'provider': self.name,
            'model': self.model,
            'is_available': self.is_available,
            'request_count': self.request_count,
            'total_tokens': self.total_tokens,
            'total_cost_usd': round(self.total_cost, 6),
            'last_error': self.last_error
        }
