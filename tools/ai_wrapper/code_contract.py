"""
Code Generation Contract - Contrato de Generación de Código
Define especificaciones, validaciones y formato de entrega para código generado.
"""

import re
import os
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime


@dataclass
class CodeValidationResult:
    """Resultado de validación de código."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    score: int = 0  # 0-100
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GeneratedCode:
    """Código generado con metadatos."""
    filename: str
    content: str
    language: str
    action: str  # 'create', 'modify', 'delete'
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    validation: Optional[CodeValidationResult] = None


@dataclass
class CodeGenerationRequest:
    """Solicitud de generación de código."""
    prompt: str
    target_path: Optional[str] = None
    language: Optional[str] = None
    framework: Optional[str] = None
    style_guide: Optional[str] = None
    requirements: List[str] = field(default_factory=list)


@dataclass
class CodeGenerationResponse:
    """Respuesta de generación de código."""
    success: bool
    files: List[GeneratedCode] = field(default_factory=list)
    explanation: str = ""
    errors: List[str] = field(default_factory=list)
    total_validation_score: int = 0
    timestamp: str = ""
    provider: str = ""
    model: str = ""


class CodeGenerationContract:
    """
    Contrato de Generación de Código para Hands On AI.
    Define reglas, validaciones y formato de entrega.
    """

    # Reglas permanentes de Hands On AI
    PERMANENT_RULES = {
        'typescript': [
            {'rule': 'no_any_type', 'pattern': r'\bany\b', 'message': 'Prohibido usar tipo "any" en TypeScript'},
            {'rule': 'explicit_interfaces', 'pattern': None, 'message': 'Definir interfaces explícitas para componentes'},
            {'rule': 'strict_mode', 'pattern': None, 'message': 'Usar modo estricto'},
        ],
        'nextjs': [
            {'rule': 'no_server_actions_complex', 'pattern': None, 'message': 'No usar Server Actions para lógica backend compleja'},
            {'rule': 'use_api_routes', 'pattern': None, 'message': 'Usar API Routes para backend'},
            {'rule': 'use_server_only_queries', 'pattern': None, 'message': 'use server solo para queries directas desde server components'},
        ],
        'react': [
            {'rule': 'functional_components', 'pattern': None, 'message': 'Preferir componentes funcionales'},
            {'rule': 'hooks_rules', 'pattern': None, 'message': 'Seguir reglas de hooks'},
        ],
        'general': [
            {'rule': 'no_secrets_client', 'pattern': r'(API_KEY|SECRET|PASSWORD)\s*=\s*["\'][^"\']+["\']', 'message': 'No incluir secretos en código cliente'},
            {'rule': 'code_in_english', 'pattern': None, 'message': 'Código en inglés'},
            {'rule': 'comments_in_spanish', 'pattern': None, 'message': 'Comentarios en español'},
            {'rule': 'no_console_log_prod', 'pattern': r'console\.(log|debug|info)\(', 'message': 'Eliminar console.log en producción'},
        ],
        'security': [
            {'rule': 'no_eval', 'pattern': r'\beval\s*\(', 'message': 'No usar eval()'},
            {'rule': 'no_innerhtml', 'pattern': r'\.innerHTML\s*=', 'message': 'Evitar innerHTML (riesgo XSS)'},
            {'rule': 'parameterized_queries', 'pattern': None, 'message': 'Usar queries parametrizadas para SQL'},
            {'rule': 'input_validation', 'pattern': None, 'message': 'Validar todas las entradas de usuario'},
        ],
        'style': [
            {'rule': 'tailwind_css', 'pattern': None, 'message': 'Usar Tailwind CSS para estilos'},
            {'rule': 'dark_mode_support', 'pattern': None, 'message': 'Soportar modo oscuro por defecto'},
            {'rule': 'mobile_responsive', 'pattern': None, 'message': 'Diseño responsive obligatorio'},
        ],
        'architecture': [
            {'rule': 'clean_architecture', 'pattern': None, 'message': 'Separar lógica de negocio, acceso a datos y UI'},
            {'rule': 'no_db_in_components', 'pattern': None, 'message': 'No mezclar lógica de base de datos en componentes React'},
        ]
    }

    # Extensiones de archivo por lenguaje
    LANGUAGE_EXTENSIONS = {
        'typescript': ['.ts', '.tsx'],
        'javascript': ['.js', '.jsx'],
        'python': ['.py'],
        'html': ['.html', '.htm'],
        'css': ['.css', '.scss', '.sass'],
        'json': ['.json'],
        'yaml': ['.yaml', '.yml'],
        'markdown': ['.md'],
        'sql': ['.sql'],
        'php': ['.php'],
    }

    def __init__(self, root_dir: str = None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).parent.parent.parent

    def detect_language(self, filename: str, content: str = None) -> str:
        """Detecta el lenguaje de programación."""
        ext = Path(filename).suffix.lower()

        for lang, extensions in self.LANGUAGE_EXTENSIONS.items():
            if ext in extensions:
                # TypeScript vs JavaScript
                if ext in ['.ts', '.tsx']:
                    return 'typescript'
                if ext in ['.js', '.jsx'] and content:
                    if 'import type' in content or ': string' in content or ': number' in content:
                        return 'typescript'
                return lang

        return 'unknown'

    def detect_framework(self, content: str, filename: str) -> Optional[str]:
        """Detecta el framework utilizado."""
        if 'next' in filename.lower() or "'next/" in content or '"next/' in content:
            return 'nextjs'
        if 'react' in content.lower() or 'useState' in content or 'useEffect' in content:
            return 'react'
        if 'vue' in content.lower() or '<template>' in content:
            return 'vue'
        if 'angular' in content.lower() or '@Component' in content:
            return 'angular'
        if 'flask' in content.lower() or 'from flask' in content:
            return 'flask'
        if 'fastapi' in content.lower() or 'from fastapi' in content:
            return 'fastapi'
        if 'django' in content.lower() or 'from django' in content:
            return 'django'
        if 'express' in content.lower() or "require('express')" in content:
            return 'express'

        return None

    def validate_code(self, code: GeneratedCode) -> CodeValidationResult:
        """Valida código contra las reglas del contrato."""
        errors = []
        warnings = []
        score = 100
        details = {}

        content = code.content
        language = code.language or self.detect_language(code.filename, content)
        framework = self.detect_framework(content, code.filename)

        # Aplicar reglas generales
        for rule in self.PERMANENT_RULES.get('general', []):
            if rule['pattern']:
                matches = re.findall(rule['pattern'], content, re.IGNORECASE)
                if matches:
                    if rule['rule'] == 'no_console_log_prod':
                        warnings.append(f"{rule['message']} (encontrados: {len(matches)})")
                        score -= 5
                    else:
                        errors.append(f"{rule['message']} (encontrados: {len(matches)})")
                        score -= 10

        # Aplicar reglas de seguridad
        for rule in self.PERMANENT_RULES.get('security', []):
            if rule['pattern']:
                matches = re.findall(rule['pattern'], content, re.IGNORECASE)
                if matches:
                    errors.append(f"SEGURIDAD: {rule['message']}")
                    score -= 20

        # Aplicar reglas específicas del lenguaje
        if language == 'typescript':
            for rule in self.PERMANENT_RULES.get('typescript', []):
                if rule['pattern']:
                    matches = re.findall(rule['pattern'], content)
                    if matches:
                        # Excluir comentarios y strings
                        real_matches = []
                        for match in matches:
                            # Verificación simple: no está en comentario
                            if '// any' not in content and '/* any' not in content:
                                real_matches.append(match)
                        if real_matches:
                            errors.append(f"{rule['message']} (encontrados: {len(real_matches)})")
                            score -= 15

        # Aplicar reglas del framework
        if framework == 'nextjs':
            for rule in self.PERMANENT_RULES.get('nextjs', []):
                if rule['pattern']:
                    matches = re.findall(rule['pattern'], content)
                    if matches:
                        warnings.append(rule['message'])
                        score -= 5

        # Verificar sintaxis básica
        syntax_check = self._check_basic_syntax(content, language)
        if not syntax_check['valid']:
            errors.extend(syntax_check['errors'])
            score -= 30

        # Ajustar score
        score = max(0, min(100, score))

        return CodeValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            score=score,
            details={
                'language': language,
                'framework': framework,
                'lines': content.count('\n') + 1,
                'characters': len(content)
            }
        )

    def _check_basic_syntax(self, content: str, language: str) -> Dict:
        """Verifica sintaxis básica."""
        errors = []

        # Verificar balance de llaves/paréntesis
        if language in ['typescript', 'javascript', 'json']:
            if content.count('{') != content.count('}'):
                errors.append("Llaves desbalanceadas")
            if content.count('(') != content.count(')'):
                errors.append("Paréntesis desbalanceados")
            if content.count('[') != content.count(']'):
                errors.append("Corchetes desbalanceados")

        # Verificar comillas
        if language in ['typescript', 'javascript', 'python']:
            # Contar comillas fuera de strings es complejo, verificación simple
            single_quotes = content.count("'") - content.count("\\'")
            double_quotes = content.count('"') - content.count('\\"')
            # Las comillas deben ser pares (aproximado)
            if single_quotes % 2 != 0:
                errors.append("Posibles comillas simples desbalanceadas")
            if double_quotes % 2 != 0:
                errors.append("Posibles comillas dobles desbalanceadas")

        return {'valid': len(errors) == 0, 'errors': errors}

    def extract_code_blocks(self, response: str) -> List[GeneratedCode]:
        """Extrae bloques de código de una respuesta de IA."""
        files = []

        # Patrón para bloques de código con nombre de archivo
        # ```typescript:src/components/Button.tsx
        # ```python filename="app.py"
        # ```js // filepath: src/utils.js
        patterns = [
            r'```(\w+):([^\n]+)\n(.*?)```',  # ```lang:path
            r'```(\w+)\s+filename=["\']([^"\']+)["\']\n(.*?)```',  # ```lang filename="path"
            r'```(\w+)\s*//\s*filepath:\s*([^\n]+)\n(.*?)```',  # ```lang // filepath: path
            r'```(\w+)\s*#\s*file:\s*([^\n]+)\n(.*?)```',  # ```lang # file: path
        ]

        for pattern in patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            for match in matches:
                lang, filepath, content = match
                files.append(GeneratedCode(
                    filename=filepath.strip(),
                    content=content.strip(),
                    language=lang.lower(),
                    action='create'
                ))

        # Si no encontramos archivos específicos, buscar bloques genéricos
        if not files:
            generic_pattern = r'```(\w+)\n(.*?)```'
            matches = re.findall(generic_pattern, response, re.DOTALL)
            for i, match in enumerate(matches):
                lang, content = match
                ext = self._get_extension(lang.lower())
                files.append(GeneratedCode(
                    filename=f"generated_{i+1}{ext}",
                    content=content.strip(),
                    language=lang.lower(),
                    action='create'
                ))

        return files

    def _get_extension(self, language: str) -> str:
        """Obtiene extensión de archivo para un lenguaje."""
        extensions = {
            'typescript': '.ts',
            'tsx': '.tsx',
            'javascript': '.js',
            'jsx': '.jsx',
            'python': '.py',
            'html': '.html',
            'css': '.css',
            'json': '.json',
            'yaml': '.yaml',
            'sql': '.sql',
            'bash': '.sh',
            'shell': '.sh',
            'php': '.php',
        }
        return extensions.get(language, '.txt')

    def write_files(self, files: List[GeneratedCode], base_path: str = None) -> Dict:
        """Escribe archivos generados a disco."""
        base = Path(base_path) if base_path else self.root_dir / 'project'
        results = {'written': [], 'failed': [], 'skipped': []}

        for file in files:
            try:
                filepath = base / file.filename

                # Crear directorio si no existe
                filepath.parent.mkdir(parents=True, exist_ok=True)

                # Validar antes de escribir
                validation = self.validate_code(file)
                file.validation = validation

                if not validation.is_valid:
                    # Escribir con advertencia
                    results['skipped'].append({
                        'file': file.filename,
                        'reason': 'Validación fallida',
                        'errors': validation.errors
                    })
                    continue

                # Escribir archivo
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(file.content)

                results['written'].append({
                    'file': file.filename,
                    'path': str(filepath),
                    'validation_score': validation.score
                })

            except Exception as e:
                results['failed'].append({
                    'file': file.filename,
                    'error': str(e)
                })

        return results

    def generate_system_prompt(self, request: CodeGenerationRequest) -> str:
        """Genera system prompt con las reglas del contrato."""
        rules_text = []

        # Reglas generales
        rules_text.append("## Reglas Obligatorias de Generación de Código\n")
        rules_text.append("### General")
        for rule in self.PERMANENT_RULES['general']:
            rules_text.append(f"- {rule['message']}")

        # Reglas de seguridad
        rules_text.append("\n### Seguridad")
        for rule in self.PERMANENT_RULES['security']:
            rules_text.append(f"- {rule['message']}")

        # Reglas específicas del lenguaje
        if request.language == 'typescript' or request.framework in ['nextjs', 'react']:
            rules_text.append("\n### TypeScript")
            for rule in self.PERMANENT_RULES['typescript']:
                rules_text.append(f"- {rule['message']}")

        # Reglas del framework
        if request.framework == 'nextjs':
            rules_text.append("\n### Next.js")
            for rule in self.PERMANENT_RULES['nextjs']:
                rules_text.append(f"- {rule['message']}")

        # Reglas de estilo
        rules_text.append("\n### Estilo")
        for rule in self.PERMANENT_RULES['style']:
            rules_text.append(f"- {rule['message']}")

        # Reglas de arquitectura
        rules_text.append("\n### Arquitectura")
        for rule in self.PERMANENT_RULES['architecture']:
            rules_text.append(f"- {rule['message']}")

        # Formato de entrega
        rules_text.append("\n## Formato de Entrega")
        rules_text.append("Entrega el código en bloques con el formato:")
        rules_text.append("```lenguaje:ruta/al/archivo.ext")
        rules_text.append("// código aquí")
        rules_text.append("```")

        return "\n".join(rules_text)

    def process_response(
        self,
        response: str,
        request: CodeGenerationRequest,
        provider: str = "",
        model: str = ""
    ) -> CodeGenerationResponse:
        """Procesa respuesta de IA y genera CodeGenerationResponse."""
        files = self.extract_code_blocks(response)

        # Validar cada archivo
        total_score = 0
        all_errors = []

        for file in files:
            validation = self.validate_code(file)
            file.validation = validation
            total_score += validation.score
            all_errors.extend(validation.errors)

        avg_score = total_score // len(files) if files else 0

        return CodeGenerationResponse(
            success=len(all_errors) == 0,
            files=files,
            explanation=self._extract_explanation(response),
            errors=all_errors,
            total_validation_score=avg_score,
            timestamp=datetime.now().isoformat(),
            provider=provider,
            model=model
        )

    def _extract_explanation(self, response: str) -> str:
        """Extrae explicación de la respuesta (texto fuera de bloques de código)."""
        # Remover bloques de código
        without_code = re.sub(r'```[\s\S]*?```', '', response)
        # Limpiar
        explanation = without_code.strip()
        # Limitar longitud
        if len(explanation) > 500:
            explanation = explanation[:500] + "..."
        return explanation
