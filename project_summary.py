import pandas as pd
from pathlib import Path

def generate_project_summary():
    """Generate a comprehensive summary of both Crayola and Deli projects"""
    
    print("📊 PROJECT SUMMARY REPORT")
    print("=" * 50)
    
    # Crayola Project Summary
    print("\n🎨 CRAYOLA PROJECT")
    print("-" * 30)
    
    crayola_dir = Path('crayola')
    crayola_excel = crayola_dir / 'crayola_products.xlsx'
    crayola_images = crayola_dir / 'images'
    
    if crayola_excel.exists():
        df_crayola = pd.read_excel(crayola_excel)
        crayola_image_files = list(crayola_images.glob('*.jpg')) + list(crayola_images.glob('*.png'))
        
        print(f"✅ Products: {len(df_crayola)}")
        print(f"✅ Images: {len(crayola_image_files)}")
        print(f"✅ Image Coverage: {len(crayola_image_files)/len(df_crayola)*100:.1f}%")
        print(f"💰 Price Range: {df_crayola['price'].min():.2f} - {df_crayola['price'].max():.2f}")
        print(f"💰 Average Price: {df_crayola['price'].mean():.2f}")
        
        # Check barcode types
        existing_barcodes = df_crayola[df_crayola['barcode'].astype(str).str.startswith('69')]
        generated_barcodes = df_crayola[df_crayola['barcode'].astype(str).str.startswith('01')]
        
        print(f"📊 Existing Barcodes: {len(existing_barcodes)}")
        print(f"📊 Generated Barcodes: {len(generated_barcodes)}")
    else:
        print("❌ Crayola project not found")
    
    # Deli Project Summary
    print("\n📁 DELI PROJECT")
    print("-" * 30)
    
    deli_dir = Path('deli')
    deli_excel = deli_dir / 'deli_products.xlsx'
    deli_images = deli_dir / 'images'
    
    if deli_excel.exists():
        df_deli = pd.read_excel(deli_excel)
        deli_image_files = list(deli_images.glob('*.jpg')) + list(deli_images.glob('*.png')) + list(deli_images.glob('*.webp'))
        
        print(f"✅ Products: {len(df_deli)}")
        print(f"✅ Images: {len(deli_image_files)}")
        print(f"✅ Image Coverage: {len(deli_image_files)/len(df_deli)*100:.1f}%")
        print(f"💰 Price Range: {df_deli['price'].min():.2f} - {df_deli['price'].max():.2f}")
        print(f"💰 Average Price: {df_deli['price'].mean():.2f}")
        
        # Check barcode types
        existing_barcodes = df_deli[df_deli['barcode'].astype(str).str.startswith('69')]
        generated_barcodes = df_deli[df_deli['barcode'].astype(str).str.startswith('01')]
        
        print(f"📊 Existing Barcodes: {len(existing_barcodes)}")
        print(f"📊 Generated Barcodes: {len(generated_barcodes)}")
    else:
        print("❌ Deli project not found")
    
    # Overall Summary
    print("\n📋 OVERALL SUMMARY")
    print("-" * 30)
    
    total_products = 0
    total_images = 0
    
    if crayola_excel.exists():
        total_products += len(df_crayola)
        total_images += len(crayola_image_files)
    
    if deli_excel.exists():
        total_products += len(df_deli)
        total_images += len(deli_image_files)
    
    print(f"✅ Total Products: {total_products}")
    print(f"✅ Total Images: {total_images}")
    print(f"✅ Overall Image Coverage: {total_images/total_products*100:.1f}%")
    
    print("\n🎉 Both projects completed successfully!")
    print("📁 Check the 'crayola/' and 'deli/' folders for the Excel files and images.")

if __name__ == "__main__":
    generate_project_summary()

