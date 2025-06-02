
#!/usr/bin/env python3
"""
Final Aggressive Translation Fix
Last resort script to fix remaining translation issues
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
        
        # Aggressive translation mappings for common patterns
        self.pattern_translations = {
            'de': {
                'heating': 'Heizung', 'cooling': 'Kühlung', 'none': 'Keine',
                'basic': 'Basis', 'standard': 'Standard', 'advanced': 'Erweitert',
                'security': 'Sicherheit', 'system': 'System', 'installation': 'Installation',
                'delivery': 'Lieferung', 'transport': 'Transport', 'analysis': 'Analyse',
                'configuration': 'Konfiguration', 'professional': 'Professionell',
                'materials': 'Materialien', 'assembly': 'Montage', 'custom': 'Benutzerdefiniert',
                'underfloor': 'Fußboden', 'cold water': 'Kaltwasser', 'crane': 'Kran',
                'solar': 'Solar', 'terrace': 'Terrasse', 'extended': 'Erweitert',
                'full': 'Vollständig', 'ramp': 'Rampe', 'lift': 'Aufzug',
                'built-in': 'Eingebaut', 'furniture': 'Möbel', 'layout': 'Layout'
            },
            'fr': {
                'heating': 'chauffage', 'cooling': 'refroidissement', 'none': 'Aucun',
                'basic': 'de base', 'standard': 'standard', 'advanced': 'avancé',
                'security': 'sécurité', 'system': 'système', 'installation': 'installation',
                'delivery': 'livraison', 'transport': 'transport', 'analysis': 'analyse',
                'configuration': 'configuration', 'professional': 'professionnel',
                'materials': 'matériaux', 'assembly': 'assemblage', 'custom': 'personnalisé',
                'underfloor': 'plancher', 'cold water': 'eau froide', 'crane': 'grue',
                'solar': 'solaire', 'terrace': 'terrasse', 'extended': 'étendu',
                'full': 'complet', 'ramp': 'rampe', 'lift': 'ascenseur',
                'built-in': 'intégré', 'furniture': 'meubles', 'layout': 'disposition'
            },
            'es': {
                'heating': 'calefacción', 'cooling': 'refrigeración', 'none': 'Ninguno',
                'basic': 'básico', 'standard': 'estándar', 'advanced': 'avanzado',
                'security': 'seguridad', 'system': 'sistema', 'installation': 'instalación',
                'delivery': 'entrega', 'transport': 'transporte', 'analysis': 'análisis',
                'configuration': 'configuración', 'professional': 'profesional',
                'materials': 'materiales', 'assembly': 'montaje', 'custom': 'personalizado',
                'underfloor': 'suelo', 'cold water': 'agua fría', 'crane': 'grúa',
                'solar': 'solar', 'terrace': 'terraza', 'extended': 'extendido',
                'full': 'completo', 'ramp': 'rampa', 'lift': 'ascensor',
                'built-in': 'incorporado', 'furniture': 'muebles', 'layout': 'diseño'
            },
            'it': {
                'heating': 'riscaldamento', 'cooling': 'raffreddamento', 'none': 'Nessuno',
                'basic': 'di base', 'standard': 'standard', 'advanced': 'avanzato',
                'security': 'sicurezza', 'system': 'sistema', 'installation': 'installazione',
                'delivery': 'consegna', 'transport': 'trasporto', 'analysis': 'analisi',
                'configuration': 'configurazione', 'professional': 'professionale',
                'materials': 'materiali', 'assembly': 'assemblaggio', 'custom': 'personalizzato',
                'underfloor': 'pavimento', 'cold water': 'acqua fredda', 'crane': 'gru',
                'solar': 'solare', 'terrace': 'terrazza', 'extended': 'esteso',
                'full': 'completo', 'ramp': 'rampa', 'lift': 'ascensore',
                'built-in': 'incorporato', 'furniture': 'mobili', 'layout': 'layout'
            },
            'nl': {
                'heating': 'verwarming', 'cooling': 'koeling', 'none': 'Geen',
                'basic': 'basis', 'standard': 'standaard', 'advanced': 'geavanceerd',
                'security': 'beveiliging', 'system': 'systeem', 'installation': 'installatie',
                'delivery': 'levering', 'transport': 'transport', 'analysis': 'analyse',
                'configuration': 'configuratie', 'professional': 'professioneel',
                'materials': 'materialen', 'assembly': 'montage', 'custom': 'aangepast',
                'underfloor': 'vloer', 'cold water': 'koud water', 'crane': 'kraan',
                'solar': 'zonne', 'terrace': 'terras', 'extended': 'uitgebreid',
                'full': 'volledig', 'ramp': 'helling', 'lift': 'lift',
                'built-in': 'ingebouwd', 'furniture': 'meubels', 'layout': 'indeling'
            },
            'cs': {
                'heating': 'vytápění', 'cooling': 'chlazení', 'none': 'Žádný',
                'basic': 'základní', 'standard': 'standardní', 'advanced': 'pokročilý',
                'security': 'bezpečnost', 'system': 'systém', 'installation': 'instalace',
                'delivery': 'dodání', 'transport': 'doprava', 'analysis': 'analýza',
                'configuration': 'konfigurace', 'professional': 'profesionální',
                'materials': 'materiály', 'assembly': 'montáž', 'custom': 'vlastní',
                'underfloor': 'podlaha', 'cold water': 'studená voda', 'crane': 'jeřáb',
                'solar': 'solární', 'terrace': 'terasa', 'extended': 'rozšířený',
                'full': 'úplný', 'ramp': 'rampa', 'lift': 'výtah',
                'built-in': 'vestavěný', 'furniture': 'nábytek', 'layout': 'rozložení'
            },
            'hu': {
                'heating': 'fűtés', 'cooling': 'hűtés', 'none': 'Nincs',
                'basic': 'alap', 'standard': 'szabványos', 'advanced': 'haladó',
                'security': 'biztonság', 'system': 'rendszer', 'installation': 'telepítés',
                'delivery': 'szállítás', 'transport': 'szállítás', 'analysis': 'elemzés',
                'configuration': 'konfiguráció', 'professional': 'szakmai',
                'materials': 'anyagok', 'assembly': 'összeszerelés', 'custom': 'egyedi',
                'underfloor': 'padló', 'cold water': 'hideg víz', 'crane': 'daru',
                'solar': 'napenergia', 'terrace': 'terasz', 'extended': 'kiterjesztett',
                'full': 'teljes', 'ramp': 'rámpa', 'lift': 'lift',
                'built-in': 'beépített', 'furniture': 'bútor', 'layout': 'elrendezés'
            },
            'sk': {
                'heating': 'vykurovanie', 'cooling': 'chladenie', 'none': 'Žiadny',
                'basic': 'základný', 'standard': 'štandardný', 'advanced': 'pokročilý',
                'security': 'bezpečnosť', 'system': 'systém', 'installation': 'inštalácia',
                'delivery': 'dodanie', 'transport': 'doprava', 'analysis': 'analýza',
                'configuration': 'konfigurácia', 'professional': 'profesionálny',
                'materials': 'materiály', 'assembly': 'montáž', 'custom': 'vlastný',
                'underfloor': 'podlaha', 'cold water': 'studená voda', 'crane': 'žeriav',
                'solar': 'solárny', 'terrace': 'terasa', 'extended': 'rozšírený',
                'full': 'úplný', 'ramp': 'rampa', 'lift': 'výťah',
                'built-in': 'vstavaný', 'furniture': 'nábytok', 'layout': 'rozloženie'
            },
            'sv': {
                'heating': 'uppvärmning', 'cooling': 'kylning', 'none': 'Ingen',
                'basic': 'grundläggande', 'standard': 'standard', 'advanced': 'avancerad',
                'security': 'säkerhet', 'system': 'system', 'installation': 'installation',
                'delivery': 'leverans', 'transport': 'transport', 'analysis': 'analys',
                'configuration': 'konfiguration', 'professional': 'professionell',
                'materials': 'material', 'assembly': 'montering', 'custom': 'anpassad',
                'underfloor': 'golv', 'cold water': 'kallt vatten', 'crane': 'kran',
                'solar': 'sol', 'terrace': 'terrass', 'extended': 'utökad',
                'full': 'fullständig', 'ramp': 'ramp', 'lift': 'hiss',
                'built-in': 'inbyggd', 'furniture': 'möbler', 'layout': 'layout'
            },
            'fi': {
                'heating': 'lämmitys', 'cooling': 'jäähdytys', 'none': 'Ei mitään',
                'basic': 'perus', 'standard': 'vakio', 'advanced': 'edistynyt',
                'security': 'turvallisuus', 'system': 'järjestelmä', 'installation': 'asennus',
                'delivery': 'toimitus', 'transport': 'kuljetus', 'analysis': 'analyysi',
                'configuration': 'konfiguraatio', 'professional': 'ammattimainen',
                'materials': 'materiaalit', 'assembly': 'kokoonpano', 'custom': 'mukautettu',
                'underfloor': 'lattia', 'cold water': 'kylmä vesi', 'crane': 'nosturi',
                'solar': 'aurinko', 'terrace': 'terassi', 'extended': 'laajennettu',
                'full': 'täydellinen', 'ramp': 'luiska', 'lift': 'hissi',
                'built-in': 'sisäänrakennettu', 'furniture': 'huonekalut', 'layout': 'asettelu'
            },
            'uk': {
                'heating': 'опалення', 'cooling': 'охолодження', 'none': 'Немає',
                'basic': 'базовий', 'standard': 'стандартний', 'advanced': 'просунутий',
                'security': 'безпека', 'system': 'система', 'installation': 'встановлення',
                'delivery': 'доставка', 'transport': 'транспорт', 'analysis': 'аналіз',
                'configuration': 'конфігурація', 'professional': 'професійний',
                'materials': 'матеріали', 'assembly': 'збірка', 'custom': 'власний',
                'underfloor': 'підлога', 'cold water': 'холодна вода', 'crane': 'кран',
                'solar': 'сонячний', 'terrace': 'тераса', 'extended': 'розширений',
                'full': 'повний', 'ramp': 'пандус', 'lift': 'ліфт',
                'built-in': 'вбудований', 'furniture': 'меблі', 'layout': 'планування'
            }
        }

    def is_likely_english(self, text: str) -> bool:
        """Check if text is likely English"""
        english_indicators = ['the', 'and', 'or', 'of', 'to', 'for', 'with', 'by', 'from', 'system', 'configuration', 'analysis']
        words = text.lower().split()
        return any(word in english_indicators for word in words)

    def fix_with_patterns(self, text: str, lang_code: str) -> str:
        """Fix text using pattern matching"""
        if lang_code not in self.pattern_translations:
            return text
            
        text_lower = text.lower().strip()
        patterns = self.pattern_translations[lang_code]
        
        # Try exact matches first
        for english_word, translation in patterns.items():
            if text_lower == english_word:
                return translation
            # Try partial matches for compound words
            if english_word in text_lower and len(english_word) > 3:
                return text.replace(english_word, translation)
                
        return text

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
            current = current[key]
        current[keys[-1]] = value

    def fix_language_aggressively(self, lang_code: str) -> bool:
        """Apply aggressive fixes to a language file"""
        print(f"🚀 Aggressively fixing {lang_code.upper()}...")
        
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
            
        # Load Polish base
        try:
            with open(os.path.join(self.locales_dir, "pl.json"), 'r', encoding='utf-8') as f:
                base_data = json.load(f)
        except Exception as e:
            print(f"❌ Error loading Polish base: {e}")
            return False
            
        base_translations = self.get_all_keys_flat(base_data)
        lang_translations = self.get_all_keys_flat(lang_data)
        
        fixes_made = 0
        
        # Fix all translations
        for key, polish_text in base_translations.items():
            current_text = lang_translations.get(key, "")
            
            # Skip if already properly translated
            if current_text and not self.is_likely_english(current_text) and current_text != polish_text:
                continue
                
            # Try pattern matching first
            pattern_result = self.fix_with_patterns(current_text or polish_text, lang_code)
            if pattern_result != (current_text or polish_text):
                self.set_nested_value(lang_data, key, pattern_result)
                fixes_made += 1
                print(f"   ✓ Pattern: {key}")
                continue
                
            # Try AI translation
            try:
                translated = self.ai_service._translate_text(polish_text, lang_code)
                if translated and translated != polish_text and not self.is_likely_english(translated):
                    self.set_nested_value(lang_data, key, translated)
                    fixes_made += 1
                    print(f"   ✓ AI: {key}")
            except Exception as e:
                print(f"   ⚠️ AI error for {key}: {e}")
        
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
        """Fix all languages aggressively"""
        print("🚀 FINAL AGGRESSIVE TRANSLATION FIX")
        print("=" * 60)
        
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

def main():
    fixer = FinalTranslationFixer()
    fixer.fix_all_languages()

if __name__ == "__main__":
    main()
