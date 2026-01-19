"""
RAG Knowledge Indexer - Sistema de indexación para documentos de planning
Indexa y gestiona embeddings de documentos de planning y knowledge base.
"""

import os
import json
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import glob


class PlanningRAG:
    """
    Sistema RAG para indexar y recuperar contexto relevante desde planning documents.
    """

    def __init__(self, config_path: str = None):
        """
        Inicializa el sistema RAG.

        Args:
            config_path: Ruta al archivo rag-config.json
        """
        # Load configuration
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = self._default_config()

        # Initialize vector store (placeholder - requires actual vector DB)
        self.vectorstore = None
        self.embeddings_model = None

        # Document cache
        self.indexed_documents = {}
        self.document_index = {}

        # Paths
        self.kb_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.persist_directory = self.config.get('vector_store', {}).get('configuration', {}).get('persist_directory', './data/chroma_db')

    def _default_config(self) -> Dict:
        """Retorna configuración por defecto."""
        return {
            "vector_store": {
                "provider": "simple",
                "configuration": {
                    "persist_directory": "./data/chroma_db"
                }
            },
            "embedding_model": {
                "provider": "simple",
                "model": "tfidf"
            },
            "chunking_strategy": {
                "strategy": "fixed",
                "chunk_size": 1000,
                "chunk_overlap": 200
            },
            "indexing": {
                "index_patterns": [
                    "knowledge_base/**/*.md",
                    "project_meta/**/*.json",
                    "project_meta/**/*.md"
                ]
            }
        }

    def index_planning_docs(self) -> Dict:
        """
        Indexa todos los documentos de planning.

        Returns:
            Dict con estadísticas de indexación
        """
        stats = {
            'start_time': datetime.now().isoformat(),
            'documents_processed': 0,
            'chunks_created': 0,
            'errors': []
        }

        # Get all files to index
        files_to_index = self._get_files_to_index()

        print(f"Indexing {len(files_to_index)} files...")

        for file_path in files_to_index:
            try:
                # Process file
                chunks = self._process_document(file_path)
                stats['chunks_created'] += len(chunks)
                stats['documents_processed'] += 1

                print(f"  ✓ Indexed: {file_path} ({len(chunks)} chunks)")

            except Exception as e:
                stats['errors'].append({
                    'file': file_path,
                    'error': str(e)
                })
                print(f"  ✗ Error indexing {file_path}: {e}")

        stats['end_time'] = datetime.now().isoformat()

        # Save index
        self._save_index(stats)

        return stats

    def _get_files_to_index(self) -> List[str]:
        """Obtiene lista de archivos a indexar."""
        files = []

        index_patterns = self.config.get('indexing', {}).get('index_patterns', [])

        for pattern in index_patterns:
            full_pattern = os.path.join(self.kb_root, pattern)
            matched_files = glob.glob(full_pattern, recursive=True)
            files.extend(matched_files)

        # Remove duplicates
        files = list(set(files))

        # Apply exclusions
        exclude_patterns = self.config.get('indexing', {}).get('exclude_patterns', [])
        for exclude_pattern in exclude_patterns:
            files = [f for f in files if exclude_pattern not in f]

        return files

    def _process_document(self, file_path: str) -> List[Dict]:
        """
        Procesa un documento y lo divide en chunks.

        Args:
            file_path: Ruta al documento

        Returns:
            Lista de chunks con metadata
        """
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata
        metadata = self._extract_metadata(file_path, content)

        # Chunk document
        chunks = self._chunk_document(content, file_path)

        # Add metadata to each chunk
        for chunk in chunks:
            chunk['metadata'] = metadata

        # Store in index
        doc_id = self._generate_doc_id(file_path)
        self.indexed_documents[doc_id] = {
            'file_path': file_path,
            'chunks': chunks,
            'metadata': metadata,
            'indexed_at': datetime.now().isoformat()
        }

        return chunks

    def _chunk_document(self, content: str, file_path: str) -> List[Dict]:
        """
        Divide un documento en chunks.

        Args:
            content: Contenido del documento
            file_path: Ruta del archivo

        Returns:
            Lista de chunks
        """
        strategy = self.config.get('chunking_strategy', {}).get('strategy', 'fixed')
        chunk_size = self.config.get('chunking_strategy', {}).get('chunk_size', 1000)
        chunk_overlap = self.config.get('chunking_strategy', {}).get('chunk_overlap', 200)

        chunks = []

        if strategy == "fixed":
            # Fixed-size chunking
            for i in range(0, len(content), chunk_size - chunk_overlap):
                chunk_text = content[i:i + chunk_size]
                if chunk_text.strip():
                    chunks.append({
                        'text': chunk_text,
                        'start': i,
                        'end': i + len(chunk_text),
                        'chunk_id': len(chunks)
                    })

        elif strategy == "semantic":
            # Semantic chunking (simple paragraph-based)
            paragraphs = content.split('\n\n')
            current_chunk = ""

            for para in paragraphs:
                if len(current_chunk) + len(para) < chunk_size:
                    current_chunk += para + "\n\n"
                else:
                    if current_chunk.strip():
                        chunks.append({
                            'text': current_chunk,
                            'chunk_id': len(chunks)
                        })
                    current_chunk = para + "\n\n"

            if current_chunk.strip():
                chunks.append({
                    'text': current_chunk,
                    'chunk_id': len(chunks)
                })

        return chunks

    def _extract_metadata(self, file_path: str, content: str) -> Dict:
        """
        Extrae metadata del documento.

        Args:
            file_path: Ruta del archivo
            content: Contenido del documento

        Returns:
            Dict con metadata
        """
        metadata = {
            'file_path': file_path,
            'file_type': os.path.splitext(file_path)[1],
            'file_name': os.path.basename(file_path),
            'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
            'size': len(content)
        }

        # Extract additional metadata based on file type
        if file_path.endswith('.json'):
            try:
                data = json.loads(content)
                if 'title' in data:
                    metadata['title'] = data['title']
                if 'metadata' in data:
                    metadata.update(data['metadata'])
            except:
                pass

        elif file_path.endswith('.md'):
            # Extract title from first heading
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    metadata['title'] = line.lstrip('# ').strip()
                    break

        # Determine section/category
        if 'knowledge_base' in file_path:
            metadata['section'] = 'knowledge_base'
            # Extract technology category
            path_parts = file_path.split(os.sep)
            if 'technologies' in path_parts:
                idx = path_parts.index('technologies')
                if idx + 1 < len(path_parts):
                    metadata['category'] = path_parts[idx + 1]
        elif 'project_meta' in file_path:
            metadata['section'] = 'project_meta'

        return metadata

    def _generate_doc_id(self, file_path: str) -> str:
        """Genera un ID único para un documento."""
        return hashlib.md5(file_path.encode()).hexdigest()

    def query_context(self, query: str, k: int = 5) -> List[Dict]:
        """
        Recupera contexto relevante para una consulta.

        Args:
            query: Consulta de búsqueda
            k: Número de resultados a retornar

        Returns:
            Lista de chunks relevantes con scores
        """
        # Simple TF-IDF based search (placeholder for actual vector search)
        results = []

        query_terms = set(query.lower().split())

        for doc_id, doc_data in self.indexed_documents.items():
            for chunk in doc_data['chunks']:
                chunk_text = chunk['text'].lower()
                chunk_terms = set(chunk_text.split())

                # Calculate simple relevance score (Jaccard similarity)
                intersection = query_terms & chunk_terms
                union = query_terms | chunk_terms
                score = len(intersection) / len(union) if union else 0

                if score > 0:
                    results.append({
                        'text': chunk['text'],
                        'score': score,
                        'metadata': chunk['metadata'],
                        'doc_id': doc_id
                    })

        # Sort by score and return top k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:k]

    def _save_index(self, stats: Dict):
        """Guarda el índice en disco."""
        index_path = os.path.join(self.persist_directory, 'index.json')
        os.makedirs(self.persist_directory, exist_ok=True)

        index_data = {
            'last_indexed': datetime.now().isoformat(),
            'stats': stats,
            'documents': {
                doc_id: {
                    'file_path': doc_data['file_path'],
                    'metadata': doc_data['metadata'],
                    'indexed_at': doc_data['indexed_at'],
                    'num_chunks': len(doc_data['chunks'])
                }
                for doc_id, doc_data in self.indexed_documents.items()
            }
        }

        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Index saved to {index_path}")

    def load_index(self):
        """Carga el índice desde disco."""
        index_path = os.path.join(self.persist_directory, 'index.json')

        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                self.document_index = json.load(f)
            print(f"✓ Index loaded from {index_path}")
        else:
            print("No existing index found")


def main():
    """Función principal para testing."""
    import argparse

    parser = argparse.ArgumentParser(description='RAG Knowledge Indexer')
    parser.add_argument('--index', action='store_true', help='Index all planning documents')
    parser.add_argument('--query', type=str, help='Query the index')
    parser.add_argument('--config', help='Path to rag-config.json')

    args = parser.parse_args()

    # Initialize RAG system
    rag = PlanningRAG(config_path=args.config)

    if args.index:
        print("Indexing planning documents...")
        stats = rag.index_planning_docs()

        print(f"\n✓ Indexing complete!")
        print(f"  Documents processed: {stats['documents_processed']}")
        print(f"  Chunks created: {stats['chunks_created']}")
        if stats['errors']:
            print(f"  Errors: {len(stats['errors'])}")

    elif args.query:
        print(f"Querying: {args.query}")
        rag.load_index()
        results = rag.query_context(args.query)

        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Score: {result['score']:.3f}")
            print(f"   Source: {result['metadata'].get('file_name', 'Unknown')}")
            print(f"   Text: {result['text'][:150]}...")

    else:
        print("Use --index to index documents or --query to search")


if __name__ == "__main__":
    main()
