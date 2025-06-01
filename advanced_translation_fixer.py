
#!/usr/bin/env python3
"""
Advanced Translation Fixer
Uses Polish as base to fix all translation issues across languages
"""

import json
import os
import time
from typing import Dict, List, Tuple
from utils.ai_translation_service import AITranslationService

class AdvancedTranslationFixer:
    """Advanced translation fixer using Polish as base reference"""
    
    def __init__(self):
        self.ai_service = AITranslationService()
        self.locales_dir = "locales"
        self.base_language = "pl"  # Polish as base
        self.target_languages = ['cs', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'nl', 'sk', 'sv', 'uk']
    
    def load_json_file(self, filepath: str) -> Dict:
        """Load JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading {filepath}: {e}")
            return {}
    
    def save_json_file(self, filepath: str, data: Dict) -> bool:
        """Save JSON file with proper formatting"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
            return True
        except Exception as e:
            print(f"❌ Error saving {filepath}: {e}")
            return False
    
    def get_all_keys_flat(self, data: Dict, prefix: str = "") -> Dict[str, str]:
        """Get all keys from nested dict as flat key-value pairs"""
        result = {}
        
        if not isinstance(data, dict):
            return result
        
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                result.update(self.get_all_keys_flat(value, full_key))
            elif isinstance(value, str):
                result[full_key] = value
            # Skip non-string, non-dict values
        
        return result
    
    def set_nested_value(self, data: Dict, key_path: str, value: str):
        """Set nested value using dot notation"""
        keys = key_path.split('.')
        current = data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            elif not isinstance(current[key], dict):
                # If current value is not a dict, replace it with empty dict
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def is_placeholder_text(self, text: str) -> bool:
        """Check if text is a placeholder"""
        if not text:
            return False
        
        placeholder_indicators = [
            '[AUTO]', '[TRANSLATE]', '[TODO]', '[FIXME]',
            'placeholder_', 'temp_', 'auto_'
        ]
        
        return any(indicator in text for indicator in placeholder_indicators)
    
    def is_likely_english(self, text: str, target_language: str = None) -> bool:
        """Check if text is likely English (only relevant for non-English languages)"""
        if not text or len(text) < 3:
            return False
        
        # If target language is English, English words are expected and correct
        if target_language == 'en':
            return False
        
        english_indicators = [
            'container', 'basic', 'standard', 'premium', 'advanced',
            'configuration', 'installation', 'delivery', 'transport',
            'office', 'equipment', 'security', 'system', 'analysis'
        ]
        
        text_lower = text.lower()
        return any(word in text_lower for word in english_indicators)
    
    def should_translate(self, text: str) -> bool:
        """Check if text should be translated"""
        if not text:
            return False
        
        # Don't translate these terms
        keep_unchanged = [
            'KAN-BUD', 'OpenAI', 'GPT', 'API', 'PDF', 'DWG', 'HVAC',
            'ISO', 'EN', 'DIN', 'mm', 'cm', 'm', 'kg', 'EUR', 'PLN', 'USD'
        ]
        
        text_upper = text.upper()
        for term in keep_unchanged:
            if term in text_upper:
                return False
        
        # Don't translate very short text
        if len(text) <= 3:
            return False
        
        return True
    
    def fix_language_translations(self, language: str) -> bool:
        """Fix all translation issues for a specific language"""
        print(f"🔧 Fixing {language.upper()} translations...")
        
        # Load Polish base
        base_file = os.path.join(self.locales_dir, f"{self.base_language}.json")
        base_data = self.load_json_file(base_file)
        if not base_data:
            print(f"❌ Could not load Polish base translations")
            return False
        
        # Load target language
        lang_file = os.path.join(self.locales_dir, f"{language}.json")
        lang_data = self.load_json_file(lang_file)
        if not lang_data:
            print(f"❌ Could not load {language} translations")
            return False
        
        # Get flat translations
        base_translations = self.get_all_keys_flat(base_data)
        lang_translations = self.get_all_keys_flat(lang_data)
        
        fixes_made = 0
        
        # Fix missing translations
        missing_keys = []
        for key, polish_value in base_translations.items():
            if key not in lang_translations:
                missing_keys.append(key)
        
        if missing_keys:
            print(f"   📝 Fixing {len(missing_keys)} missing translations...")
            for key in missing_keys:
                try:
                    polish_value = base_translations[key]
                    if self.should_translate(polish_value):
                        translated = self.ai_service._translate_text(polish_value, language)
                        if translated and translated != polish_value:
                            self.set_nested_value(lang_data, key, translated)
                            fixes_made += 1
                            time.sleep(0.1)  # Rate limiting
                except Exception as e:
                    print(f"      ⚠️ Error fixing key '{key}': {e}")
                    continue
        
        # Fix placeholder translations
        placeholder_fixes = 0
        for key, target_value in lang_translations.items():
            try:
                if self.is_placeholder_text(target_value):
                    polish_value = base_translations.get(key)
                    if polish_value and self.should_translate(polish_value):
                        # Remove placeholder tags and translate the clean text
                        clean_text = target_value.replace("[AUTO] ", "").replace("[TRANSLATE] ", "")
                        if not clean_text:
                            clean_text = polish_value
                        
                        translated = self.ai_service._translate_text(clean_text, language)
                        if translated and not translated.startswith("["):
                            self.set_nested_value(lang_data, key, translated)
                            placeholder_fixes += 1
                            fixes_made += 1
                            time.sleep(0.1)
            except Exception as e:
                print(f"      ⚠️ Error fixing placeholder for key '{key}': {e}")
                continue
        
        if placeholder_fixes:
            print(f"   🏷️  Fixed {placeholder_fixes} placeholder translations")
        
        # Fix English translations (skip for English language)
        english_fixes = 0
        if language != 'en':  # Only check for English in non-English languages
            for key, target_value in lang_translations.items():
                if self.is_likely_english(target_value, language):
                    polish_value = base_translations.get(key)
                    if polish_value and self.should_translate(polish_value):
                        translated = self.ai_service._translate_text(polish_value, language)
                        if translated and translated != target_value and translated != polish_value:
                            self.set_nested_value(lang_data, key, translated)
                            english_fixes += 1
                            fixes_made += 1
                            time.sleep(0.1)
        
        if english_fixes:
            print(f"   🔤 Fixed {english_fixes} English translations")
        
        # Save fixes
        if fixes_made > 0:
            if self.save_json_file(lang_file, lang_data):
                print(f"✅ {language.upper()}: Successfully fixed {fixes_made} translations")
                return True
            else:
                print(f"❌ {language.upper()}: Failed to save fixes")
                return False
        else:
            print(f"✅ {language.upper()}: No fixes needed")
            return True
    
    def fix_all_languages(self):
        """Fix translations for all target languages"""
        print("🚀 ADVANCED TRANSLATION FIXER")
        print("Using Polish as base language reference")
        print("="*60)
        
        success_count = 0
        total_languages = len(self.target_languages)
        
        for language in self.target_languages:
            try:
                if self.fix_language_translations(language):
                    success_count += 1
                print()  # Add spacing
            except Exception as e:
                print(f"❌ Error fixing {language}: {e}\n")
        
        print("="*60)
        print(f"🎉 Translation fixing complete!")
        print(f"✅ Successfully fixed {success_count}/{total_languages} languages")
        
        if success_count < total_languages:
            print(f"⚠️  {total_languages - success_count} languages had issues")
        
        print("\n📋 Next steps:")
        print("1. Run 'python comprehensive_translation_checker.py' to verify fixes")
        print("2. Test the application with different languages")
        print("3. Review AI translations for business context accuracy")

def main():
    """Main function"""
    fixer = AdvancedTranslationFixer()
    fixer.fix_all_languages()

if __name__ == "__main__":
    main()
