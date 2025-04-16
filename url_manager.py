import uuid
import csv
import os
from typing import Dict, List, Set, Optional
from urllib.parse import urlparse
import datetime

class URLManager:
    """Manage URLs and their associated metadata to prevent duplicates"""
    
    def __init__(self):
        """Initialize the URL manager with empty collections"""
        self.urls = {}  # Dictionary mapping URLs to their metadata
        self.url_hashes = set()  # Set of URL hashes for quick lookup
    
    def add_url(self, url: str) -> Dict:
        """
        Add a URL to the manager if it doesn't exist.
        
        Args:
            url: The URL to add
            
        Returns:
            Dictionary with URL metadata
        """
        # Create a unique hash for the URL
        url_hash = self._hash_url(url)
        
        # Check if URL already exists
        if url_hash in self.url_hashes:
            return self.urls[url]
        
        # Add new URL
        url_id = str(uuid.uuid4())
        parsed_url = urlparse(url)
        
        metadata = {
            'url': url,
            'id': url_id,
            'domain': parsed_url.netloc,
            'path': parsed_url.path,
            'query': parsed_url.query,
            'timestamp': None,  # Will be set when QR code is generated
            'version': None,    # Will be set when QR code is generated
            'qr_data': None,    # Will be set when QR code is generated
            'processed': False  # Flag to indicate if QR code has been generated
        }
        
        self.urls[url] = metadata
        self.url_hashes.add(url_hash)
        
        return metadata
    
    def _hash_url(self, url: str) -> str:
        """
        Create a hash of the URL for duplicate detection.
        
        Args:
            url: The URL to hash
            
        Returns:
            A string hash of the URL
        """
        # This is a simple hash, but we could use a more robust method
        return url
    
    def get_unprocessed_urls(self) -> List[Dict]:
        """
        Get all URLs that haven't been processed yet.
        
        Returns:
            List of URL metadata dictionaries
        """
        return [metadata for url, metadata in self.urls.items() if not metadata['processed']]
    
    def mark_as_processed(self, url: str, version: int, qr_data: str) -> None:
        """
        Mark a URL as processed with QR code data.
        
        Args:
            url: The URL that was processed
            version: QR code version number
            qr_data: Binary QR code data
        """
        if url in self.urls:
            self.urls[url]['processed'] = True
            self.urls[url]['timestamp'] = datetime.datetime.now().isoformat()
            self.urls[url]['version'] = version
            self.urls[url]['qr_data'] = qr_data
    
    def export_to_csv(self, output_path: str) -> str:
        """
        Export all URLs and their metadata to a CSV file.
        
        Args:
            output_path: Directory to save the CSV file
            
        Returns:
            Path to the created CSV file
        """
        csv_path = os.path.join(output_path, "urls.csv")
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['url', 'timestamp', 'version', 'binary_data'])
            
            for url, metadata in self.urls.items():
                writer.writerow([
                    url,
                    metadata.get('timestamp', ''),
                    metadata.get('version', ''),
                    metadata.get('qr_data', '')
                ])
        
        return csv_path