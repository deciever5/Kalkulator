"""
AI Translation Service
Uses Deep Translator for free translation with fallback to AI services
"""

import os
import json
import time
import streamlit as st
from typing import Dict, Any, List, Optional
from deep_translator import GoogleTranslator, MyMemoryTranslator
from .groq_service import GroqService

class AITranslationService:
    """Enhanced translation service with free alternatives"""

    def __init__(self):
        # Use GroqService which has built-in failover support
        self.groq_service = GroqService()
        self.groq_client = self.groq_service.client if self.groq_service.client else None

        # Language code mapping
        self.languages = {
            'en': 'English',
            'de': 'German', 
            'fr': 'French',
            'es': 'Spanish',
            'it': 'Italian',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'fi': 'Finnish',
            'cs': 'Czech',
            'sk': 'Slovak',
            'hu': 'Hungarian',
            'uk': 'Ukrainian',
            'ru': 'Russian',
            'pl': 'Polish'
        }

    def translate_missing_keys(self, target_lang: str, source_lang: str = 'pl'):
        """Translate missing keys using free translation services with AI fallback"""

        print(f"🌐 Processing {target_lang.upper()}...")

        # Load source and target files
        source_file = f'locales/{source_lang}.json'
        target_file = f'locales/{target_lang}.json'

        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                source_data = json.load(f)
        except FileNotFoundError:
            print(f"❌ Source file {source_file} not found")
            return False

        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                target_data = json.load(f)
        except FileNotFoundError:
            target_data = {}

        # Find missing translations
        missing_keys = self._find_missing_translations(source_data, target_data)

        if not missing_keys:
            print(f"✅ {target_lang.upper()}: No missing translations found")
            return True

        print(f"Found {len(missing_keys)} missing translations for {target_lang}")

        # Translate missing keys
        translated_count = 0
        for key_path, source_text in missing_keys.items():
            if translated_text := self._translate_text(source_text, target_lang):
                self._set_nested_value(target_data, key_path, translated_text)
                translated_count += 1

                # Rate limiting
                time.sleep(0.1)

        # Save updated translations
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(target_data, f, ensure_ascii=False, indent=2)

        print(f"✅ {target_lang.upper()}: Added {translated_count} translations")
        return True

    def _translate_text(self, text: str, target_lang: str) -> Optional[str]:
        """Translate text using multiple free services with fallbacks"""

        if not text or not text.strip():
            return text

        # Try Deep Translator (Google Translate) first
        try:
            translator = GoogleTranslator(source='pl', target=target_lang)
            result = translator.translate(text)
            if result and result.strip():
                return result
        except Exception as e:
            print(f"Google Translator error: {e}")

        # Try MyMemory translator as fallback
        try:
            translator = MyMemoryTranslator(source='pl', target=target_lang)
            result = translator.translate(text)
            if result and result.strip():
                return result
        except Exception as e:
            print(f"MyMemory Translator error: {e}")

        # Use Groq AI as final fallback if available
        if self.groq_service and self.groq_service.api_keys:
            try:
                return self._groq_translate_with_failover(text, target_lang)
            except Exception as e:
                print(f"Groq translation error: {e}")

        # Return original text if all methods fail
        print(f"⚠️ Translation failed for: {text[:50]}...")
        return text

    def _groq_translate_with_failover(self, text: str, target_lang: str) -> Optional[str]:
        """Translate using Groq AI with failover support"""

        target_language_name = self.languages.get(target_lang, target_lang)
        max_retries = len(self.groq_service.api_keys)
        
        for attempt in range(max_retries):
            try:
                prompt = f"""Translate the following Polish text to {target_language_name}. 
                Provide only the translation, no explanations:

                Text: {text}"""

                response = self.groq_service.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are a professional translator. Translate accurately from Polish to {target_language_name}. Respond only with the translation."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,
                    max_tokens=500
                )

                return response.choices[0].message.content.strip()

            except Exception as e:
                error_msg = str(e).lower()
                if "rate limit" in error_msg or "429" in error_msg:
                    print(f"Rate limit hit on API key {self.groq_service.current_key_index + 1}: {str(e)}")
                    
                    # Try next API key
                    if self.groq_service._try_next_key():
                        print(f"Switched to reserve API key {self.groq_service.current_key_index}")
                        continue
                    else:
                        print("All Groq API keys exhausted or rate limited")
                        # Wait for rate limit reset before giving up
                        print("Waiting 11 seconds for rate limit reset...")
                        time.sleep(11)
                        # Reset to first key and try once more
                        self.groq_service.current_key_index = 0
                        self.groq_service._initialize_client()
                        break
                else:
                    print(f"Groq translation error: {e}")
                    break
        
        return None

    def _find_missing_translations(self, source_data: Dict, target_data: Dict, prefix: str = "") -> Dict[str, str]:
        """Recursively find missing translation keys"""

        missing = {}

        for key, value in source_data.items():
            current_path = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                if key not in target_data or not isinstance(target_data[key], dict):
                    target_data[key] = {}

                nested_missing = self._find_missing_translations(
                    value, target_data[key], current_path
                )
                missing.update(nested_missing)

            elif isinstance(value, str):
                if key not in target_data or not target_data[key] or target_data[key] == value:
                    missing[current_path] = value

        return missing

    def _set_nested_value(self, data: Dict, key_path: str, value: str):
        """Set value in nested dictionary using dot notation"""

        keys = key_path.split('.')
        current = data

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value

    def translate_all_languages(self, source_lang: str = 'pl'):
        """Translate missing keys for all supported languages"""

        print("🤖 Starting AI-powered translation for incomplete languages...")

        target_languages = [lang for lang in self.languages.keys() if lang != source_lang]

        for lang in target_languages:
            try:
                self.translate_missing_keys(lang, source_lang)
            except Exception as e:
                print(f"❌ Error translating {lang}: {e}")

        print("🎉 AI translation complete! All languages now have complete translations.")
        print("📝 Note: Review and refine the translations as needed for your specific business context.")

    def check_translation_quality(self, base_lang: str = 'pl'):
        """Check translation quality across all languages"""

        print(f"🔍 Checking translation quality using {base_lang.upper()} as base...")

        # Load base language
        base_file = f'locales/{base_lang}.json'
        try:
            with open(base_file, 'r', encoding='utf-8') as f:
                base_data = json.load(f)
        except FileNotFoundError:
            print(f"❌ Base language file {base_file} not found")
            return

        issues_found = []

        for lang in self.languages.keys():
            if lang == base_lang:
                continue

            lang_file = f'locales/{lang}.json'
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    lang_data = json.load(f)

                missing_keys = self._find_missing_translations(base_data, lang_data)

                if missing_keys:
                    issues_found.append(f"{lang.upper()}: {len(missing_keys)} missing translations")

            except FileNotFoundError:
                issues_found.append(f"{lang.upper()}: Translation file missing")

        if issues_found:
            print("⚠️ Translation quality issues found:")
            for issue in issues_found:
                print(f"  - {issue}")
        else:
            print("✅ All languages have complete translations!")

# CLI usage
if __name__ == "__main__":
    import sys

    service = AITranslationService()

    if len(sys.argv) > 1:
        if sys.argv[1] == "check":
            service.check_translation_quality()
        elif sys.argv[1] == "translate":
            service.translate_all_languages()
        else:
            print("Usage: python ai_translation_service.py [check|translate]")
    else:
        service.translate_all_languages()