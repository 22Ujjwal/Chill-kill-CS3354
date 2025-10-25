"""
Pinecone vector database module.
Manages storage and retrieval of embeddings in Pinecone.
"""

from pinecone import Pinecone
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class PineconeVectorStore:
    """Manages vector storage and retrieval in Pinecone."""
    
    def __init__(
        self,
        api_key: str,
        index_name: str,
        environment: str = "us-east-1",
        namespace: str = "default"
    ):
        """
        Initialize Pinecone vector store.
        
        Args:
            api_key (str): Pinecone API key
            index_name (str): Name of Pinecone index
            environment (str): Pinecone environment
            namespace (str): Namespace for vectors
        """
        self.pc = Pinecone(api_key=api_key, environment=environment)
        self.index_name = index_name
        self.namespace = namespace
        
        try:
            self.index = self.pc.Index(index_name)
            logger.info(f"Connected to Pinecone index: {index_name}")
        except Exception as e:
            logger.error(f"Failed to connect to Pinecone index: {e}")
            self.index = None
    
    def upsert_embeddings(
        self,
        vectors: List[Tuple[str, List[float], Dict[str, Any]]]
    ) -> bool:
        """
        Store or update embeddings in Pinecone.
        
        Args:
            vectors (List[Tuple]): List of (id, embedding, metadata) tuples
            
        Returns:
            bool: Success status
        """
        if not self.index:
            logger.error("Index not initialized")
            return False
        
        try:
            # Prepare vectors for upsert
            upsert_data = [
                (
                    vector[0],  # ID
                    vector[1],  # Embedding
                    vector[2]   # Metadata
                )
                for vector in vectors
            ]
            
            # Upsert in batches to avoid size limits
            batch_size = 100
            for i in range(0, len(upsert_data), batch_size):
                batch = upsert_data[i:i + batch_size]
                self.index.upsert(
                    vectors=batch,
                    namespace=self.namespace
                )
            
            logger.info(f"Upserted {len(upsert_data)} vectors to Pinecone")
            return True
            
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            return False
    
    def query_similar(
        self,
        embedding: List[float],
        top_k: int = 5,
        include_metadata: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Find similar embeddings in Pinecone.
        
        Args:
            embedding (List[float]): Query embedding
            top_k (int): Number of results to return
            include_metadata (bool): Include metadata in results
            
        Returns:
            List[Dict]: Similar documents with scores
        """
        if not self.index:
            logger.error("Index not initialized")
            return []
        
        try:
            results = self.index.query(
                vector=embedding,
                top_k=top_k,
                include_metadata=include_metadata,
                namespace=self.namespace
            )
            
            matches = []
            for match in results.matches:
                item = {
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata if include_metadata else {}
                }
                matches.append(item)
            
            logger.info(f"Retrieved {len(matches)} similar vectors")
            return matches
            
        except Exception as e:
            logger.error(f"Error querying vectors: {e}")
            return []
    
    def delete_vectors(self, vector_ids: List[str]) -> bool:
        """
        Delete vectors from Pinecone.
        
        Args:
            vector_ids (List[str]): IDs of vectors to delete
            
        Returns:
            bool: Success status
        """
        if not self.index:
            logger.error("Index not initialized")
            return False
        
        try:
            self.index.delete(ids=vector_ids, namespace=self.namespace)
            logger.info(f"Deleted {len(vector_ids)} vectors from Pinecone")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            return False
    
    def clear_namespace(self) -> bool:
        """
        Delete all vectors in current namespace.
        
        Returns:
            bool: Success status
        """
        if not self.index:
            logger.error("Index not initialized")
            return False
        
        try:
            self.index.delete(delete_all=True, namespace=self.namespace)
            logger.info(f"Cleared namespace: {self.namespace}")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing namespace: {e}")
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the Pinecone index.
        
        Returns:
            Dict: Index statistics
        """
        if not self.index:
            logger.error("Index not initialized")
            return {}
        
        try:
            stats = None
            # Preferred: index.describe_index_stats()
            if hasattr(self.index, "describe_index_stats"):
                stats_attr = getattr(self.index, "describe_index_stats")
                logger.debug(f"describe_index_stats attr type: {type(stats_attr)}")
                if callable(stats_attr):
                    stats = stats_attr()
                else:
                    stats = stats_attr
            # Alternate name
            if stats is None and hasattr(self.index, "describe_stats"):
                alt = getattr(self.index, "describe_stats")
                logger.debug(f"describe_stats attr type: {type(alt)}")
                if callable(alt):
                    stats = alt()
                else:
                    stats = alt
            # Client-level describe (v4)
            if stats is None and hasattr(self.pc, "describe_index"):
                describe = getattr(self.pc, "describe_index")
                logger.debug(f"pc.describe_index type: {type(describe)}")
                if callable(describe):
                    stats = describe(self.index_name)
                else:
                    stats = describe

            logger.info(f"Index stats fetched")
            return stats or {}
        except TypeError as e:
            logger.error(f"Type error getting index stats: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {}


def store_documents_in_pinecone(
    api_key: str,
    index_name: str,
    documents: List[Dict[str, Any]]
) -> bool:
    """
    Convenience function to store embedded documents in Pinecone.
    
    Args:
        api_key (str): Pinecone API key
        index_name (str): Pinecone index name
        documents (List[Dict]): Documents with 'embedding' field
        
    Returns:
        bool: Success status
    """
    vector_store = PineconeVectorStore(api_key, index_name)
    
    # Prepare vectors for upsert
    vectors = []
    for doc in documents:
        if "embedding" not in doc:
            logger.warning(f"Skipping document without embedding: {doc.get('url', 'unknown')}")
            continue
        
        # Create unique ID from URL
        vector_id = doc.get("url", "").replace("https://", "").replace("/", "_")
        
        # Metadata to store with vector
        metadata = {
            "url": doc.get("url", ""),
            "title": doc.get("title", ""),
            "source": "nintendo_website"
        }
        
        vectors.append((vector_id, doc["embedding"], metadata))
    
    return vector_store.upsert_embeddings(vectors)
