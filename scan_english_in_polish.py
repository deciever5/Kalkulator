
import json
import re

def load_json_file(file_path):
    """Load JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def get_all_keys_flat(data, prefix=""):
    """Recursively get all key-value pairs from nested dictionary"""
    items = {}
    for key, value in data.items():
        current_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            items.update(get_all_keys_flat(value, current_key))
        else:
            items[current_key] = value
    return items

def is_likely_english(text):
    """Check if text contains English words that should be translated"""
    if not isinstance(text, str):
        return False
    
    # Skip proper nouns and technical terms that shouldn't be translated
    proper_nouns = [
        'KAN-BUD', 'OpenAI', 'Anthropic', 'PDF', 'DWG', 'IoT', 'AI', 'HVAC', 
        'ADA', 'GDPR', 'VRV', 'VRF', 'LED', 'UPS', 'GPS', 'USB', 'WiFi',
        'Bluetooth', 'SMS', 'GPS', 'API', 'URL', 'HTTP', 'HTTPS', 'FTP',
        'C2', 'C3', 'C4', 'C5', 'C5M'  # Paint codes
    ]
    
    # Container size formats that are international
    size_patterns = [
        r'\d+ft', r'\d+x\d+', r'\d+m', r'\d+cm', r'\d+mm', r'\d+°C',
        r'\d+-\d+°C', r'\d+A', r'\d+W', r'\d+kW', r'\d+V'
    ]
    
    # Check if it's just a proper noun or technical term
    if text in proper_nouns:
        return False
    
    # Check if it matches size/technical patterns
    for pattern in size_patterns:
        if re.match(pattern, text):
            return False
    
    # Common English words that should be translated to Polish
    english_words = [
        'container', 'basic', 'standard', 'premium', 'luxury', 'system', 
        'analysis', 'configuration', 'installation', 'professional', 
        'advanced', 'delivery', 'transport', 'office', 'equipment', 
        'security', 'lighting', 'ventilation', 'electrical', 'plumbing',
        'drawing', 'technical', 'estimate', 'quote', 'comparison', 
        'visualization', 'custom', 'industrial', 'commercial', 'residential',
        'workshop', 'storage', 'medical', 'laboratory', 'restaurant',
        'retail', 'marine', 'outdoor', 'indoor', 'central', 'double',
        'high', 'cube', 'compact', 'multi', 'unit', 'refurbished',
        'dimensions', 'climate', 'zone', 'finish', 'level', 'flooring',
        'windows', 'doors', 'additional', 'modifications', 'reinforcement',
        'insulation', 'package', 'structural', 'fire', 'safety', 'emergency',
        'access', 'accessibility', 'heating', 'cooling', 'split', 'heat',
        'pump', 'energy', 'efficient', 'smart', 'none', 'with', 'without',
        'full', 'complete', 'partial', 'external', 'internal', 'automatic',
        'manual', 'digital', 'analog', 'wireless', 'wired', 'mobile',
        'portable', 'fixed', 'temporary', 'permanent', 'flexible', 'rigid'
    ]
    
    text_lower = text.lower()
    
    # Check for English words
    for word in english_words:
        if word in text_lower:
            # Make sure it's a whole word, not part of another word
            if re.search(r'\b' + word + r'\b', text_lower):
                return True
    
    # Check for common English patterns
    english_patterns = [
        r'\band\b', r'\bthe\b', r'\bwith\b', r'\bfor\b', r'\bin\b',
        r'\bon\b', r'\bat\b', r'\bto\b', r'\bfrom\b', r'\bof\b',
        r'\bis\b', r'\bare\b', r'\bwas\b', r'\bwere\b', r'\bhas\b',
        r'\bhave\b', r'\bcan\b', r'\bwill\b', r'\bshould\b', r'\bmust\b'
    ]
    
    for pattern in english_patterns:
        if re.search(pattern, text_lower):
            return True
    
    return False

def scan_english_in_polish():
    """Scan Polish translations for English text"""
    print("🔍 Scanning Polish translations for English text...")
    print("=" * 60)
    
    # Load Polish translations
    pl_data = load_json_file('locales/pl.json')
    if not pl_data:
        print("❌ Could not load Polish translations")
        return
    
    # Get all translations
    all_translations = get_all_keys_flat(pl_data)
    
    english_found = []
    
    for key, value in all_translations.items():
        if is_likely_english(value):
            english_found.append((key, value))
    
    if english_found:
        print(f"🚨 Found {len(english_found)} potentially English translations in Polish:")
        print("-" * 60)
        
        for key, value in english_found:
            print(f"📍 Key: {key}")
            print(f"   Value: '{value}'")
            print()
    else:
        print("✅ No obvious English translations found in Polish file")
    
    # Statistics
    total_keys = len(all_translations)
    english_count = len(english_found)
    percentage = (english_count / total_keys) * 100 if total_keys > 0 else 0
    
    print(f"📊 Summary:")
    print(f"   Total translations: {total_keys}")
    print(f"   English translations found: {english_count}")
    print(f"   Percentage needing translation: {percentage:.1f}%")

if __name__ == "__main__":
    scan_english_in_polish()
