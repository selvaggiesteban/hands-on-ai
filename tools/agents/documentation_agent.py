"""
Documentation Agent - Generación y actualización de documentación
Genera documentación automática desde código y planning documents.
"""

import json
import re
from typing import Dict, List, Any
from datetime import datetime


class DocumentationAgent:
    """
    Agente especializado en generación de documentación.
    """

    def __init__(self, ai_config: Dict):
        """
        Inicializa el agente de documentación.

        Args:
            ai_config: Configuración de AI
        """
        self.ai_config = ai_config

    def generate_docs(self, code: str, language: str, doc_type: str = "api") -> Dict:
        """
        Genera documentación para código.

        Args:
            code: Código fuente
            language: Lenguaje del código
            doc_type: Tipo de documentación (api/module/class/function)

        Returns:
            Dict con documentación generada
        """
        result = {
            'timestamp': datetime.now().isoformat(),
            'language': language,
            'doc_type': doc_type,
            'documentation': '',
            'format': 'markdown'
        }

        if doc_type == "api":
            result['documentation'] = self._generate_api_docs(code, language)
        elif doc_type == "module":
            result['documentation'] = self._generate_module_docs(code, language)
        elif doc_type == "function":
            result['documentation'] = self._generate_function_docs(code, language)
        else:
            result['documentation'] = self._generate_generic_docs(code, language)

        return result

    def _generate_api_docs(self, code: str, language: str) -> str:
        """Genera documentación de API."""
        docs = "# API Documentation\n\n"
        docs += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # Extract API endpoints
        endpoints = self._extract_endpoints(code)

        if endpoints:
            docs += "## Endpoints\n\n"
            for endpoint in endpoints:
                docs += f"### {endpoint['method']} {endpoint['path']}\n\n"
                docs += f"**Description**: {endpoint.get('description', 'No description')}\n\n"

                if endpoint.get('params'):
                    docs += "**Parameters**:\n"
                    for param in endpoint['params']:
                        docs += f"- `{param}`: (description)\n"
                    docs += "\n"

                docs += "**Response**:\n```json\n{\n  \"success\": true,\n  \"data\": {}\n}\n```\n\n"
        else:
            docs += "No endpoints found in code.\n\n"

        return docs

    def _extract_endpoints(self, code: str) -> List[Dict]:
        """Extrae endpoints del código."""
        endpoints = []

        # Pattern for Express routes: router.METHOD('path', ...)
        patterns = [
            r"router\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]",
            r"app\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]"
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                method = match.group(1).upper()
                path = match.group(2)

                endpoints.append({
                    'method': method,
                    'path': path,
                    'description': self._extract_description(code, path)
                })

        return endpoints

    def _extract_description(self, code: str, path: str) -> str:
        """Extrae descripción de un endpoint desde comentarios."""
        lines = code.split('\n')

        for i, line in enumerate(lines):
            if path in line:
                # Look for comment in previous lines
                for j in range(max(0, i - 5), i):
                    if '/**' in lines[j] or '//' in lines[j]:
                        comment = lines[j].strip().lstrip('/*').rstrip('*/').strip('/').strip()
                        if comment:
                            return comment

        return "No description available"

    def _generate_module_docs(self, code: str, language: str) -> str:
        """Genera documentación de módulo."""
        docs = "# Module Documentation\n\n"

        # Extract module description from top comment
        lines = code.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            if '/**' in line or '"""' in line or '#' in line:
                description = line.strip().lstrip('/*#').rstrip('*/').strip()
                if description:
                    docs += f"{description}\n\n"
                    break

        # Extract functions/classes
        docs += "## Functions\n\n"

        if language in ['javascript', 'typescript']:
            functions = re.findall(r'(?:function|const)\s+(\w+)\s*\(([^)]*)\)', code)
            for func_name, params in functions:
                docs += f"### `{func_name}({params})`\n\n"
                docs += "Description: TODO\n\n"

        elif language == 'python':
            functions = re.findall(r'def\s+(\w+)\s*\(([^)]*)\)', code)
            for func_name, params in functions:
                docs += f"### `{func_name}({params})`\n\n"
                docs += "Description: TODO\n\n"

        return docs

    def _generate_function_docs(self, code: str, language: str) -> str:
        """Genera documentación de función específica."""
        docs = "# Function Documentation\n\n"

        # Extract function signature
        if language in ['javascript', 'typescript']:
            match = re.search(r'(?:function|const)\s+(\w+)\s*\(([^)]*)\)', code)
            if match:
                func_name = match.group(1)
                params = match.group(2)
                docs += f"## `{func_name}({params})`\n\n"

        elif language == 'python':
            match = re.search(r'def\s+(\w+)\s*\(([^)]*)\)', code)
            if match:
                func_name = match.group(1)
                params = match.group(2)
                docs += f"## `{func_name}({params})`\n\n"

        docs += "### Description\n\nTODO: Add description\n\n"
        docs += "### Parameters\n\nTODO: Document parameters\n\n"
        docs += "### Returns\n\nTODO: Document return value\n\n"
        docs += "### Example\n\n```\nTODO: Add example usage\n```\n\n"

        return docs

    def _generate_generic_docs(self, code: str, language: str) -> str:
        """Genera documentación genérica."""
        docs = "# Code Documentation\n\n"
        docs += f"Language: {language}\n\n"
        docs += "## Overview\n\nTODO: Add overview\n\n"

        return docs

    def update_readme(self, project_info: Dict) -> str:
        """
        Genera/actualiza README.md del proyecto.

        Args:
            project_info: Información del proyecto

        Returns:
            Contenido del README
        """
        readme = f"# {project_info.get('name', 'Project')}\n\n"
        readme += f"{project_info.get('description', 'Project description')}\n\n"

        readme += "## Features\n\n"
        for feature in project_info.get('features', []):
            readme += f"- {feature}\n"
        readme += "\n"

        readme += "## Tech Stack\n\n"
        readme += f"{project_info.get('tech_stack', 'Not specified')}\n\n"

        readme += "## Installation\n\n"
        readme += "```bash\n"
        readme += "npm install\n"
        readme += "```\n\n"

        readme += "## Usage\n\n"
        readme += "```bash\n"
        readme += "npm start\n"
        readme += "```\n\n"

        readme += "## Documentation\n\n"
        readme += "See [docs/](./docs/) for detailed documentation.\n\n"

        readme += "## License\n\n"
        readme += "MIT\n"

        return readme

    def generate_changelog(self, changes: List[Dict]) -> str:
        """
        Genera CHANGELOG.md

        Args:
            changes: Lista de cambios

        Returns:
            Contenido del changelog
        """
        changelog = "# Changelog\n\n"
        changelog += "All notable changes to this project will be documented in this file.\n\n"

        # Group by version
        versions = {}
        for change in changes:
            version = change.get('version', 'Unreleased')
            if version not in versions:
                versions[version] = []
            versions[version].append(change)

        for version, changes_list in sorted(versions.items(), reverse=True):
            changelog += f"## [{version}]\n\n"

            # Group by type
            by_type = {'added': [], 'changed': [], 'fixed': [], 'removed': []}
            for change in changes_list:
                change_type = change.get('type', 'changed')
                by_type[change_type].append(change)

            for type_name, type_changes in by_type.items():
                if type_changes:
                    changelog += f"### {type_name.capitalize()}\n\n"
                    for change in type_changes:
                        changelog += f"- {change.get('description', 'No description')}\n"
                    changelog += "\n"

        return changelog


def main():
    print("Documentation Agent - Automated Documentation Generation")


if __name__ == "__main__":
    main()
