
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

def find_all_translations(data: Dict, prefix: str = "") -> List[Tuple[str, str]]:
    """Find all translation entries"""
    translations = []
    
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        
        if isinstance(value, dict):
            translations.extend(find_all_translations(value, full_key))
        elif isinstance(value, str):
            translations.append((full_key, value))
    
    return translations

def analyze_translation_quality():
    """Analyze semantic quality of translations by comparing with English"""
    
    # Load English as reference
    en_translations = load_translation_file('en')
    if not en_translations:
        print("❌ Cannot load English translations for reference")
        return
    
    languages = ['de', 'nl', 'cs', 'hu', 'pl']
    
    print("=== SEMANTIC TRANSLATION QUALITY ANALYSIS ===\n")
    
    # Get all English translations for reference
    en_all = find_all_translations(en_translations)
    
    for lang in languages:
        print(f"🔍 {lang.upper()} Semantic Analysis:")
        
        lang_translations = load_translation_file(lang)
        if not lang_translations:
            print(f"   ❌ Could not load {lang} translations")
            continue
            
        lang_all = find_all_translations(lang_translations)
        
        # Analyze different quality issues
        auto_prefixed = []
        identical_to_english = []
        missing_translations = []
        good_translations = []
        suspicious_translations = []
        
        for en_key, en_value in en_all:
            lang_value = get_nested_value(lang_translations, en_key)
            
            if lang_value is None:
                missing_translations.append(en_key)
            elif lang_value.startswith("[AUTO]"):
                auto_prefixed.append((en_key, lang_value))
            elif lang_value == en_value:
                # Same as English - might be intentional (brand names) or missing translation
                if is_likely_untranslatable(en_value):
                    good_translations.append((en_key, lang_value))
                else:
                    identical_to_english.append((en_key, lang_value))
            elif is_suspicious_translation(en_value, lang_value, lang):
                suspicious_translations.append((en_key, en_value, lang_value))
            else:
                good_translations.append((en_key, lang_value))
        
        # Report findings
        total_keys = len(en_all)
        print(f"   📊 Translation Status:")
        print(f"      ✅ Good translations: {len(good_translations)} ({len(good_translations)/total_keys*100:.1f}%)")
        print(f"      🤖 Auto-generated (needs translation): {len(auto_prefixed)} ({len(auto_prefixed)/total_keys*100:.1f}%)")
        print(f"      🔄 Identical to English: {len(identical_to_english)} ({len(identical_to_english)/total_keys*100:.1f}%)")
        print(f"      ⚠️  Suspicious translations: {len(suspicious_translations)} ({len(suspicious_translations)/total_keys*100:.1f}%)")
        print(f"      ❌ Missing: {len(missing_translations)} ({len(missing_translations)/total_keys*100:.1f}%)")
        
        # Show examples of issues
        if auto_prefixed:
            print(f"\n   🤖 Sample auto-generated (priority for translation):")
            for key, value in auto_prefixed[:3]:
                clean_value = value.replace("[AUTO] ", "")
                print(f"      {key}: '{clean_value}'")
        
        if identical_to_english:
            print(f"\n   🔄 Sample identical to English (may need translation):")
            for key, value in identical_to_english[:3]:
                print(f"      {key}: '{value}'")
        
        if suspicious_translations:
            print(f"\n   ⚠️  Sample suspicious translations:")
            for key, en_val, lang_val in suspicious_translations[:3]:
                print(f"      {key}:")
                print(f"        EN: '{en_val}'")
                print(f"        {lang.upper()}: '{lang_val}'")
        
        print()

def is_likely_untranslatable(text: str) -> bool:
    """Check if text is likely meant to stay in English (brand names, technical terms)"""
    untranslatable_patterns = [
        r'^KAN-BUD',
        r'^OpenAI',
        r'^Anthropic',
        r'^PDF$',
        r'^DWG$',
        r'^IoT$',
        r'^AI$',
        r'^HVAC$',
        r'^ADA$',
        r'^GDPR$',
        r'^C[2-5]M?$',  # Paint codes like C2, C3, C4, C5M
        r'^\d+ft',  # Container sizes like 20ft, 40ft
        r'^HC$',  # High Cube
        r'^DD$',  # Double Door
    ]
    
    for pattern in untranslatable_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    return False

def is_suspicious_translation(en_text: str, translated_text: str, target_lang: str) -> bool:
    """Check if translation seems suspicious or incorrect"""
    
    # Check if translation is just English with different casing
    if en_text.lower() == translated_text.lower() and en_text != translated_text:
        return True
    
    # Check if translation contains obvious English words that should be translated
    english_words_should_translate = [
        'container', 'basic', 'standard', 'premium', 'system', 'analysis', 
        'configuration', 'installation', 'professional', 'advanced',
        'delivery', 'transport', 'office', 'equipment', 'security',
        'lighting', 'ventilation', 'electrical', 'plumbing'
    ]
    
    translated_lower = translated_text.lower()
    for word in english_words_should_translate:
        if word in translated_lower and len(translated_text) > len(word) + 2:
            # Word appears in translation and it's not just the word itself
            return True
    
    # Check for mixed language (contains both English and target language patterns)
    if target_lang == 'de':
        # German should have some German characteristics
        german_patterns = ['ung$', 'tion$', 'isch$', 'lich$', 'heit$', 'keit$']
        has_german = any(re.search(pattern, translated_text) for pattern in german_patterns)
        has_english = any(word in translated_lower for word in ['and', 'the', 'with', 'for'])
        if has_english and not has_german and len(translated_text.split()) > 2:
            return True
    
    elif target_lang == 'pl':
        # Polish should have Polish characteristics
        polish_chars = 'ąćęłńóśźż'
        has_polish_chars = any(char in translated_text.lower() for char in polish_chars)
        polish_endings = ['acja$', 'owanie$', 'ność$', 'owy$', 'owa$', 'owe$']
        has_polish_ending = any(re.search(pattern, translated_text) for pattern in polish_endings)
        has_english = any(word in translated_lower for word in ['and', 'the', 'with', 'for'])
        
        if has_english and not (has_polish_chars or has_polish_ending) and len(translated_text.split()) > 2:
            return True
    
    return False

def generate_translation_recommendations():
    """Generate recommendations for improving translations"""
    print("\n=== TRANSLATION IMPROVEMENT RECOMMENDATIONS ===\n")
    
    print("🎯 PRIORITY ACTIONS:")
    print("1. Translate all [AUTO] prefixed entries - these are just English text")
    print("2. Review identical-to-English entries - some may need proper translation")
    print("3. Check suspicious translations for accuracy")
    print("4. Fill in missing translations")
    
    print("\n📋 QUALITY CHECKLIST:")
    print("✓ Use native language sentence structure")
    print("✓ Translate technical terms appropriately for your market")
    print("✓ Keep UI terminology consistent across the application")
    print("✓ Preserve formatting placeholders like {error}")
    print("✓ Test translations in context to ensure they fit UI space")
    
    print("\n🔧 TECHNICAL TERMS GUIDANCE:")
    print("• Keep brand names (KAN-BUD, OpenAI) unchanged")
    print("• Keep file extensions (PDF, DWG) unchanged")
    print("• Keep technical standards (HVAC, ADA, GDPR) unchanged")
    print("• Translate descriptive terms (Basic, Standard, Premium)")
    print("• Adapt measurement units to local conventions where appropriate")

if __name__ == "__main__":
    analyze_translation_quality()
    generate_translation_recommendations()
