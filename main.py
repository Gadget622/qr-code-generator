# main.py
import os
import argparse
from typing import List, Set, Dict, Any

from url_extractor import URLExtractor
from url_processor import URLProcessor
from qr_generator import QRGenerator
from csv_manager import CSVManager
from pdf_generator import PDFGenerator
from config_manager import ConfigManager

class LinkExtractorQRGenerator:
    """Main application class"""
    
    def __init__(self, config_path: str = None):
        """Initialize the application"""
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.get_config()
        
        self.url_extractor = URLExtractor()
        self.url_processor = URLProcessor()
        self.qr_generator = QRGenerator(self.config)
        self.csv_manager = CSVManager(self.config.get('csv_path', 'master_urls.csv'))
        self.pdf_generator = PDFGenerator()
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Process a single file"""
        # Extract URLs
        raw_urls = self.url_extractor.extract_urls(file_path)
        print(f"Found {len(raw_urls)} raw URLs")
        
        # Process URLs (deduplicate and normalize)
        processed_urls = self.url_processor.deduplicate_urls(raw_urls)
        print(f"After deduplication: {len(processed_urls)} unique URLs")
        
        # Get existing URLs to avoid duplication
        existing_urls = self.csv_manager.get_existing_urls()
        new_urls = [url for url in processed_urls if url not in existing_urls]
        print(f"New URLs to process: {len(new_urls)}")
        
        # Generate QR codes for new URLs and add to CSV
        for url in new_urls:
            qr_image, binary_data = self.qr_generator.generate(url)
            # Add to CSV
            self.csv_manager.add_entry(url, 1, binary_data, qr_image)
            print(f"Generated QR code for: {url}")
        
        # Generate outputs
        output_dir = self.config.get('output_dir', 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        result = {
            'input_file': file_path,
            'total_urls': len(raw_urls),
            'unique_urls': len(processed_urls),
            'new_urls': len(new_urls),
            'outputs': {}
        }
        
        # Generate PDF if configured
        if self.config.get('output_pdf', True):
            pdf_path = os.path.join(output_dir, "qr_codes.pdf")
            entries = self.csv_manager.get_all_entries()
            if self.pdf_generator.generate(entries, pdf_path):
                result['outputs']['pdf'] = pdf_path
        
        return result

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description="Extract links from files and generate QR codes."
    )
    parser.add_argument(
        "input_file", 
        help="Path to input file"
    )
    parser.add_argument(
        "-c", "--config", 
        help="Path to YAML configuration file"
    )
    parser.add_argument(
        "-o", "--output-dir",
        help="Output directory"
    )
    
    args = parser.parse_args()
    
    # Check input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} not found.")
        return 1
    
    # Initialize application
    app = LinkExtractorQRGenerator(args.config)
    
    # Update output directory if specified
    if args.output_dir:
        app.config['output_dir'] = args.output_dir
    
    # Process file
    result = app.process_file(args.input_file)
    
    # Print summary
    print("\nProcessing complete!")
    print(f"Total URLs found: {result['total_urls']}")
    print(f"Unique URLs: {result['unique_urls']}")
    print(f"New URLs added: {result['new_urls']}")
    
    for output_type, path in result['outputs'].items():
        print(f"Generated {output_type.upper()}: {path}")
    
    return 0

if __name__ == "__main__":
    main()