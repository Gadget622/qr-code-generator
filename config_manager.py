# config_manager.py
import os
import yaml
from typing import Dict, Any

class ConfigManager:
    """Manage configuration for the application"""
    
    def __init__(self, config_path: str = None):
        """Initialize with optional config path"""
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            'output_pptx': True,
            'output_pdf': True,
            'qr_error_correction': 'ERROR_CORRECT_L',
            'qr_box_size': 10,
            'qr_border': 4,
            'csv_path': 'master_urls.csv',
            'output_dir': 'output'
        }
        
        if self.config_path and os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                if user_config:
                    default_config.update(user_config)
            except Exception as e:
                print(f"Error loading config: {e}")
                print("Using default configuration.")
        
        return default_config
    
    def get_config(self) -> Dict[str, Any]:
        """Get the current configuration"""
        return self.config