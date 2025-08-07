# Talabat List - Product Data Processing Project

This project processes product data from CSV files and creates organized Excel files with product information, barcodes, and downloaded images.

## Project Overview

The project consists of three main components:
1. **265 Test Project** - Processing of main product data
2. **Crayola Project** - Crayola brand products processing
3. **Deli Project** - Deli brand products processing

## Project Structure

```
talabat list/
├── 265.csv                          # Main source data file
├── list/                            # Main project folder
│   ├── excel/
│   │   ├── 1.xlsx                   # Template structure
│   │   └── 265 test.xlsx            # Main processed output
│   └── pics/                        # Product images
├── crayola/                         # Crayola project
│   ├── crayola_products.xlsx        # Crayola products data
│   └── images/                      # Crayola product images
├── deli/                            # Deli project
│   ├── deli_products.xlsx           # Deli products data
│   └── images/                      # Deli product images
├── downloaded_images/               # Main project images
└── scripts/                         # Processing scripts
```

## Key Scripts

### Main Processing Scripts
- `process_unique_products.py` - Creates 265 test.xlsx from 265.csv
- `process_crayola_csv.py` - Processes Crayola products
- `process_deli_csv.py` - Processes Deli products

### Utility Scripts
- `project_summary.py` - Generates comprehensive project reports
- `fix_crayola_issues.py` - Fixes barcode formatting issues
- `check_crayola_project.py` - Verifies project data quality
- `translate_to_arabic.py` - Adds Arabic translations
- `replace_ampersand.py` - Fixes text formatting
- `update_1xlsx_with_pics.py` - Updates 1.xlsx with image data

### Image Processing Scripts
- `download_final_images.py` - Downloads images for main project
- `fix_duplicate_barcodes.py` - Handles duplicate barcodes
- `final_excel_fix.py` - Fixes Excel formatting issues

## Features

### Data Processing
- Extracts English and Arabic product titles
- Handles product pricing
- Generates 12-digit barcodes (starting with "01") for products without existing barcodes
- Removes duplicate products based on titles
- Cleans and formats data

### Image Management
- Downloads product images from URLs
- Renames images to match product barcodes
- Organizes images in brand-specific folders
- Handles multiple image formats (JPG, PNG, WebP)

### Data Quality
- Validates barcode formats
- Ensures unique barcodes across products
- Maintains data consistency
- Provides comprehensive error handling

## Project Results

### 265 Test Project
- **Products**: 257 unique products
- **Images**: 257 downloaded images
- **Coverage**: 100% image coverage
- **Output**: `list/excel/265 test.xlsx`

### Crayola Project
- **Products**: 107 unique products
- **Images**: 105 downloaded images
- **Coverage**: 98.1% image coverage
- **Output**: `crayola/crayola_products.xlsx`

### Deli Project
- **Products**: 51 unique products
- **Images**: 49 downloaded images
- **Coverage**: 96.1% image coverage
- **Output**: `deli/deli_products.xlsx`

## Usage

1. **Run project summary**:
   ```bash
   python project_summary.py
   ```

2. **Process main data**:
   ```bash
   python process_unique_products.py
   ```

3. **Process Crayola products**:
   ```bash
   python process_crayola_csv.py
   ```

4. **Process Deli products**:
   ```bash
   python process_deli_csv.py
   ```

## Requirements

- Python 3.7+
- pandas
- requests
- pathlib
- openpyxl (for Excel file handling)

## Notes

- Large data files (CSV, Excel, images) are excluded from Git via .gitignore
- Scripts are designed to handle errors gracefully
- All barcodes are formatted as 12-digit strings
- Images are automatically organized by product barcodes
