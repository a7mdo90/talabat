import pandas as pd
from pathlib import Path

def replace_ampersand():
    """Replace A&amp;T with A&T in 265 test.xlsx"""
    
    print("Replacing A&amp;T with A&T in 265 test.xlsx...")
    
    # Load the Excel file
    excel_file = Path('list/excel/265 test.xlsx')
    if not excel_file.exists():
        print("❌ list/excel/265 test.xlsx file not found!")
        return
    
    df = pd.read_excel(excel_file)
    print(f"✅ Loaded 265 test.xlsx with {len(df)} products")
    print(f"📋 Current columns: {df.columns.tolist()}")
    
    # Show sample before replacement
    print(f"\n📊 Sample data before replacement:")
    print(df.head(3).to_string(index=False))
    
    # Count occurrences before replacement
    total_replacements = 0
    columns_with_replacements = []
    
    # Replace A&amp;T with A&T in all text columns
    for column in df.columns:
        if df[column].dtype == 'object':  # Only text columns
            before_count = df[column].astype(str).str.contains('A&amp;T', na=False).sum()
            if before_count > 0:
                df[column] = df[column].astype(str).str.replace('A&amp;T', 'A&T', regex=False)
                after_count = df[column].astype(str).str.contains('A&amp;T', na=False).sum()
                replacements_in_column = before_count - after_count
                total_replacements += replacements_in_column
                columns_with_replacements.append((column, replacements_in_column))
                print(f"✅ Column '{column}': {replacements_in_column} replacements")
    
    print(f"\n✅ Total replacements made: {total_replacements}")
    
    if total_replacements > 0:
        # Save the updated Excel file
        df.to_excel(excel_file, index=False)
        print(f"✅ Updated {excel_file}")
        
        # Show sample after replacement
        print(f"\n📊 Sample data after replacement:")
        print(df.head(3).to_string(index=False))
        
        # Show detailed statistics
        print(f"\n=== REPLACEMENT STATISTICS ===")
        print(f"Total replacements: {total_replacements}")
        print(f"Columns with replacements:")
        for column, count in columns_with_replacements:
            print(f"  - {column}: {count} replacements")
    else:
        print("ℹ️  No 'A&amp;T' found in the file - no replacements needed")

if __name__ == "__main__":
    replace_ampersand()
