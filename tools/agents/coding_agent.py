"""
Coding Agent - Genera código desde planning documents
Utiliza prompts estructurados y RAG para generar código de calidad.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime


class CodingAgent:
    """
    Agente especializado en generación de código desde especificaciones.
    """

    def __init__(self, plan: Dict, ai_config: Dict):
        """
        Inicializa el agente de coding.

        Args:
            plan: Diccionario del plan.json
            ai_config: Configuración de AI
        """
        self.plan = plan
        self.ai_config = ai_config

        # Extract configurations
        self.tech_stack = plan.get('metadata', {}).get('techStack', 'Unknown')
        self.security_policies = plan.get('security_policies', {})
        self.quality_gates = plan.get('quality_gates', {})

        # Load prompt templates
        self.prompt_templates = ai_config.get('prompt_library', {}).get('task_templates', {})

    def generate_code(self, task: Dict, context: Optional[Dict] = None) -> Dict:
        """
        Genera código para una tarea específica.

        Args:
            task: Tarea con especificaciones
            context: Contexto adicional desde RAG

        Returns:
            Dict con código generado y metadata
        """
        task_type = task.get('type', 'feature_development')

        # Route to appropriate generator
        if task_type == 'backend_development':
            return self._generate_backend_code(task, context)
        elif task_type == 'frontend_development':
            return self._generate_frontend_code(task, context)
        elif task_type == 'database_development':
            return self._generate_database_code(task, context)
        else:
            return self._generate_generic_code(task, context)

    def _generate_backend_code(self, task: Dict, context: Optional[Dict]) -> Dict:
        """
        Genera código backend (API endpoints, business logic, etc.)
        """
        result = {
            'task_id': task.get('id', 'unknown'),
            'code_files': [],
            'generated_at': datetime.now().isoformat(),
            'status': 'success'
        }

        # Extract API endpoint info from acceptance criteria
        endpoints = self._extract_api_endpoints(task)

        for endpoint in endpoints:
            # Generate endpoint code
            code = self._generate_api_endpoint_code(endpoint, task)
            result['code_files'].append(code)

        # Generate tests
        test_code = self._generate_backend_tests(task, endpoints)
        result['code_files'].append(test_code)

        return result

    def _extract_api_endpoints(self, task: Dict) -> List[Dict]:
        """
        Extrae información de API endpoints desde la tarea.
        """
        endpoints = []

        # Parse acceptance criteria for endpoint patterns
        for criteria in task.get('acceptance_criteria', []):
            # Simple heuristic: look for REST verbs
            if any(verb in criteria.upper() for verb in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']):
                endpoint = {
                    'description': criteria,
                    'method': self._extract_http_method(criteria),
                    'path': self._extract_path(criteria, task),
                    'module': task.get('module', 'general')
                }
                endpoints.append(endpoint)

        # If no endpoints found, create a default one
        if not endpoints:
            endpoints.append({
                'description': task.get('story', ''),
                'method': 'POST',
                'path': f"/api/{task.get('module', 'general')}",
                'module': task.get('module', 'general')
            })

        return endpoints

    def _extract_http_method(self, criteria: str) -> str:
        """Extrae el método HTTP desde el criteria."""
        criteria_upper = criteria.upper()
        for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            if method in criteria_upper:
                return method
        return 'POST'  # Default

    def _extract_path(self, criteria: str, task: Dict) -> str:
        """Extrae el path del endpoint."""
        module = task.get('module', 'general')
        # Simple extraction (could be improved with NLP)
        return f"/api/{module}"

    def _generate_api_endpoint_code(self, endpoint: Dict, task: Dict) -> Dict:
        """
        Genera el código de un API endpoint.
        """
        method = endpoint['method'].lower()
        path = endpoint['path']
        module = endpoint['module']

        # Template para Express/Node.js (adaptable a otros frameworks)
        code_template = f"""
/**
 * {endpoint['description']}
 * Generated from: {task.get('story', 'N/A')}
 */

const express = require('express');
const router = express.Router();
const {{ authenticate }} = require('../middleware/auth');
const {{ validate }} = require('../middleware/validation');
const {{ {module}Schema }} = require('../schemas/{module}');

/**
 * {method.upper()} {path}
 * @route {method.upper()} {path}
 * @access {self._determine_access_level(task)}
 */
router.{method}('{path}',
  authenticate,
  validate({module}Schema),
  async (req, res, next) => {{
    try {{
      // Extract data from request
      const data = req.body;

      // Business logic here
      // TODO: Implement business logic based on acceptance criteria

      // Return response
      res.status(200).json({{
        success: true,
        data: data,
        message: '{module} operation completed'
      }});

    }} catch (error) {{
      next(error);
    }}
  }}
);

