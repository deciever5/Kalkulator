
import json
import os
import re
import sys
from typing import Dict, Any, List, Set, Tuple

# Add parent directory to path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.groq_service import GroqService
import asyncio


class LanguageFixer:
    """
    Language validation and fixing tool that uses English as base language
    """
    
    def __init__(self):
        self.base_language = 'en'
        self.locales_dir = 'locales'
        self.groq_service = GroqService()
        
        # Language detection patterns
        self.language_patterns = {
            'en': re.compile(r'^[a-zA-Z0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$'),
            'de': re.compile(r'^[a-zA-ZäöüßÄÖÜ0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$'),
            'fr': re.compile(r'^[a-zA-ZàâäæçéèêëïîôùûüÿñÀÂÄÆÇÉÈÊËÏÎÔÙÛÜŸÑ0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$'),
            'es': re.compile(r'^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ¿¡0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$'),
            'it': re.compile(r'^[a-zA-ZàèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$'),
            'pl': re.compile(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$'),
            'cs': re.compile(r'^[a-zA-ZáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$'),
            'hu': re.compile(r'^[a-zA-ZáéíóöőúüűÁÉÍÓÖŐÚÜŰ0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$'),
            'nl': re.compile(r'^[a-zA-ZáéíóúàèìòùäëïöüÁÉÍÓÚÀÈÌÒÙÄËÏÖÜ0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$'),
            'fi': re.compile(r'^[a-zA-ZäöåÄÖÅ0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$'),
            'sv': re.compile(r'^[a-zA-ZäöåÄÖÅ0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$'),
            'uk': re.compile(r'^[а-яіїєґА-ЯІЇЄҐ0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$'),
            'sk': re.compile(r'^[a-zA-ZáäčďéíĺľňóôŕšťúýžÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ0-9\s\.,;:!?\-\'\"()[\]{}/@#$%^&*+=<>~`|\\]+$')
        }
    
    def load_translation_file(self, language_code: str) -> Dict[str, Any]:
        """Load translation file for given language"""
        file_path = os.path.join(self.locales_dir, f"{language_code}.json")
        if not os.path.exists(file_path):
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return {}
    
    def get_all_keys_recursive(self, data: Dict[str, Any], prefix: str = "") -> Set[str]:
        """Get all nested keys from translation data"""
        keys = set()
        
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                keys.update(self.get_all_keys_recursive(value, full_key))
            else:
                keys.add(full_key)
        
        return keys
    
    def get_nested_value(self, data: Dict[str, Any], key_path: str) -> str:
        """Get value from nested dictionary using dot notation"""
        keys = key_path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return ""
        
        return current if isinstance(current, str) else ""
    
    def is_text_long_enough(self, text: str) -> bool:
        """Check if text has words longer than 3 characters"""
        if not text:
            return False
        
        # Remove special characters and numbers for word length check
        words = re.findall(r'[a-zA-ZàâäæçéèêëïîôùûüÿñÀÂÄÆÇÉÈÊËÏÎÔÙÛÜŸÑáéíóúüñÁÉÍÓÚÜÑ¿¡àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚąćęłńóśźżĄĆĘŁŃÓŚŹŻáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽáéíóöőúüűÁÉÍÓÖŐÚÜŰäöåÄÖÅа-яіїєґА-ЯІЇЄҐ]+', text)
        
        # Check if any word is longer than 3 characters
        return any(len(word) > 3 for word in words)
    
    def detect_language(self, text: str, expected_language: str) -> bool:
        """Detect if text matches expected language pattern"""
        if not text or len(text.strip()) == 0:
            return True  # Empty text is considered valid
        
        # Skip very short texts
        if not self.is_text_long_enough(text):
            return True
        
        pattern = self.language_patterns.get(expected_language)
        if not pattern:
            return True  # Unknown language, assume valid
        
        return bool(pattern.match(text.strip()))
    
    async def translate_text(self, text: str, target_language: str) -> str:
        """Translate text using Groq service"""
        if not self.groq_service.client:
            print(f"Groq client not available for translation to {target_language}")
            return text
            
        try:
            # Use the existing groq service client directly for translation
            language_names = {
                'en': 'English', 'de': 'German', 'fr': 'French', 'es': 'Spanish',
                'it': 'Italian', 'pl': 'Polish', 'cs': 'Czech', 'hu': 'Hungarian',
                'nl': 'Dutch', 'fi': 'Finnish', 'uk': 'Ukrainian', 'sk': 'Slovak',
                'sv': 'Swedish'
            }
            
            target_language_name = language_names.get(target_language, target_language)
            
            response = self.groq_service.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate accurately to {target_language_name}. Return only the translation, no explanations."
                    },
                    {
                        "role": "user",
                        "content": f"Translate this text to {target_language_name}: {text}"
                    }
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            translation = response.choices[0].message.content.strip()
            return translation if translation else text
            
        except Exception as e:
            error_msg = str(e).lower()
            if "rate limit" in error_msg or "429" in error_msg:
                print(f"Translation rate limit hit, trying next API key...")
                # Try next API key using GroqService method
                if self.groq_service._try_next_key():
                    # Retry translation with new key
                    return await self.translate_text(text, target_language)
                else:
                    print("All translation API keys exhausted or rate limited")
                    return text
            else:
                print(f"Translation error for '{text}' to {target_language}: {e}")
                return text
    
    def check_structure_consistency(self, base_data: Dict[str, Any], target_data: Dict[str, Any], language_code: str) -> Tuple[Set[str], Set[str]]:
        """Check if target language has same structure as base language"""
        base_keys = self.get_all_keys_recursive(base_data)
        target_keys = self.get_all_keys_recursive(target_data)
        
        missing_keys = base_keys - target_keys
        extra_keys = target_keys - base_keys
        
        return missing_keys, extra_keys
    
    def check_translation_completeness(self, base_data: Dict[str, Any], target_data: Dict[str, Any], language_code: str) -> List[str]:
        """Check for untranslated (English) text in target language"""
        untranslated_keys = []
        base_keys = self.get_all_keys_recursive(base_data)
        
        for key in base_keys:
            base_text = self.get_nested_value(base_data, key)
            target_text = self.get_nested_value(target_data, key)
            
            # Skip if text is too short or empty
            if not self.is_text_long_enough(base_text):
                continue
            
            # Check if target text is identical to base text (untranslated)
            if target_text == base_text:
                untranslated_keys.append(key)
        
        return untranslated_keys
    
    def check_language_accuracy(self, target_data: Dict[str, Any], language_code: str) -> List[Tuple[str, str]]:
        """Check if text in target language file is actually in that language"""
        incorrect_language_keys = []
        target_keys = self.get_all_keys_recursive(target_data)
        
        for key in target_keys:
            text = self.get_nested_value(target_data, key)
            
            # Skip short texts
            if not self.is_text_long_enough(text):
                continue
            
            # Check if text matches expected language
            if not self.detect_language(text, language_code):
                incorrect_language_keys.append((key, text))
        
        return incorrect_language_keys
    
    async def fix_language_file(self, language_code: str, base_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix language file by translating missing/incorrect entries"""
        target_data = self.load_translation_file(language_code)
        
        print(f"\n🔧 Fixing {language_code}.json...")
        
        # Check structure
        missing_keys, extra_keys = self.check_structure_consistency(base_data, target_data, language_code)
        
        # Add missing keys
        for key in missing_keys:
            base_text = self.get_nested_value(base_data, key)
            if self.is_text_long_enough(base_text):
                print(f"  📝 Translating missing key: {key}")
                translated_text = await self.translate_text(base_text, language_code)
                self.set_nested_value(target_data, key, translated_text)
        
        # Check and fix untranslated text
        untranslated_keys = self.check_translation_completeness(base_data, target_data, language_code)
        for key in untranslated_keys:
            base_text = self.get_nested_value(base_data, key)
            print(f"  🔄 Retranslating untranslated key: {key}")
            translated_text = await self.translate_text(base_text, language_code)
            self.set_nested_value(target_data, key, translated_text)
        
        # Check and fix incorrect language
        incorrect_keys = self.check_language_accuracy(target_data, language_code)
        for key, text in incorrect_keys:
            print(f"  🌐 Fixing incorrect language for key: {key}")
            # Try to translate from English base
            base_text = self.get_nested_value(base_data, key)
            if base_text:
                translated_text = await self.translate_text(base_text, language_code)
                self.set_nested_value(target_data, key, translated_text)
        
        return target_data
    
    def set_nested_value(self, data: Dict[str, Any], key_path: str, value: str):
        """Set value in nested dictionary using dot notation"""
        keys = key_path.split('.')
        current = data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def save_translation_file(self, language_code: str, data: Dict[str, Any]):
        """Save translation file with proper formatting"""
        file_path = os.path.join(self.locales_dir, f"{language_code}.json")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  ✅ Saved {file_path}")
        except Exception as e:
            print(f"  ❌ Error saving {file_path}: {e}")
    
    async def analyze_all_languages(self):
        """Analyze all language files and provide detailed report"""
        print("🔍 LANGUAGE ANALYSIS REPORT")
        print("=" * 50)
        
        # Load base language (English)
        base_data = self.load_translation_file(self.base_language)
        if not base_data:
            print(f"❌ Could not load base language file: {self.base_language}.json")
            return
        
        base_keys = self.get_all_keys_recursive(base_data)
        print(f"📖 Base language ({self.base_language}) has {len(base_keys)} keys")
        
        # Get all available language files
        language_files = []
        for file in os.listdir(self.locales_dir):
            if file.endswith('.json') and file != f'{self.base_language}.json':
                lang_code = file[:-5]  # Remove .json extension
                language_files.append(lang_code)
        
        print(f"🌐 Found {len(language_files)} language files to analyze")
        
        for language_code in sorted(language_files):
            print(f"\n📄 Analyzing {language_code}.json...")
            
            target_data = self.load_translation_file(language_code)
            if not target_data:
                print(f"  ❌ Could not load {language_code}.json")
                continue
            
            # Structure consistency check
            missing_keys, extra_keys = self.check_structure_consistency(base_data, target_data, language_code)
            
            print(f"  📊 Structure Analysis:")
            print(f"    ✅ Missing keys: {len(missing_keys)}")
            if missing_keys:
                for key in sorted(list(missing_keys)[:5]):  # Show first 5
                    print(f"      - {key}")
                if len(missing_keys) > 5:
                    print(f"      ... and {len(missing_keys) - 5} more")
            
            print(f"    ➕ Extra keys: {len(extra_keys)}")
            if extra_keys:
                for key in sorted(list(extra_keys)[:3]):  # Show first 3
                    print(f"      + {key}")
                if len(extra_keys) > 3:
                    print(f"      ... and {len(extra_keys) - 3} more")
            
            # Translation completeness check
            untranslated_keys = self.check_translation_completeness(base_data, target_data, language_code)
            print(f"  🔄 Untranslated keys: {len(untranslated_keys)}")
            if untranslated_keys:
                for key in untranslated_keys[:3]:  # Show first 3
                    print(f"      ! {key}")
                if len(untranslated_keys) > 3:
                    print(f"      ... and {len(untranslated_keys) - 3} more")
            
            # Language accuracy check
            incorrect_keys = self.check_language_accuracy(target_data, language_code)
            print(f"  🌐 Incorrect language entries: {len(incorrect_keys)}")
            if incorrect_keys:
                for key, text in incorrect_keys[:2]:  # Show first 2
                    preview = text[:50] + "..." if len(text) > 50 else text
                    print(f"      ? {key}: '{preview}'")
                if len(incorrect_keys) > 2:
                    print(f"      ... and {len(incorrect_keys) - 2} more")
    
    async def add_missing_keys_from_english(self, language_code: str) -> bool:
        """
        Add and translate missing keys from English to specified language
        
        Args:
            language_code: Target language code (e.g., 'de', 'fr', 'sv')
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n🔧 Adding missing keys to {language_code}.json from English...")
        
        # Load English base language
        base_data = self.load_translation_file(self.base_language)
        if not base_data:
            print(f"❌ Could not load English base file: {self.base_language}.json")
            return False
        
        # Load target language
        target_data = self.load_translation_file(language_code)
        if not target_data:
            print(f"  ℹ️ Creating new language file for {language_code}")
            target_data = {}
        
        # Find missing keys
        base_keys = self.get_all_keys_recursive(base_data)
        target_keys = self.get_all_keys_recursive(target_data)
        missing_keys = base_keys - target_keys
        
        if not missing_keys:
            print(f"  ✅ No missing keys found in {language_code}.json")
            return True
        
        print(f"  📝 Found {len(missing_keys)} missing keys to translate")
        
        # Translate and add missing keys
        translation_count = 0
        for key in sorted(missing_keys):
            base_text = self.get_nested_value(base_data, key)
            
            # Skip empty or very short texts
            if not base_text or not self.is_text_long_enough(base_text):
                # For short texts, just copy directly
                self.set_nested_value(target_data, key, base_text)
                continue
            
            try:
                print(f"    🌐 Translating: {key}")
                translated_text = await self.translate_text(base_text, language_code)
                self.set_nested_value(target_data, key, translated_text)
                translation_count += 1
                
                # Add small delay to avoid rate limiting
                if translation_count % 10 == 0:
                    await asyncio.sleep(1)
                    
            except Exception as e:
                print(f"    ❌ Translation failed for {key}: {e}")
                # Fallback to English text
                self.set_nested_value(target_data, key, base_text)
        
        # Save the updated file
        try:
            self.save_translation_file(language_code, target_data)
            print(f"  ✅ Successfully added {len(missing_keys)} keys to {language_code}.json")
            print(f"  📊 Translated: {translation_count}, Copied: {len(missing_keys) - translation_count}")
            return True
        except Exception as e:
            print(f"  ❌ Error saving {language_code}.json: {e}")
            return False
    
    async def add_missing_keys_to_all_languages(self):
        """Add missing keys from English to all language files"""
        print("🌍 ADDING MISSING KEYS TO ALL LANGUAGES")
        print("=" * 50)
        
        # Load base language (English)
        base_data = self.load_translation_file(self.base_language)
        if not base_data:
            print(f"❌ Could not load base language file: {self.base_language}.json")
            return
        
        # Get all available language files
        language_files = []
        for file in os.listdir(self.locales_dir):
            if file.endswith('.json') and file != f'{self.base_language}.json':
                lang_code = file[:-5]  # Remove .json extension
                language_files.append(lang_code)
        
        print(f"🌐 Processing {len(language_files)} language files...")
        
        success_count = 0
        for language_code in sorted(language_files):
            try:
                if await self.add_missing_keys_from_english(language_code):
                    success_count += 1
            except Exception as e:
                print(f"  ❌ Error processing {language_code}: {e}")
        
        print(f"\n✅ Successfully updated {success_count}/{len(language_files)} language files!")

    def remove_nested_key(self, data: Dict[str, Any], key_path: str) -> bool:
        """Remove a nested key from dictionary using dot notation"""
        keys = key_path.split('.')
        current = data
        
        # Navigate to the parent of the key to remove
        for key in keys[:-1]:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return False  # Path doesn't exist
        
        # Remove the final key
        if isinstance(current, dict) and keys[-1] in current:
            del current[keys[-1]]
            return True
        
        return False

    async def remove_extra_keys_from_language(self, language_code: str) -> bool:
        """
        Remove extra keys from specified language that don't exist in English
        
        Args:
            language_code: Target language code (e.g., 'de', 'fr', 'sv')
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n🗑️ Removing extra keys from {language_code}.json...")
        
        # Load English base language
        base_data = self.load_translation_file(self.base_language)
        if not base_data:
            print(f"❌ Could not load English base file: {self.base_language}.json")
            return False
        
        # Load target language
        target_data = self.load_translation_file(language_code)
        if not target_data:
            print(f"❌ Could not load {language_code}.json")
            return False
        
        # Find extra keys
        base_keys = self.get_all_keys_recursive(base_data)
        target_keys = self.get_all_keys_recursive(target_data)
        extra_keys = target_keys - base_keys
        
        if not extra_keys:
            print(f"  ✅ No extra keys found in {language_code}.json")
            return True
        
        print(f"  🗑️ Found {len(extra_keys)} extra keys to remove")
        
        # Remove extra keys
        removal_count = 0
        for key in sorted(extra_keys, reverse=True):  # Remove in reverse order to avoid key path issues
            try:
                print(f"    ❌ Removing: {key}")
                if self.remove_nested_key(target_data, key):
                    removal_count += 1
                else:
                    print(f"    ⚠️ Could not remove: {key}")
            except Exception as e:
                print(f"    ❌ Error removing {key}: {e}")
        
        # Save the updated file
        try:
            self.save_translation_file(language_code, target_data)
            print(f"  ✅ Successfully removed {removal_count} extra keys from {language_code}.json")
            return True
        except Exception as e:
            print(f"  ❌ Error saving {language_code}.json: {e}")
            return False

    async def remove_extra_keys_from_all_languages(self):
        """Remove extra keys from all language files that don't exist in English"""
        print("🗑️ REMOVING EXTRA KEYS FROM ALL LANGUAGES")
        print("=" * 50)
        
        # Load base language (English)
        base_data = self.load_translation_file(self.base_language)
        if not base_data:
            print(f"❌ Could not load base language file: {self.base_language}.json")
            return
        
        # Get all available language files
        language_files = []
        for file in os.listdir(self.locales_dir):
            if file.endswith('.json') and file != f'{self.base_language}.json':
                lang_code = file[:-5]  # Remove .json extension
                language_files.append(lang_code)
        
        print(f"🌐 Processing {len(language_files)} language files...")
        
        success_count = 0
        total_removed = 0
        for language_code in sorted(language_files):
            try:
                if await self.remove_extra_keys_from_language(language_code):
                    success_count += 1
            except Exception as e:
                print(f"  ❌ Error processing {language_code}: {e}")
        
        print(f"\n✅ Successfully processed {success_count}/{len(language_files)} language files!")

    async def fix_all_languages(self):
        """Fix all language files"""
        print("🔧 LANGUAGE FIXING PROCESS")
        print("=" * 50)
        
        # Load base language (English)
        base_data = self.load_translation_file(self.base_language)
        if not base_data:
            print(f"❌ Could not load base language file: {self.base_language}.json")
            return
        
        # Get all available language files
        language_files = []
        for file in os.listdir(self.locales_dir):
            if file.endswith('.json') and file != f'{self.base_language}.json':
                lang_code = file[:-5]  # Remove .json extension
                language_files.append(lang_code)
        
        print(f"🌐 Fixing {len(language_files)} language files...")
        
        for language_code in sorted(language_files):
            try:
                fixed_data = await self.fix_language_file(language_code, base_data)
                self.save_translation_file(language_code, fixed_data)
            except Exception as e:
                print(f"  ❌ Error fixing {language_code}: {e}")
        
        print("\n✅ Language fixing complete!")


async def main():
    """Main function to run the language fixer"""
    fixer = LanguageFixer()
    
    print("KAN-BUD Language Fixer Tool")
    print("=" * 40)
    print("1. Analyze all languages")
    print("2. Fix all languages")
    print("3. Add missing keys from English to all languages")
    print("4. Add missing keys to specific language")
    print("5. Remove extra keys from all languages")
    print("6. Remove extra keys from specific language")
    print("7. Both analyze and fix")
    print("8. Complete cleanup (add missing + remove extra)")
    
    choice = input("\nSelect option (1-8): ").strip()
    
    if choice == "1":
        await fixer.analyze_all_languages()
    elif choice == "2":
        await fixer.fix_all_languages()
    elif choice == "3":
        await fixer.add_missing_keys_to_all_languages()
    elif choice == "4":
        available_langs = ['de', 'nl', 'cs', 'hu', 'pl', 'es', 'it', 'sv', 'fi', 'uk', 'sk', 'fr']
        print(f"Available languages: {', '.join(available_langs)}")
        lang_code = input("Enter language code (e.g., 'sv', 'de'): ").strip().lower()
        if lang_code in available_langs:
            await fixer.add_missing_keys_from_english(lang_code)
        else:
            print(f"Invalid language code. Available: {', '.join(available_langs)}")
    elif choice == "5":
        await fixer.remove_extra_keys_from_all_languages()
    elif choice == "6":
        available_langs = ['de', 'nl', 'cs', 'hu', 'pl', 'es', 'it', 'sv', 'fi', 'uk', 'sk', 'fr']
        print(f"Available languages: {', '.join(available_langs)}")
        lang_code = input("Enter language code (e.g., 'sv', 'de'): ").strip().lower()
        if lang_code in available_langs:
            await fixer.remove_extra_keys_from_language(lang_code)
        else:
            print(f"Invalid language code. Available: {', '.join(available_langs)}")
    elif choice == "7":
        await fixer.analyze_all_languages()
        print("\n" + "=" * 50)
        await fixer.fix_all_languages()
    elif choice == "8":
        await fixer.add_missing_keys_to_all_languages()
        print("\n" + "=" * 50)
        await fixer.remove_extra_keys_from_all_languages()
    else:
        print("Invalid choice. Please run again and select 1-8.")


if __name__ == "__main__":
    asyncio.run(main())
