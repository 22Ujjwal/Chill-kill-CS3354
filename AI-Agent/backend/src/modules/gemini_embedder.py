"""
Gemini embeddings module for converting text to vector embeddings.
Uses Google Gemini API to create embeddings for documents and queries.
"""

from google import genai
from typing import List, Dict, Any
import hashlib
import random
import logging

logger = logging.getLogger(__name__)


from src.config.settings import EMBEDDING_DIMENSION


class GeminiEmbedder:
    """Manages text embedding using Google Gemini API."""
    
    def __init__(self, api_key: str, model: str = "embedding-001"):
        """
        Initialize Gemini embedder.
        
        Args:
            api_key (str): Google API key
            model (str): Embedding model name
        """
        self.client = genai.Client(api_key=api_key)
        self.model = model

    
    def _fallback_embedding(self, text: str, dim: int = EMBEDDING_DIMENSION) -> List[float]:
        """
        Deterministic fallback embedding using a hash-seeded PRNG.
        Produces a vector of length `dim` with values in [-1, 1].
        """
        seed = int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % (2**32)
        rng = random.Random(seed)
        # Simple zero-mean distribution approximation
        vec = [rng.uniform(-1.0, 1.0) for _ in range(dim)]
        # Optional: normalize to unit length to keep scale consistent
        norm = sum(v*v for v in vec) ** 0.5 or 1.0
        return [v / norm for v in vec]

    def embed_text(self, text: str) -> List[float]:
        """
        Convert a single text string to an embedding.
        
        Args:
            text (str): Text to embed
        
        Returns:
            List[float]: Embedding vector
        """
        try:
            result = self.client.models.embed_content(
                model=self.model,
                contents=[text]
            )
            # Try multiple likely response shapes
            embedding = None
            if hasattr(result, "embeddings") and result.embeddings:
                emb0 = result.embeddings[0]
                # Some SDKs return objects with .values
                embedding = getattr(emb0, "values", emb0)
            elif isinstance(result, dict):
                data = result.get("embeddings") or result.get("data") or []
                if data:
                    emb0 = data[0]
                    embedding = emb0.get("values") if isinstance(emb0, dict) else emb0

            if embedding and isinstance(embedding, list):
                logger.debug(f"Generated embedding of dimension {len(embedding)}")
                return embedding
            else:
                logger.warning("Gemini returned no embeddings; using fallback")
                return self._fallback_embedding(text)
        except Exception as e:
            # Common when API quotas are exhausted or network fails
            logger.error(f"Error embedding text with Gemini, using fallback: {e}")
            return self._fallback_embedding(text)
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Convert multiple texts to embeddings. Automatically batches to respect
        API limits (Gemini allows at most 100 requests per batch).
        
        Args:
            texts (List[str]): List of texts to embed
        """
        def _embed_batch(batch: List[str]) -> List[List[float]]:
            """Call the API for a batch and parse embeddings robustly."""
            try:
                res = self.client.models.embed_content(
                    model=self.model,
                    contents=batch
                )
                parsed: List[List[float]] = []
                if hasattr(res, "embeddings") and res.embeddings:
                    for emb in res.embeddings:
                        parsed.append(getattr(emb, "values", emb))
                elif isinstance(res, dict):
                    data = res.get("embeddings") or res.get("data") or []
                    for emb in data:
                        parsed.append(emb.get("values") if isinstance(emb, dict) else emb)
                # If nothing parsed, fall back per text in this batch
                if not parsed:
                    logger.warning("Gemini returned no embeddings for batch; using fallback per text")
                    parsed = [self._fallback_embedding(t) for t in batch]
                return parsed
            except Exception as e:
                logger.error(f"Error embedding batch with Gemini, using fallback: {e}")
                return [self._fallback_embedding(t) for t in batch]

        # Batch by at most 100 to satisfy API constraint
        BATCH_LIMIT = 100
        all_embeddings: List[List[float]] = []
        for i in range(0, len(texts), BATCH_LIMIT):
            batch = texts[i:i + BATCH_LIMIT]
            all_embeddings.extend(_embed_batch(batch))

        logger.info(f"Prepared embeddings for {len(texts)} texts (batched)")
        return all_embeddings
    def embed_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Convert document contents to embeddings.
        
        Args:
            documents (List[Dict]): List of documents with 'content' field
            
        Returns:
            List[Dict]: Documents with added 'embedding' field
        """
        embedded_docs = []
        
        for doc in documents:
            content = doc.get("content", "")
            if not content:
                logger.warning(f"Skipping document with empty content: {doc.get('url', 'unknown')}")
                continue
            
            # Chunk large documents to avoid API limits
            chunks = self._chunk_text(content, chunk_size=1000)
            
            # Embed each chunk
            chunk_embeddings = self.embed_texts(chunks)
            
            # Use first chunk's embedding as document embedding (could also average)
            if chunk_embeddings:
                embedded_doc = doc.copy()
                embedded_doc["embedding"] = chunk_embeddings[0]
                embedded_doc["chunks"] = chunks
                embedded_doc["chunk_embeddings"] = chunk_embeddings
                embedded_docs.append(embedded_doc)
        
        logger.info(f"Embedded {len(embedded_docs)} documents")
        return embedded_docs
    
    @staticmethod
    def _chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text (str): Text to chunk
            chunk_size (int): Size of each chunk
            overlap (int): Overlap between chunks
            
        Returns:
            List[str]: List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        
        return chunks if chunks else [text]


def embed_content_for_storage(
    api_key: str,
    documents: List[Dict[str, str]]
) -> List[Dict[str, Any]]:
    """
    Convenience function to embed documents for storage in vector DB.
    
    Args:
        api_key (str): Google API key
        documents (List[Dict]): Documents to embed
        
    Returns:
        List[Dict]: Documents with embeddings
    """
    embedder = GeminiEmbedder(api_key)
    return embedder.embed_documents(documents)