module.exports = router;
"""

        return {
            'file_path': f"src/routes/{module}.routes.js",
            'code': code_template,
            'language': 'javascript',
            'type': 'route'
        }

    def _determine_access_level(self, task: Dict) -> str:
        """Determina el nivel de acceso requerido."""
        labels = task.get('labels', [])
        if any('auth' in label.lower() for label in labels):
            return 'Private'
        return 'Public'

    def _generate_backend_tests(self, task: Dict, endpoints: List[Dict]) -> Dict:
        """
        Genera tests para los endpoints backend.
        """
        module = task.get('module', 'general')

        test_code = f"""
/**
 * Tests for {module} module
 * Generated from: {task.get('story', 'N/A')}
 */

const request = require('supertest');
const app = require('../app');
const {{ describe, it, expect, beforeAll, afterAll }} = require('@jest/globals');

describe('{module} API Tests', () => {{

  beforeAll(async () => {{
    // Setup test database
  }});

  afterAll(async () => {{
    // Cleanup
  }});

"""

        # Generate test for each endpoint
        for endpoint in endpoints:
            method = endpoint['method'].lower()
            path = endpoint['path']

            test_code += f"""
  describe('{endpoint["method"]} {path}', () => {{
    it('should handle valid request', async () => {{
      const response = await request(app)
        .{method}('{path}')
        .send({{
          // Test data here
        }});

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('success', true);
    }});

    it('should handle invalid request', async () => {{
      const response = await request(app)
        .{method}('{path}')
        .send({{}});

      expect(response.status).toBe(400);
    }});
  }});
"""

        test_code += "\n});\n"

        return {
            'file_path': f"tests/{module}.test.js",
            'code': test_code,
            'language': 'javascript',
            'type': 'test'
        }

    def _generate_frontend_code(self, task: Dict, context: Optional[Dict]) -> Dict:
        """
        Genera código frontend (componentes React, etc.)
        """
        result = {
            'task_id': task.get('id', 'unknown'),
            'code_files': [],
            'generated_at': datetime.now().isoformat(),
            'status': 'success'
        }

        module = task.get('module', 'general')

        # Generate React component
        component_code = self._generate_react_component(task, module)
        result['code_files'].append(component_code)

        # Generate component tests
        test_code = self._generate_frontend_tests(task, module)
        result['code_files'].append(test_code)

        return result

    def _generate_react_component(self, task: Dict, module: str) -> Dict:
        """Genera un componente React."""
        component_name = module.replace('-', '').capitalize()

        code = f"""
import React, {{ useState, useEffect }} from 'react';
import PropTypes from 'prop-types';

/**
 * {component_name} Component
 * {task.get('story', 'N/A')}
 */
const {component_name} = ({{ /* props */ }}) => {{
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {{
    // Component logic here
  }}, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {{error}}</div>;

  return (
    <div className="{module}-container">
      <h1>{component_name}</h1>
      {{/* Component UI here */}}
    </div>
  );
}};

{component_name}.propTypes = {{
  // Define prop types
}};

export default {component_name};
"""

        return {
            'file_path': f"src/components/{component_name}.jsx",
            'code': code,
            'language': 'javascript',
            'type': 'component'
        }

    def _generate_frontend_tests(self, task: Dict, module: str) -> Dict:
        """Genera tests para componente frontend."""
        component_name = module.replace('-', '').capitalize()

        code = f"""
import React from 'react';
import {{ render, screen, fireEvent }} from '@testing-library/react';
import {component_name} from './{component_name}';

describe('{component_name}', () => {{
  it('renders without crashing', () => {{
    render(<{component_name} />);
    expect(screen.getByText(/{component_name}/i)).toBeInTheDocument();
  }});

  // Add more tests based on acceptance criteria
}});
"""

        return {
            'file_path': f"src/components/{component_name}.test.jsx",
            'code': code,
            'language': 'javascript',
            'type': 'test'
        }

    def _generate_database_code(self, task: Dict, context: Optional[Dict]) -> Dict:
        """
        Genera código relacionado con base de datos (models, migrations, etc.)
        """
        result = {
            'task_id': task.get('id', 'unknown'),
            'code_files': [],
            'generated_at': datetime.now().isoformat(),
            'status': 'success'
        }

        # Placeholder: implementar según necesidades
        return result

    def _generate_generic_code(self, task: Dict, context: Optional[Dict]) -> Dict:
        """
        Genera código genérico para tareas no especializadas.
        """
        result = {
            'task_id': task.get('id', 'unknown'),
            'code_files': [],
            'generated_at': datetime.now().isoformat(),
            'status': 'pending',
            'message': 'Generic code generation not yet implemented'
        }
        return result

    def apply_security_policies(self, code: str) -> str:
        """
        Aplica políticas de seguridad al código generado.
        """
        # Placeholder: implementar checks de seguridad
        return code

    def apply_code_standards(self, code: str, language: str) -> str:
        """
        Aplica estándares de código (formatting, linting, etc.)
        """
        # Placeholder: integrar con prettier, eslint, etc.
        return code


def main():
    """Función principal para testing."""
    print("Coding Agent - Code Generation from Planning")
    print("This agent generates code based on planning documents and user stories.")


if __name__ == "__main__":
    main()
