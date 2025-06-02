
#!/usr/bin/env python3
"""
Mixed Language Translation Fixer
Detects and fixes translations that contain mixed languages (e.g., Polish words in Ukrainian text)
Translates complete sentences from original Polish to maintain context and meaning
"""

import json
import os
import re
import time
from typing import Dict, List, Tuple, Set
from utils.ai_translation_service import AITranslationService

class MixedLanguageTranslationFixer:
    def __init__(self):
        self.ai_service = AITranslationService()
        self.locales_dir = "locales"
        self.base_language = "pl"
        self.skip_languages = {"pl", "en"}  # Skip Polish base and English
        
        # Common Polish words that should not appear in other languages
        self.polish_indicators = {
            'systemów', 'sprzętu', 'montażu', 'dostawa', 'tylko', 'serwerownia',
            'bezpieczeństwo', 'zaawansowane', 'podstawowe', 'standardowe',
            'rozszerzone', 'maksymalne', 'przemysłowe', 'kontenerowa',
            'standardowa', 'wzmocnione', 'okienne', 'czujniki', 'syrena',
            'felügyelet', 'wibracji', 'biometria', 'central', 'systemy',
            'gazowe', 'panic', 'room', 'okładziny', 'blacha', 'izolacja',
            'termiczna', 'akustyczna', 'przeciwpożarowa', 'standardowej',
            'wentylacja', 'klimatyzacja', 'ogrzewanie', 'instalacja',
            'elektryczna', 'hydrauliczna', 'sanitarna', 'telekomunikacyjna'
        }
        
        # Language patterns to help detect mixed content
        self.language_patterns = {
            'uk': {
                'chars': 'іїєґ',
                'words': {'без', 'та', 'або', 'для', 'від', 'до', 'на', 'в', 'з'}
            },
            'cs': {
                'chars': 'ěščřžýáíéúůď',
                'words': {'bez', 'se', 'na', 'do', 'za', 'od', 'pro', 'při'}
            },
            'sk': {
                'chars': 'ľščťžýáíéúôäň',
                'words': {'bez', 'sa', 'na', 'do', 'za', 'od', 'pre', 'pri'}
            },
            'hu': {
                'chars': 'őűáéíóúöü',
                'words': {'és', 'vagy', 'nem', 'a', 'az', 'el', 'be', 'ki'}
            },
            'de': {
                'chars': 'äöüß',
                'words': {'und', 'oder', 'nicht', 'mit', 'ohne', 'für', 'von', 'zu'}
            },
            'fr': {
                'chars': 'àáâäçéèêëïîôùûüÿñæœ',
                'words': {'et', 'ou', 'non', 'avec', 'sans', 'pour', 'de', 'à'}
            },
            'es': {
                'chars': 'ñáéíóúü',
                'words': {'y', 'o', 'no', 'con', 'sin', 'para', 'de', 'a'}
            },
            'it': {
                'chars': 'àáèéìíîòóùú',
                'words': {'e', 'o', 'non', 'con', 'senza', 'per', 'di', 'a'}
            },
            'nl': {
                'chars': 'áéíóúàèëïöü',
                'words': {'en', 'of', 'niet', 'met', 'zonder', 'voor', 'van', 'aan'}
            },
            'sv': {
                'chars': 'åäöé',
                'words': {'och', 'eller', 'inte', 'med', 'utan', 'för', 'av', 'till'}
            },
            'fi': {
                'chars': 'äöåé',
                'words': {'ja', 'tai', 'ei', 'kanssa', 'ilman', 'varten', 'ja', 'on'}
            }
        }

    def load_json_file(self, filepath: str) -> Dict:
        """Load JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return {}

    def save_json_file(self, filepath: str, data: Dict) -> bool:
        """Save JSON file with proper formatting"""
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
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def contains_polish_words(self, text: str) -> List[str]:
        """Check if text contains Polish words"""
        if not text:
            return []
        
        text_lower = text.lower()
        found_polish = []
        
        for polish_word in self.polish_indicators:
            if polish_word in text_lower:
                found_polish.append(polish_word)
        
        return found_polish

    def is_mixed_language(self, text: str, target_lang: str) -> bool:
        """Check if text contains mixed languages"""
        if not text or target_lang not in self.language_patterns:
            return False
        
        # Check for Polish words
        polish_words = self.contains_polish_words(text)
        if polish_words:
            return True
        
        # Check for target language characteristics
        lang_pattern = self.language_patterns[target_lang]
        
        # Count target language characteristics
        target_chars = sum(1 for char in text.lower() if char in lang_pattern['chars'])
        target_words = sum(1 for word in lang_pattern['words'] if word in text.lower())
        
        # Count Polish characteristics (basic check)
        polish_patterns = ['ąćęłńóśźż', 'sz', 'cz', 'rz', 'dż']
        polish_score = 0
        for pattern in polish_patterns:
            if isinstance(pattern, str) and len(pattern) == 1:
                polish_score += sum(1 for char in text.lower() if char in pattern)
            else:
                polish_score += len(re.findall(pattern, text.lower()))
        
        # If we have Polish characteristics but few target language characteristics, it's mixed
        return polish_score > 0 and (target_chars + target_words) < polish_score

    def detect_mixed_translations(self, lang: str) -> Dict[str, Tuple[str, List[str]]]:
        """Detect translations with mixed languages"""
        lang_file = os.path.join(self.locales_dir, f"{lang}.json")
        lang_data = self.load_json_file(lang_file)
        
        if not lang_data:
            return {}
        
        lang_translations = self.get_all_keys_flat(lang_data)
        mixed_translations = {}
        
        for key, value in lang_translations.items():
            if self.is_mixed_language(value, lang):
                polish_words = self.contains_polish_words(value)
                mixed_translations[key] = (value, polish_words)
        
        return mixed_translations

    def translate_complete_sentence(self, polish_text: str, target_lang: str) -> str:
        """Translate complete sentence from Polish to target language"""
        if not polish_text or not polish_text.strip():
            return polish_text
        
        try:
            # Use AI service to translate the complete sentence
            translated = self.ai_service._translate_text(polish_text, target_lang)
            if translated and translated.strip():
                return translated
        except Exception as e:
            print(f"   ⚠️ Translation error: {e}")
        
        return polish_text

    def fix_language_translations(self, lang: str) -> bool:
        """Fix mixed language translations for a specific language"""
        print(f"🔍 Analyzing {lang.upper()} for mixed language issues...")
        
        # Load Polish base
        pl_file = os.path.join(self.locales_dir, f"{self.base_language}.json")
        pl_data = self.load_json_file(pl_file)
        if not pl_data:
            print(f"   ❌ Could not load Polish base translations")
            return False
        
        # Load target language
        lang_file = os.path.join(self.locales_dir, f"{lang}.json")
        lang_data = self.load_json_file(lang_file)
        if not lang_data:
            print(f"   ❌ Could not load {lang} translations")
            return False
        
        # Get all translations
        pl_translations = self.get_all_keys_flat(pl_data)
        
        # Detect mixed translations
        mixed_translations = self.detect_mixed_translations(lang)
        
        if not mixed_translations:
            print(f"   ✅ No mixed language issues found in {lang.upper()}")
            return True
        
        print(f"   🚨 Found {len(mixed_translations)} mixed language translations in {lang.upper()}")
        
        # Show examples
        for i, (key, (mixed_text, polish_words)) in enumerate(list(mixed_translations.items())[:3]):
            print(f"      Example {i+1}: {key}")
            print(f"         Mixed: '{mixed_text}'")
            print(f"         Polish words: {', '.join(polish_words)}")
        
        # Fix translations by translating complete Polish sentences
        fixed_count = 0
        for key, (mixed_text, polish_words) in mixed_translations.items():
            if key in pl_translations:
                original_polish = pl_translations[key]
                print(f"   🔄 Fixing: {key}")
                print(f"      Original PL: '{original_polish}'")
                print(f"      Mixed {lang.upper()}: '{mixed_text}'")
                
                # Translate complete sentence from Polish
                new_translation = self.translate_complete_sentence(original_polish, lang)
                
                if new_translation and new_translation != mixed_text:
                    self.set_nested_value(lang_data, key, new_translation)
                    print(f"      New {lang.upper()}: '{new_translation}'")
                    fixed_count += 1
                else:
                    print(f"      ⚠️ Translation failed or unchanged")
                
                # Rate limiting
                time.sleep(0.2)
        
        # Save updated translations
        if fixed_count > 0:
            if self.save_json_file(lang_file, lang_data):
                print(f"   ✅ Fixed {fixed_count} mixed language translations in {lang.upper()}")
                return True
            else:
                print(f"   ❌ Failed to save fixed translations for {lang.upper()}")
                return False
        else:
            print(f"   ⚠️ No translations were successfully fixed for {lang.upper()}")
            return True

    def fix_all_mixed_translations(self):
        """Fix mixed language translations for all languages"""
        print("🌐 MIXED LANGUAGE TRANSLATION FIXER")
        print("Detecting and fixing translations with mixed Polish/target language content")
        print("="*70)
        
        # Get all available languages except base and English
        available_languages = []
        for filename in os.listdir(self.locales_dir):
            if filename.endswith('.json'):
                lang = filename[:-5]
                if lang not in self.skip_languages:
                    available_languages.append(lang)
        
        available_languages.sort()
        
        if not available_languages:
            print("❌ No target languages found to process")
            return
        
        print(f"📋 Processing languages: {', '.join(lang.upper() for lang in available_languages)}")
        print()
        
        success_count = 0
        total_fixed = 0
        
        for lang in available_languages:
            try:
                if self.fix_language_translations(lang):
                    success_count += 1
                print()  # Add spacing
            except Exception as e:
                print(f"   ❌ Error processing {lang.upper()}: {e}")
                print()
        
        print("="*70)
        print(f"🎉 Mixed language translation fixing complete!")
        print(f"✅ Successfully processed {success_count}/{len(available_languages)} languages")
        print()
        print("📋 Next steps:")
        print("1. Test the application to verify translations display correctly")
        print("2. Run translation quality check to verify improvements")
        print("3. Review any remaining translation issues manually")

def main():
    fixer = MixedLanguageTranslationFixer()
    fixer.fix_all_mixed_translations()

if __name__ == "__main__":
    main()
