#!/usr/bin/env python3
"""
Batch Link Extractor and QR Code Generator

This script processes multiple files in a directory to extract links and generate
QR codes, organizing them in a timestamped directory structure.
"""

import os
import sys
import argparse
import datetime
import yaml
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Any, Set
import concurrent.futures
import subprocess


class BatchProcessor:
    """Process multiple files for link extraction and QR code generation."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the batch processor with optional configuration file.
        
        Args:
            config_path: Path to configuration YAML file
        """
        self.config = self._load_config(config_path)
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from YAML file or use defaults."""
        default_config = {
            'output_pptx': True,
            'output_pdf': True,
            'output_raw': True,
            'qr_error_correction': 'ERROR_CORRECT_L',
            'qr_box_size': 10,
            'qr_border': 4,
            'generate_descriptive_titles': True,
            'max_workers': 4,  # Number of parallel workers for processing
            'file_extensions': ['.txt', '.md', '.csv', '.pdf', '.docx', '.html', '.htm', '.yaml', '.yml', '.json'],
            'recursive': False  # Whether to search subdirectories
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                if user_config:
                    default_config.update(user_config)
            except Exception as e:
                print(f"Error loading config from {config_path}: {e}")
                print("Using default configuration.")
        
        return default_config
    
    def get_files_to_process(self, input_dir: str) -> List[str]:
        """
        Get all files in the directory that match the configured extensions.
        
        Args:
            input_dir: Directory to scan for input files
            
        Returns:
            List of file paths to process
        """
        files_to_process = []
        
        allowed_extensions = self.config.get('file_extensions', [])
        is_recursive = self.config.get('recursive', False)
        
        if is_recursive:
            # Walk through all subdirectories
            for root, _, files in os.walk(input_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    ext = os.path.splitext(file_path)[1].lower()
                    if ext in allowed_extensions:
                        files_to_process.append(file_path)
        else:
            # Only look at files in the specified directory
            for file in os.listdir(input_dir):
                file_path = os.path.join(input_dir, file)
                if os.path.isfile(file_path):
                    ext = os.path.splitext(file_path)[1].lower()
                    if ext in allowed_extensions:
                        files_to_process.append(file_path)
        
        return files_to_process
    
    def process_file(self, file_path: str, output_dir: str, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a single file by calling the link_extractor_qr_generator script.
        
        Args:
            file_path: Path to the file to process
            output_dir: Directory for output
            config_path: Path to configuration file
            
        Returns:
            Dictionary with processing results
        """
        try:
            # Create the output directory for this file
            base_filename = os.path.splitext(os.path.basename(file_path))[0]
            file_output_dir = os.path.join(output_dir, base_filename)
            os.makedirs(file_output_dir, exist_ok=True)
            
            # Build the command
            cmd = [sys.executable, "link_extractor_qr_generator.py", file_path, "-o", file_output_dir]
            if config_path:
                cmd.extend(["-c", config_path])
            
            # Run the command
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                check=True
            )
            
            # Parse output to get links found
            output_text = result.stdout
            links_found = 0
            for line in output_text.split('\n'):
                if "Found" in line and "unique links" in line:
                    try:
                        links_found = int(line.split("Found")[1].split("unique")[0].strip())
                    except:
                        pass
            
            return {
                'input_file': file_path,
                'output_dir': file_output_dir,
                'links_found': links_found,
                'success': True
            }
        except subprocess.CalledProcessError as e:
            print(f"Error processing file {file_path}: {e}")
            print(f"Error output: {e.stderr}")
            return {
                'input_file': file_path,
                'error': str(e),
                'success': False
            }
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return {
                'input_file': file_path,
                'error': str(e),
                'success': False
            }
    
    def process_directory(self, input_dir: str, output_base_dir: str = "batch_output", config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Process all compatible files in the input directory.
        
        Args:
            input_dir: Directory containing input files
            output_base_dir: Base directory for output
            config_path: Path to configuration file
            
        Returns:
            Dictionary with batch processing results
        """
        print(f"Processing directory: {input_dir}")
        
        # Create timestamped output directory
        batch_output_dir = os.path.join(output_base_dir, f"batch_{self.timestamp}")
        os.makedirs(batch_output_dir, exist_ok=True)
        
        # Get list of files to process
        files_to_process = self.get_files_to_process(input_dir)
        print(f"Found {len(files_to_process)} files to process")
        
        # Process files
        results = []
        
        # Determine if we should use parallel processing
        max_workers = self.config.get('max_workers', 4)
        
        if max_workers > 1 and len(files_to_process) > 1:
            # Process files in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all tasks
                future_to_file = {
                    executor.submit(self.process_file, file_path, batch_output_dir, config_path): file_path
                    for file_path in files_to_process
                }
                
                # Process as they complete
                completed = 0
                for future in concurrent.futures.as_completed(future_to_file):
                    file_path = future_to_file[future]
                    completed += 1
                    print(f"Progress: {completed}/{len(files_to_process)} files processed")
                    
                    try:
                        result = future.result()
                        results.append(result)
                        print(f"  - Completed: {os.path.basename(file_path)} - Found {result.get('links_found', 0)} links")
                    except Exception as e:
                        print(f"  - Error processing {os.path.basename(file_path)}: {e}")
                        results.append({
                            'input_file': file_path,
                            'error': str(e),
                            'success': False
                        })
        else:
            # Process files sequentially
            for i, file_path in enumerate(files_to_process, 1):
                print(f"Processing file {i}/{len(files_to_process)}: {os.path.basename(file_path)}")
                result = self.process_file(file_path, batch_output_dir, config_path)
                results.append(result)
                
                if result.get('success', False):
                    print(f"  - Found {result.get('links_found', 0)} links")
                else:
                    print(f"  - Error: {result.get('error', 'Unknown error')}")
        
        # Create a summary report
        self._create_summary_report(results, batch_output_dir)
        
        return {
            'input_directory': input_dir,
            'output_directory': batch_output_dir,
            'files_processed': len(results),
            'timestamp': self.timestamp,
            'results': results
        }
    
    def _create_summary_report(self, results: List[Dict[str, Any]], output_dir: str) -> None:
        """
        Create a summary report of the batch processing.
        
        Args:
            results: List of processing results
            output_dir: Directory to save the report
        """
        report_path = os.path.join(output_dir, "batch_summary.md")
        
        total_files = len(results)
        successful_files = sum(1 for r in results if r.get('success', True))
        total_links = sum(r.get('links_found', 0) for r in results)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# Batch Processing Summary\n\n")
            f.write(f"**Timestamp:** {self.timestamp}\n\n")
            f.write(f"**Files Processed:** {total_files}\n")
            f.write(f"**Successfully Processed:** {successful_files}\n")
            f.write(f"**Failed:** {total_files - successful_files}\n")
            f.write(f"**Total Links Found:** {total_links}\n\n")
            
            f.write("## File Details\n\n")
            f.write("| File | Status | Links Found |\n")
            f.write("|------|--------|-------------|\n")
            
            for result in results:
                file_name = os.path.basename(result.get('input_file', 'Unknown'))
                status = "✅ Success" if result.get('success', True) else f"❌ Failed: {result.get('error', 'Unknown error')}"
                links_found = result.get('links_found', 0)
                
                f.write(f"| {file_name} | {status} | {links_found} |\n")
        
        print(f"Summary report created: {report_path}")


def main():
    """Main entry point for the command line interface."""
    parser = argparse.ArgumentParser(
        description="Batch process files to extract links and generate QR codes."
    )
    parser.add_argument(
        "input_directory", 
        help="Directory containing input files"
    )
    parser.add_argument(
        "-o", "--output-dir", 
        default="batch_output",
        help="Base directory for outputs (default: batch_output)"
    )
    parser.add_argument(
        "-c", "--config", 
        help="Path to YAML configuration file"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Process subdirectories recursively"
    )
    
    args = parser.parse_args()
    
    # Check if input directory exists
    if not os.path.isdir(args.input_directory):
        print(f"Error: Input directory '{args.input_directory}' not found.")
        return 1
    
    # Create processor instance
    processor = BatchProcessor(args.config)
    
    # Override recursive setting if specified in command line
    if args.recursive:
        processor.config['recursive'] = True
    
    # Process directory
    result = processor.process_directory(args.input_directory, args.output_dir, args.config)
    
    # Print summary
    print("\nBatch processing complete!")
    print(f"Processed {result['files_processed']} files")
    print(f"Output saved to: {result['output_directory']}")
    print(f"See batch_summary.md in the output directory for details")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())