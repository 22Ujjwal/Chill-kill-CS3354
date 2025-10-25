"""
Firecrawl module for scraping website content.
Fetches and processes HTML/markdown from the target website.
"""

import requests
import json
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class FirecrawlScraper:
    """Manages website scraping using Firecrawl API."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.firecrawl.dev/v2"):
        """
        Initialize Firecrawl scraper.
        
        Args:
            api_key (str): Firecrawl API key
            base_url (str): Firecrawl API base URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def crawl_website(
        self,
        target_url: str,
        limit: int = 10,
        include_sitemap: bool = True,
        crawl_entire_domain: bool = False,
        only_main_content: bool = False,
        include_pdf: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Crawl a website and extract content.
        
        Args:
            target_url (str): URL to crawl
            limit (int): Max number of pages to crawl
            include_sitemap (bool): Include sitemap in crawl
            crawl_entire_domain (bool): Whether to crawl entire domain
            only_main_content (bool): Only extract main content
            include_pdf (bool): Include PDF parsing
            
        Returns:
            List[Dict]: List of crawled pages with content
        """
        payload = {
            "url": target_url,
            "sitemap": "include" if include_sitemap else "exclude",
            "crawlEntireDomain": crawl_entire_domain,
            "limit": limit,
            "scrapeOptions": {
                "onlyMainContent": only_main_content,
                "maxAge": 172800000,  # 48 hours cache
                "parsers": ["pdf"] if include_pdf else [],
                "formats": ["markdown", "html"]
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/crawl",
                json=payload,
                headers=self.headers,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success"):
                data = result.get("data", [])
                logger.info(f"Successfully crawled {len(data)} pages from {target_url}")
                return data
            else:
                logger.error(f"Crawl failed: {result.get('error', 'Unknown error')}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error during crawl: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return []
    
    def extract_text_from_pages(self, pages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Extract and clean text from crawled pages.
        
        Args:
            pages (List[Dict]): List of crawled pages
            
        Returns:
            List[Dict]: List of pages with cleaned text content
        """
        extracted = []
        
        for page in pages:
            doc = {
                "url": page.get("url", ""),
                "title": page.get("metadata", {}).get("title", ""),
                "content": page.get("markdown", page.get("content", "")),
                "html": page.get("html", "")
            }
            
            if doc["content"]:
                extracted.append(doc)
        
        logger.info(f"Extracted text from {len(extracted)} pages")
        return extracted


def scrape_nintendo_website(
    api_key: str,
    target_url: str = "https://www.nintendo.com/us/",
    limit: int = 10
) -> List[Dict[str, str]]:
    """
    Convenience function to scrape Nintendo website.
    
    Args:
        api_key (str): Firecrawl API key
        target_url (str): URL to crawl (default: Nintendo US)
        limit (int): Max pages to crawl
        
    Returns:
        List[Dict]: List of extracted pages
    """
    scraper = FirecrawlScraper(api_key)
    pages = scraper.crawl_website(
        target_url,
        limit=limit,
        include_sitemap=True,
        crawl_entire_domain=False,
        only_main_content=False
    )
    extracted = scraper.extract_text_from_pages(pages)

    # Fallback: if Firecrawl returns no content, try a simple HTTP GET
    if not extracted:
        try:
            logger.warning("Firecrawl returned no pages; attempting simple HTTP GET fallback")
            resp = requests.get(target_url, timeout=20)
            resp.raise_for_status()
            # Use raw HTML as content for a minimal single document
            extracted = [{
                "url": target_url,
                "title": "Nintendo Homepage (fallback)",
                "content": resp.text,
                "html": resp.text
            }]
            logger.info("Fallback fetch succeeded; created 1 document from homepage HTML")
        except Exception as e:
            logger.error(f"Fallback fetch failed: {e}")
            extracted = []

    return extracted
