
import json
import os
from utils.ai_translation_service import AITranslationService

def add_save_configuration_to_all_languages():
    """Add save_configuration key to all language files"""
    
    # Base translations
    base_translations = {
        'en': 'Save Configuration',
        'pl': 'Zapisz konfigurację'
    }
    
    locales_dir = 'locales'
    
    # Initialize AI translation service
    ai_service = AITranslationService()
    
    for filename in os.listdir(locales_dir):
        if filename.endswith('.json') and not filename.endswith('.backup'):
            lang_code = filename.replace('.json', '')
            filepath = os.path.join(locales_dir, filename)
            
            print(f"Processing {lang_code}...")
            
            # Load existing translations
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Skip if key already exists
            if 'save_configuration' in data:
                print(f"  Key already exists in {lang_code}")
                continue
            
            # Use base translation if available, otherwise translate
            if lang_code in base_translations:
                translation = base_translations[lang_code]
            else:
                try:
                    translation = ai_service._translate_text(
                        "Save Configuration",
                        lang_code
                    )
                    if translation:
                        print(f"  Translated to: {translation}")
                    else:
                        translation = "Save Configuration"  # fallback
                except Exception as e:
                    print(f"  Translation failed for {lang_code}: {e}")
                    translation = "Save Configuration"  # fallback
            
            # Add the key
            data['save_configuration'] = translation
            
            # Save back
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"  Added to {lang_code}: {translation}")

if __name__ == "__main__":
    add_save_configuration_to_all_languages()
    print("✅ Finished adding save_configuration key to all languages")
