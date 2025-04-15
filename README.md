# Link Extractor and QR Code Generator

A hypermodular tool for extracting links from various file types and generating QR codes with multiple output formats.

## Features

- Extract links from various file types:
  - Text files (.txt)
  - Markdown files (.md)
  - CSV files
  - PDF files
  - Word documents (.docx)
  - HTML files
- Generate QR codes for each link
- Organize outputs in a structured directory format
- Generate multiple output formats:
  - PowerPoint presentation with clickable links
  - PDF document
  - Raw QR code files (PNG and binary format)
- Configurable via YAML configuration file

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/link-extractor-qr-generator.git
   cd link-extractor-qr-generator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

   Note: You can install only the core dependencies if you don't need all output formats:
   ```
   pip install qrcode Pillow PyYAML
   ```

## Usage

### Basic Usage

Process a file and generate QR codes:

```bash
python link_extractor_qr_generator.py path/to/your/file.txt
```

This will:
1. Extract all links from the file
2. Generate QR codes for each link
3. Save them in the `output/` directory
4. Create a PowerPoint presentation and PDF if the required libraries are installed

### Specifying Output Directory

```bash
python link_extractor_qr_generator.py path/to/your/file.txt -o custom_output_dir
```

### Using Custom Configuration

```bash
python link_extractor_qr_generator.py path/to/your/file.txt -c custom_config.yaml
```

## Configuration

The default configuration can be overridden by creating a custom YAML file. Here's an example:

```yaml
# Output Options
output_pptx: true    # Generate PowerPoint presentation
output_pdf: true     # Generate PDF document
output_raw: true     # Generate raw QR code files in directories

# QR Code Settings
qr_error_correction: ERROR_CORRECT_M  # Increase error correction
qr_box_size: 10
qr_border: 4

# Content Options
generate_descriptive_titles: true
```

## Output Structure

The tool creates the following directory structure:

```
output/
└── filename/                     # Based on input filename
    ├── domain_path1/             # Sanitized directory name based on URL
    │   ├── qrcode.bin            # Binary data
    │   ├── qrcode.png            # QR code image
    │   └── url.md                # URL in markdown format
    ├── domain_path2/
    │   ├── qrcode.bin
    │   ├── qrcode.png
    │   └── url.md
    ├── qr_codes.pptx             # PowerPoint presentation (if enabled)
    └── qr_codes.pdf              # PDF document (if enabled)
```

## Dependencies

- **Core:**
  - qrcode: For generating QR codes
  - Pillow: For image processing
  - PyYAML: For configuration file handling

- **Optional:**
  - python-pptx: For PowerPoint generation
  - fpdf: For PDF generation
  - PyPDF2: For extracting text from PDFs
  - python-docx: For processing Word documents
  - pandas: For processing CSV files

## License

[MIT License](LICENSE)