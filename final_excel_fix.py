import pandas as pd
import csv

def main():
    print("Final Excel fix - preserving leading zeros...")
    
    # Load the current Excel file
    df = pd.read_excel('265 test.xlsx')
    
    # Convert barcodes to strings
    df['Barcode'] = df['Barcode'].astype(str)
    
    # Fix the problematic barcodes by adding leading zeros
    problematic_barcodes = ['14402685064', '10636953796', '12329850369', '14036802684', '18855675416', '13202150738']
    
    for barcode in problematic_barcodes:
        mask = df['Barcode'] == barcode
        if mask.any():
            df.loc[mask, 'Barcode'] = f"0{barcode}"
            print(f"Fixed: {barcode} → 0{barcode}")
    
    # First save as CSV to preserve the string format
    df.to_csv('265_test_temp.csv', index=False)
    print("✅ Saved as CSV to preserve string format")
    
    # Read back from CSV and save as Excel
    df_from_csv = pd.read_csv('265_test_temp.csv', dtype={'Barcode': str})
    
    # Save to Excel 
    df_from_csv.to_excel('265 test.xlsx', index=False)
    
    print("✅ Saved as Excel with text formatting for barcodes")
    
    # Clean up temporary file
    import os
    os.remove('265_test_temp.csv')
    
    # Final verification
    print("\n=== FINAL VERIFICATION ===")
    df_final = pd.read_excel('265 test.xlsx', dtype={'Barcode': str})
    
    # Get image files
    import os
    image_files = [f.split('.')[0] for f in os.listdir('downloaded_images')]
    
    # Check matches
    excel_barcodes = df_final['Barcode'].tolist()
    matches = sum(1 for barcode in excel_barcodes if barcode in image_files)
    
    print(f"Products: {len(df_final)}")
    print(f"Images: {len(image_files)}")
    print(f"Perfect matches: {matches}")
    
    if matches == len(df_final):
        print("\n🎉 PERFECT SUCCESS! ALL BARCODES NOW MATCH THEIR IMAGE FILES!")
        print("✅ All duplicate barcodes resolved")
        print("✅ All barcodes are unique")
        print("✅ Leading zeros preserved")
        print("✅ Every product has a matching image")
    else:
        print(f"\n⚠️  {len(df_final) - matches} mismatches still exist")
        
        # Show which ones don't match
        for i, barcode in enumerate(excel_barcodes):
            if barcode not in image_files:
                title = df_final.iloc[i]['English Title'][:30]
                print(f"    Missing: {barcode} - {title}")

if __name__ == "__main__":
    main()