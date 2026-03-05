import os
import json
import faiss
import numpy as np
import logging
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class DocumentRetriever:
    def __init__(self, model_name: str = "BAAI/bge-small-en", storage_dir: str = "storage"):
        self.storage_dir = storage_dir
        self.index_path = os.path.join(storage_dir, "index.faiss")
        self.metadata_path = os.path.join(storage_dir, "metadata.json")
        
        # Load embedding model
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        # Initialize or load FAISS and metadata
        self.index = None
        self.metadata: List[Dict[str, Any]] = []
        self._init_index()

    def _init_index(self):
        """Initializes the FAISS index and metadata storage."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir, exist_ok=True)
            
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            logger.info("Loading existing FAISS index and metadata.")
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            logger.info("Creating new FAISS index.")
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []

    def _save_index(self):
        """Saves the FAISS index and metadata to disk."""
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]]):
        """Adds a list of documents and their metadata to the index."""
        if not documents:
            return
            
        logger.info(f"Encoding {len(documents)} documents...")
        embeddings = self.model.encode(documents, normalize_embeddings=True)
        embeddings = np.array(embeddings).astype('float32')
        
        self.index.add(embeddings)
        
        # Store metadata along with the document text
        for i, doc in enumerate(documents):
            meta = metadatas[i] if metadatas else {}
            meta['text'] = doc
            self.metadata.append(meta)
            
        self._save_index()
        logger.info(f"Successfully added {len(documents)} documents. Total in index: {self.index.ntotal}")

    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Retrieves top-k evidence chunks for a query."""
        if self.index.ntotal == 0:
            logger.warning("FAISS index is empty. No evidence to retrieve.")
            return []
            
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        query_embedding = np.array(query_embedding).astype('float32')
        
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1 and idx < len(self.metadata):
                result = dict(self.metadata[idx])
                result['distance'] = float(dist)
                results.append(result)
                
        return results
