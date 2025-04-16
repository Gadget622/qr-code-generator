# url_processor.py
from typing import Set, List
from urllib.parse import urlparse, urlunparse

class URLProcessor:
    """Process and normalize URLs"""
    
    def normalize_url(self, url: str) -> str:
        """Normalize a URL for consistent comparison"""
        try:
            parsed = urlparse(url)
            # Normalize scheme
            scheme = parsed.scheme.lower()
            # Normalize netloc (remove www. if present)
            netloc = parsed.netloc.lower()
            if netloc.startswith('www.'):
                netloc = netloc[4:]
            # Reconstruct URL with normalized components
            normalized = urlunparse((
                scheme,
                netloc,
                parsed.path,
                parsed.params,
                parsed.query,
                ''  # Remove fragment
            ))
            return normalized
        except Exception:
            return url
    
    def deduplicate_urls(self, urls: Set[str]) -> List[str]:
        """Remove duplicate URLs after normalization"""
        normalized_urls = {}
        
        for url in urls:
            normalized = self.normalize_url(url)
            if normalized not in normalized_urls:
                normalized_urls[normalized] = url
        
        return list(normalized_urls.values())