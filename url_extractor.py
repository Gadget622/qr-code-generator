# url_extractor.py
import re
import os
from typing import Set, Dict, Any, List
from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """Abstract base class for all extractors"""
    
    @abstractmethod
    def extract(self, file_path: str) -> Set[str]:
        """Extract URLs from the file"""
        pass

class TextExtractor(BaseExtractor):
    """Extract URLs from text-based files"""
    
    def __init__(self):
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    def extract(self, file_path: str) -> Set[str]:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            return set(self.url_pattern.findall(content))
        except Exception as e:
            print(f"Error extracting from {file_path}: {e}")
            return set()

# Additional extractor classes for different file types...

class URLExtractorFactory:
    """Factory for creating appropriate extractors"""
    
    @staticmethod
    def get_extractor(file_extension: str) -> BaseExtractor:
        """Get the appropriate extractor for the file type"""
        extractors = {
            '.txt': TextExtractor(),
            '.md': TextExtractor(),
            # Map other extensions to their extractors
        }
        return extractors.get(file_extension.lower(), TextExtractor())

class URLExtractor:
    """Main extraction controller"""
    
    def extract_urls(self, file_path: str) -> Set[str]:
        """Extract URLs from the given file"""
        _, extension = os.path.splitext(file_path)
        extractor = URLExtractorFactory.get_extractor(extension)
        return extractor.extract(file_path)