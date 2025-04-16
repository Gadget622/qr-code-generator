# csv_manager.py
import csv
import os
from typing import List, Dict, Any, Optional
import base64
from io import BytesIO
from PIL import Image

class CSVManager:
    """Manage the master CSV file for URLs and QR codes"""
    
    def __init__(self, csv_path: str = "master_urls.csv"):
        """Initialize with path to CSV file"""
        self.csv_path = csv_path
        self.headers = ["url", "qr_version", "binary_data", "image_data"]
        
        # Create CSV with headers if it doesn't exist
        if not os.path.exists(csv_path):
            self._create_csv()
    
    def _create_csv(self):
        """Create a new CSV file with headers"""
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)
    
    def get_existing_urls(self) -> List[str]:
        """Get list of URLs already in the CSV"""
        if not os.path.exists(self.csv_path):
            return []
        
        urls = []
        try:
            with open(self.csv_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    urls.append(row.get('url', ''))
        except Exception as e:
            print(f"Error reading CSV: {e}")
        
        return urls
    
    def add_entry(self, url: str, qr_version: int, binary_data: str, image: Image.Image) -> bool:
        """Add a new entry to the CSV"""
        try:
            # Convert image to base64
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Write to CSV
            with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([url, qr_version, binary_data, img_str])
            
            return True
        except Exception as e:
            print(f"Error adding entry to CSV: {e}")
            return False
    
    def get_all_entries(self) -> List[Dict[str, Any]]:
        """Get all entries from the CSV"""
        entries = []
        try:
            with open(self.csv_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    entries.append(dict(row))
        except Exception as e:
            print(f"Error reading CSV: {e}")
        
        return entries