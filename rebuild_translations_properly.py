#!/usr/bin/env python3
"""
Rebuild All Translations Properly
Copies the exact working structure from Polish to all other languages with placeholders
"""

import json
import os

def load_json_file(filepath):
    """Load JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def save_json_file(filepath, data):
    """Save JSON file with proper formatting"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def copy_structure_with_placeholders(obj, language_code, key_path=""):
    """Recursively copy structure replacing Polish text with language placeholders"""
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            current_path = f"{key_path}.{key}" if key_path else key
            result[key] = copy_structure_with_placeholders(value, language_code, current_path)
        return result
    elif isinstance(obj, str):
        # Create a clear placeholder that indicates translation is needed
        return f"[{language_code.upper()}_NEEDS_TRANSLATION] {obj}"
    elif isinstance(obj, list):
        return [copy_structure_with_placeholders(item, language_code, key_path) for item in obj]
    else:
        return obj

def rebuild_language_file(language_code):
    """Rebuild a language file based on Polish structure"""
    print(f"Rebuilding {language_code} based on Polish structure...")
    
    # Load Polish file as the master template
    pl_data = load_json_file('locales/pl.json')
    if not pl_data:
        print(f"  ✗ Could not load Polish template")
        return False
    
    # Load existing language file to preserve any good translations
    existing_data = load_json_file(f'locales/{language_code}.json')
    
    # Copy Polish structure with placeholders
    new_data = copy_structure_with_placeholders(pl_data, language_code)
    
    # If we have existing data, try to preserve good translations
    if existing_data:
        new_data = merge_existing_translations(new_data, existing_data, language_code)
    
    # Save the rebuilt file
    if save_json_file(f'locales/{language_code}.json', new_data):
        print(f"  ✓ Successfully rebuilt {language_code}")
        return True
    else:
        print(f"  ✗ Failed to rebuild {language_code}")
        return False

def merge_existing_translations(new_data, existing_data, language_code, key_path=""):
    """Merge existing good translations into the new structure"""
    if isinstance(new_data, dict) and isinstance(existing_data, dict):
        result = {}
        for key, new_value in new_data.items():
            if key in existing_data:
                current_path = f"{key_path}.{key}" if key_path else key
                result[key] = merge_existing_translations(new_value, existing_data[key], language_code, current_path)
            else:
                result[key] = new_value
        return result
    elif isinstance(new_data, str) and isinstance(existing_data, str):
        # If existing translation doesn't look like Polish and isn't a placeholder, keep it
        if not is_likely_polish_or_placeholder(existing_data):
            return existing_data
        else:
            return new_data
    else:
        return new_data

def is_likely_polish_or_placeholder(text):
    """Check if text appears to be Polish or a placeholder"""
    if not isinstance(text, str):
        return False
    
    polish_indicators = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż', 'Polskie', 'Polski']
    placeholder_indicators = ['PLACEHOLDER', 'NEEDS_TRANSLATION', 'TODO', '[EN_', '[DE_', '[FR_']
    
    return any(indicator in text for indicator in polish_indicators + placeholder_indicators)

def main():
    """Main function"""
    print("Rebuilding all translation files based on working Polish structure...")
    
    # Languages to rebuild (excluding Polish which is the template)
    languages = ['en', 'de', 'fr', 'es', 'it', 'nl', 'cs', 'sk', 'hu', 'sv', 'fi', 'uk']
    
    success_count = 0
    for lang in languages:
        if rebuild_language_file(lang):
            success_count += 1
    
    print(f"\nTranslation rebuild complete: {success_count}/{len(languages)} languages rebuilt")
    print("All language files now have the same structure as the working Polish version")
    print("Text marked with [LANG_NEEDS_TRANSLATION] placeholders can be translated later")

if __name__ == "__main__":
    main()