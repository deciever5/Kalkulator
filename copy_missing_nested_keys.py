#!/usr/bin/env python3
"""
Copy Missing Nested Translation Keys
Copies all missing nested translation structures from Polish to other languages
"""

import json

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

def get_all_nested_keys(obj, prefix=""):
    """Get all nested keys from a dictionary"""
    keys = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_key = f"{prefix}.{key}" if prefix else key
            keys.append(current_key)
            if isinstance(value, dict):
                keys.extend(get_all_nested_keys(value, current_key))
    return keys

def copy_structure_with_placeholders(source_obj, target_lang):
    """Copy structure from source with placeholder values for target language"""
    if isinstance(source_obj, dict):
        result = {}
        for key, value in source_obj.items():
            if isinstance(value, dict):
                result[key] = copy_structure_with_placeholders(value, target_lang)
            elif isinstance(value, str):
                # Create placeholder that indicates it needs translation
                result[key] = f"[{target_lang.upper()}_TRANSLATION_NEEDED] {value}"
            else:
                result[key] = value
        return result
    else:
        return source_obj

def copy_missing_keys_to_language(lang_code):
    """Copy missing nested keys from Polish to target language"""
    if lang_code == 'pl':
        return True
        
    print(f"Copying missing nested keys to {lang_code}...")
    
    # Load Polish and target language files
    pl_data = load_json_file('locales/pl.json')
    target_data = load_json_file(f'locales/{lang_code}.json')
    
    if not pl_data or not target_data:
        return False
    
    # Get all Polish keys
    pl_keys = get_all_nested_keys(pl_data)
    target_keys = get_all_nested_keys(target_data)
    
    # Find missing nested structures
    missing_nested_structures = [
        'ventilation', 'roof_modifications', 'insulation', 'windows'
    ]
    
    added_count = 0
    
    for structure in missing_nested_structures:
        if structure in pl_data and structure not in target_data:
            # Copy entire structure with placeholders
            target_data[structure] = copy_structure_with_placeholders(pl_data[structure], lang_code)
            added_count += 1
            print(f"  Added {structure} structure to {lang_code}")
    
    # Save the updated file
    if save_json_file(f'locales/{lang_code}.json', target_data):
        print(f"  ✓ Successfully added {added_count} nested structures to {lang_code}")
        return True
    else:
        print(f"  ✗ Failed to update {lang_code}")
        return False

def main():
    """Main function"""
    print("Copying missing nested translation structures from Polish to all languages...")
    
    languages = ['en', 'de', 'fr', 'es', 'it', 'nl', 'cs', 'sk', 'hu', 'sv', 'fi', 'uk']
    
    success_count = 0
    for lang in languages:
        if copy_missing_keys_to_language(lang):
            success_count += 1
    
    print(f"Missing nested structures copy complete: {success_count}/{len(languages)} languages updated")

if __name__ == "__main__":
    main()