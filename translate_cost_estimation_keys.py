
import json
import os
from groq import Groq

def translate_cost_estimation_keys():
    """Translate the new cost estimation keys to all languages"""
    
    # Initialize Groq client
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("❌ Error: GROQ_API_KEY not found in environment variables")
        print("Please set your Groq API key in the Secrets tool")
        return
    
    client = Groq(api_key=api_key)
    
    # Load Polish translations (source)
    with open('locales/pl.json', 'r', encoding='utf-8') as f:
        pl_data = json.load(f)
    
    # New keys that need translation
    new_keys = {
        "cost_estimation.estimate_title": "💰 Szacunkowa Wycena Projektu",
        "cost_estimation.cost_breakdown_title": "Podział Kosztów:",
        "cost_estimation.base_container_line": "Kontener bazowy:",
        "cost_estimation.modifications_equipment_line": "Modyfikacje i wyposażenie:",
        "cost_estimation.total_cost_line": "CAŁKOWITY KOSZT:",
        "cost_estimation.important_warning": "⚠️ Ważne:",
        "cost_estimation.preliminary_estimate_full": "To wstępne szacowanie. Ostateczna cena zależy od szczegółowych specyfikacji, aktualnych cen materiałów i dostępności. Dla dokładnej wyceny skontaktuj się z naszym zespołem.",
        "cost_estimation.configuration_saved_success": "✅ Konfiguracja zapisana pomyślnie!"
    }
    
    # Language mappings
    languages = {
        'de': 'German',
        'nl': 'Dutch', 
        'cs': 'Czech',
        'hu': 'Hungarian',
        'es': 'Spanish',
        'it': 'Italian',
        'sv': 'Swedish',
        'fi': 'Finnish',
        'uk': 'Ukrainian',
        'sk': 'Slovak',
        'fr': 'French'
    }
    
    for lang_code, lang_name in languages.items():
        print(f"Translating to {lang_name} ({lang_code})...")
        
        # Load existing translation file
        file_path = f'locales/{lang_code}.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lang_data = json.load(f)
        except FileNotFoundError:
            print(f"Warning: {file_path} not found, skipping...")
            continue
        except json.JSONDecodeError as e:
            print(f"JSON decode error in {file_path}: {e}")
            print(f"Skipping {lang_code} due to malformed JSON...")
            continue
        
        # Ensure cost_estimation section exists
        if 'cost_estimation' not in lang_data:
            lang_data['cost_estimation'] = {}
        
        # Translate each new key
        for key_path, polish_text in new_keys.items():
            key_name = key_path.split('.')[-1]  # Get the last part after the dot
            
            if key_name in lang_data['cost_estimation']:
                print(f"  Key {key_name} already exists, skipping...")
                continue
            
            try:
                # Create translation prompt
                prompt = f"""
                Translate this Polish text to {lang_name} for a container modification cost estimation interface.

                Polish text: "{polish_text}"

                Requirements:
                - Maintain professional business tone
                - Keep emojis and symbols (💰, ⚠️, ✅)
                - Preserve formatting (colons, punctuation)
                - Use appropriate currency/business terminology
                - Make it sound natural in {lang_name}

                Translate to {lang_name}:
                """
                
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=200
                )
                
                translated_text = response.choices[0].message.content.strip()
                
                # Remove quotes if present
                if translated_text.startswith('"') and translated_text.endswith('"'):
                    translated_text = translated_text[1:-1]
                
                # Add to language data
                lang_data['cost_estimation'][key_name] = translated_text
                print(f"  Added {key_name}: {translated_text}")
                
            except Exception as e:
                print(f"  Error translating {key_name}: {e}")
                continue
        
        # Save updated translation file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(lang_data, f, ensure_ascii=False, indent=2)
            print(f"✅ Updated {lang_code}.json")
        except Exception as e:
            print(f"❌ Error saving {lang_code}.json: {e}")
    
    print("\n🎉 Translation of cost estimation keys completed!")

if __name__ == "__main__":
    translate_cost_estimation_keys()
