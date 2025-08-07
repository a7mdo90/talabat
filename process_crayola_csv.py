import pandas as pd
import requests
from pathlib import Path
import time
import random
import string
import re

def generate_barcode():
    """Generate a random 12-digit barcode starting with 01"""
    return "01" + ''.join(random.choices(string.digits, k=10))

def download_image(image_url, file_path):
    """Download an image from URL to file path"""
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")
        return False

def clean_title(title):
    """Clean the title by removing the Arabic part after ||"""
    if '||' in title:
        return title.split('||')[0].strip()
    return title.strip()

def extract_arabic_title(title):
    """Extract Arabic title from the full title"""
    if '||' in title:
        arabic_part = title.split('||')[1].strip()
        return arabic_part
    return f"كرايولا {title}"

def process_crayola_csv():
    """Process crayola.csv and create Excel file with images"""
    crayola_dir = Path('crayola')
    images_dir = crayola_dir / 'images'
    
    # Create directories if they don't exist
    crayola_dir.mkdir(exist_ok=True)
    images_dir.mkdir(exist_ok=True)
    
    # Read the CSV file
    print("📖 Reading crayola.csv...")
    df = pd.read_csv('crayola.csv')
    
    print(f"📊 Found {len(df)} rows in crayola.csv")
    
    # Filter for unique products (remove duplicates based on Handle)
    df_unique = df.drop_duplicates(subset=['Handle'], keep='first')
    print(f"✅ Found {len(df_unique)} unique products")
    
    # Process products
    processed_products = []
    downloaded_images = 0
    
    for idx, row in df_unique.iterrows():
        # Extract data
        title = str(row.get('Title', ''))
        price = float(row.get('Variant Price', 0))
        barcode = str(row.get('Variant Barcode', ''))
        image_url = str(row.get('Image Src', ''))
        
        # Clean title and extract Arabic
        english_name = clean_title(title)
        arabic_name = extract_arabic_title(title)
        
        # Generate barcode if none exists
        if not barcode or barcode == 'nan':
            barcode = generate_barcode()
        
        # Clean barcode (remove quotes if present)
        barcode = barcode.replace("'", "").replace('"', '')
        
        product_data = {
            'english_name': english_name,
            'arabic_name': arabic_name,
            'barcode': barcode,
            'price': price
        }
        
        processed_products.append(product_data)
        
        # Download image if available
        if image_url and image_url != 'nan' and image_url.startswith('http'):
            # Determine file extension
            if '.jpg' in image_url.lower() or '.jpeg' in image_url.lower():
                ext = '.jpg'
            elif '.png' in image_url.lower():
                ext = '.png'
            else:
                ext = '.jpg'  # default
            
            image_filename = f"{barcode}{ext}"
            image_path = images_dir / image_filename
            
            if download_image(image_url, image_path):
                downloaded_images += 1
                print(f"✅ Downloaded: {image_filename}")
            else:
                print(f"❌ Failed to download: {image_filename}")
        
        time.sleep(0.1)  # Rate limiting
    
    # Create DataFrame and save to Excel
    df_final = pd.DataFrame(processed_products)
    excel_file = crayola_dir / 'crayola_products.xlsx'
    df_final.to_excel(excel_file, index=False)
    
    print(f"✅ Created crayola_products.xlsx with {len(processed_products)} products")
    print(f"✅ Downloaded {downloaded_images} images to crayola/images/")
    
    # Create download summary
    summary_file = images_dir / 'download_summary.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Crayola Products Download Summary\n")
        f.write(f"================================\n")
        f.write(f"Total products: {len(processed_products)}\n")
        f.write(f"Images downloaded: {downloaded_images}\n")
        f.write(f"Download date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Show sample of processed data
    print("\n📋 Sample of processed products:")
    for i, product in enumerate(processed_products[:5]):
        print(f"{i+1}. {product['english_name']} - {product['price']} - {product['barcode']}")
    
    return df_final

if __name__ == "__main__":
    process_crayola_csv()

