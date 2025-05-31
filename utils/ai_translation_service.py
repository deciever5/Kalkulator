
import json
import os
from typing import Dict, List, Any, Optional
from utils.ai_services import OpenAIService, AnthropicService, GroqService

class AITranslationService:
    """AI-powered translation service for technical container terminology"""
    
    def __init__(self):
        self.services = {
            'groq': GroqService,
            'openai': OpenAIService,
            'anthropic': AnthropicService
        }
    
    def translate_missing_keys(self, source_lang: str, target_lang: str, missing_keys: Dict[str, str]) -> Dict[str, str]:
        """Translate missing translation keys using AI services"""
        
        if not missing_keys:
            return {}
            
        # Build context-aware translation prompt
        prompt = self._build_translation_prompt(source_lang, target_lang, missing_keys)
        
        # Try each AI service in order
        for service_name, service_class in self.services.items():
            try:
                print(f"Attempting translation with {service_name}...")
                service = service_class()
                
                if service_name == 'groq':
                    result = self._translate_with_groq(service, prompt)
                elif service_name == 'openai':
                    result = self._translate_with_openai(service, prompt)
                elif service_name == 'anthropic':
                    result = self._translate_with_anthropic(service, prompt)
                
                if result and isinstance(result, dict):
                    print(f"✅ Successfully translated {len(result)} keys with {service_name}")
                    return result
                    
            except Exception as e:
                print(f"❌ {service_name} translation failed: {e}")
                continue
        
        print("⚠️ All AI translation services failed, using fallback")
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
    
    def _translate_with_groq(self, service: GroqService, prompt: str) -> Dict[str, str]:
        """Translate using Groq service"""
        try:
            response = service.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional technical translator. Return only valid JSON with translated key-value pairs."
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
            # Clean up response to ensure valid JSON
            if result_text.startswith('```json'):
                result_text = result_text[7:-3]
            elif result_text.startswith('```'):
                result_text = result_text[3:-3]
                
            return json.loads(result_text)
            
        except Exception as e:
            print(f"Groq translation error: {e}")
            return {}
    
    def _translate_with_openai(self, service: OpenAIService, prompt: str) -> Dict[str, str]:
        """Translate using OpenAI service"""
        try:
            response = service.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional technical translator. Return only valid JSON with translated key-value pairs."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=4000
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"OpenAI translation error: {e}")
            return {}
    
    def _translate_with_anthropic(self, service: AnthropicService, prompt: str) -> Dict[str, str]:
        """Translate using Anthropic service"""
        try:
            response = service.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": prompt + "\n\nReturn only valid JSON with the translations."
                    }
                ]
            )
            
            result_text = response.content[0].text.strip()
            # Clean up response to ensure valid JSON
            if result_text.startswith('```json'):
                result_text = result_text[7:-3]
            elif result_text.startswith('```'):
                result_text = result_text[3:-3]
                
            return json.loads(result_text)
            
        except Exception as e:
            print(f"Anthropic translation error: {e}")
            return {}
    
    def _fallback_translation(self, target_lang: str, missing_keys: Dict[str, str]) -> Dict[str, str]:
        """Fallback translation when AI services fail"""
        # Keep English values but mark them as needing translation
        return {key: f"[TRANSLATE] {value}" for key, value in missing_keys.items()}

def translate_incomplete_languages():
    """Fill missing translations for incomplete languages using AI"""
    
    print("🤖 Starting AI-powered translation for incomplete languages...")
    
    # Load English as reference
    with open('locales/en.json', 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    def get_all_keys_flat(data: Dict, prefix: str = "") -> Dict[str, str]:
        """Get all keys from nested dict as flat key-value pairs"""
        result = {}
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                result.update(get_all_keys_flat(value, full_key))
            elif isinstance(value, str):
                result[full_key] = value
        return result
    
    def set_nested_value(data: Dict, key_path: str, value: str):
        """Set nested value using dot notation"""
        keys = key_path.split('.')
        current = data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value
    
    en_keys = get_all_keys_flat(en_data)
    incomplete_languages = ['fi', 'uk', 'sk', 'fr']
    
    ai_translator = AITranslationService()
    
    for lang in incomplete_languages:
        print(f"\n🌐 Processing {lang.upper()}...")
        
        # Load existing translations
        lang_path = f'locales/{lang}.json'
        with open(lang_path, 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        
        existing_keys = get_all_keys_flat(lang_data)
        
        # Find missing keys
        missing_keys = {}
        for key, value in en_keys.items():
            if key not in existing_keys:
                missing_keys[key] = value
        
        print(f"Found {len(missing_keys)} missing translations for {lang}")
        
        if missing_keys:
            # Translate in batches to avoid token limits
            batch_size = 50
            translated_count = 0
            
            for i in range(0, len(missing_keys), batch_size):
                batch_keys = dict(list(missing_keys.items())[i:i+batch_size])
                print(f"Translating batch {i//batch_size + 1} ({len(batch_keys)} keys)...")
                
                translations = ai_translator.translate_missing_keys('en', lang, batch_keys)
                
                # Add translations to language data
                for key, translated_value in translations.items():
                    set_nested_value(lang_data, key, translated_value)
                    translated_count += 1
            
            # Save updated language file
            with open(lang_path, 'w', encoding='utf-8') as f:
                json.dump(lang_data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
            
            print(f"✅ {lang.upper()}: Added {translated_count} AI translations")
        
        else:
            print(f"✅ {lang.upper()}: No missing translations found")
    
    print("\n🎉 AI translation complete! All languages now have complete translations.")
    print("📝 Note: Review and refine the AI translations as needed for your specific business context.")

if __name__ == "__main__":
    translate_incomplete_languages()
