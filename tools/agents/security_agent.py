"""
Security Agent - Análisis de vulnerabilidades y compliance
Verifica código contra OWASP Top 10 y políticas de seguridad.
"""

import json
from typing import Dict, List, Any
from datetime import datetime


class SecurityAgent:
    """
    Agente especializado en seguridad y compliance.
    """

    def __init__(self, security_policies: Dict, ai_config: Dict):
        """
        Inicializa el agente de seguridad.

        Args:
            security_policies: Políticas de seguridad del proyecto
            ai_config: Configuración de AI
        """
        self.security_policies = security_policies
        self.ai_config = ai_config

        # OWASP Top 10 checks
        self.owasp_checks = [
            'broken_access_control',
            'cryptographic_failures',
            'injection',
            'insecure_design',
            'security_misconfiguration',
            'vulnerable_components',
            'identification_authentication_failures',
            'software_data_integrity_failures',
            'security_logging_monitoring_failures',
            'ssrf'
        ]

    def audit(self, code: str, language: str, context: Dict = None) -> Dict:
        """
        Audita código para vulnerabilidades de seguridad.

        Args:
            code: Código a auditar
            language: Lenguaje del código
            context: Contexto adicional

        Returns:
            Dict con resultado del audit
        """
        audit_result = {
            'timestamp': datetime.now().isoformat(),
            'language': language,
            'status': 'completed',
            'vulnerabilities': [],
            'compliance_checks': [],
            'passed': False,
            'risk_level': 'low'
        }

        # Run OWASP checks
        audit_result['vulnerabilities'].extend(self._check_owasp_top_10(code, language))

        # Check compliance with security policies
        audit_result['compliance_checks'].extend(self._check_compliance(code))

        # Determine risk level
        audit_result['risk_level'] = self._calculate_risk_level(audit_result['vulnerabilities'])
        audit_result['passed'] = audit_result['risk_level'] in ['low', 'medium']

        return audit_result

    def _check_owasp_top_10(self, code: str, language: str) -> List[Dict]:
        """Verifica contra OWASP Top 10."""
        vulnerabilities = []

        # A01: Broken Access Control
        if 'role' not in code.lower() and 'permission' not in code.lower():
            if 'router.' in code or 'app.' in code:
                vulnerabilities.append({
                    'owasp_id': 'A01',
                    'category': 'Broken Access Control',
                    'severity': 'high',
                    'description': 'No access control checks detected',
                    'recommendation': 'Implement role-based or attribute-based access control'
                })

        # A02: Cryptographic Failures
        if 'password' in code.lower():
            if 'bcrypt' not in code and 'argon2' not in code and 'scrypt' not in code:
                vulnerabilities.append({
                    'owasp_id': 'A02',
                    'category': 'Cryptographic Failures',
                    'severity': 'critical',
                    'description': 'Password handling without proper hashing',
                    'recommendation': 'Use bcrypt, argon2, or scrypt for password hashing'
                })

        # A03: Injection
        injection_patterns = [
            (r'query.*\+', 'SQL Injection risk - string concatenation in query'),
            (r'eval\(', 'Code injection risk - use of eval()'),
            (r'exec\(', 'Command injection risk - use of exec()')
        ]

        for pattern, description in injection_patterns:
            if any(p in code for p in [pattern.replace(r'\(', '(').replace(r'\+', '+')]):
                vulnerabilities.append({
                    'owasp_id': 'A03',
                    'category': 'Injection',
                    'severity': 'critical',
                    'description': description,
                    'recommendation': 'Use parameterized queries and avoid dynamic code execution'
                })

        # A05: Security Misconfiguration
        if 'cors' in code.lower():
            if '*' in code:
                vulnerabilities.append({
                    'owasp_id': 'A05',
                    'category': 'Security Misconfiguration',
                    'severity': 'medium',
                    'description': 'Overly permissive CORS configuration',
                    'recommendation': 'Restrict CORS to specific origins'
                })

        # A07: Identification and Authentication Failures
        if 'jwt' in code.lower() or 'token' in code.lower():
            if 'HS256' in code and 'secret' in code.lower():
                if len([line for line in code.split('\n') if 'secret' in line.lower()]) > 0:
                    vulnerabilities.append({
                        'owasp_id': 'A07',
                        'category': 'Authentication Failures',
                        'severity': 'high',
                        'description': 'Potential hardcoded secret for JWT',
                        'recommendation': 'Use environment variables for secrets'
                    })

        return vulnerabilities

    def _check_compliance(self, code: str) -> List[Dict]:
        """Verifica compliance con políticas de seguridad."""
        compliance_checks = []

        # Check auth strategy
        required_auth = self.security_policies.get('auth_strategy', 'JWT')
        if required_auth.lower() in code.lower():
            compliance_checks.append({
                'policy': 'auth_strategy',
                'status': 'compliant',
                'message': f'Uses required auth strategy: {required_auth}'
            })
        else:
            compliance_checks.append({
                'policy': 'auth_strategy',
                'status': 'non_compliant',
                'message': f'Does not use required auth strategy: {required_auth}'
            })

        # Check encryption requirements
        encryption_config = self.security_policies.get('encryption', {})
        password_hashing = encryption_config.get('password_hashing', 'bcrypt')

        if password_hashing.lower() in code.lower():
            compliance_checks.append({
                'policy': 'password_hashing',
                'status': 'compliant',
                'message': f'Uses required password hashing: {password_hashing}'
            })

        return compliance_checks

    def _calculate_risk_level(self, vulnerabilities: List[Dict]) -> str:
        """Calcula el nivel de riesgo general."""
        if not vulnerabilities:
            return 'low'

        severities = [v['severity'] for v in vulnerabilities]

        if 'critical' in severities:
            return 'critical'
        elif 'high' in severities:
            return 'high'
        elif 'medium' in severities:
            return 'medium'
        else:
            return 'low'

    def generate_threat_model(self, task: Dict) -> Dict:
        """
        Genera un threat model básico para una tarea.
        """
        threat_model = {
            'task_id': task.get('id', 'unknown'),
            'generated_at': datetime.now().isoformat(),
            'threats': [],
            'mitigations': []
        }

        # Analyze based on task type
        task_type = task.get('type', '')
        labels = task.get('labels', [])

        # Backend threats
        if 'backend' in task_type or any('backend' in label for label in labels):
            threat_model['threats'].extend([
                {
                    'category': 'Injection',
                    'description': 'SQL/NoSQL injection through API inputs',
                    'likelihood': 'high',
                    'impact': 'critical'
                },
                {
                    'category': 'Broken Authentication',
                    'description': 'Weak or missing authentication',
                    'likelihood': 'medium',
                    'impact': 'high'
                }
            ])

            threat_model['mitigations'].extend([
                'Use parameterized queries',
                'Implement input validation',
                'Use JWT with proper expiry',
                'Implement rate limiting'
            ])

        return threat_model


def main():
    print("Security Agent - Vulnerability Analysis")


if __name__ == "__main__":
    main()
