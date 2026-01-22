"""
Security Policy Enforcer - Valida código contra políticas de seguridad
Enforces security policies defined in plan.json
"""

import json
import re
import os
import yaml
from typing import Dict, List, Any
from datetime import datetime


class SecurityPolicyEnforcer:
    """
    Enforcer de políticas de seguridad del proyecto.
    """

    def __init__(self, security_policies: Dict = None):
        """
        Inicializa el enforcer. Si no se dan políticas, intenta cargar threat-model.yaml.
        """
        self.security_policies = security_policies or {}
        
        if not self.security_policies:
            self._load_threat_model()

    def _load_threat_model(self):
        """Intenta cargar el modelo de amenazas desde project_meta."""
        # Asumimos que estamos corriendo desde la raíz o que podemos encontrar el archivo
        # Buscamos hacia arriba hasta encontrar project_meta
        base_path = os.getcwd()
        threat_path = os.path.join(base_path, 'project_meta', 'security', 'threat-model.yaml')
        
        if os.path.exists(threat_path):
            try:
                with open(threat_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    # Mapear threat model a security policies simples
                    self.security_policies['auth_strategy'] = "JWT" # Default extraction logic
                    # Aquí se podría hacer un mapeo más complejo
                    print(f"Loaded threat model from {threat_path}")
            except Exception as e:
                print(f"Error loading threat model: {e}")

    def validate_against_plan(self, code: str, language: str) -> Dict:
        """
        Valida que el código cumple con las políticas de seguridad.

        Args:
            code: Código a validar
            language: Lenguaje del código

        Returns:
            Dict con resultado de la validación
        """
        result = {
            'timestamp': datetime.now().isoformat(),
            'compliant': True,
            'violations': [],
            'warnings': [],
            'passed_checks': []
        }

        # Check 1: Secrets hardcodeados
        if self.detect_secrets(code):
            result['violations'].append({
                'policy': 'no_hardcoded_secrets',
                'severity': 'critical',
                'message': 'Hardcoded secrets detected',
                'remediation': 'Use environment variables for secrets'
            })
            result['compliant'] = False
        else:
            result['passed_checks'].append('no_hardcoded_secrets')

        # Check 2: Authentication strategy
        auth_check = self._validate_auth_strategy(code)
        if not auth_check['compliant']:
            result['violations'].append(auth_check)
            result['compliant'] = False
        else:
            result['passed_checks'].append('auth_strategy')

        # Check 3: Crypto algorithms
        crypto_check = self._validate_crypto(code)
        if not crypto_check['compliant']:
            result['violations'].append(crypto_check)
            result['compliant'] = False
        else:
            result['passed_checks'].append('crypto_algorithms')

        # Check 4: Input validation
        validation_check = self._validate_input_validation(code)
        if not validation_check['compliant']:
            result['warnings'].append(validation_check)
        else:
            result['passed_checks'].append('input_validation')

        # Check 5: Security headers
        if language in ['javascript', 'typescript']:
            headers_check = self._validate_security_headers(code)
            if not headers_check['compliant']:
                result['warnings'].append(headers_check)
            else:
                result['passed_checks'].append('security_headers')

        return result

    def detect_secrets(self, code: str) -> bool:
        """
        Detecta secrets hardcodeados en el código.

        Returns:
            True si encuentra secrets
        """
        # Patterns for common secrets
        secret_patterns = [
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'api[_-]?secret\s*=\s*["\'][^"\']+["\']',
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'private[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'aws[_-]?access[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
        ]

        for pattern in secret_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                # Exclude common false positives
                if 'process.env' not in code and 'env.' not in code.lower():
                    return True

        return False

    def _validate_auth_strategy(self, code: str) -> Dict:
        """Valida que se use la estrategia de autenticación correcta."""
        required_auth = self.security_policies.get('auth_strategy', 'JWT')

        result = {
            'policy': 'auth_strategy',
            'severity': 'high',
            'compliant': True
        }

        # Check if code contains auth-related logic
        has_auth_logic = any(keyword in code.lower() for keyword in ['auth', 'login', 'token', 'session'])

        if has_auth_logic:
            # Verify it uses the required strategy
            if required_auth.lower() not in code.lower():
                result['compliant'] = False
                result['message'] = f'Does not use required auth strategy: {required_auth}'
                result['remediation'] = f'Implement {required_auth} authentication'

        return result

    def _validate_crypto(self, code: str) -> Dict:
        """Valida que se usen algoritmos criptográficos permitidos."""
        result = {
            'policy': 'crypto_algorithms',
            'severity': 'high',
            'compliant': True
        }

        encryption_config = self.security_policies.get('encryption', {})
        password_hashing = encryption_config.get('password_hashing', 'bcrypt')

        # Check for weak algorithms
        weak_algorithms = ['md5', 'sha1', 'des']

        for weak_algo in weak_algorithms:
            if weak_algo in code.lower():
                result['compliant'] = False
                result['message'] = f'Weak cryptographic algorithm detected: {weak_algo}'
                result['remediation'] = f'Use strong algorithms like {password_hashing} for password hashing, AES-256 for encryption'

        return result

    def _validate_input_validation(self, code: str) -> Dict:
        """Valida que exista validación de inputs."""
        result = {
            'policy': 'input_validation',
            'severity': 'medium',
            'compliant': True
        }

        validator = self.security_policies.get('input_validation', {}).get('validator', 'joi')

        # Check if code handles user input
        handles_input = any(keyword in code for keyword in ['req.body', 'req.params', 'req.query', 'request.'])

        if handles_input:
            # Check for validation
            has_validation = validator.lower() in code.lower() or 'validate' in code.lower()

            if not has_validation:
                result['compliant'] = False
                result['message'] = 'No input validation detected'
                result['remediation'] = f'Add input validation using {validator}'

        return result

    def _validate_security_headers(self, code: str) -> Dict:
        """Valida que se configuren security headers."""
        result = {
            'policy': 'security_headers',
            'severity': 'medium',
            'compliant': True
        }

        headers_config = self.security_policies.get('security_headers', {})
        helmet_enabled = headers_config.get('helmet_enabled', True)

        if helmet_enabled:
            # Check for Express app configuration
            is_express_app = 'express()' in code or 'app = ' in code

            if is_express_app:
                if 'helmet' not in code.lower():
                    result['compliant'] = False
                    result['message'] = 'Helmet middleware not configured'
                    result['remediation'] = 'Add app.use(helmet()) to configure security headers'

        return result

    def scan_for_vulnerabilities(self, code: str, language: str) -> Dict:
        """
        Escanea código en busca de vulnerabilidades comunes.

        Returns:
            Dict con vulnerabilidades encontradas
        """
        vulnerabilities = []

        # SQL Injection
        if 'sql' in code.lower() or 'query' in code.lower():
            if '+' in code or '${' in code:
                vulnerabilities.append({
                    'type': 'SQL Injection',
                    'severity': 'critical',
                    'description': 'Possible SQL injection through string concatenation',
                    'line': None
                })

        # XSS
        if 'innerHTML' in code:
            vulnerabilities.append({
                'type': 'XSS',
                'severity': 'high',
                'description': 'Potential XSS vulnerability through innerHTML',
                'line': None
            })

        # Path Traversal
        if 'readFile' in code or 'fs.' in code:
            if 'req.' in code:
                vulnerabilities.append({
                    'type': 'Path Traversal',
                    'severity': 'high',
                    'description': 'Possible path traversal if user input is used',
                    'line': None
                })

        # Command Injection
        if 'exec' in code or 'spawn' in code:
            vulnerabilities.append({
                'type': 'Command Injection',
                'severity': 'critical',
                'description': 'Potential command injection through exec/spawn',
                'line': None
            })

        return {
            'total_vulnerabilities': len(vulnerabilities),
            'vulnerabilities': vulnerabilities
        }


def main():
    """Función principal para testing."""
    print("Security Policy Enforcer")

    # Example usage
    sample_code = '''
    const express = require('express');
    const app = express();

    app.post('/login', (req, res) => {
        const password = 'hardcoded_password_123';
        // Authentication logic
    });
    '''

    enforcer = SecurityPolicyEnforcer({
        'auth_strategy': 'JWT',
        'encryption': {
            'password_hashing': 'bcrypt'
        }
    })

    result = enforcer.validate_against_plan(sample_code, 'javascript')
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
