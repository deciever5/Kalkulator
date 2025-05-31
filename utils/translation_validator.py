
"""
Translation validation utility to ensure consistency across all language files.
"""
import json
import os
from typing import Dict, List, Set

def load_all_translations() -> Dict[str, Dict]:
    """Load all translation files"""
    translations = {}
    # Get the directory where this script is located and go up one level to find locales
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    locales_dir = os.path.join(script_dir, "locales")
    
    if not os.path.exists(locales_dir):
        print(f"Locales directory not found at: {locales_dir}")
        return translations
    
    for filename in os.listdir(locales_dir):
        if filename.endswith('.json'):
            lang_code = filename[:-5]
            with open(os.path.join(locales_dir, filename), 'r', encoding='utf-8') as f:
                translations[lang_code] = json.load(f)
    
    return translations

def get_all_keys(data: Dict, prefix: str = "") -> Set[str]:
    """Recursively get all keys from nested dictionary"""
    keys = set()
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        keys.add(full_key)
        if isinstance(value, dict):
            keys.update(get_all_keys(value, full_key))
    return keys

def validate_translations() -> Dict[str, any]:
    """Validate translation completeness across all languages"""
    translations = load_all_translations()
    
    if not translations:
        return {"error": "No translation files found"}
    
    # Get all keys from all languages
    all_keys_by_lang = {}
    for lang, content in translations.items():
        all_keys_by_lang[lang] = get_all_keys(content)
    
    # Find the language with the most keys (reference)
    reference_lang = max(all_keys_by_lang.keys(), key=lambda x: len(all_keys_by_lang[x]))
    reference_keys = all_keys_by_lang[reference_lang]
    
    # Find missing keys for each language
    missing_keys = {}
    for lang, keys in all_keys_by_lang.items():
        if lang != reference_lang:
            missing_keys[lang] = reference_keys - keys
    
    return {
        "reference_language": reference_lang,
        "reference_key_count": len(reference_keys),
        "languages": {lang: len(keys) for lang, keys in all_keys_by_lang.items()},
        "missing_keys": missing_keys,
        "total_missing": sum(len(keys) for keys in missing_keys.values())
    }

def generate_missing_translations_report():
    """Generate a detailed report of missing translations"""
    result = validate_translations()
    
    print("=== TRANSLATION VALIDATION REPORT ===")
    print(f"Reference Language: {result['reference_language']} ({result['reference_key_count']} keys)")
    print("\nLanguage Coverage:")
    
    for lang, count in result['languages'].items():
        coverage = (count / result['reference_key_count']) * 100
        status = "✓" if lang == result['reference_language'] else f"⚠ {len(result['missing_keys'].get(lang, []))} missing"
        print(f"  {lang}: {count} keys ({coverage:.1f}%) {status}")
    
    print(f"\nTotal missing translations: {result['total_missing']}")
    
    # Show missing keys for each language
    for lang, missing in result['missing_keys'].items():
        if missing:
            print(f"\n--- Missing keys in {lang} ---")
            for key in sorted(missing)[:10]:  # Show first 10
                print(f"  {key}")
            if len(missing) > 10:
                print(f"  ... and {len(missing) - 10} more")

if __name__ == "__main__":
    generate_missing_translations_report()
