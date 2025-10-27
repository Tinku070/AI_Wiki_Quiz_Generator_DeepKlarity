# C:\Users\bonab\OneDrive\Desktop\AI_Wiki_Quiz_Generator_DeepKlarity\backend\app\services\scraping_service.py

import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_wikipedia_article(url: str) -> str:
    """
    Scrapes the main content text from a Wikipedia article URL.

    Args:
        url: The URL of the Wikipedia article.

    Returns:
        The clean, extracted text content of the article (max 30,000 chars).

    Raises:
        Exception: If a network error occurs or the main content cannot be found.
    """
    
    # Add a User-Agent header to avoid 403 Forbidden
    headers = {
        'User-Agent': 'DeepKlarityQuizGenerator/1.0 (YourAppContact; +https://example.com)',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main Wikipedia content div
        main_content_div = soup.find(id="mw-content-text")
        
        # Check for NoneType to prevent unpacking/attribute errors
        if not main_content_div:
            raise Exception("Scraping failed: Could not find main Wikipedia content div ('mw-content-text'). The page structure may be unexpected or the URL is not a standard article.")
        
        # Remove common non-article elements (tables, sidebars, TOCs)
        # We use .find_all() to safely look for multiple tags.
        for tag in main_content_div.find_all(['table', 'figure', 'div', 'span'], class_=['toc', 'navbox', 'vertical-navbox', 'metadata', 'printfooter']):
            tag.decompose()
            
        # Extract title (optional, for context)
        title_element = soup.find('h1', id="firstHeading")
        title = title_element.get_text(strip=True) if title_element else "Untitled Article"
        
        # Extract all text from the main content div
        article_text = main_content_div.get_text(separator=' ', strip=True)
        
        # Combine title and text, then limit the size for the LLM
        full_text = f"Title: {title}\n\n{article_text}"
        
        return full_text[:30000]

    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error during scraping: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error during scraping: {e}")
    except Exception as e:
        logger.error(f"Scraping failed for {url}: {e}")
        raise