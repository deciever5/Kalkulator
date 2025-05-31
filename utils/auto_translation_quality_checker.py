
import json
import os
from typing import Dict, List, Tuple
import re

def load_translation_file(language: str) -> Dict:
    """Load a specific translation file"""
    filepath = f"locales/{language}.json"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def find_auto_translations(data: Dict, prefix: str = "") -> List[Tuple[str, str]]:
    """Find all auto-translated entries (prefixed with [AUTO])"""
    auto_translations = []
    
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        
        if isinstance(value, dict):
            auto_translations.extend(find_auto_translations(value, full_key))
        elif isinstance(value, str) and value.startswith("[AUTO]"):
            auto_translations.append((full_key, value))
    
    return auto_translations

def analyze_auto_translation_quality():
    """Analyze the quality and completeness of auto-translations"""
    languages = ['de', 'nl', 'cs', 'hu', 'pl']
    
    print("=== AUTO-TRANSLATION QUALITY ANALYSIS ===\n")
    
    total_auto_count = 0
    language_stats = {}
    
    for lang in languages:
        translations = load_translation_file(lang)
        if not translations:
            continue
            
        auto_translations = find_auto_translations(translations)
        auto_count = len(auto_translations)
        total_auto_count += auto_count
        
        language_stats[lang] = {
            'auto_count': auto_count,
            'auto_translations': auto_translations
        }
        
        print(f"🔍 {lang.upper()} Analysis:")
        print(f"   Auto-translations found: {auto_count}")
        
        if auto_count > 0:
            print("   Sample auto-translations:")
            for key, value in auto_translations[:5]:  # Show first 5
                clean_value = value.replace("[AUTO] ", "")
                print(f"     {key}: '{clean_value}'")
            
            if auto_count > 5:
                print(f"     ... and {auto_count - 5} more")
        
        print()
    
    # Summary
    print("=== SUMMARY ===")
    print(f"Total auto-translations across all languages: {total_auto_count}")
    
    if total_auto_count > 0:
        print("\n🚨 TRANSLATION QUALITY ISSUES:")
        print("- All auto-translations are English text with [AUTO] prefix")
        print("- These need manual translation to target languages")
        print("- Auto-translations may cause poor user experience")
        
        print("\n📝 RECOMMENDED ACTIONS:")
        print("1. Prioritize translating frequently used UI elements")
        print("2. Focus on customer-facing text first")
        print("3. Consider professional translation services for accuracy")
        print("4. Test translations with native speakers")
        
        # Show most common auto-translation patterns
        all_auto_keys = []
        for lang_data in language_stats.values():
            all_auto_keys.extend([key for key, _ in lang_data['auto_translations']])
        
        key_frequency = {}
        for key in all_auto_keys:
            key_frequency[key] = key_frequency.get(key, 0) + 1
        
        common_keys = sorted(key_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        
        print("\n🔥 MOST COMMON AUTO-TRANSLATIONS (Priority for manual translation):")
        for key, freq in common_keys:
            print(f"   {key} (appears in {freq} languages)")
    
    else:
        print("✅ No auto-translations found - all content is properly translated!")
    
    return language_stats

def check_translation_consistency():
    """Check for inconsistencies in translations"""
    print("\n=== TRANSLATION CONSISTENCY CHECK ===")
    
    # Load English as reference
    en_translations = load_translation_file('en')
    languages = ['de', 'nl', 'cs', 'hu', 'pl']
    
    inconsistencies = []
    
    for lang in languages:
        lang_translations = load_translation_file(lang)
        auto_translations = find_auto_translations(lang_translations)
        
        for key, auto_value in auto_translations:
            # Get the English original
            en_value = get_nested_value(en_translations, key)
            clean_auto = auto_value.replace("[AUTO] ", "")
            
            if en_value and clean_auto == en_value:
                # This is a proper auto-translation
                continue
            elif en_value:
                inconsistencies.append({
                    'language': lang,
                    'key': key,
                    'english': en_value,
                    'auto_translation': clean_auto,
                    'issue': 'Mismatch with English source'
                })
    
    if inconsistencies:
        print(f"⚠️  Found {len(inconsistencies)} inconsistencies:")
        for issue in inconsistencies[:10]:  # Show first 10
            print(f"   {issue['language']}: {issue['key']}")
            print(f"      EN: '{issue['english']}'")
            print(f"      AUTO: '{issue['auto_translation']}'")
            print()
    else:
        print("✅ No major inconsistencies found in auto-translations")

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

if __name__ == "__main__":
    language_stats = analyze_auto_translation_quality()
    check_translation_consistency()
    
    print("\n=== NEXT STEPS ===")
    print("1. Run 'python utils/translation_validator.py' to check completeness")
    print("2. Manually translate [AUTO] prefixed items in JSON files")
    print("3. Test the application with each language")
    print("4. Consider using professional translation services for accuracy")
