import pandas as pd
from pathlib import Path
import requests
import time
import json

def translate_text(text, target_lang='ar'):
    """Translate text using Google Translate API (free alternative)"""
    try:
        # Using a free translation service
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': 'en',
            'tl': target_lang,
            'dt': 't',
            'q': text
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Extract translation from response
        translation_data = response.json()
        if translation_data and len(translation_data) > 0:
            translated_text = ''.join([part[0] for part in translation_data[0] if part[0]])
            return translated_text.strip()
        
        return text  # Return original if translation fails
        
    except Exception as e:
        print(f"⚠️  Translation error for '{text[:30]}...': {e}")
        return text  # Return original text if translation fails

def translate_missing_arabic():
    """Translate missing Arabic translations in 265 test.xlsx"""
    
    print("Translating missing Arabic translations in 265 test.xlsx...")
    
    # Load the Excel file
    excel_file = Path('list/excel/265 test.xlsx')
    if not excel_file.exists():
        print("❌ list/excel/265 test.xlsx file not found!")
        return
    
    df = pd.read_excel(excel_file)
    print(f"✅ Loaded 265 test.xlsx with {len(df)} products")
    
    # Check Arabic Title column
    arabic_column = 'Arabic Title'
    english_column = 'English Title'
    
    if arabic_column not in df.columns:
        print(f"❌ {arabic_column} column not found!")
        return
    
    if english_column not in df.columns:
        print(f"❌ {english_column} column not found!")
        return
    
    # Find rows missing Arabic translations
    missing_arabic_mask = df[arabic_column].isna()
    missing_count = missing_arabic_mask.sum()
    
    if missing_count == 0:
        print("🎉 All products already have Arabic translations!")
        return
    
    print(f"📋 Found {missing_count} products missing Arabic translations")
    
    # Translate missing titles
    translations_made = 0
    for idx, row in df[missing_arabic_mask].iterrows():
        english_title = str(row[english_column]) if pd.notna(row[english_column]) else ''
        
        if english_title and english_title.strip():
            print(f"🔄 Translating: {english_title[:50]}...")
            
            # Translate to Arabic
            arabic_translation = translate_text(english_title, 'ar')
            
            # Update the Arabic Title column
            df.at[idx, arabic_column] = arabic_translation
            translations_made += 1
            
            print(f"✅ Translated: {arabic_translation[:50]}...")
            
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
            
            # Show progress every 10 translations
            if translations_made % 10 == 0:
                print(f"📊 Progress: {translations_made}/{missing_count} translations completed")
    
    print(f"\n✅ Completed {translations_made} translations")
    
    # Save the updated Excel file
    df.to_excel(excel_file, index=False)
    print(f"✅ Updated {excel_file}")
    
    # Final statistics
    final_missing = df[arabic_column].isna().sum()
    final_has_arabic = df[arabic_column].notna().sum()
    
    print(f"\n=== FINAL STATISTICS ===")
    print(f"Total products: {len(df)}")
    print(f"Products with Arabic translation: {final_has_arabic}")
    print(f"Products still missing Arabic translation: {final_missing}")
    print(f"Completion rate: {(final_has_arabic/len(df)*100):.1f}%")
    
    # Show sample of new translations
    if translations_made > 0:
        print(f"\n📝 Sample of new translations:")
        new_translations = df[df[arabic_column].notna()].tail(5)  # Show last 5
        for idx, row in new_translations.iterrows():
            english = str(row[english_column])[:40] if pd.notna(row[english_column]) else ''
            arabic = str(row[arabic_column])[:40] if pd.notna(row[arabic_column]) else ''
            print(f"  {english}... → {arabic}...")

if __name__ == "__main__":
    translate_missing_arabic()
