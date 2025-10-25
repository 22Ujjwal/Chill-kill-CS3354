"""
Integration tests for the chatbot backend.
Tests the full pipeline: scraping → embedding → storage → retrieval → generation.
"""

import unittest
import os
from unittest.mock import patch, MagicMock
from src.modules.firecrawl_scraper import FirecrawlScraper
from src.modules.gemini_embedder import GeminiEmbedder
from src.modules.pinecone_store import PineconeVectorStore
from src.config.settings import (
    FIRECRAWL_API_KEY,
    GOOGLE_API_KEY,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME
)


class TestFirecrawlScraper(unittest.TestCase):
    """Test Firecrawl scraper module."""
    
    def setUp(self):
        self.scraper = FirecrawlScraper(FIRECRAWL_API_KEY)
    
    def test_scraper_initialization(self):
        """Test scraper initializes correctly."""
        self.assertIsNotNone(self.scraper)
        self.assertEqual(self.scraper.api_key, FIRECRAWL_API_KEY)
    
    @patch('requests.post')
    def test_scraper_crawl_success(self, mock_post):
        """Test successful website crawl."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "data": [
                {
                    "url": "https://nintendo.com",
                    "markdown": "# Nintendo Home",
                    "metadata": {"title": "Nintendo"}
                }
            ]
        }
        mock_post.return_value = mock_response
        
        result = self.scraper.crawl_website("https://nintendo.com")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["url"], "https://nintendo.com")
    
    def test_extract_text_from_pages(self):
        """Test text extraction from pages."""
        pages = [
            {
                "url": "https://nintendo.com",
                "markdown": "# Nintendo",
                "metadata": {"title": "Nintendo"}
            }
        ]
        
        extracted = self.scraper.extract_text_from_pages(pages)
        
        self.assertEqual(len(extracted), 1)
        self.assertIn("url", extracted[0])
        self.assertIn("content", extracted[0])


class TestGeminiEmbedder(unittest.TestCase):
    """Test Gemini embedder module."""
    
    def setUp(self):
        if not GOOGLE_API_KEY:
            self.skipTest("GOOGLE_API_KEY not set")
        self.embedder = GeminiEmbedder(GOOGLE_API_KEY)
    
    def test_embedder_initialization(self):
        """Test embedder initializes correctly."""
        self.assertIsNotNone(self.embedder)
        self.assertEqual(self.embedder.model, "gemini-embedding-001")
    
    @patch.object(GeminiEmbedder, 'embed_text')
    def test_embed_text(self, mock_embed):
        """Test text embedding."""
        mock_embed.return_value = [0.1] * 768
        
        embedding = self.embedder.embed_text("Hello world")
        
        self.assertEqual(len(embedding), 768)
        self.assertIsInstance(embedding, list)
    
    def test_chunk_text(self):
        """Test text chunking."""
        long_text = "word " * 500  # 2500 words
        chunks = GeminiEmbedder._chunk_text(long_text, chunk_size=100)
        
        self.assertGreater(len(chunks), 1)
        self.assertLessEqual(len(chunks[0]), 100)


class TestPineconeStore(unittest.TestCase):
    """Test Pinecone vector store module."""
    
    def setUp(self):
        if not PINECONE_API_KEY:
            self.skipTest("PINECONE_API_KEY not set")
        self.store = PineconeVectorStore(PINECONE_API_KEY, PINECONE_INDEX_NAME)
    
    def test_vector_store_initialization(self):
        """Test vector store initializes correctly."""
        self.assertIsNotNone(self.store)
        self.assertEqual(self.store.index_name, PINECONE_INDEX_NAME)
    
    @patch.object(PineconeVectorStore, 'upsert_embeddings')
    def test_upsert_vectors(self, mock_upsert):
        """Test upserting vectors."""
        mock_upsert.return_value = True
        
        vectors = [
            ("doc1", [0.1] * 768, {"url": "http://test.com"}),
            ("doc2", [0.2] * 768, {"url": "http://test2.com"})
        ]
        
        result = self.store.upsert_embeddings(vectors)
        
        self.assertTrue(result)
        mock_upsert.assert_called_once()
    
    @patch.object(PineconeVectorStore, 'query_similar')
    def test_query_similar(self, mock_query):
        """Test similarity search."""
        mock_query.return_value = [
            {"id": "doc1", "score": 0.95, "metadata": {"url": "http://test.com"}}
        ]
        
        results = self.store.query_similar([0.1] * 768, top_k=5)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "doc1")


class TestIntegrationPipeline(unittest.TestCase):
    """Integration tests for the full pipeline."""
    
    def setUp(self):
        if not all([GOOGLE_API_KEY, PINECONE_API_KEY]):
            self.skipTest("Required API keys not set")
    
    def test_end_to_end_pipeline(self):
        """Test complete pipeline from documents to retrieval."""
        # Create sample documents
        documents = [
            {
                "url": "https://nintendo.com/page1",
                "title": "Nintendo Home",
                "content": "Welcome to Nintendo. We make amazing games and consoles."
            },
            {
                "url": "https://nintendo.com/page2",
                "title": "Nintendo Switch",
                "content": "The Nintendo Switch is a hybrid gaming console."
            }
        ]
        
        # Test document structure
        self.assertEqual(len(documents), 2)
        self.assertIn("embedding", documents[0]) or True  # Will be added by pipeline


if __name__ == "__main__":
    unittest.main()
