
#!/usr/bin/env python3
"""
Check Polish translation completeness by comparing with English translations
"""

import json
import os

def load_json_file(filepath):
    """Load JSON file safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return {}

def get_all_keys_flat(data, prefix=""):
    """Get all keys from nested JSON as flat dictionary"""
    result = {}
    
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                result.update(get_all_keys_flat(value, new_key))
            else:
                result[new_key] = value
    
    return result

def check_polish_completeness():
    """Check Polish translation completeness"""
    print("🔍 Checking Polish translation completeness...")
    print("="*60)
    
    # Load English (reference) and Polish translations
    en_data = load_json_file('locales/en.json')
    pl_data = load_json_file('locales/pl.json')
    
    if not en_data or not pl_data:
        print("❌ Could not load translation files")
        return
    
    # Get flat key-value pairs
    en_translations = get_all_keys_flat(en_data)
    pl_translations = get_all_keys_flat(pl_data)
    
    print(f"📊 English translations: {len(en_translations)} keys")
    print(f"📊 Polish translations: {len(pl_translations)} keys")
    
    # Find missing keys
    missing_keys = set(en_translations.keys()) - set(pl_translations.keys())
    extra_keys = set(pl_translations.keys()) - set(en_translations.keys())
    
    if missing_keys:
        print(f"\n🚨 Missing Polish translations ({len(missing_keys)} keys):")
        print("-" * 40)
        for key in sorted(missing_keys):
            en_value = en_translations[key]
            print(f"  {key}: '{en_value}'")
    
    if extra_keys:
        print(f"\n➕ Extra Polish keys not in English ({len(extra_keys)} keys):")
        print("-" * 40)
        for key in sorted(extra_keys):
            pl_value = pl_translations[key]
            print(f"  {key}: '{pl_value}'")
    
    # Check for potentially untranslated values (same as English)
    same_values = []
    for key in en_translations:
        if key in pl_translations:
            en_val = en_translations[key].strip()
            pl_val = pl_translations[key].strip()
            if en_val == pl_val and len(en_val) > 3:  # Skip short values
                # Skip technical terms that should be the same
                skip_terms = ['KAN-BUD', 'OpenAI', 'GPT', 'API', 'PDF', 'DWG', 'HVAC', 'ISO', 'EUR', 'PLN']
                if not any(term in en_val.upper() for term in skip_terms):
                    same_values.append((key, en_val))
    
    if same_values:
        print(f"\n⚠️  Potentially untranslated values ({len(same_values)} keys):")
        print("-" * 40)
        for key, value in same_values:
            print(f"  {key}: '{value}'")
    
    # Summary
    print(f"\n📈 SUMMARY:")
    print(f"   English keys: {len(en_translations)}")
    print(f"   Polish keys: {len(pl_translations)}")
    print(f"   Missing: {len(missing_keys)}")
    print(f"   Extra: {len(extra_keys)}")
    print(f"   Potentially untranslated: {len(same_values)}")
    
    completeness = ((len(pl_translations) - len(same_values)) / len(en_translations)) * 100
    print(f"   Translation completeness: {completeness:.1f}%")
    
    if missing_keys or same_values:
        print(f"\n💡 RECOMMENDATIONS:")
        print("1. Add missing Polish translations to locales/pl.json")
        print("2. Review potentially untranslated values")
        print("3. Test the app manually in Polish mode")

if __name__ == "__main__":
    check_polish_completeness()
