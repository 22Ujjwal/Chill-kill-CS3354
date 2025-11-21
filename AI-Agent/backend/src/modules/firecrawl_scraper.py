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
    
    def scrape_single_page(
        self,
        target_url: str,
        only_main_content: bool = False,
        include_pdf: bool = True
    ) -> Dict[str, Any]:
        """
        Scrape a single page using Firecrawl /v2/scrape endpoint.
        
        Args:
            target_url (str): URL to scrape
            only_main_content (bool): Only extract main content
            include_pdf (bool): Include PDF parsing
            
        Returns:
            Dict: Scraped page content
        """
        payload = {
            "url": target_url,
            "onlyMainContent": only_main_content,
            "maxAge": 172800000,  # 48 hours cache
            "parsers": ["pdf"] if include_pdf else [],
            "formats": ["markdown", "html"]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/scrape",
                json=payload,
                headers=self.headers,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Successfully scraped {target_url}")
            return result
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error during scrape: {e}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return {}
    
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
        Crawl a website and extract content (using scrape endpoint for better results).
        
        Args:
            target_url (str): URL to crawl
            limit (int): Max number of pages to crawl (note: /scrape handles one page at a time)
            include_sitemap (bool): Include sitemap in crawl
            crawl_entire_domain (bool): Whether to crawl entire domain
            only_main_content (bool): Only extract main content
            include_pdf (bool): Include PDF parsing
            
        Returns:
            List[Dict]: List of scraped pages with content
        """
        # Use /v2/scrape endpoint for better single-page extraction
        result = self.scrape_single_page(
            target_url,
            only_main_content=only_main_content,
            include_pdf=include_pdf
        )
        
        # Handle various response formats from Firecrawl
        if not result:
            return []
        
        # Unwrap if wrapped in 'data' key
        data = result.get("data", result) if isinstance(result, dict) else result
        
        # If data is a list, return it; otherwise wrap single item
        if isinstance(data, list):
            logger.info(f"Successfully scraped {len(data)} item(s) from {target_url}")
            return data
        elif isinstance(data, dict):
            logger.info(f"Successfully scraped 1 page from {target_url}")
            return [data]
        else:
            logger.warning(f"Unexpected response format from scrape: {type(data)}")
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
    limit: int = 10,
    additional_urls: List[str] | None = None
) -> List[Dict[str, str]]:
    """
    Convenience function to scrape Nintendo website using Firecrawl /v2/scrape endpoint.
    
    Args:
        api_key (str): Firecrawl API key
        target_url (str): URL to scrape (default: Nintendo US)
        limit (int): Max pages to scrape (note: currently scrapes one page at a time)
        additional_urls (List[str]): Additional URLs to scrape
        
    Returns:
        List[Dict]: List of extracted pages with content
    """
    scraper = FirecrawlScraper(api_key)
    
    # Main URL scraping using /v2/scrape endpoint
    pages = scraper.crawl_website(
        target_url,
        limit=limit,
        include_sitemap=False,
        crawl_entire_domain=False,
        only_main_content=False
    )
    extracted = scraper.extract_text_from_pages(pages)

    # Scrape additional specific URLs
    if additional_urls:
        for url in additional_urls:
            try:
                result = scraper.scrape_single_page(url, only_main_content=False)
                
                if result:
                    # Handle various response formats
                    data = result.get("data", result) if isinstance(result, dict) else result
                    
                    # If data is a list, take first item
                    if isinstance(data, list) and data:
                        data = data[0]
                    
                    if isinstance(data, dict):
                        doc = {
                            "url": url,
                            "title": (data.get("metadata", {}) or {}).get("title", ""),
                            "content": data.get("markdown", data.get("content", "")),
                            "html": data.get("html", "")
                        }
                        if doc["content"]:
                            extracted.append(doc)
                            logger.info(f"✓ Added URL via Firecrawl /scrape: {url}")
                            continue
                
                # Fallback: simple HTTP GET
                http = requests.get(url, timeout=20)
                http.raise_for_status()
                extracted.append({
                    "url": url,
                    "title": "Additional Page",
                    "content": http.text,
                    "html": http.text
                })
                logger.info(f"✓ Added URL via HTTP fallback: {url}")
                
            except Exception as e:
                logger.warning(f"Failed to fetch additional URL {url}: {e}")

    # Fallback: if no content scraped, try simple HTTP GET on main URL
    if not extracted:
        try:
            logger.warning("Firecrawl returned no pages; attempting simple HTTP GET fallback")
            resp = requests.get(target_url, timeout=20)
            resp.raise_for_status()
            extracted = [{
                "url": target_url,
                "title": "Nintendo Homepage (HTTP Fallback)",
                "content": resp.text,
                "html": resp.text
            }]
            logger.info("✓ Fallback fetch succeeded; created 1 document from homepage HTML")
        except Exception as e:
            logger.error(f"✗ Fallback fetch failed: {e}")
            extracted = []

    return extracted
