"""
Smart Translation Validator
Understands when translations should be identical and when they need fixing
"""

import json
import os
import re
from typing import Dict, List, Set, Tuple

class SmartTranslationValidator:
    def __init__(self):
        self.locales_dir = "locales"
        self.base_language = "pl"  # Polish as base

        # Terms that should remain unchanged across languages
        self.universal_terms = {
            'KAN-BUD', 'OpenAI', 'GPT', 'API', 'PDF', 'DWG', 'HVAC',
            'ISO', 'EN', 'DIN', 'ADA', 'GDPR', 'IoT', 'AI', 'USB',
            'WiFi', 'Bluetooth', 'LED', 'LCD', 'GPS', 'QR', 'URL'
        }

        # Measurement units that stay the same
        self.units = {
            'mm', 'cm', 'm', 'km', 'kg', 'g', 'ton', 'l', 'ml',
            'EUR', 'PLN', 'USD', 'GBP', '°C', '°F', 'kW', 'V', 'A'
        }

        # Technical terms by domain that might be acceptable in English
        self.technical_terms = {
            'container_types': {'HC', 'DD', 'OT', 'FR', 'RF'},
            'standards': {'C2M', 'C3M', 'C4M', 'C5M'},
            'file_formats': {'DWG', 'PDF', 'CAD', 'BIM'},
            'systems': {'HVAC', 'IoT', 'LED'}
        }

    def load_json_file(self, filepath: str) -> Dict:
        """Load JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return {}

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

        return result

    def should_remain_unchanged(self, text: str) -> bool:
        """Check if text should remain unchanged across languages"""
        if not text:
            return False

        text_upper = text.upper()
        text_clean = text.strip()

        # Check universal terms
        for term in self.universal_terms:
            if term.upper() in text_upper:
                return True

        # Check units
        for unit in self.units:
            if unit in text_clean:
                return True

        # Check technical terms
        for category, terms in self.technical_terms.items():
            for term in terms:
                if term in text_upper:
                    return True

        # Check if it's a number with units
        if re.match(r'^\d+\s*(mm|cm|m|kg|EUR|PLN|USD)$', text_clean):
            return True

        # Check if it's a model number or code
        if re.match(r'^[A-Z0-9-]+$', text_clean) and len(text_clean) <= 10:
            return True

        return False

    def is_good_translation(self, source_text: str, target_text: str, target_lang: str) -> Tuple[bool, List[str]]:
        """Determine if a translation is good, considering context"""
        issues = []

        # If target language is English, English words are expected
        if target_lang == 'en':
            # For English, we mainly check if it's not placeholder text
            if target_text.startswith('[AUTO]') or target_text.startswith('[TRANSLATE]'):
                issues.append("Contains placeholder text")
            return len(issues) == 0, issues

        # Check if text should remain unchanged
        if self.should_remain_unchanged(source_text):
            if source_text == target_text:
                return True, []  # Correctly unchanged
            else:
                issues.append(f"Technical term unnecessarily translated")

        # Check for placeholder text
        if target_text.startswith('[AUTO]') or target_text.startswith('[TRANSLATE]'):
            issues.append("Contains placeholder text")

        # Check if identical to source when it should be translated
        if source_text == target_text and not self.should_remain_unchanged(source_text):
            # Only flag as issue if it's a translatable term
            if len(source_text.split()) > 1 or source_text.lower() in [
                'container', 'basic', 'standard', 'premium', 'configuration',
                'installation', 'delivery', 'office', 'equipment'
            ]:
                issues.append("Identical to source (may need translation)")

        return len(issues) == 0, issues

    def validate_language_translations(self, language: str) -> Dict:
        """Validate translations for a specific language"""
        print(f"🔍 Validating {language.upper()} translations...")

        # Load Polish base
        base_file = os.path.join(self.locales_dir, f"{self.base_language}.json")
        base_data = self.load_json_file(base_file)
        if not base_data:
            return {"error": "Could not load Polish base translations"}

        # Load target language
        lang_file = os.path.join(self.locales_dir, f"{language}.json")
        lang_data = self.load_json_file(lang_file)
        if not lang_data:
            return {"error": f"Could not load {language} translations"}

        # Get flat translations
        base_translations = self.get_all_keys_flat(base_data)
        lang_translations = self.get_all_keys_flat(lang_data)

        # Categorize translations
        good_translations = []
        needs_translation = []
        needs_review = []
        missing = []

        for key, base_value in base_translations.items():
            target_value = lang_translations.get(key)

            if target_value is None:
                missing.append(key)
            else:
                is_good, issues = self.is_good_translation(base_value, target_value, language)

                if is_good:
                    good_translations.append(key)
                elif "placeholder text" in str(issues):
                    needs_translation.append((key, target_value, issues))
                else:
                    needs_review.append((key, base_value, target_value, issues))

        total_keys = len(base_translations)

        return {
            "language": language,
            "total_keys": total_keys,
            "good_count": len(good_translations),
            "needs_translation_count": len(needs_translation),
            "needs_review_count": len(needs_review),
            "missing_count": len(missing),
            "good_translations": good_translations,
            "needs_translation": needs_translation,
            "needs_review": needs_review,
            "missing": missing,
            "quality_score": (len(good_translations) / total_keys * 100) if total_keys > 0 else 0
        }

    def validate_all_languages(self):
        """Validate all language translations"""
        print("🎯 SMART TRANSLATION VALIDATION")
        print("Understanding context and technical terms")
        print("="*60)

        target_languages = ['en', 'de', 'cs', 'sk', 'hu', 'nl', 'fr', 'es', 'it', 'sv', 'fi', 'uk']

        results = {}

        for lang in target_languages:
            try:
                result = self.validate_language_translations(lang)
                if "error" not in result:
                    results[lang] = result

                    print(f"\n📊 {lang.upper()} Quality Report:")
                    print(f"   ✅ Good translations: {result['good_count']} ({result['quality_score']:.1f}%)")
                    print(f"   🔧 Needs translation: {result['needs_translation_count']}")
                    print(f"   👀 Needs review: {result['needs_review_count']}")
                    print(f"   ❌ Missing: {result['missing_count']}")

                    # Show examples of what needs attention
                    if result['needs_translation']:
                        print(f"   📝 Example needs translation:")
                        for key, value, issues in result['needs_translation'][:3]:
                            clean_value = value.replace('[AUTO] ', '').replace('[TRANSLATE] ', '')
                            print(f"      {key}: '{clean_value}'")

                    if result['needs_review']:
                        print(f"   🔍 Example needs review:")
                        for key, source, target, issues in result['needs_review'][:3]:
                            print(f"      {key}: '{source}' → '{target}' ({', '.join(issues)})")

            except Exception as e:
                print(f"❌ Error validating {lang}: {e}")

        # Overall summary
        print("\n" + "="*60)
        print("📈 OVERALL QUALITY SUMMARY")

        if results:
            avg_quality = sum(r['quality_score'] for r in results.values()) / len(results)
            total_needs_work = sum(r['needs_translation_count'] + r['needs_review_count'] + r['missing_count'] 
                                 for r in results.values())

            print(f"Average quality score: {avg_quality:.1f}%")
            print(f"Total items needing attention: {total_needs_work}")

            # Best and worst performing languages
            best_lang = max(results.keys(), key=lambda x: results[x]['quality_score'])
            worst_lang = min(results.keys(), key=lambda x: results[x]['quality_score'])

            print(f"Best: {best_lang.upper()} ({results[best_lang]['quality_score']:.1f}%)")
            print(f"Needs most work: {worst_lang.upper()} ({results[worst_lang]['quality_score']:.1f}%)")

        return results

def main():
    validator = SmartTranslationValidator()
    validator.validate_all_languages()

if __name__ == "__main__":
    main()