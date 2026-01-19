"""
Site Indexer - Sistema de indexación con cache para Hands On AI
Se ejecuta al iniciar orchestrator.py y cachea después del primer inicio.
Similar a un sitemap para SEO - permite a las máquinas entender la estructura.
"""

import os
import json
import hashlib
import glob
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path


class SiteIndexer:
    """
    Indexador del sitio que crea un mapa completo del proyecto.
    Diseñado para ejecutarse al inicio y cachear resultados.
    """

    def __init__(self, root_dir: str = None):
        """
        Inicializa el indexador.

        Args:
            root_dir: Directorio raíz del proyecto
        """
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).parent.parent.parent
        self.cache_dir = self.root_dir / 'data' / 'cache'
        self.index_file = self.cache_dir / 'site_index.json'
        self.hash_file = self.cache_dir / 'content_hash.json'

        # Asegurar que existe el directorio de cache
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Índice actual
        self.index = None
        self.is_cached = False

    def _calculate_directory_hash(self) -> str:
        """
        Calcula un hash de todo el contenido indexable.
        Usado para detectar cambios y invalidar cache.
        """
        content_hash = hashlib.md5()

        indexable_patterns = [
            'knowledge_base/**/*.md',
            'knowledge_base/**/*.json',
            'project_meta/**/*.json',
            'project_meta/**/*.md',
            'tools/**/*.py',
            'external/**/*.md',
            '*.py',
            '*.json'
        ]

        files_to_hash = []
        for pattern in indexable_patterns:
            files_to_hash.extend(glob.glob(str(self.root_dir / pattern), recursive=True))

        # Ordenar para consistencia
        files_to_hash.sort()

        for file_path in files_to_hash:
            try:
                mtime = os.path.getmtime(file_path)
                content_hash.update(f"{file_path}:{mtime}".encode())
            except:
                pass

        return content_hash.hexdigest()

    def _is_cache_valid(self) -> bool:
        """Verifica si el cache es válido."""
        if not self.index_file.exists() or not self.hash_file.exists():
            return False

        try:
            with open(self.hash_file, 'r') as f:
                cached_hash = json.load(f).get('hash', '')

            current_hash = self._calculate_directory_hash()
            return cached_hash == current_hash
        except:
            return False

    def _load_cache(self) -> bool:
        """Carga el índice desde cache."""
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
            self.is_cached = True
            return True
        except:
            return False

    def _save_cache(self):
        """Guarda el índice en cache."""
        try:
            # Guardar índice
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2, ensure_ascii=False)

            # Guardar hash
            with open(self.hash_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'hash': self._calculate_directory_hash(),
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)

        except Exception as e:
            pass

    def index_knowledge_base(self) -> Dict:
        """Indexa la knowledge base."""
        kb_dir = self.root_dir / 'knowledge_base'
        kb_index = {
            'path': str(kb_dir),
            'categories': {},
            'total_files': 0,
            'total_technologies': 0
        }

        if not kb_dir.exists():
            return kb_index

        # Indexar categorías principales
        for category_dir in kb_dir.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('.'):
                category_name = category_dir.name
                kb_index['categories'][category_name] = {
                    'path': str(category_dir),
                    'items': []
                }

                # Indexar archivos en la categoría
                for file_path in category_dir.rglob('*.md'):
                    kb_index['categories'][category_name]['items'].append({
                        'name': file_path.stem,
                        'path': str(file_path),
                        'relative_path': str(file_path.relative_to(self.root_dir))
                    })
                    kb_index['total_files'] += 1

                # Contar tecnologías
                if category_name == 'technologies':
                    kb_index['total_technologies'] = len(kb_index['categories'][category_name]['items'])

        return kb_index

    def index_project_meta(self) -> Dict:
        """Indexa project_meta."""
        meta_dir = self.root_dir / 'project_meta'
        meta_index = {
            'path': str(meta_dir),
            'sections': {},
            'schemas': []
        }

        if not meta_dir.exists():
            return meta_index

        for section_dir in meta_dir.iterdir():
            if section_dir.is_dir():
                section_name = section_dir.name
                meta_index['sections'][section_name] = {
                    'path': str(section_dir),
                    'files': []
                }

                for file_path in section_dir.glob('*'):
                    if file_path.is_file():
                        meta_index['sections'][section_name]['files'].append({
                            'name': file_path.name,
                            'path': str(file_path),
                            'type': file_path.suffix
                        })

        return meta_index

    def index_tools(self) -> Dict:
        """Indexa herramientas."""
        tools_dir = self.root_dir / 'tools'
        tools_index = {
            'path': str(tools_dir),
            'categories': {},
            'total_tools': 0
        }

        if not tools_dir.exists():
            return tools_index

        for tool_dir in tools_dir.iterdir():
            if tool_dir.is_dir() and not tool_dir.name.startswith('__'):
                category_name = tool_dir.name
                tools_index['categories'][category_name] = {
                    'path': str(tool_dir),
                    'scripts': []
                }

                for py_file in tool_dir.glob('*.py'):
                    tools_index['categories'][category_name]['scripts'].append({
                        'name': py_file.stem,
                        'path': str(py_file),
                        'executable': True
                    })
                    tools_index['total_tools'] += 1

        return tools_index

    def index_external_providers(self) -> Dict:
        """Indexa proveedores externos clonados."""
        external_dir = self.root_dir / 'external' / 'providers'
        providers_index = {
            'path': str(external_dir),
            'providers': {}
        }

        if not external_dir.exists():
            return providers_index

        for provider_dir in external_dir.iterdir():
            if provider_dir.is_dir():
                provider_name = provider_dir.name
                providers_index['providers'][provider_name] = {
                    'path': str(provider_dir),
                    'repositories': []
                }

                for repo_dir in provider_dir.iterdir():
                    if repo_dir.is_dir() and not repo_dir.name.startswith('.'):
                        providers_index['providers'][provider_name]['repositories'].append({
                            'name': repo_dir.name,
                            'path': str(repo_dir),
                            'has_readme': (repo_dir / 'README.md').exists()
                        })

        return providers_index

    def index_roadmaps(self) -> Dict:
        """Indexa roadmaps disponibles."""
        roadmaps_dir = self.root_dir / 'knowledge_base' / 'roadmaps'
        roadmaps_index = {
            'path': str(roadmaps_dir),
            'roadmaps': []
        }

        if not roadmaps_dir.exists():
            return roadmaps_index

        for roadmap_file in roadmaps_dir.glob('*.json'):
            try:
                with open(roadmap_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    roadmaps_index['roadmaps'].append({
                        'id': data.get('id', roadmap_file.stem),
                        'title': data.get('title', 'Sin título'),
                        'path': str(roadmap_file),
                        'phases_count': len(data.get('phases', []))
                    })
            except:
                pass

        return roadmaps_index

    def build_index(self, force: bool = False) -> Dict:
        """
        Construye el índice completo del sitio.

        Args:
            force: Forzar reconstrucción ignorando cache

        Returns:
            Índice completo del sitio
        """
        # Verificar cache
        if not force and self._is_cache_valid():
            if self._load_cache():
                return self.index


        self.index = {
            'metadata': {
                'version': '1.0.0',
                'generated_at': datetime.now().isoformat(),
                'root_dir': str(self.root_dir),
                'total_items': 0
            },
            'knowledge_base': self.index_knowledge_base(),
            'project_meta': self.index_project_meta(),
            'tools': self.index_tools(),
            'external_providers': self.index_external_providers(),
            'roadmaps': self.index_roadmaps()
        }

        # Calcular totales
        total = 0
        total += self.index['knowledge_base']['total_files']
        total += self.index['tools']['total_tools']
        total += len(self.index['roadmaps']['roadmaps'])
        for provider in self.index['external_providers']['providers'].values():
            total += len(provider['repositories'])

        self.index['metadata']['total_items'] = total

        # Guardar cache
        self._save_cache()

        return self.index

    def get_sitemap(self) -> List[Dict]:
        """
        Genera un sitemap simplificado.

        Returns:
            Lista de URLs/rutas indexadas
        """
        if not self.index:
            self.build_index()

        sitemap = []

        # Knowledge base
        for category, data in self.index['knowledge_base']['categories'].items():
            for item in data['items']:
                sitemap.append({
                    'type': 'knowledge',
                    'category': category,
                    'name': item['name'],
                    'path': item['relative_path']
                })

        # Tools
        for category, data in self.index['tools']['categories'].items():
            for script in data['scripts']:
                sitemap.append({
                    'type': 'tool',
                    'category': category,
                    'name': script['name'],
                    'path': script['path']
                })

        # Roadmaps
        for roadmap in self.index['roadmaps']['roadmaps']:
            sitemap.append({
                'type': 'roadmap',
                'name': roadmap['title'],
                'path': roadmap['path']
            })

        # External providers
        for provider, data in self.index['external_providers']['providers'].items():
            for repo in data['repositories']:
                sitemap.append({
                    'type': 'external',
                    'provider': provider,
                    'name': repo['name'],
                    'path': repo['path']
                })

        return sitemap

    def search(self, query: str) -> List[Dict]:
        """
        Busca en el índice.

        Args:
            query: Término de búsqueda

        Returns:
            Lista de resultados
        """
        if not self.index:
            self.build_index()

        results = []
        query_lower = query.lower()

        for item in self.get_sitemap():
            if query_lower in item['name'].lower():
                results.append(item)
            elif query_lower in item.get('category', '').lower():
                results.append(item)
            elif query_lower in item.get('provider', '').lower():
                results.append(item)

        return results

    def get_statistics(self) -> Dict:
        """
        Obtiene estadísticas del índice.

        Returns:
            Diccionario con estadísticas
        """
        if not self.index:
            self.build_index()

        return {
            'total_items': self.index['metadata']['total_items'],
            'knowledge_base_files': self.index['knowledge_base']['total_files'],
            'total_technologies': self.index['knowledge_base']['total_technologies'],
            'total_tools': self.index['tools']['total_tools'],
            'total_roadmaps': len(self.index['roadmaps']['roadmaps']),
            'external_providers': len(self.index['external_providers']['providers']),
            'cached': self.is_cached,
            'generated_at': self.index['metadata']['generated_at']
        }


def init_index(root_dir: str = None, force: bool = False) -> SiteIndexer:
    """
    Función de conveniencia para inicializar el índice.
    Llamar desde orchestrator.py al inicio.

    Args:
        root_dir: Directorio raíz
        force: Forzar reconstrucción

    Returns:
        Instancia de SiteIndexer con índice cargado
    """
    indexer = SiteIndexer(root_dir)
    indexer.build_index(force=force)
    return indexer


def main():
    """Función principal para testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Site Indexer')
    parser.add_argument('--force', action='store_true', help='Forzar reconstrucción')
    parser.add_argument('--stats', action='store_true', help='Mostrar estadísticas')
    parser.add_argument('--sitemap', action='store_true', help='Generar sitemap')
    parser.add_argument('--search', type=str, help='Buscar en el índice')

    args = parser.parse_args()

    indexer = SiteIndexer()

    if args.force:
        indexer.build_index(force=True)
    else:
        indexer.build_index()

    if args.stats:
        stats = indexer.get_statistics()
        print("\n📊 Estadísticas del Índice:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

    if args.sitemap:
        sitemap = indexer.get_sitemap()
        print(f"\n🗺️ Sitemap ({len(sitemap)} items):")
        for item in sitemap[:20]:  # Mostrar primeros 20
            print(f"  [{item['type']}] {item['name']}")
        if len(sitemap) > 20:
            print(f"  ... y {len(sitemap) - 20} más")

    if args.search:
        results = indexer.search(args.search)
        print(f"\n🔍 Resultados para '{args.search}' ({len(results)}):")
        for result in results:
            print(f"  [{result['type']}] {result['name']}: {result['path']}")


if __name__ == "__main__":
    main()
