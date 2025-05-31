
import json
import os
from typing import Dict

def load_json_file(filepath: str) -> Dict:
    """Load a JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def save_json_file(filepath: str, data: Dict) -> bool:
    """Save data to JSON file with proper formatting"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def get_nested_value(data: Dict, key_path: str):
    """Get nested value using dot notation"""
    keys = key_path.split('.')
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current

def set_nested_value(data: Dict, key_path: str, value: str):
    """Set nested value using dot notation"""
    keys = key_path.split('.')
    current = data
    
    # Navigate to the parent of the target key
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    # Set the final key
    current[keys[-1]] = value

def get_all_keys_flat(data: Dict, prefix: str = "") -> Dict[str, str]:
    """Get all keys from nested dict as flat key-value pairs"""
    result = {}
    
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        
        if isinstance(value, dict):
            result.update(get_all_keys_flat(value, full_key))
        elif isinstance(value, str):
            result[full_key] = value
    
    return result

def fix_missing_translations():
    """Add missing translations to all language files using AI translation services"""
    from utils.ai_translation_service import AITranslationService
    
    locales_dir = "locales"
    
    # Load English as reference
    en_path = os.path.join(locales_dir, "en.json")
    en_data = load_json_file(en_path)
    
    if not en_data:
        print("Could not load English translations!")
        return
    
    # Get all English keys and values
    en_keys = get_all_keys_flat(en_data)
    print(f"Found {len(en_keys)} keys in English reference")
    
    # Process incomplete languages with AI translation
    incomplete_languages = ['fi', 'uk', 'sk', 'fr']
    ai_translator = AITranslationService()
    
    for lang in incomplete_languages:
        lang_path = os.path.join(locales_dir, f"{lang}.json")
        lang_data = load_json_file(lang_path)
        
        if not lang_data:
            print(f"Could not load {lang} translations!")
            continue
        
        # Get existing keys
        existing_keys = get_all_keys_flat(lang_data)
        
        # Find missing keys and their English values
        missing_keys = {}
        for key, value in en_keys.items():
            if key not in existing_keys:
                missing_keys[key] = value
        
        print(f"\n🤖 {lang.upper()}: AI translating {len(missing_keys)} missing keys...")
        
        if missing_keys:
            # Use AI translation service
            batch_size = 50  # Process in batches to avoid token limits
            translated_count = 0
            
            for i in range(0, len(missing_keys), batch_size):
                batch_keys = dict(list(missing_keys.items())[i:i+batch_size])
                print(f"   Translating batch {i//batch_size + 1} ({len(batch_keys)} keys)...")
                
                # Get AI translations
                translations = ai_translator.translate_missing_keys('en', lang, batch_keys)
                
                # Add translations to language data
                for key, translated_value in translations.items():
                    set_nested_value(lang_data, key, translated_value)
                    translated_count += 1
            
            # Save updated file
            if save_json_file(lang_path, lang_data):
                print(f"✅ {lang.upper()}: Successfully added {translated_count} AI translations")
            else:
                print(f"❌ {lang.upper()}: Failed to save translations")
        else:
            print(f"✅ {lang.upper()}: No missing translations found")
    
    print(f"\n🎉 AI translation fixing complete!")
    print("All incomplete languages now have AI-generated technical translations.")
    print("📝 Note: Review the AI translations for accuracy and business context.")

if __name__ == "__main__":
    fix_missing_translations()
