"""
Chat Manager - Gestión de Sesiones de Chat (CRUD)
Facilita la conversación en lenguaje natural manteniendo contexto e historial.
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field, asdict

@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class ChatManager:
    """
    Gestor de sesiones de chat.
    Permite Crear, Leer, Actualizar y Borrar (CRUD) el historial de conversación.
    """

    def __init__(self, storage_path: str = "chat_history.json"):
        self.storage_path = storage_path
        self.history: List[ChatMessage] = []
        self.load_history()

    def add_message(self, role: str, content: str):
        """CREATE: Agrega un mensaje al historial."""
        msg = ChatMessage(role=role, content=content)
        self.history.append(msg)
        self.save_history()

    def get_context(self, limit: int = 10) -> List[Dict[str, str]]:
        """READ: Obtiene el contexto reciente para la IA."""
        # Retorna los últimos 'limit' mensajes en formato dict simple
        return [
            {'role': m.role, 'content': m.content} 
            for m in self.history[-limit:]
        ]

    def get_full_history(self) -> List[ChatMessage]:
        """READ: Obtiene todo el historial."""
        return self.history

    def update_last_message(self, new_content: str):
        """UPDATE: Modifica el último mensaje (útil para correcciones)."""
        if self.history:
            self.history[-1].content = new_content
            self.history[-1].timestamp = datetime.now().isoformat()
            self.save_history()

    def clear_history(self):
        """DELETE: Borra todo el historial."""
        self.history = []
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)

    def save_history(self):
        """Persiste el historial en disco."""
        data = [asdict(m) for m in self.history]
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error guardando historial: {e}")

    def load_history(self):
        """Carga el historial desde disco."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = [ChatMessage(**m) for m in data]
            except Exception as e:
                print(f"⚠️ Error cargando historial: {e}")
                self.history = []

    def export_conversation(self, filepath: str):
        """Exporta la conversación a un archivo de texto legible."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"--- Chat Exportado: {datetime.now().isoformat()} ---\n\n")
                for msg in self.history:
                    icon = "👤" if msg.role == 'user' else "🤖"
                    f.write(f"{icon} [{msg.role.upper()}]:\n{msg.content}\n\n{'-'*40}\n\n")
            return True
        except Exception:
            return False