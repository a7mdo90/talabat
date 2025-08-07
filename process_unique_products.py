import pandas as pd
import random
import re

def extract_titles_from_combined(title_text):
    """Extract English and Arabic titles from combined title text"""
    if pd.isna(title_text) or not isinstance(title_text, str):
        return "", ""
    
    # Split by '||' which seems to separate English and Arabic
    if '||' in title_text:
        parts = title_text.split('||')
        english_title = parts[0].strip()
        arabic_title = parts[1].strip() if len(parts) > 1 else ""
    else:
        # If no separator, try to detect Arabic vs English
        arabic_chars = re.findall(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', title_text)
        if arabic_chars:
            english_title = title_text
            arabic_title = title_text
        else:
            english_title = title_text
            arabic_title = ""
    
    return english_title, arabic_title

def generate_barcode():
    """Generate a 12-digit barcode starting with 01"""
    remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    return f"01{remaining_digits}"

def clean_barcode(existing_barcode):
    """Clean and validate existing barcode"""
    if pd.isna(existing_barcode):
        return None
    
    barcode_str = str(existing_barcode).strip().replace("'", "").replace('"', '')
    barcode_clean = ''.join(filter(str.isdigit, barcode_str))
    
    if barcode_clean and len(barcode_clean) >= 8:
        return barcode_clean
    return None

def main():
    print("Loading 265.csv...")
    df = pd.read_csv('265.csv')
    
    print(f"Total rows: {len(df)}")
    print(f"Unique titles: {df['Title'].nunique()}")
    
    # Group by title and take the first occurrence of each unique product
    unique_products = df.groupby('Title').first().reset_index()
    
    print(f"After removing duplicates: {len(unique_products)} unique products")
    
    processed_data = []
    
    for idx, row in unique_products.iterrows():
        if idx % 50 == 0:
            print(f"Processing unique product {idx + 1}/{len(unique_products)}")
        
        # Extract English and Arabic titles
        english_title, arabic_title = extract_titles_from_combined(row['Title'])
        
        # Get price
        price = row['Variant Price'] if pd.notna(row['Variant Price']) else 0.0
        
        # Get or generate barcode
        existing_barcode = row['Variant Barcode']
        cleaned_barcode = clean_barcode(existing_barcode)
        barcode = cleaned_barcode if cleaned_barcode else generate_barcode()
        
        # Get image URL
        image_url = row['Image Src'] if pd.notna(row['Image Src']) else ""
        
        processed_data.append({
            'English Title': english_title,
            'Arabic Title': arabic_title,
            'Price': price,
            'Barcode': barcode,
            'Image URL': image_url
        })
    
    # Create DataFrame with processed unique products
    result_df = pd.DataFrame(processed_data)
    
    print("Saving to 265 test.xlsx...")
    result_df.to_excel('265 test.xlsx', index=False)
    
    print("Preview of processed unique products:")
    print(result_df.head().to_string(index=False))
    
    print(f"\nFinal Summary:")
    print(f"- Total unique products: {len(result_df)}")
    print(f"- Products with images: {len([url for url in result_df['Image URL'] if url])}")
    print(f"- Products with Arabic titles: {len([title for title in result_df['Arabic Title'] if title])}")
    
    return result_df

if __name__ == "__main__":
    df = main()