
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from groq import Groq

class AITranslationService:
    """AI-powered translation service for technical container terminology using Groq"""

    def __init__(self):
        self.api_key = os.environ.get('GROQ_API_KEY')
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                print("✅ Groq API configured successfully")
            except Exception as e:
                print(f"⚠️ Groq configuration failed: {e}")
                self.client = None
        else:
            self.client = None
            print("⚠️ No GROQ_API_KEY found - using fallback translations")

    def check_all_translations_quality(self, base_lang: str = 'pl'):
        """Check translation quality for all languages using specified base language"""
        
        print(f"🔍 Starting AI translation quality check with {base_lang.upper()} as base language...")
        
        # Load base language
        base_data = self._load_language_file(base_lang)
        if not base_data:
            print(f"❌ Could not load base language {base_lang}")
            return
            
        base_keys = self._get_all_keys_flat(base_data)
        print(f"📚 Loaded {len(base_keys)} translation keys from {base_lang.upper()}")
        
        # All supported languages
        all_languages = ['en', 'de', 'fr', 'es', 'it', 'nl', 'cs', 'sk', 'hu', 'sv', 'fi', 'uk']
        target_languages = [lang for lang in all_languages if lang != base_lang]
        
        results = {}
        
        for target_lang in target_languages:
            print(f"\n🌐 Checking {target_lang.upper()} translations...")
            
            target_data = self._load_language_file(target_lang)
            if not target_data:
                print(f"⚠️ Could not load {target_lang}")
                continue
                
            result = self._analyze_language_quality(base_lang, target_lang, base_keys, target_data)
            results[target_lang] = result
            
            self._print_language_summary(target_lang, result)
            
            # Fix issues if needed
            if result['needs_fixes']:
                self._fix_translation_issues(target_lang, target_data, result)
        
        self._print_overall_summary(results)
        return results

    def _load_language_file(self, lang_code: str) -> Dict:
        """Load a language file"""
        filepath = f"locales/{lang_code}.json"
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return {}

    def _get_all_keys_flat(self, data: Dict, prefix: str = "") -> Dict[str, str]:
        """Get all keys from nested dict as flat key-value pairs"""
        result = {}
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                result.update(self._get_all_keys_flat(value, full_key))
            elif isinstance(value, str):
                result[full_key] = value
        return result

    def _analyze_language_quality(self, base_lang: str, target_lang: str, base_keys: Dict[str, str], target_data: Dict) -> Dict:
        """Analyze translation quality for a specific language"""
        
        target_keys = self._get_all_keys_flat(target_data)
        
        # Find different types of issues
        missing_keys = {}
        auto_translations = {}
        identical_translations = {}
        suspicious_translations = {}
        good_translations = {}
        
        for key, base_value in base_keys.items():
            target_value = target_keys.get(key)
            
            if target_value is None:
                missing_keys[key] = base_value
            elif target_value.startswith("[AUTO]") or target_value.startswith("[TRANSLATE]"):
                auto_translations[key] = target_value
            elif target_value == base_value:
                # Check if it should be identical (brand names, etc.)
                if self._is_likely_untranslatable(base_value):
                    good_translations[key] = target_value
                else:
                    identical_translations[key] = target_value
            elif self._is_suspicious_translation(base_value, target_value, target_lang):
                suspicious_translations[key] = (base_value, target_value)
            else:
                good_translations[key] = target_value
        
        total_keys = len(base_keys)
        quality_score = len(good_translations) / total_keys * 100
        
        return {
            'total_keys': total_keys,
            'missing_keys': missing_keys,
            'auto_translations': auto_translations,
            'identical_translations': identical_translations,
            'suspicious_translations': suspicious_translations,
            'good_translations': good_translations,
            'quality_score': quality_score,
            'needs_fixes': bool(missing_keys or auto_translations or suspicious_translations)
        }

    def _print_language_summary(self, lang: str, result: Dict):
        """Print summary for a language"""
        total = result['total_keys']
        
        print(f"   📊 {lang.upper()} Translation Analysis:")
        print(f"      ✅ Good translations: {len(result['good_translations'])} ({len(result['good_translations'])/total*100:.1f}%)")
        print(f"      🤖 Auto/placeholder: {len(result['auto_translations'])} ({len(result['auto_translations'])/total*100:.1f}%)")
        print(f"      🔄 Identical to base: {len(result['identical_translations'])} ({len(result['identical_translations'])/total*100:.1f}%)")
        print(f"      ⚠️  Suspicious: {len(result['suspicious_translations'])} ({len(result['suspicious_translations'])/total*100:.1f}%)")
        print(f"      ❌ Missing: {len(result['missing_keys'])} ({len(result['missing_keys'])/total*100:.1f}%)")
        print(f"      🎯 Quality Score: {result['quality_score']:.1f}%")
        
        # Show examples of issues
        if result['auto_translations']:
            print(f"   🤖 Sample auto translations:")
            for key, value in list(result['auto_translations'].items())[:3]:
                clean_value = value.replace("[AUTO] ", "").replace("[TRANSLATE] ", "")
                print(f"      {key}: '{clean_value}'")
        
        if result['suspicious_translations']:
            print(f"   ⚠️  Sample suspicious translations:")
            for key, (base_val, target_val) in list(result['suspicious_translations'].items())[:2]:
                print(f"      {key}:")
                print(f"        Base: '{base_val}'")
                print(f"        Target: '{target_val}'")

    def _print_overall_summary(self, results: Dict):
        """Print overall summary of all languages"""
        print("\n" + "="*60)
        print("📋 OVERALL TRANSLATION QUALITY SUMMARY")
        print("="*60)
        
        # Sort by quality score
        sorted_results = sorted(results.items(), key=lambda x: x[1]['quality_score'], reverse=True)
        
        print(f"{'Language':<10} {'Quality':<8} {'Missing':<8} {'Auto':<8} {'Suspicious':<12}")
        print("-" * 60)
        
        for lang, result in sorted_results:
            quality = f"{result['quality_score']:.1f}%"
            missing = len(result['missing_keys'])
            auto = len(result['auto_translations'])
            suspicious = len(result['suspicious_translations'])
            
            status = "🟢" if result['quality_score'] > 90 else "🟡" if result['quality_score'] > 70 else "🔴"
            
            print(f"{lang.upper():<10} {quality:<8} {missing:<8} {auto:<8} {suspicious:<12} {status}")
        
        # Priority recommendations
        print(f"\n🎯 PRIORITY ACTIONS:")
        high_priority = [lang for lang, result in results.items() if result['quality_score'] < 70]
        medium_priority = [lang for lang, result in results.items() if 70 <= result['quality_score'] < 90]
        
        if high_priority:
            print(f"🔴 High Priority (fix immediately): {', '.join(h.upper() for h in high_priority)}")
        if medium_priority:
            print(f"🟡 Medium Priority (review and improve): {', '.join(m.upper() for m in medium_priority)}")

    def _fix_translation_issues(self, lang: str, target_data: Dict, result: Dict):
        """Fix translation issues using AI"""
        
        if not self.client:
            print(f"⚠️ No AI service available for fixing {lang}")
            return
            
        fixes_needed = {}
        fixes_needed.update(result['missing_keys'])
        fixes_needed.update({k: v.replace("[AUTO] ", "").replace("[TRANSLATE] ", "") 
                           for k, v in result['auto_translations'].items()})
        
        if not fixes_needed:
            return
            
        print(f"🔧 Attempting to fix {len(fixes_needed)} issues in {lang.upper()}...")
        
        try:
            # Translate in batches
            batch_size = 20
            fixed_count = 0
            
            for i in range(0, len(fixes_needed), batch_size):
                batch = dict(list(fixes_needed.items())[i:i+batch_size])
                translations = self.translate_missing_keys('pl', lang, batch)
                
                # Apply fixes
                for key, translated_value in translations.items():
                    self._set_nested_value(target_data, key, translated_value)
                    fixed_count += 1
            
            # Save updated file
            filepath = f"locales/{lang}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(target_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Fixed {fixed_count} translations in {lang.upper()}")
            
        except Exception as e:
            print(f"❌ Failed to fix {lang}: {e}")

    def _set_nested_value(self, data: Dict, key_path: str, value: str):
        """Set nested value using dot notation"""
        keys = key_path.split('.')
        current = data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def translate_missing_keys(self, source_lang: str, target_lang: str, missing_keys: Dict[str, str]) -> Dict[str, str]:
        """Translate missing translation keys using Groq AI service"""

        if not missing_keys:
            return {}

        if not self.client:
            print("⚠️ Groq API not available, using fallback translation")
            return self._fallback_translation(target_lang, missing_keys)

        # Build context-aware translation prompt
        prompt = self._build_translation_prompt(source_lang, target_lang, missing_keys)

        try:
            result = self._translate_with_groq(prompt)

            if result and isinstance(result, dict):
                return result

        except Exception as e:
            print(f"❌ Groq translation failed: {e}")

        return self._fallback_translation(target_lang, missing_keys)

    def _build_translation_prompt(self, source_lang: str, target_lang: str, missing_keys: Dict[str, str]) -> str:
        """Build context-aware translation prompt"""

        lang_names = {
            'en': 'English',
            'pl': 'Polish',
            'de': 'German',
            'fr': 'French',
            'es': 'Spanish',
            'it': 'Italian',
            'nl': 'Dutch',
            'cs': 'Czech',
            'sk': 'Slovak',
            'hu': 'Hungarian',
            'sv': 'Swedish',
            'fi': 'Finnish',
            'uk': 'Ukrainian'
        }

        source_name = lang_names.get(source_lang, source_lang)
        target_name = lang_names.get(target_lang, target_lang)

        # Sample of key-value pairs for context
        sample_keys = dict(list(missing_keys.items())[:10])

        prompt = f"""
You are a professional translator specializing in technical construction and container modification terminology.

Task: Translate the following {source_name} terms to {target_name} for a container modification and construction company.

Context: This is for a professional container modification business (KAN-BUD) that designs, builds, and modifies shipping containers for various purposes (offices, workshops, residential, storage, etc.).

Important guidelines:
1. Maintain technical accuracy for construction/engineering terms
2. Keep brand names (KAN-BUD, OpenAI, etc.) unchanged
3. Keep file extensions (PDF, DWG) unchanged  
4. Keep technical standards (HVAC, ADA, GDPR) unchanged
5. Translate UI elements naturally for the target language
6. Use appropriate business/professional language
7. Consider local construction terminology and standards
8. For measurement units, adapt to local conventions where appropriate

Format: Return ONLY a valid JSON object with the translated key-value pairs.

Sample terms to translate:
{json.dumps(sample_keys, indent=2, ensure_ascii=False)}

Full translation list:
{json.dumps(missing_keys, indent=2, ensure_ascii=False)}

Return the translations as a JSON object with the same keys but translated values.
"""

        return prompt

    def _translate_with_groq(self, prompt: str) -> Dict[str, str]:
        """Translate using Groq service"""
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional technical translator. Return only valid JSON with translated key-value pairs. Do not include any explanatory text before or after the JSON."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=4000
            )

            result_text = response.choices[0].message.content.strip()
            
            # Multiple attempts to extract valid JSON
            json_candidates = []
            
            # Method 1: Direct parsing
            json_candidates.append(result_text)
            
            # Method 2: Remove markdown code blocks
            if '```json' in result_text:
                try:
                    start = result_text.find('```json') + 7
                    end = result_text.find('```', start)
                    if end != -1:
                        json_candidates.append(result_text[start:end].strip())
                except:
                    pass
            
            # Method 3: Extract first JSON object
            try:
                import re
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', result_text, re.DOTALL)
                if json_match:
                    json_candidates.append(json_match.group())
            except:
                pass
            
            # Method 4: Find content between first { and last }
            try:
                start_idx = result_text.find('{')
                end_idx = result_text.rfind('}')
                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    json_candidates.append(result_text[start_idx:end_idx+1])
            except:
                pass
            
            # Try to parse each candidate
            for candidate in json_candidates:
                if not candidate:
                    continue
                    
                try:
                    # Clean up common JSON issues
                    cleaned = candidate.strip()
                    # Remove trailing commas
                    cleaned = re.sub(r',\s*}', '}', cleaned)
                    cleaned = re.sub(r',\s*]', ']', cleaned)
                    
                    result = json.loads(cleaned)
                    if isinstance(result, dict):
                        return result
                except json.JSONDecodeError as je:
                    print(f"JSON parse attempt failed: {je}")
                    continue
                except Exception:
                    continue
            
            print(f"All JSON parsing attempts failed for response: {result_text[:200]}...")
            return {}

        except Exception as e:
            print(f"Groq translation error: {e}")
            return {}

    def _fallback_translation(self, target_lang: str, missing_keys: Dict[str, str]) -> Dict[str, str]:
        """Fallback translation when AI services fail"""
        return {key: f"[TRANSLATE] {value}" for key, value in missing_keys.items()}

    def _is_likely_untranslatable(self, text: str) -> bool:
        """Check if text is likely meant to stay in original language"""
        import re
        
        untranslatable_patterns = [
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
        
        for pattern in untranslatable_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False

    def _is_suspicious_translation(self, base_text: str, translated_text: str, target_lang: str) -> bool:
        """Check if translation seems suspicious or incorrect"""
        
        # Check if translation is just base text with different casing
        if base_text.lower() == translated_text.lower() and base_text != translated_text:
            return True
        
        # Check for obvious issues
        if len(translated_text) < 2:
            return True
            
        # Check if contains placeholder markers
        if any(marker in translated_text for marker in ['[AUTO]', '[TRANSLATE]', 'TODO:', 'FIXME:']):
            return True
            
        return False

def check_translation_quality_all_languages():
    """Main function to check translation quality for all languages using Polish as base"""
    ai_service = AITranslationService()
    results = ai_service.check_all_translations_quality('pl')
    return results

if __name__ == "__main__":
    check_translation_quality_all_languages()
