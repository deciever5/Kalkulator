#!/usr/bin/env python3
"""
Fix Save Configuration Translations
Replaces long AI-generated text with simple, clean translations for configuration_saved_success
"""

import json
import os
from typing import Dict

def load_json_file(filepath: str) -> Dict:
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filepath: str, data: Dict) -> bool:
    """Save JSON file with proper formatting"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def get_proper_translations() -> Dict[str, str]:
    """Get proper simple translations for configuration_saved_success"""
    return {
        'en': '✅ Configuration saved successfully!',
        'de': '✅ Konfiguration erfolgreich gespeichert!',
        'es': '✅ Configuración guardada con éxito!',
        'fr': '✅ Configuration sauvegardée avec succès!',
        'it': '✅ Configurazione salvata con successo!',
        'nl': '✅ Configuratie succesvol opgeslagen!',
        'sv': '✅ Konfiguration sparad framgångsrikt!',
        'fi': '✅ Konfiguraatio tallennettu onnistuneesti!',
        'cs': '✅ Konfigurace úspěšně uložena!',
        'sk': '✅ Konfigurácia úspešne uložená!',
        'hu': '✅ Konfiguráció sikeresen elmentve!',
        'uk': '✅ Конфігурацію успішно збережено!',
        'pl': '✅ Konfiguracja zapisana pomyślnie!'
    }

def fix_all_languages():
    """Fix configuration_saved_success in all language files"""
    locales_dir = 'locales'
    proper_translations = get_proper_translations()
    
    for filename in os.listdir(locales_dir):
        if filename.endswith('.json'):
            lang_code = filename.replace('.json', '')
            filepath = os.path.join(locales_dir, filename)
            
            print(f"Processing {lang_code}...")
            
            # Load existing translations
            data = load_json_file(filepath)
            
            # Check if cost_estimation section exists
            if 'cost_estimation' not in data:
                data['cost_estimation'] = {}
            
            # Get the proper translation for this language
            if lang_code in proper_translations:
                new_translation = proper_translations[lang_code]
                
                # Update the translation
                data['cost_estimation']['configuration_saved_success'] = new_translation
                
                # Save the file
                if save_json_file(filepath, data):
                    print(f"  ✅ Updated {lang_code}: {new_translation}")
                else:
                    print(f"  ❌ Failed to update {lang_code}")
            else:
                print(f"  ⚠️ No translation defined for {lang_code}")

def main():
    """Main function"""
    print("🔧 Fixing Save Configuration Translations")
    print("=" * 50)
    
    fix_all_languages()
    
    print("\n✅ Translation fixes completed!")
    print("\nNow the save configuration button will show:")
    print("• Simple, clean success messages")
    print("• No long AI analysis text")
    print("• Consistent format across all languages")

if __name__ == "__main__":
    main()