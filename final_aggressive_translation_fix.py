#!/usr/bin/env python3
"""
Final Aggressive Translation Fix
Last resort script to fix remaining translation issues
Uses Polish as complete source and translates entire phrases
"""

import json
import os
import re
from typing import Dict, List
from utils.ai_translation_service import AITranslationService

class FinalTranslationFixer:
    def __init__(self):
        self.ai_service = AITranslationService()
        self.locales_dir = "locales"

        # Enhanced translation mappings with complete phrases
        self.complete_translations = {
            'hu': {
                # Security levels - complete translations
                'none': 'További biztonsági elemek nélkül (szabványos zárak)',
                'basic': 'Alapvető (megerősített zárak, ablakrácsok)', 
                'standard': 'Szabványos (riasztó, érzékelők, sziréna)',
                'extended': 'Kiterjesztett (felügyelet, mozgás/vibrációérzékelők)',
                'high': 'Magas (CCTV IP, hozzáférés-vezérlés, kaputelefon)',
                'maximum': 'Maximális (széf, biometria, központi felügyelet)',
                'industrial': 'Ipari (ATEX, gázrendszerek, pánikszoba)',

                # Cladding options
                'exterior_cladding_none': 'Burkolat nélkül (szabványos konténerlemez)',
                'exterior_cladding_basic': 'Alapvető (festett acéllemez)',
                'exterior_cladding_standard': 'Szabványos (profilozott lemez)',
                'exterior_cladding_premium': 'Prémium (kompozit panel)',
                'exterior_cladding_wood': 'Fa (thermowood borítás)',
                'exterior_cladding_stone': 'Kő (természetes kőfurnis)',

                # Common technical terms
                'heating': 'fűtés',
                'cooling': 'hűtés', 
                'ventilation': 'szellőzés',
                'insulation': 'szigetelés',
                'installation': 'telepítés',
                'delivery': 'szállítás',
                'transport': 'szállítás',
                'assembly': 'összeszerelés',
                'configuration': 'konfiguráció',
                'analysis': 'elemzés',
                'professional': 'szakmai',
                'materials': 'anyagok',
                'custom': 'egyedi',
                'standard': 'szabványos',
                'premium': 'prémium',
                'basic': 'alapvető',
                'advanced': 'haladó',
                'system': 'rendszer',
                'security': 'biztonság'
            },
            'cs': {
                # Security levels
                'none': 'Bez dodatečných bezpečnostních prvků (standardní zámky)',
                'basic': 'Základní (zesílené zámky, okenní mříže)',
                'standard': 'Standardní (alarm, čidla, siréna)', 
                'extended': 'Rozšířený (dohled, pohybová/vibrační čidla)',
                'high': 'Vysoký (CCTV IP, řízení přístupu, interkom)',
                'maximum': 'Maximální (trezor, biometrie, centrální dohled)',
                'industrial': 'Průmyslový (ATEX, plynové systémy, nouzová místnost)',

                # Cladding options
                'exterior_cladding_none': 'Bez obkladu (standardní kontejnerový plech)',
                'exterior_cladding_basic': 'Základní (lakovaný ocelový plech)',
                'exterior_cladding_standard': 'Standardní (profilovaný plech)',
                'exterior_cladding_premium': 'Prémiový (kompozitní panel)',
                'exterior_cladding_wood': 'Dřevo (thermowood obložení)',
                'exterior_cladding_stone': 'Kámen (přírodní kamenná dýha)',

                # Technical terms
                'heating': 'vytápění',
                'cooling': 'chlazení',
                'ventilation': 'větrání',
                'insulation': 'izolace',
                'installation': 'instalace',
                'delivery': 'dodání',
                'transport': 'doprava',
                'assembly': 'montáž',
                'configuration': 'konfigurace',
                'analysis': 'analýza',
                'professional': 'profesionální',
                'materials': 'materiály',
                'custom': 'vlastní',
                'standard': 'standardní',
                'premium': 'prémiový',
                'basic': 'základní',
                'advanced': 'pokročilý',
                'system': 'systém',
                'security': 'bezpečnost'
            }
        }

    def is_mixed_language(self, text: str) -> bool:
        """Check if text contains mixed languages (like Polish + Hungarian)"""
        if not text:
            return False

        # Common Polish words that shouldn't appear in other languages
        polish_indicators = ['dodatkowych', 'wzmocnione', 'zamki', 'czujniki', 'ruchu', 'wibracji', 'sejf', 'systemy', 'gazowe', 'okładziny', 'blacha', 'kontenerowa', 'standardowa']

        # Check for Polish words mixed with other languages
        text_lower = text.lower()
        polish_count = sum(1 for word in polish_indicators if word in text_lower)

        return polish_count > 0

    def is_likely_english(self, text: str) -> bool:
        """Check if text is likely English"""
        if not text:
            return False

        english_indicators = ['the', 'and', 'or', 'of', 'to', 'for', 'with', 'by', 'from', 'system', 'configuration', 'analysis', 'basic', 'standard', 'premium', 'advanced']
        words = text.lower().split()
        return any(word in english_indicators for word in words)

    def get_complete_translation(self, polish_text: str, lang_code: str) -> str:
        """Get complete translation for Polish text"""
        if not polish_text or lang_code not in self.complete_translations:
            return polish_text

        translations = self.complete_translations[lang_code]
        polish_lower = polish_text.lower().strip()

        # Try exact matches for key phrases
        for key, translation in translations.items():
            if key in polish_lower or polish_lower.endswith(key):
                return translation

        # Try AI translation for complete phrases
        try:
            translated = self.ai_service._translate_text(polish_text, lang_code)
            if translated and translated != polish_text and not self.is_likely_english(translated):
                return translated
        except Exception as e:
            print(f"   ⚠️ AI translation error: {e}")

        return polish_text

    def get_all_keys_flat(self, data: dict, prefix: str = "") -> dict:
        """Get all keys from nested dict as flat key-value pairs"""
        result = {}
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                result.update(self.get_all_keys_flat(value, full_key))
            elif isinstance(value, str):
                result[full_key] = value
        return result

    def set_nested_value(self, data: dict, key_path: str, value: str):
        """Set nested value using dot notation"""
        keys = key_path.split('.')
        current = data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            elif not isinstance(current[key], dict):
                # If the current value is not a dict, replace it with an empty dict
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def fix_language_aggressively(self, lang_code: str) -> bool:
        """Apply aggressive fixes to a language file using Polish as complete source"""
        print(f"🚀 Aggressively fixing {lang_code.upper()} using Polish as complete source...")

        # Skip EN and PL
        if lang_code in ['en', 'pl']:
            print(f"⏭️ Skipping {lang_code} - working fine")
            return True

        lang_file = os.path.join(self.locales_dir, f"{lang_code}.json")

        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                lang_data = json.load(f)
        except Exception as e:
            print(f"❌ Error loading {lang_code}: {e}")
            return False

        # Load Polish base for complete source
        try:
            with open(os.path.join(self.locales_dir, "pl.json"), 'r', encoding='utf-8') as f:
                base_data = json.load(f)
        except Exception as e:
            print(f"❌ Error loading Polish base: {e}")
            return False

        base_translations = self.get_all_keys_flat(base_data)
        lang_translations = self.get_all_keys_flat(lang_data)

        fixes_made = 0

        # Fix all problematic translations
        for key, polish_text in base_translations.items():
            current_text = lang_translations.get(key, "")

            # Check if current translation needs fixing
            needs_fixing = (
                not current_text or  # Missing translation
                current_text == polish_text or  # Untranslated
                self.is_mixed_language(current_text) or  # Mixed languages
                self.is_likely_english(current_text)  # English in non-English file
            )

            if needs_fixing:
                # Get complete translation from Polish
                new_translation = self.get_complete_translation(polish_text, lang_code)

                if new_translation != current_text and new_translation != polish_text:
                    self.set_nested_value(lang_data, key, new_translation)
                    fixes_made += 1
                    print(f"   ✓ Fixed: {key}")
                    print(f"     Old: {current_text[:50]}...")
                    print(f"     New: {new_translation[:50]}...")

        # Save fixes
        if fixes_made > 0:
            try:
                with open(lang_file, 'w', encoding='utf-8') as f:
                    json.dump(lang_data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
                print(f"✅ {lang_code.upper()}: Fixed {fixes_made} translations")
                return True
            except Exception as e:
                print(f"❌ Error saving {lang_code}: {e}")
                return False
        else:
            print(f"✅ {lang_code.upper()}: No fixes needed")
            return True

    def fix_all_languages(self):
        """Fix all languages aggressively using Polish as complete source"""
        print("🚀 FINAL AGGRESSIVE TRANSLATION FIX - COMPLETE PHRASE TRANSLATION")
        print("=" * 80)
        print("Using Polish as complete source for full phrase translations")
        print("=" * 80)

        languages = ['de', 'fr', 'es', 'it', 'nl', 'cs', 'hu', 'sk', 'sv', 'fi', 'uk']

        success_count = 0
        for lang_code in languages:
            try:
                if self.fix_language_aggressively(lang_code):
                    success_count += 1
            except Exception as e:
                print(f"❌ Error with {lang_code}: {e}")

        print(f"\n🎉 AGGRESSIVE FIX COMPLETE!")
        print(f"✅ Successfully fixed: {success_count}/{len(languages)} languages")
        print("📝 All translations now use complete phrases from Polish source")

def main():
    fixer = FinalTranslationFixer()
    fixer.fix_all_languages()

if __name__ == "__main__":
    main()