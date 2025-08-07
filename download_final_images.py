import pandas as pd
import requests
import os
from urllib.parse import urlparse
import time
from pathlib import Path

def get_file_extension(url):
    """Get file extension from URL"""
    parsed = urlparse(url)
    path = parsed.path
    if '.' in path:
        return path.split('.')[-1].lower()
    return 'jpg'  # Default extension

def download_image(url, filename, max_retries=3):
    """Download image from URL with retry logic"""
    for attempt in range(max_retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            return True
            
        except Exception as e:
            print(f"    Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
    
    return False

def main():
    print("Loading clean unique products from 265 test.xlsx...")
    df = pd.read_excel('265 test.xlsx')
    
    # Create images directory
    images_dir = Path('downloaded_images')
    images_dir.mkdir(exist_ok=True)
    
    print(f"Found {len(df)} unique products")
    
    # Filter products with image URLs
    products_with_images = df[df['Image URL'].notna() & (df['Image URL'] != '')]
    
    print(f"Products with images: {len(products_with_images)}")
    
    downloaded_count = 0
    failed_count = 0
    skipped_count = 0
    
    for idx, (_, row) in enumerate(products_with_images.iterrows()):
        image_url = row['Image URL']
        barcode = row['Barcode']
        english_title = row['English Title'][:50] if row['English Title'] else "No Title"
        
        if not image_url or not barcode:
            skipped_count += 1
            continue
        
        print(f"\n[{idx + 1}/{len(products_with_images)}] Processing: {barcode}")
        print(f"  Product: {english_title}")
        
        # Get file extension
        extension = get_file_extension(image_url)
        
        # Create filename using barcode
        filename = images_dir / f"{barcode}.{extension}"
        
        # Skip if file already exists
        if filename.exists():
            print(f"  ✓ File already exists: {filename}")
            downloaded_count += 1
            continue
        
        print(f"  Downloading: {image_url}")
        print(f"  Saving as: {filename}")
        
        if download_image(image_url, filename):
            print(f"  ✓ Downloaded successfully")
            downloaded_count += 1
        else:
            print(f"  ✗ Failed to download")
            failed_count += 1
        
        # Small delay to be respectful to the server
        time.sleep(0.5)
        
        # Progress update every 25 items
        if (idx + 1) % 25 == 0:
            print(f"\n=== Progress Update ===")
            print(f"Processed: {idx + 1}/{len(products_with_images)}")
            print(f"Downloaded: {downloaded_count}")
            print(f"Failed: {failed_count}")
    
    print(f"\n=== Final Download Summary ===")
    print(f"Total unique products: {len(df)}")
    print(f"Products with images: {len(products_with_images)}")
    print(f"Successfully downloaded: {downloaded_count}")
    print(f"Failed downloads: {failed_count}")
    print(f"Skipped (no image/barcode): {skipped_count}")
    print(f"Images saved to: {images_dir.absolute()}")
    
    # List first few downloaded files as verification
    if downloaded_count > 0:
        print(f"\nFirst few downloaded files:")
        downloaded_files = list(images_dir.glob("*"))[:5]
        for file in downloaded_files:
            print(f"  {file.name}")

if __name__ == "__main__":
    main()