
#!/usr/bin/env python3
"""
Suspicious Translation Analysis Script
Provides detailed analysis of all suspicious translations across languages
"""

import json
import os
from typing import Dict, List, Tuple
import re

class SuspiciousTranslationAnalyzer:
    def __init__(self):
        self.locales_dir = "locales"
        self.base_language = "en"
        
    def load_translation_file(self, language: str) -> Dict:
        """Load a specific translation file"""
        filepath = os.path.join(self.locales_dir, f"{language}.json")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading {filepath}: {e}")
            return {}
    
    def get_all_keys_flat(self, data: Dict, prefix: str = "") -> Dict[str, str]:
        """Get all keys from nested dict as flat key-value pairs"""
        result = {}
        
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                result.update(self.get_all_keys_flat(value, full_key))
            elif isinstance(value, str):
                result[full_key] = value
        
        return result
    
    def is_suspicious_translation(self, base_text: str, translated_text: str, target_lang: str) -> Tuple[bool, List[str]]:
        """Check if translation seems suspicious and return reasons"""
        if not base_text or not translated_text:
            return False, []
        
        reasons = []
        
        # Check if translation is just English with different casing
        if base_text.lower() == translated_text.lower() and base_text != translated_text:
            reasons.append("Case-only difference from English")
        
        # Check for obvious English words that should be translated
        english_words = [
            'container', 'basic', 'standard', 'premium', 'system', 'analysis',
            'configuration', 'installation', 'professional', 'advanced',
            'delivery', 'transport', 'office', 'equipment', 'security',
            'lighting', 'ventilation', 'electrical', 'plumbing', 'drawing',
            'technical', 'estimate', 'quote', 'comparison', 'visualization'
        ]
        
        translated_lower = translated_text.lower()
        found_english_words = []
        for word in english_words:
            if word in translated_lower and len(translated_text) > len(word) + 2:
                found_english_words.append(word)
        
        if found_english_words:
            reasons.append(f"Contains untranslated English words: {', '.join(found_english_words)}")
        
        # Language-specific checks
        if target_lang == 'de':
            # German should have some German characteristics
            german_patterns = ['ung$', 'tion$', 'isch$', 'lich$', 'heit$', 'keit$']
            has_german = any(re.search(pattern, translated_text) for pattern in german_patterns)
            has_english = any(word in translated_lower for word in ['and', 'the', 'with', 'for'])
            if has_english and not has_german and len(translated_text.split()) > 2:
                reasons.append("Contains English words without German language patterns")
        
        elif target_lang == 'pl':
            # Polish should have Polish characteristics
            polish_chars = 'ąćęłńóśźż'
            has_polish_chars = any(char in translated_text.lower() for char in polish_chars)
            polish_endings = ['acja$', 'owanie$', 'ność$', 'owy$', 'owa$', 'owe$']
            has_polish_ending = any(re.search(pattern, translated_text) for pattern in polish_endings)
            has_english = any(word in translated_lower for word in ['and', 'the', 'with', 'for'])
            
            if has_english and not (has_polish_chars or has_polish_ending) and len(translated_text.split()) > 2:
                reasons.append("Contains English words without Polish language patterns")
        
        elif target_lang == 'fr':
            # French specific checks
            has_english = any(word in translated_lower for word in ['and', 'the', 'with', 'for'])
            french_patterns = ['tion$', 'ment$', 'ique$', 'able$', 'ible$']
            has_french = any(re.search(pattern, translated_text) for pattern in french_patterns)
            if has_english and not has_french and len(translated_text.split()) > 2:
                reasons.append("Contains English words without French language patterns")
        
        # Check if translation is identical to English (excluding proper nouns)
        if translated_text == base_text and not self.is_likely_proper_noun(base_text):
            reasons.append("Identical to English (may need translation)")
        
        return len(reasons) > 0, reasons
    
    def is_likely_proper_noun(self, text: str) -> bool:
        """Check if text is likely a proper noun that shouldn't be translated"""
        proper_noun_patterns = [
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
            r'^C[2-5]M?$',  # Paint codes
            r'^\d+ft',  # Container sizes
            r'^HC$',  # High Cube
            r'^DD$',  # Double Door
        ]
        
        for pattern in proper_noun_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def analyze_suspicious_translations(self):
        """Analyze all suspicious translations across languages"""
        # Load base language
        base_data = self.load_translation_file(self.base_language)
        if not base_data:
            print(f"❌ Could not load base language ({self.base_language})")
            return
        
        base_translations = self.get_all_keys_flat(base_data)
        
        # Get all available languages
        available_languages = []
        for filename in os.listdir(self.locales_dir):
            if filename.endswith('.json'):
                lang = filename[:-5]  # Remove .json extension
                if lang != self.base_language:
                    available_languages.append(lang)
        
        available_languages.sort()
        
        print("🔍 SUSPICIOUS TRANSLATION DETAILED ANALYSIS")
        print("=" * 80)
        print()
        
        total_suspicious = 0
        
        for language in available_languages:
            lang_data = self.load_translation_file(language)
            if not lang_data:
                continue
            
            lang_translations = self.get_all_keys_flat(lang_data)
            
            suspicious_translations = []
            
            for key, base_value in base_translations.items():
                lang_value = lang_translations.get(key)
                
                if lang_value:
                    is_suspicious, reasons = self.is_suspicious_translation(base_value, lang_value, language)
                    if is_suspicious:
                        suspicious_translations.append((key, base_value, lang_value, reasons))
            
            if suspicious_translations:
                print(f"🚨 {language.upper()} - {len(suspicious_translations)} suspicious translations:")
                print("-" * 60)
                
                for key, en_text, lang_text, reasons in suspicious_translations:
                    print(f"📍 Key: {key}")
                    print(f"   EN: '{en_text}'")
                    print(f"   {language.upper()}: '{lang_text}'")
                    print(f"   ⚠️  Issues: {'; '.join(reasons)}")
                    print()
                
                total_suspicious += len(suspicious_translations)
            else:
                print(f"✅ {language.upper()} - No suspicious translations found")
            
            print()
        
        print("=" * 80)
        print(f"📊 SUMMARY: Found {total_suspicious} suspicious translations across all languages")
        
        if total_suspicious > 0:
            print("\n🎯 RECOMMENDED ACTIONS:")
            print("1. Review each suspicious translation for accuracy")
            print("2. Replace English words with proper target language translations")
            print("3. Fix case-only differences")
            print("4. Ensure translations follow target language grammar")
            print("5. Test translations in context to ensure they make sense")
        else:
            print("\n🎉 Great! No suspicious translations detected!")

def main():
    analyzer = SuspiciousTranslationAnalyzer()
    analyzer.analyze_suspicious_translations()

if __name__ == "__main__":
    main()
