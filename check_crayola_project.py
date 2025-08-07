import pandas as pd
from pathlib import Path

def check_crayola_project():
    """Check the Crayola project for completeness"""
    crayola_dir = Path('crayola')
    excel_file = crayola_dir / 'crayola_products.xlsx'
    images_dir = crayola_dir / 'images'
    
    print("🔍 Checking Crayola project...")
    
    # Check if Excel file exists
    if not excel_file.exists():
        print("❌ crayola_products.xlsx not found!")
        return
    
    # Load data
    df = pd.read_excel(excel_file)
    print(f"✅ Excel file found with {len(df)} products")
    
    # Check columns
    print(f"📋 Columns: {df.columns.tolist()}")
    
    # Check barcodes
    print(f"\n📊 Barcode analysis:")
    existing_barcodes = df[df['barcode'].astype(str).str.startswith('07')]
    generated_barcodes = df[df['barcode'].astype(str).str.startswith('01')]
    
    print(f"   - Products with existing barcodes: {len(existing_barcodes)}")
    print(f"   - Products with generated barcodes: {len(generated_barcodes)}")
    
    # Check prices
    print(f"\n💰 Price analysis:")
    print(f"   - Price range: {df['price'].min():.2f} - {df['price'].max():.2f}")
    print(f"   - Average price: {df['price'].mean():.2f}")
    
    # Check images
    if images_dir.exists():
        image_files = list(images_dir.glob('*.jpg')) + list(images_dir.glob('*.png'))
        print(f"\n🖼️  Image analysis:")
        print(f"   - Images downloaded: {len(image_files)}")
        print(f"   - Products: {len(df)}")
        print(f"   - Image coverage: {len(image_files)/len(df)*100:.1f}%")
        
        # Check for missing images
        barcodes_in_excel = set(df['barcode'].astype(str))
        image_barcodes = set([f.stem for f in image_files])
        missing_images = barcodes_in_excel - image_barcodes
        
        if missing_images:
            print(f"   - Missing images for {len(missing_images)} products")
        else:
            print(f"   - ✅ All products have images")
    else:
        print("❌ Images directory not found!")
    
    # Check for empty values
    print(f"\n🔍 Data quality check:")
    empty_english = df['english_name'].isna().sum()
    empty_arabic = df['arabic_name'].isna().sum()
    empty_barcode = df['barcode'].isna().sum()
    empty_price = df['price'].isna().sum()
    
    print(f"   - Empty English names: {empty_english}")
    print(f"   - Empty Arabic names: {empty_arabic}")
    print(f"   - Empty barcodes: {empty_barcode}")
    print(f"   - Empty prices: {empty_price}")
    
    # Show sample of existing barcodes
    if len(existing_barcodes) > 0:
        print(f"\n📋 Sample products with existing barcodes:")
        for idx, row in existing_barcodes.head(5).iterrows():
            print(f"   - {row['english_name']} (Barcode: {row['barcode']})")
    
    print(f"\n✅ Crayola project check complete!")

if __name__ == "__main__":
    check_crayola_project()

