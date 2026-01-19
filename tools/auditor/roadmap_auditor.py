"""
Roadmap Auditor - Sistema de auditoría para verificar progreso en roadmaps
Invocable por el orchestrator principal para verificar estado de proyectos.
"""

import os
import json
import subprocess
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path


class RoadmapAuditor:
    """
    Auditor de roadmaps que verifica el cumplimiento de cada fase.
    Diseñado para ser invocado por el orchestrator principal.
    """

    def __init__(self, roadmap_path: str = None):
        """
        Inicializa el auditor con un roadmap específico.

        Args:
            roadmap_path: Ruta al archivo JSON del roadmap
        """
        self.root_dir = Path(__file__).parent.parent.parent
        self.roadmaps_dir = self.root_dir / 'knowledge_base' / 'roadmaps'

        if roadmap_path:
            self.roadmap = self._load_roadmap(roadmap_path)
        else:
            self.roadmap = None

        self.audit_results = []
        self.last_audit_time = None

    def _load_roadmap(self, roadmap_path: str) -> Dict:
        """Carga un roadmap desde archivo JSON."""
        try:
            with open(roadmap_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando roadmap: {e}")
            return {}

    def list_available_roadmaps(self) -> List[Dict]:
        """Lista todos los roadmaps disponibles."""
        roadmaps = []
        if self.roadmaps_dir.exists():
            for file in self.roadmaps_dir.glob('*.json'):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        roadmaps.append({
                            'id': data.get('id', file.stem),
                            'title': data.get('title', 'Sin título'),
                            'path': str(file),
                            'phases_count': len(data.get('phases', []))
                        })
                except:
                    pass
        return roadmaps

    def audit_environment(self, item: str) -> Dict:
        """
        Audita un item de tipo environment.
        Placeholder para verificación de software instalado.
        """
        result = {
            'item': item,
            'type': 'environment',
            'status': 'pending',
            'message': ''
        }

        # Placeholder: Implementar verificaciones reales
        checks = {
            'Python 3.11+ instalado': self._check_python_version,
            'Docker instalado': self._check_docker,
            'GPU disponible': self._check_gpu
        }

        for check_name, check_func in checks.items():
            if check_name.lower() in item.lower():
                try:
                    is_valid, message = check_func()
                    result['status'] = 'passed' if is_valid else 'failed'
                    result['message'] = message
                    return result
                except Exception as e:
                    result['status'] = 'error'
                    result['message'] = str(e)
                    return result

        # Si no hay verificación específica, marcar como pendiente manual
        result['status'] = 'manual_check_required'
        result['message'] = 'Requiere verificación manual'
        return result

    def audit_library(self, item: str) -> Dict:
        """
        Audita un item de tipo library.
        Verifica si una librería Python es importable.
        """
        result = {
            'item': item,
            'type': 'library',
            'status': 'pending',
            'message': ''
        }

        # Extraer nombre de librería del item
        library_mappings = {
            'numpy': 'numpy',
            'pandas': 'pandas',
            'matplotlib': 'matplotlib',
            'seaborn': 'seaborn',
            'scikit-learn': 'sklearn',
            'tensorflow': 'tensorflow',
            'pytorch': 'torch',
            'langchain': 'langchain',
            'nltk': 'nltk',
            'spacy': 'spacy',
            'transformers': 'transformers',
            'mlflow': 'mlflow',
            'scipy': 'scipy',
            'statsmodels': 'statsmodels',
            'sqlalchemy': 'sqlalchemy',
            'pymongo': 'pymongo',
            'openai': 'openai',
            'anthropic': 'anthropic'
        }

        item_lower = item.lower()
        for lib_name, import_name in library_mappings.items():
            if lib_name in item_lower:
                try:
                    # Placeholder: En producción usar importlib
                    result['status'] = 'placeholder'
                    result['message'] = f'Verificación de {import_name} pendiente de implementación'
                    return result
                except:
                    pass

        result['status'] = 'unknown'
        result['message'] = 'Librería no reconocida'
        return result

    def audit_api(self, item: str) -> Dict:
        """
        Audita un item de tipo api.
        Verifica si una API key está configurada.
        """
        result = {
            'item': item,
            'type': 'api',
            'status': 'pending',
            'message': ''
        }

        api_env_vars = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'google': 'GOOGLE_AI_API_KEY',
            'gemini': 'GEMINI_API_KEY'
        }

        item_lower = item.lower()
        for api_name, env_var in api_env_vars.items():
            if api_name in item_lower:
                if os.environ.get(env_var):
                    result['status'] = 'passed'
                    result['message'] = f'{env_var} configurada'
                else:
                    result['status'] = 'failed'
                    result['message'] = f'{env_var} no encontrada en variables de entorno'
                return result

        result['status'] = 'unknown'
        result['message'] = 'API no reconocida'
        return result

    def audit_project(self, item: str, project_path: str = None) -> Dict:
        """
        Audita un item de tipo project.
        Placeholder para verificación de proyectos completados.
        """
        result = {
            'item': item,
            'type': 'project',
            'status': 'manual_check_required',
            'message': 'Requiere verificación manual del proyecto'
        }

        # Placeholder: Implementar verificación de estructura de proyecto
        if project_path and os.path.exists(project_path):
            result['status'] = 'exists'
            result['message'] = f'Proyecto encontrado en {project_path}'

        return result

    def audit_phase(self, phase_id: int) -> Dict:
        """
        Audita una fase completa del roadmap.

        Args:
            phase_id: ID de la fase a auditar

        Returns:
            Dict con resultados de auditoría de la fase
        """
        if not self.roadmap:
            return {'error': 'No hay roadmap cargado'}

        phases = self.roadmap.get('phases', [])
        phase = None
        for p in phases:
            if p.get('id') == phase_id:
                phase = p
                break

        if not phase:
            return {'error': f'Fase {phase_id} no encontrada'}

        results = {
            'phase_id': phase_id,
            'phase_name': phase.get('name', 'Sin nombre'),
            'audit_time': datetime.now().isoformat(),
            'checklist_results': [],
            'summary': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'pending': 0
            }
        }

        checklist = phase.get('audit_checklist', [])
        for check_item in checklist:
            item_text = check_item.get('item', '')
            item_type = check_item.get('type', 'unknown')

            if item_type == 'environment':
                check_result = self.audit_environment(item_text)
            elif item_type == 'library':
                check_result = self.audit_library(item_text)
            elif item_type == 'api':
                check_result = self.audit_api(item_text)
            elif item_type == 'project':
                check_result = self.audit_project(item_text)
            else:
                check_result = {
                    'item': item_text,
                    'type': item_type,
                    'status': 'manual_check_required',
                    'message': f'Tipo de auditoría no implementado: {item_type}'
                }

            results['checklist_results'].append(check_result)
            results['summary']['total'] += 1

            status = check_result.get('status', 'pending')
            if status == 'passed':
                results['summary']['passed'] += 1
            elif status == 'failed':
                results['summary']['failed'] += 1
            else:
                results['summary']['pending'] += 1

        return results

    def audit_full_roadmap(self) -> Dict:
        """
        Audita todas las fases del roadmap.

        Returns:
            Dict con resultados completos de auditoría
        """
        if not self.roadmap:
            return {'error': 'No hay roadmap cargado'}

        results = {
            'roadmap_id': self.roadmap.get('id', 'unknown'),
            'roadmap_title': self.roadmap.get('title', 'Sin título'),
            'audit_time': datetime.now().isoformat(),
            'phases_results': [],
            'overall_summary': {
                'total_phases': 0,
                'total_items': 0,
                'passed': 0,
                'failed': 0,
                'pending': 0
            }
        }

        phases = self.roadmap.get('phases', [])
        for phase in phases:
            phase_result = self.audit_phase(phase.get('id'))
            results['phases_results'].append(phase_result)

            results['overall_summary']['total_phases'] += 1
            results['overall_summary']['total_items'] += phase_result['summary']['total']
            results['overall_summary']['passed'] += phase_result['summary']['passed']
            results['overall_summary']['failed'] += phase_result['summary']['failed']
            results['overall_summary']['pending'] += phase_result['summary']['pending']

        self.audit_results = results
        self.last_audit_time = datetime.now()

        return results

    def _check_python_version(self) -> tuple:
        """Verifica la versión de Python."""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 11:
            return True, f"Python {version.major}.{version.minor}.{version.micro}"
        return False, f"Python {version.major}.{version.minor} (requiere 3.11+)"

    def _check_docker(self) -> tuple:
        """Verifica si Docker está instalado."""
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return True, result.stdout.strip()
            return False, "Docker no encontrado"
        except FileNotFoundError:
            return False, "Docker no instalado"

    def _check_gpu(self) -> tuple:
        """Verifica disponibilidad de GPU (placeholder)."""
        # Placeholder: Implementar verificación real de GPU
        return False, "Verificación de GPU no implementada"

    def generate_report(self, output_format: str = 'text') -> str:
        """
        Genera un reporte de los resultados de auditoría.

        Args:
            output_format: Formato de salida ('text', 'json', 'markdown')

        Returns:
            Reporte formateado
        """
        if not self.audit_results:
            return "No hay resultados de auditoría. Ejecute audit_full_roadmap() primero."

        if output_format == 'json':
            return json.dumps(self.audit_results, indent=2, ensure_ascii=False)

        elif output_format == 'markdown':
            report = f"# Reporte de Auditoría: {self.audit_results.get('roadmap_title', 'N/A')}\n\n"
            report += f"**Fecha:** {self.audit_results.get('audit_time', 'N/A')}\n\n"

            summary = self.audit_results.get('overall_summary', {})
            report += "## Resumen General\n\n"
            report += f"- Total de fases: {summary.get('total_phases', 0)}\n"
            report += f"- Total de items: {summary.get('total_items', 0)}\n"
            report += f"- Aprobados: {summary.get('passed', 0)}\n"
            report += f"- Fallidos: {summary.get('failed', 0)}\n"
            report += f"- Pendientes: {summary.get('pending', 0)}\n\n"

            for phase in self.audit_results.get('phases_results', []):
                report += f"### Fase {phase.get('phase_id')}: {phase.get('phase_name')}\n\n"
                for item in phase.get('checklist_results', []):
                    status_icon = "✅" if item['status'] == 'passed' else "❌" if item['status'] == 'failed' else "⏳"
                    report += f"- {status_icon} {item['item']}: {item['message']}\n"
                report += "\n"

            return report

        else:  # text
            report = f"=== Reporte de Auditoría: {self.audit_results.get('roadmap_title', 'N/A')} ===\n\n"
            summary = self.audit_results.get('overall_summary', {})
            report += f"Fases: {summary.get('total_phases', 0)} | "
            report += f"Items: {summary.get('total_items', 0)} | "
            report += f"OK: {summary.get('passed', 0)} | "
            report += f"FAIL: {summary.get('failed', 0)} | "
            report += f"Pendiente: {summary.get('pending', 0)}\n"

            return report


def main():
    """Función principal para testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Roadmap Auditor')
    parser.add_argument('--list', action='store_true', help='Listar roadmaps disponibles')
    parser.add_argument('--roadmap', help='Ruta al roadmap a auditar')
    parser.add_argument('--phase', type=int, help='Auditar fase específica')
    parser.add_argument('--full', action='store_true', help='Auditar roadmap completo')
    parser.add_argument('--format', choices=['text', 'json', 'markdown'], default='text',
                       help='Formato de salida')

    args = parser.parse_args()

    auditor = RoadmapAuditor()

    if args.list:
        roadmaps = auditor.list_available_roadmaps()
        print("Roadmaps disponibles:")
        for rm in roadmaps:
            print(f"  - {rm['id']}: {rm['title']} ({rm['phases_count']} fases)")
        return

    if args.roadmap:
        auditor = RoadmapAuditor(args.roadmap)

        if args.phase:
            result = auditor.audit_phase(args.phase)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif args.full:
            auditor.audit_full_roadmap()
            print(auditor.generate_report(args.format))
        else:
            print("Especifique --phase o --full para auditar")
    else:
        print("Use --list para ver roadmaps o --roadmap <ruta> para auditar")


if __name__ == "__main__":
    main()
