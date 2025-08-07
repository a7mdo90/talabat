import pandas as pd
import os
from pathlib import Path
import shutil

def main():
    print("Updating list/excel/1.xlsx to match list/pics folder barcodes...")
    
    # Load the 1.xlsx file
    excel_file = Path('list/excel/1.xlsx')
    if not excel_file.exists():
        print("❌ list/excel/1.xlsx file not found!")
        return
    
    df = pd.read_excel(excel_file)
    print(f"Loaded 1.xlsx with {len(df)} products")
    print(f"Columns: {df.columns.tolist()}")
    
    # Show current structure
    print(f"\nCurrent data structure:")
    print(df.head().to_string(index=False))
    
    # Get image files from pics folder
    pics_folder = Path('list/pics')
    if not pics_folder.exists():
        print("❌ list/pics folder not found!")
        return
    
    pics_files = list(pics_folder.glob('*'))
    pics_files = [f for f in pics_files if f.is_file()]  # Only files, not directories
    print(f"Found {len(pics_files)} image files in pics folder")
    
    # Extract barcodes from pic filenames (remove extension)
    pic_barcodes = []
    for pic_file in pics_files:
        barcode = pic_file.stem  # filename without extension
        pic_barcodes.append(barcode)
    
    # Sort for consistent assignment
    sorted_pic_barcodes = sorted(pic_barcodes)
    
    print(f"\nFirst 10 barcodes from pics folder:")
    for i, barcode in enumerate(sorted_pic_barcodes[:10]):
        print(f"  {i+1}. {barcode}")
    
    print(f"\nComparison:")
    print(f"  Products in 1.xlsx: {len(df)}")
    print(f"  Images in pics folder: {len(pic_barcodes)}")
    
    # Identify the barcode column in the Excel file
    barcode_column = None
    possible_barcode_cols = ['Variant Barcode', 'Barcode', 'variant barcode', 'barcode']
    
    for col in possible_barcode_cols:
        if col in df.columns:
            barcode_column = col
            break
    
    if not barcode_column:
        print("❌ Could not find barcode column in 1.xlsx!")
        print(f"Available columns: {df.columns.tolist()}")
        return
    
    print(f"✅ Found barcode column: '{barcode_column}'")
    
    # Update barcodes in the Excel file
    print(f"\nUpdating barcodes in 1.xlsx...")
    
    changes_made = []
    for i, (idx, row) in enumerate(df.iterrows()):
        if i < len(sorted_pic_barcodes):
            old_barcode = str(row[barcode_column]) if pd.notna(row[barcode_column]) else "None"
            new_barcode = sorted_pic_barcodes[i]
            
            # Update the barcode
            df.at[idx, barcode_column] = new_barcode
            
            # Get product title for reference
            title_col = 'Title' if 'Title' in df.columns else df.columns[1]  # Use Title or second column
            title = str(row[title_col])[:40] if pd.notna(row[title_col]) else "No Title"
            
            changes_made.append({
                'title': title,
                'old_barcode': old_barcode,
                'new_barcode': new_barcode,
                'index': i
            })
            
            if i < 5:  # Show first 5 changes
                print(f"  {i+1}. {title}...")
                print(f"     {old_barcode} → {new_barcode}")
        else:
            print(f"⚠️  Product {i+1} has no matching image from pics folder")
    
    # Save the updated Excel file
    df.to_excel(excel_file, index=False)
    print(f"\n✅ Updated {excel_file} with {len(changes_made)} barcode changes")
    
    # Now copy images from pics folder to downloaded_images with correct barcode names
    downloaded_images_dir = Path('downloaded_images')
    
    # Clear existing downloaded_images folder and recreate
    if downloaded_images_dir.exists():
        shutil.rmtree(downloaded_images_dir)
    downloaded_images_dir.mkdir()
    
    print(f"\nCopying images from pics folder to downloaded_images...")
    
    copied_count = 0
    for change in changes_made:
        new_barcode = change['new_barcode']
        title = change['title']
        
        # Find the source image in pics folder
        source_files = list(pics_folder.glob(f"{new_barcode}.*"))
        
        if source_files:
            source_file = source_files[0]  # Take first match
            extension = source_file.suffix
            dest_file = downloaded_images_dir / f"{new_barcode}{extension}"
            
            # Copy the file
            shutil.copy2(source_file, dest_file)
            copied_count += 1
            
            if copied_count <= 5:  # Show first 5 copies
                print(f"  ✅ Copied: {source_file.name} → {dest_file.name}")
        else:
            print(f"  ❌ No image found for barcode: {new_barcode}")
    
    print(f"\n✅ Copied {copied_count} images to downloaded_images folder")
    
    # Final verification
    print(f"\n=== FINAL VERIFICATION ===")
    df_final = pd.read_excel(excel_file)
    final_images = list(downloaded_images_dir.glob('*'))
    
    excel_barcodes = df_final[barcode_column].astype(str).tolist()
    image_barcodes = [f.stem for f in final_images]
    
    matches = sum(1 for barcode in excel_barcodes if barcode in image_barcodes)
    
    print(f"Products in list/excel/1.xlsx: {len(df_final)}")
    print(f"Images in downloaded_images: {len(final_images)}")
    print(f"Perfect matches: {matches}")
    print(f"Barcode column used: '{barcode_column}'")
    
    if matches == len(df_final) and matches == len(final_images):
        print("\n🎉 PERFECT! All barcodes in 1.xlsx now match pics folder image names!")
        print("✅ All products have correct barcodes from pics folder")
        print("✅ All images copied and renamed correctly")
        print("✅ Ready for use!")
    else:
        print(f"\n⚠️  {len(df_final) - matches} products don't have matching images")
        
        # Show sample of updated data
        print(f"\nSample of updated data:")
        print(df_final.head(3).to_string(index=False))

if __name__ == "__main__":
    main()


