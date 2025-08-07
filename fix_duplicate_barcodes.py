import pandas as pd
import random
import shutil
from pathlib import Path
import os

def generate_barcode():
    """Generate a 12-digit barcode starting with 01"""
    remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    return f"01{remaining_digits}"

def main():
    print("Loading Excel file...")
    df = pd.read_excel('265 test.xlsx')
    
    print(f"Total products: {len(df)}")
    
    # Find duplicate barcodes
    barcode_counts = df['Barcode'].value_counts()
    duplicate_barcodes = barcode_counts[barcode_counts > 1]
    
    print(f"\nDuplicate barcodes found:")
    for barcode, count in duplicate_barcodes.items():
        print(f"  Barcode {barcode}: {count} products")
        
        # Show which products have this barcode
        duplicate_products = df[df['Barcode'] == barcode]
        for idx, row in duplicate_products.iterrows():
            title = row['English Title'][:50] if row['English Title'] else "No Title"
            print(f"    - {title}...")
    
    # Create a copy of the dataframe to modify
    df_fixed = df.copy()
    
    # Track all existing barcodes to avoid generating duplicates
    all_barcodes = set(df['Barcode'].astype(str).tolist())
    
    # Fix duplicates by assigning new barcodes (except keep original for first occurrence)
    changes_made = []
    
    for duplicate_barcode in duplicate_barcodes.index:
        duplicate_rows = df_fixed[df_fixed['Barcode'] == duplicate_barcode]
        
        # Skip the first occurrence (keep original), change the rest
        for i, (idx, row) in enumerate(duplicate_rows.iterrows()):
            if i == 0:  # Keep first occurrence unchanged
                continue
                
            # Generate new unique barcode
            new_barcode = generate_barcode()
            while new_barcode in all_barcodes:
                new_barcode = generate_barcode()
            
            # Update the dataframe
            old_barcode = row['Barcode']
            df_fixed.at[idx, 'Barcode'] = new_barcode
            all_barcodes.add(new_barcode)
            
            title = row['English Title'][:40] if row['English Title'] else "No Title"
            changes_made.append({
                'title': title,
                'old_barcode': str(old_barcode),
                'new_barcode': new_barcode,
                'row_index': idx
            })
            
            print(f"\nChanged: {title}...")
            print(f"  Old barcode: {old_barcode}")
            print(f"  New barcode: {new_barcode}")
    
    # Save updated Excel file
    df_fixed.to_excel('265 test.xlsx', index=False)
    print(f"\n✅ Updated Excel file with {len(changes_made)} barcode changes")
    
    # Now handle the image files
    images_dir = Path('downloaded_images')
    
    for change in changes_made:
        old_barcode = change['old_barcode']
        new_barcode = change['new_barcode']
        title = change['title']
        
        # Find the image file with the old barcode
        old_image_files = list(images_dir.glob(f"{old_barcode}.*"))
        
        if old_image_files:
            old_image_file = old_image_files[0]  # Take the first match
            extension = old_image_file.suffix
            new_image_file = images_dir / f"{new_barcode}{extension}"
            
            # Copy the image file with new name
            shutil.copy2(old_image_file, new_image_file)
            print(f"📸 Copied image: {old_image_file.name} → {new_image_file.name}")
        else:
            print(f"⚠️  No image found for old barcode: {old_barcode}")
    
    # Verify final results
    print(f"\n=== VERIFICATION ===")
    df_final = pd.read_excel('265 test.xlsx')
    final_barcode_counts = df_final['Barcode'].value_counts()
    remaining_duplicates = final_barcode_counts[final_barcode_counts > 1]
    
    if len(remaining_duplicates) == 0:
        print("✅ SUCCESS: All barcodes are now unique!")
    else:
        print(f"⚠️  Still have {len(remaining_duplicates)} duplicate barcodes:")
        for barcode, count in remaining_duplicates.items():
            print(f"  - {barcode}: {count} times")
    
    # Count image files
    image_files = list(images_dir.glob("*"))
    print(f"📸 Total image files: {len(image_files)}")
    print(f"📋 Total products: {len(df_final)}")
    
    print(f"\nSummary of changes:")
    print(f"- Products with changed barcodes: {len(changes_made)}")
    print(f"- New image files created: {len(changes_made)}")
    print(f"- Total unique barcodes: {len(df_final['Barcode'].unique())}")

if __name__ == "__main__":
    main()