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
- Generate QR codes for each unique link
- CSV-first approach prevents link duplication
- Timestamp tracking for all URL extractions
- Organize outputs in a structured directory format
- Generate multiple output formats:
  - PDF document with 4 QR codes per page
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
python improved_qr_generator.py path/to/your/file.txt
```

This will:
1. Extract all links from the file
2. Store unique links in a CSV with timestamps
3. Generate QR codes for each link
4. Save them in the `output/` directory
5. Create a PDF with 4 QR codes per page

### Specifying Output Directory

```bash
python improved_qr_generator.py path/to/your/file.txt -o custom_output_dir
```

### Using Custom Configuration

```bash
python improved_qr_generator.py path/to/your/file.txt -c custom_config.yaml
```

## Configuration

The default configuration can be overridden by creating a custom YAML file. Here's an example:

```yaml
# Output Options
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
    ├── urls.csv                  # Master CSV with all unique URLs and timestamps
    ├── domain_path1/             # Sanitized directory name based on URL
    │   ├── qrcode.bin            # Binary data
    │   ├── qrcode.png            # QR code image
    │   └── url.md                # URL in markdown format
    ├── domain_path2/
    │   ├── qrcode.bin
    │   ├── qrcode.png
    │   └── url.md
    └── qr_codes.pdf              # PDF document (4 codes per page)
```

## CSV Format

The master CSV file includes:
- URL: The unique link extracted
- Timestamp: When the URL was first extracted
- Version: QR code version information
- Binary data: Binary representation of the QR code

This CSV-first approach ensures:
- No duplicate links across multiple runs
- Consistent QR code generation
- Trackable history of each URL

## Dependencies

- **Core:**
  - qrcode: For generating QR codes
  - Pillow: For image processing
  - PyYAML: For configuration file handling

- **Optional:**
  - fpdf: For PDF generation
  - PyPDF2: For extracting text from PDFs
  - python-docx: For processing Word documents
  - pandas: For processing CSV files
  - beautifulsoup4: For HTML processing

## Batch Processing

To process multiple files, use the batch processor:

```bash
python batch_processor.py directory_with_files
```

## License

[MIT License](LICENSE)