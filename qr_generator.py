# qr_generator.py
import qrcode
import io
from PIL import Image
from typing import Dict, Any, Tuple

class QRGenerator:
    """Generate QR codes for URLs"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize QR generator with configuration"""
        self.error_correction = getattr(qrcode.constants, 
                                      config.get('qr_error_correction', 'ERROR_CORRECT_L'))
        self.box_size = config.get('qr_box_size', 10)
        self.border = config.get('qr_border', 4)
    
    def generate(self, url: str) -> Tuple[Image.Image, str]:
        """
        Generate a QR code for the URL
        
        Returns:
            Tuple containing:
                - Pillow Image object
                - Binary string representation
        """
        qr = qrcode.QRCode(
            version=None,  # Auto-determine
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Generate binary representation
        data = qr.get_matrix()
        binary_data = ""
        for row in data:
            for cell in row:
                binary_data += "1" if cell else "0"
        
        return img, binary_data