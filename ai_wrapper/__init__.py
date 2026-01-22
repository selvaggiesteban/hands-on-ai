# AI Wrapper - Sistema Multi-Modelo para Hands On AI
# Procesamiento paralelo con rotación equitativa, merge inteligente y junta directiva
from .multi_model import MultiModelProcessor, MultiModelConfig
from .code_contract import CodeGenerationContract
from .chat_manager import ChatManager

__all__ = ['MultiModelProcessor', 'MultiModelConfig', 'CodeGenerationContract', 'ChatManager']