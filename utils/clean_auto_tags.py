
import json
import os

def clean_auto_tags():
    """Remove all [AUTO] tags from translation files"""
    locales_dir = "locales"
    languages = ['de', 'nl', 'cs', 'hu', 'pl', 'en', 'es', 'it', 'sv', 'fi', 'uk', 'sk', 'fr']
    
    def clean_dict(data):
        """Recursively clean [AUTO] tags from dictionary"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and value.startswith("[AUTO] "):
                    data[key] = value.replace("[AUTO] ", "")
                elif isinstance(value, dict):
                    clean_dict(value)
        return data
    
    for lang in languages:
        filepath = os.path.join(locales_dir, f"{lang}.json")
        
        if not os.path.exists(filepath):
            continue
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clean the data
            clean_dict(data)
            
            # Save back
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Cleaned [AUTO] tags from {lang}.json")
            
        except Exception as e:
            print(f"❌ Error processing {lang}.json: {e}")

if __name__ == "__main__":
    clean_auto_tags()
    print("🎉 All [AUTO] tags have been removed from translation files!")
