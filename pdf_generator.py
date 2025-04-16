# pdf_generator.py - Quadrant layout version
from typing import List, Dict, Any
import base64
from io import BytesIO
import os
import uuid
import math

class PDFGenerator:
    """Generate PDF with QR codes arranged in quadrants"""
    
    def __init__(self):
        """Initialize the PDF generator"""
        try:
            from fpdf import FPDF
            self.FPDF = FPDF
            self.available = True
        except ImportError:
            print("fpdf not installed. PDF generation not available.")
            self.available = False
    
    def generate(self, csv_entries: List[Dict[str, Any]], output_path: str) -> bool:
        """
        Generate PDF from CSV entries with 4 QR codes per page
        
        Args:
            csv_entries: List of dictionaries containing QR code data
            output_path: Path to save the PDF file
            
        Returns:
            True if PDF generation was successful, False otherwise
        """
        if not self.available:
            print("PDF generation not available because fpdf is not installed.")
            return False
        
        try:
            # Create PDF object (A4 format)
            pdf = self.FPDF(orientation='P', unit='mm', format='A4')
            # A4 dimensions: 210mm x 297mm
            page_width = 210
            page_height = 297
            
            # Calculate quadrant dimensions
            quadrant_width = page_width / 2
            quadrant_height = page_height / 2
            
            # Calculate centers of each quadrant
            quadrant_centers = [
                # Top-left
                (quadrant_width / 2, quadrant_height / 2),
                # Top-right
                (quadrant_width * 1.5, quadrant_height / 2),
                # Bottom-left
                (quadrant_width / 2, quadrant_height * 1.5),
                # Bottom-right
                (quadrant_width * 1.5, quadrant_height * 1.5)
            ]
            
            # Set up tracking
            temp_files = []
            temp_dir = f"temp_qr_{uuid.uuid4().hex}"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Process QR codes in groups of 4
            total_qr_codes = len(csv_entries)
            num_pages = math.ceil(total_qr_codes / 4)
            
            for page_idx in range(num_pages):
                pdf.add_page()
                
                # Process each quadrant
                for quadrant_idx in range(4):
                    entry_idx = page_idx * 4 + quadrant_idx
                    
                    # Skip if we've processed all entries
                    if entry_idx >= total_qr_codes:
                        continue
                    
                    entry = csv_entries[entry_idx]
                    
                    # Extract image data
                    img_data = entry.get('image_data', '')
                    if not img_data:
                        print(f"No image data for entry {entry_idx}")
                        continue
                    
                    # Get quadrant center
                    center_x, center_y = quadrant_centers[quadrant_idx]
                    
                    # Save QR code to temporary file
                    temp_img_path = os.path.join(temp_dir, f"temp_qr_{entry_idx}_{uuid.uuid4().hex}.png")
                    temp_files.append(temp_img_path)
                    
                    try:
                        # Save image to temp file
                        img_bytes = base64.b64decode(img_data)
                        with open(temp_img_path, 'wb') as f:
                            f.write(img_bytes)
                        
                        # QR code size (adjusted to fit nicely in quadrant)
                        qr_size = 70  # mm
                        
                        # Calculate position to center QR code in quadrant
                        x_pos = center_x - (qr_size / 2)
                        y_pos = center_y - (qr_size / 2)
                        
                        # Add QR code to PDF
                        pdf.image(temp_img_path, x=x_pos, y=y_pos, w=qr_size)
                    except Exception as e:
                        print(f"Error processing QR code {entry_idx}: {e}")
            
            # Save the PDF
            pdf.output(output_path)
            
            # Clean up temporary files
            for file_path in temp_files:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error removing temp file: {e}")
            
            # Remove temp directory
            try:
                os.rmdir(temp_dir)
            except Exception as e:
                print(f"Error removing temp directory: {e}")
            
            print(f"PDF generated successfully with {total_qr_codes} QR codes across {num_pages} pages")
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False