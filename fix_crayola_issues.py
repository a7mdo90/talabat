import pandas as pd
from pathlib import Path
import re

def fix_crayola_issues():
    """Fix barcode format and image matching issues in Crayola project"""
    crayola_dir = Path('crayola')
    excel_file = crayola_dir / 'crayola_products.xlsx'
    images_dir = crayola_dir / 'images'
    
    print("🔧 Fixing Crayola project issues...")
    
    # Load data
    df = pd.read_excel(excel_file)
    print(f"📊 Loaded {len(df)} products")
    
    # Fix barcode format - ensure all are 12 digits with leading zeros
    print("\n🔧 Fixing barcode formats...")
    fixed_count = 0
    
    for idx, row in df.iterrows():
        barcode = str(row['barcode'])
        
        # Remove any non-digit characters
        barcode_clean = re.sub(r'[^\d]', '', barcode)
        
        # Ensure it's 12 digits with leading zeros
        if len(barcode_clean) < 12:
            barcode_fixed = barcode_clean.zfill(12)
            df.at[idx, 'barcode'] = barcode_fixed
            fixed_count += 1
            print(f"   Fixed: {barcode} -> {barcode_fixed}")
    
    print(f"✅ Fixed {fixed_count} barcode formats")
    
    # Check image matching
    print("\n🖼️  Checking image matching...")
    image_files = list(images_dir.glob('*.jpg')) + list(images_dir.glob('*.png'))
    image_barcodes = set([f.stem for f in image_files])
    
    barcodes_in_excel = set(df['barcode'].astype(str))
    missing_images = barcodes_in_excel - image_barcodes
    extra_images = image_barcodes - barcodes_in_excel
    
    print(f"   - Images downloaded: {len(image_files)}")
    print(f"   - Products in Excel: {len(df)}")
    print(f"   - Missing images: {len(missing_images)}")
    print(f"   - Extra images: {len(extra_images)}")
    
    if missing_images:
        print(f"\n❌ Products missing images:")
        for barcode in list(missing_images)[:5]:
            product = df[df['barcode'] == barcode]
            if not product.empty:
                print(f"   - {product.iloc[0]['english_name']} (Barcode: {barcode})")
    
    # Save fixed Excel file
    df.to_excel(excel_file, index=False)
    print(f"\n✅ Saved fixed crayola_products.xlsx")
    
    # Final summary
    print(f"\n📋 Final Summary:")
    print(f"   - Total products: {len(df)}")
    print(f"   - Products with images: {len(df) - len(missing_images)}")
    print(f"   - Image coverage: {(len(df) - len(missing_images))/len(df)*100:.1f}%")
    
    return df

if __name__ == "__main__":
    fix_crayola_issues()

