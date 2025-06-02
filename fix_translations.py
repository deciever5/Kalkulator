#!/usr/bin/env python3
"""
Translation Repair Script
Automatically fixes missing, auto-generated, and suspicious translations
"""

import json
import os
import time
from typing import Dict, List, Tuple
from utils.ai_translation_service import AITranslationService
from utils.translation_quality_analyzer import TranslationQualityAnalyzer

class TranslationRepairer:
    """Repairs translation issues automatically"""

    def __init__(self):
        self.ai_service = AITranslationService()
        self.analyzer = TranslationQualityAnalyzer()
        self.locales_dir = "locales"

    def load_json_file(self, filepath: str) -> Dict:
        """Load a JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return {}

    def save_json_file(self, filepath: str, data: Dict) -> bool:
        """Save data to JSON file with proper formatting"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
            return True
        except Exception as e:
            print(f"Error saving {filepath}: {e}")
            return False

    def set_nested_value(self, data: Dict, key_path: str, value: str):
        """Set nested value using dot notation"""
        keys = key_path.split('.')
        current = data

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value

    def get_nested_value(self, data: Dict, key_path: str):
        """Get nested value using dot notation"""
        keys = key_path.split('.')
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current

    def repair_language_translations(self, language: str) -> bool:
        """Repair translations for a specific language"""
        print(f"🔧 Repairing {language.upper()} translations...")

        # Load base Polish translations (configured base language)
        base_data = self.load_json_file(os.path.join(self.locales_dir, f"{self.analyzer.base_language}.json"))
        if not base_data:
            print(f"❌ Could not load base language ({self.analyzer.base_language}) translations")
            return False

        # Load target language
        lang_file = os.path.join(self.locales_dir, f"{language}.json")
        lang_data = self.load_json_file(lang_file)
        if not lang_data:
            print(f"❌ Could not load {language} translations")
            return False

        # Get flat key-value pairs
        base_translations = self.analyzer.get_all_keys_flat(base_data)

        # Analyze current quality
        analysis = self.analyzer.analyze_language_quality(language, base_translations)
        if "error" in analysis:
            print(f"❌ Analysis error: {analysis['error']}")
            return False

        repairs_made = 0

        # Fix missing translations
        if analysis['missing']:
            print(f"   📝 Fixing {len(analysis['missing'])} missing translations...")
            for key in analysis['missing']:
                base_value = base_translations.get(key)
                if base_value:
                    translated = self.ai_service._translate_text(base_value, language)
                    if translated and translated != base_value:
                        self.set_nested_value(lang_data, key, translated)
                        repairs_made += 1
                        time.sleep(0.1)  # Rate limiting

        # Fix auto/placeholder translations
        if analysis['auto_placeholder']:
            print(f"   🤖 Fixing {len(analysis['auto_placeholder'])} auto-generated translations...")
            for key, auto_value in analysis['auto_placeholder']:
                # Extract original text from [AUTO] or [TRANSLATE] prefixes
                original_text = auto_value.replace("[AUTO] ", "").replace("[TRANSLATE] ", "")
                translated = self.ai_service._translate_text(original_text, language)
                if translated and not translated.startswith("["):
                    self.set_nested_value(lang_data, key, translated)
                    repairs_made += 1
                    time.sleep(0.1)

        # Fix identical to base (if they shouldn't be identical)
        if analysis['identical_to_base']:
            print(f"   🔄 Reviewing {len(analysis['identical_to_base'])} identical translations...")
            for key, identical_value in analysis['identical_to_base']:
                # Skip if it's likely meant to be identical (brand names, technical terms)
                if self._should_translate(identical_value):
                    translated = self.ai_service._translate_text(identical_value, language)
                    if translated and translated != identical_value:
                        self.set_nested_value(lang_data, key, translated)
                        repairs_made += 1
                        time.sleep(0.1)

        # Fix suspicious translations
        if analysis['suspicious']:
            print(f"   ⚠️  Reviewing {len(analysis['suspicious'])} suspicious translations...")
            for key, suspicious_value in analysis['suspicious']:
                base_value = base_translations.get(key)
                if base_value and self._should_translate(base_value):
                    translated = self.ai_service._translate_text(base_value, language)
                    if translated and translated != base_value and translated != suspicious_value:
                        self.set_nested_value(lang_data, key, translated)
                        repairs_made += 1
                        time.sleep(0.1)

        # Save repaired translations
        if repairs_made > 0:
            if self.save_json_file(lang_file, lang_data):
                print(f"✅ {language.upper()}: Successfully repaired {repairs_made} translations")
                return True
            else:
                print(f"❌ {language.upper()}: Failed to save repaired translations")
                return False
        else:
            print(f"✅ {language.upper()}: No repairs needed")
            return True

    def _should_translate(self, text: str) -> bool:
        """Check if text should be translated (not a brand name or technical term)"""
        if not text:
            return False

        # Don't translate these terms
        keep_unchanged = [
            'KAN-BUD', 'OpenAI', 'GPT', 'API', 'PDF', 'DWG', 'HVAC', 'ADA', 
            'GDPR', 'ISO', 'EN', 'DIN', 'C2', 'C3', 'mm', 'cm', 'm', 'kg',
            'EUR', 'PLN', 'USD', 'HTML', 'CSS', 'JavaScript', 'Python'
        ]

        text_upper = text.upper()
        for term in keep_unchanged:
            if term.upper() in text_upper:
                return False

        # Don't translate very short text that might be codes
        if len(text) <= 3:
            return False

        return True

    def repair_all_languages(self) -> None:
        """Repair translations for all languages"""
        print("🔧 Starting comprehensive translation repair...\n")

        # Get languages that need repair based on quality analysis
        target_languages = ['cs', 'de', 'es', 'fi', 'fr', 'hu', 'it', 'nl', 'pl', 'sk', 'sv', 'uk']

        success_count = 0

        for language in target_languages:
            try:
                if self.repair_language_translations(language):
                    success_count += 1
                print()  # Add spacing between languages
            except Exception as e:
                print(f"❌ Error repairing {language}: {e}\n")

        print(f"🎉 Translation repair complete!")
        print(f"✅ Successfully repaired {success_count}/{len(target_languages)} languages")
        print("\n📋 Next steps:")
        print("1. Run 'python check_translation_quality.py' to verify improvements")
        print("2. Test the application to ensure translations display correctly")
        print("3. Review and refine any translations that need business context adjustments")

def main():
    """Main function to run translation repairs"""
    repairer = TranslationRepairer()
    repairer.repair_all_languages()

if __name__ == "__main__":
    main()