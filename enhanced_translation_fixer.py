
#!/usr/bin/env python3
"""
Enhanced Translation Fixer
1. Copies missing keys from Polish (base language)
2. Translates them to target languages
3. Fixes existing bad translations
"""

import json
import os
import time
from typing import Dict, List, Tuple, Set
from utils.ai_translation_service import AITranslationService

class EnhancedTranslationFixer:
    def __init__(self):
        self.locales_dir = "locales"
        self.base_language = "pl"  # Polish as base
        self.target_languages = ['en', 'de', 'cs', 'sk', 'hu', 'nl', 'fr', 'es', 'it', 'sv', 'fi', 'uk']
        self.ai_service = AITranslationService()
    
    def load_json_file(self, filepath: str) -> Dict:
        """Load a JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return {}
    
    def save_json_file(self, filepath: str, data: Dict) -> bool:
        """Save data to JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
            return True
        except Exception as e:
            print(f"Error saving {filepath}: {e}")
            return False
    
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
    
    def set_nested_value(self, data: Dict, key_path: str, value: str):
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
    
    def copy_missing_structure(self, source_data: Dict, target_data: Dict, source_translations: Dict[str, str]):
        """Copy missing nested structure from source to target"""
        keys_added = 0
        
        for key_path, polish_value in source_translations.items():
            # Check if this key exists in target
            keys = key_path.split('.')
            current = target_data
            missing = False
            
            for key in keys:
                if key not in current:
                    missing = True
                    break
                if isinstance(current[key], dict):
                    current = current[key]
                else:
                    # Found the value, not missing
                    break
            
            if missing:
                # Copy the Polish value as placeholder
                self.set_nested_value(target_data, key_path, polish_value)
                keys_added += 1
        
        return keys_added
    
    def is_likely_english(self, text: str, target_language: str = None) -> bool:
        """Check if text is likely in English"""
        if not text or not isinstance(text, str):
            return False
        
        # Skip if target language is English
        if target_language == 'en':
            return False
        
        # Common English words that shouldn't appear in other languages
        english_indicators = [
            'the', 'and', 'for', 'with', 'from', 'system', 'basic', 'standard',
            'configuration', 'container', 'analysis', 'quote', 'estimate',
            'professional', 'technical', 'drawing', 'inquiry', 'project',
            'details', 'requirements', 'specifications', 'electrical',
            'mechanical', 'installation', 'delivery', 'transport'
        ]
        
        text_lower = text.lower()
        return any(word in text_lower for word in english_indicators)
    
    def is_placeholder_text(self, text: str) -> bool:
        """Check if text is placeholder/auto-generated"""
        if not text:
            return False
        
        placeholder_indicators = [
            '[AUTO]', '[TRANSLATE]', 'PLACEHOLDER', 'TODO',
            'FIXME', '{{', '}}', '%{', '}%'
        ]
        
        return any(indicator in text for indicator in placeholder_indicators)
    
    def is_polish_text(self, text: str) -> bool:
        """Check if text appears to be Polish"""
        if not text:
            return False
        
        # Polish specific characters
        polish_chars = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż']
        
        # Polish common words
        polish_words = [
            'bez', 'dla', 'lub', 'oraz', 'przez', 'system', 'podstawowy',
            'standardowy', 'konfiguracja', 'kontener', 'analiza', 'wycena',
            'profesjonalny', 'techniczny', 'rysunek', 'zapytanie', 'projekt',
            'szczegóły', 'wymagania', 'specyfikacje', 'elektryczny',
            'mechaniczny', 'instalacja', 'dostawa', 'transport'
        ]
        
        text_lower = text.lower()
        has_polish_chars = any(char in text_lower for char in polish_chars)
        has_polish_words = any(word in text_lower for word in polish_words)
        
        return has_polish_chars or has_polish_words
    
    def fix_language_translations(self, language: str) -> bool:
        """Fix translations for a specific language"""
        print(f"\n🔧 Fixing {language.upper()} translations...")
        
        # Load base Polish translations
        base_file = os.path.join(self.locales_dir, f"{self.base_language}.json")
        base_data = self.load_json_file(base_file)
        if not base_data:
            print(f"❌ Could not load base language file: {base_file}")
            return False
        
        # Load target language file
        lang_file = os.path.join(self.locales_dir, f"{language}.json")
        lang_data = self.load_json_file(lang_file)
        if not lang_data:
            print(f"❌ Could not load target language file: {lang_file}")
            return False
        
        # Get flat representations for easier comparison
        base_translations = self.get_all_keys_flat(base_data)
        lang_translations = self.get_all_keys_flat(lang_data)
        
        print(f"   📊 Base has {len(base_translations)} keys, target has {len(lang_translations)} keys")
        
        fixes_made = 0
        
        # Step 1: Copy missing keys from Polish
        missing_keys = []
        for key in base_translations.keys():
            if key not in lang_translations:
                missing_keys.append(key)
        
        if missing_keys:
            print(f"   📝 Copying {len(missing_keys)} missing keys from Polish...")
            keys_copied = self.copy_missing_structure(base_data, lang_data, base_translations)
            print(f"   ✅ Copied {keys_copied} missing keys")
            fixes_made += keys_copied
        
        # Step 2: Translate copied Polish text and fix bad translations
        lang_translations_updated = self.get_all_keys_flat(lang_data)
        translations_needed = []
        
        for key, value in lang_translations_updated.items():
            polish_value = base_translations.get(key)
            
            if polish_value and (
                self.is_polish_text(value) or  # Polish text in non-Polish language
                self.is_likely_english(value, language) or  # English in non-English language
                self.is_placeholder_text(value) or  # Placeholder text
                value == polish_value  # Identical to Polish (not translated)
            ):
                translations_needed.append((key, polish_value))
        
        if translations_needed:
            print(f"   🤖 Translating {len(translations_needed)} texts...")
            
            # Translate in batches
            batch_size = 20
            translated_count = 0
            
            for i in range(0, len(translations_needed), batch_size):
                batch = translations_needed[i:i+batch_size]
                
                for key, polish_text in batch:
                    if translated_text := self.ai_service._translate_text(polish_text, language):
                        if translated_text != polish_text and not self.is_polish_text(translated_text):
                            self.set_nested_value(lang_data, key, translated_text)
                            translated_count += 1
                            fixes_made += 1
                    
                    # Rate limiting
                    time.sleep(0.1)
                
                if i + batch_size < len(translations_needed):
                    print(f"   ⏳ Translated {min(i + batch_size, len(translations_needed))}/{len(translations_needed)}...")
                    time.sleep(1)  # Longer pause between batches
            
            print(f"   ✅ Translated {translated_count} texts")
        
        # Step 3: Save fixes
        if fixes_made > 0:
            if self.save_json_file(lang_file, lang_data):
                print(f"✅ {language.upper()}: Successfully applied {fixes_made} fixes")
                return True
            else:
                print(f"❌ {language.upper()}: Failed to save fixes")
                return False
        else:
            print(f"✅ {language.upper()}: No fixes needed")
            return True
    
    def fix_all_languages(self):
        """Fix translations for all target languages"""
        print("🚀 ENHANCED TRANSLATION FIXER")
        print("Using Polish as base language reference")
        print("Phase 1: Copy missing keys from Polish")
        print("Phase 2: Translate Polish text to target languages")
        print("Phase 3: Fix bad/placeholder translations")
        print("="*60)
        
        success_count = 0
        total_languages = len(self.target_languages)
        
        for language in self.target_languages:
            try:
                if self.fix_language_translations(language):
                    success_count += 1
            except Exception as e:
                print(f"❌ Error fixing {language}: {e}")
        
        print(f"\n🎉 COMPLETED!")
        print(f"✅ Successfully fixed: {success_count}/{total_languages} languages")
        
        if success_count < total_languages:
            print(f"⚠️  Failed: {total_languages - success_count} languages")
        
        print("\n📝 Next steps:")
        print("1. Review the translations for accuracy")
        print("2. Test the application with different languages")
        print("3. Run the translation quality checker")

def main():
    """Main function"""
    if len(os.sys.argv) > 1 and os.sys.argv[1] == '--single':
        # Fix single language
        if len(os.sys.argv) > 2:
            language = os.sys.argv[2]
            fixer = EnhancedTranslationFixer()
            fixer.fix_language_translations(language)
        else:
            print("Usage: python enhanced_translation_fixer.py --single <language_code>")
    else:
        # Fix all languages
        fixer = EnhancedTranslationFixer()
        fixer.fix_all_languages()

if __name__ == "__main__":
    main()
