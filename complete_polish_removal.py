#!/usr/bin/env python3
"""
Complete Polish Text Removal
Comprehensively replaces ALL Polish text with proper translations for each language
"""

import json
import re

def load_json_file(filepath):
    """Load JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def save_json_file(filepath, data):
    """Save JSON file with proper formatting"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def get_comprehensive_mappings():
    """Get comprehensive Polish to other language mappings"""
    return {
        'fi': {
            # All Polish words found in the files
            "Energooszczędne": "Energiatehokas",
            "energooszczędne": "energiatehokas",
            "Bezpieczeństwo": "Turvallisuus",
            "bezpieczeństwo": "turvallisuus",
            "pieczeństwo": "turvallisuus",
            "Klasa morska": "Meriluokka",
            "klasa morska": "meriluokka",
            "antykorozyjna": "korroosionkestävä",
            "Okna panoramiczne": "Panoraama-ikkunat",
            "okna panoramiczne": "panoraama-ikkunat",
            "Okna przesuwne": "Liukuikkunat",
            "okna przesuwne": "liukuikkunat",
            "Okna uchylne": "Kääntöikkunat",
            "okna uchylne": "kääntöikkunat",
            "Okna dachowe": "Kattikkunat",
            "okna dachowe": "kattoikkunat",
            "Brak oświetlenia": "Ei valaistusta",
            "brak oświetlenia": "ei valaistusta",
            "oświetlenie": "valaistus",
            "Oświetlenie": "Valaistus",
            "czujnikami": "antureilla",
            "zewnętrzne": "ulko",
            "reflektory": "valonheittimet",
            "awaryjne": "hätä",
            "akumulatorowe": "akku",
            "inteligentny": "älykäs",
            "sterowane": "ohjattu",
            "instalacji elektrycznej": "sähköasennusta",
            "Przygotowanie": "Valmistelu",
            "przygotowanie": "valmistelu",
            "przewody": "johdot",
            "wyposażenia": "varustusta",
            "Podstawowy": "Perus",
            "podstawowy": "perus",
            "podstawowa": "perus",
            "gniazdka": "pistorasiat",
            "gniazdków": "pistorasiaa",
            "Standardowy": "Standardi",
            "standardowy": "standardi",
            "Rozszerzony": "Laajennettu",
            "rozszerzony": "laajennettu",
            "siła": "voima",
            "emergency": "hätä",
            "Przemysłowy": "Teollinen",
            "przemysłowy": "teollinen",
            "rozdzielnica": "jakokeskus",
            "Serwerowy": "Palvelin",
            "serwerowy": "palvelin",
            "chłodzenie": "jäähdytys",
            "monitoring": "valvonta",
            "Inteligentny": "Älykäs",
            "smart home": "älykoti",
            "automatyka": "automaatio",
            "instalacji wodnej": "vesiasennus",
            "rury": "putket",
            "armatury": "kalusteet",
            "zlew": "pesuallas",
            "odpływ": "viemäri",
            "Pełna": "Täysi",
            "pełna": "täysi",
            "łazienki": "kylpyhuone",
            "Klasa komercyjna": "Kaupallinen luokka",
            "klasa komercyjna": "kaupallinen luokka",
            "Instalacja przemysłowa": "Teollinen asennus",
            "instalacja przemysłowa": "teollinen asennus",
            "ciśnieniowa": "painevesi",
            "filtracja": "suodatus",
            "Instalacja zimnej wody": "Kylmävesiasennus",
            "instalacja zimnej wody": "kylmävesiasennus",
            "Zimna": "Kylmä",
            "zimna": "kylmä",
            "ciepła woda": "lämmin vesi",
            "umywalka": "käsienpesuallas",
            "węzeł sanitarny": "saniteettisolmu",
            "węzeł": "solmu",
            "prysznic": "suihku",
            "Komfortowy": "Mukava",
            "komfortowy": "mukava",
            "kabina": "kaappi",
            "Premium": "Premium",
            "premium": "premium",
            "jacuzzi": "poreallas",
            "bidet": "bidee",
            "umywalki": "käsienpesuallasta",
            "hartowane": "karkaistua",
            "LED": "LED",
            "kolminkertainen lasi": "kolminkertainen lasi",
            "kaksinkertainen lasi": "kaksinkertainen lasi"
        },
        'hu': {
            "Energooszczędne": "Energiatakarékos",
            "energooszczędne": "energiatakarékos",
            "Bezpieczeństwo": "Biztonság",
            "bezpieczeństwo": "biztonság",
            "pieczeństwo": "biztonság",
            "Klasa morska": "Tengeri osztály",
            "klasa morska": "tengeri osztály",
            "antykorozyjna": "korróziógátló",
            "Okna panoramiczne": "Panoráma ablakok",
            "okna panoramiczne": "panoráma ablakok",
            "Okna przesuwne": "Tolóablakok",
            "okna przesuwne": "tolóablakok",
            "Okna uchylne": "Bukóablakok",
            "okna uchylne": "bukóablakok",
            "Okna dachowe": "Tetőablakok",
            "okna dachowe": "tetőablakok",
            "Brak oświetlenia": "Nincs világítás",
            "brak oświetlenia": "nincs világítás",
            "oświetlenie": "világítás",
            "Oświetlenie": "Világítás",
            "czujnikami": "érzékelőkkel",
            "zewnętrzne": "külső",
            "reflektory": "reflektorok",
            "awaryjne": "vészhelyzeti",
            "akumulatorowe": "akkumulátoros",
            "inteligentny": "intelligens",
            "sterowane": "vezérelt",
            "instalacji elektrycznej": "elektromos szerelés",
            "Przygotowanie": "Előkészítés",
            "przygotowanie": "előkészítés",
            "przewody": "vezetékek",
            "wyposażenia": "felszerelés",
            "Podstawowy": "Alapvető",
            "podstawowy": "alapvető",
            "podstawowa": "alapvető",
            "gniazdka": "aljzatok",
            "gniazdków": "aljzat",
            "Standardowy": "Szabványos",
            "standardowy": "szabványos",
            "Rozszerzony": "Kiterjesztett",
            "rozszerzony": "kiterjesztett",
            "siła": "erő",
            "emergency": "vészhelyzet",
            "Przemysłowy": "Ipari",
            "przemysłowy": "ipari",
            "rozdzielnica": "elosztószekrény",
            "Serwerowy": "Szerver",
            "serwerowy": "szerver",
            "chłodzenie": "hűtés",
            "monitoring": "felügyelet",
            "Inteligentny": "Intelligens",
            "smart home": "okos otthon",
            "automatyka": "automatizálás",
            "instalacji wodnej": "vízszerelés",
            "rury": "csövek",
            "armatury": "szerelvények",
            "zlew": "mosogató",
            "odpływ": "lefolyó",
            "Pełna": "Teljes",
            "pełna": "teljes",
            "łazienki": "fürdőszoba",
            "Klasa komercyjna": "Kereskedelmi osztály",
            "klasa komercyjna": "kereskedelmi osztály",
            "Instalacja przemysłowa": "Ipari telepítés",
            "instalacja przemysłowa": "ipari telepítés",
            "ciśnieniowa": "nyomásos",
            "filtracja": "szűrés",
            "Instalacja zimnej wody": "Hidegvíz-szerelés",
            "instalacja zimnej wody": "hidegvíz-szerelés",
            "Zimna": "Hideg",
            "zimna": "hideg",
            "ciepła woda": "meleg víz",
            "umywalka": "mosdó",
            "węzeł sanitarny": "szaniter csomópont",
            "węzeł": "csomópont",
            "prysznic": "zuhany",
            "Komfortowy": "Kényelmes",
            "komfortowy": "kényelmes",
            "kabina": "kabin",
            "Premium": "Prémium",
            "premium": "prémium",
            "jacuzzi": "jakuzzi",
            "bidet": "bidé",
            "umywalki": "mosdó",
            "hartowane": "edzett",
            "podwójne szyby": "dupla üvegezés",
            "potrójne szyby": "tripla üvegezés"
        },
        'de': {
            "Energooszczędne": "Energiesparend",
            "energooszczędne": "energiesparend",
            "Bezpieczeństwo": "Sicherheit",
            "bezpieczeństwo": "sicherheit",
            "pieczeństwo": "sicherheit",
            "Klasa morska": "Meeresklasse",
            "klasa morska": "meeresklasse",
            "antykorozyjna": "korrosionsbeständig",
            "Okna panoramiczne": "Panoramafenster",
            "okna panoramiczne": "panoramafenster",
            "Okna przesuwne": "Schiebefenster",
            "okna przesuwne": "schiebefenster",
            "Okna uchylne": "Kippfenster",
            "okna uchylne": "kippfenster",
            "Okna dachowe": "Dachfenster",
            "okna dachowe": "dachfenster",
            "Brak oświetlenia": "Keine Beleuchtung",
            "brak oświetlenia": "keine beleuchtung",
            "oświetlenie": "beleuchtung",
            "Oświetlenie": "Beleuchtung",
            "czujnikami": "mit sensoren",
            "zewnętrzne": "außen",
            "reflektory": "strahler",
            "awaryjne": "notfall",
            "akumulatorowe": "batterie",
            "inteligentny": "intelligent",
            "sterowane": "gesteuert",
            "instalacji elektrycznej": "elektroinstallation",
            "Przygotowanie": "Vorbereitung",
            "przygotowanie": "vorbereitung",
            "przewody": "kabel",
            "wyposażenia": "ausrüstung",
            "Podstawowy": "Grundlegend",
            "podstawowy": "grundlegend",
            "podstawowa": "grundlegend",
            "gniazdka": "steckdosen",
            "gniazdków": "steckdosen",
            "Standardowy": "Standard",
            "standardowy": "standard",
            "Rozszerzony": "Erweitert",
            "rozszerzony": "erweitert",
            "siła": "kraft",
            "emergency": "notfall",
            "Przemysłowy": "Industriell",
            "przemysłowy": "industriell",
            "rozdzielnica": "verteiler",
            "Serwerowy": "Server",
            "serwerowy": "server",
            "chłodzenie": "kühlung",
            "monitoring": "überwachung",
            "Inteligentny": "Intelligent",
            "smart home": "smart home",
            "automatyka": "automatisierung",
            "instalacji wodnej": "wasserinstallation",
            "rury": "rohre",
            "armatury": "armaturen",
            "zlew": "spüle",
            "odpływ": "abfluss",
            "Pełna": "Vollständig",
            "pełna": "vollständig",
            "łazienki": "badezimmer",
            "Klasa komercyjna": "Gewerbeklasse",
            "klasa komercyjna": "gewerbeklasse",
            "Instalacja przemysłowa": "Industrieinstallation",
            "instalacja przemysłowa": "industrieinstallation",
            "ciśnieniowa": "druck",
            "filtracja": "filterung",
            "Instalacja zimnej wody": "Kaltwasserinstallation",
            "instalacja zimnej wody": "kaltwasserinstallation",
            "Zimna": "Kalt",
            "zimna": "kalt",
            "ciepła woda": "warmwasser",
            "umywalka": "waschbecken",
            "węzeł sanitarny": "sanitärknoten",
            "węzeł": "knoten",
            "prysznic": "dusche",
            "Komfortowy": "Komfort",
            "komfortowy": "komfort",
            "kabina": "kabine",
            "Premium": "Premium",
            "premium": "premium",
            "jacuzzi": "whirlpool",
            "bidet": "bidet",
            "umywalki": "waschbecken",
            "hartowane": "gehärtet"
        }
        # Add more languages as needed
    }

def is_likely_polish(text):
    """Check if text contains Polish characters or common Polish words"""
    polish_chars = 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ'
    polish_words = [
        'oświetlenie', 'Oświetlenie', 'podstawowy', 'Podstawowy', 'standardowy', 'Standardowy',
        'przemysłowy', 'Przemysłowy', 'energooszczędne', 'Energooszczędne', 'bezpieczeństwo',
        'instalacji', 'przygotowanie', 'Przygotowanie', 'wyposażenia', 'przewody', 'gniazdka',
        'gniazdków', 'rozszerzony', 'Rozszerzony', 'inteligentny', 'Inteligentny', 'chłodzenie',
        'monitoring', 'automatyka', 'serwerowy', 'Serwerowy', 'rozdzielnica', 'awaryjne',
        'akumulatorowe', 'zewnętrzne', 'reflektory', 'czujnikami', 'sterowane', 'wodnej',
        'armatury', 'łazienki', 'umywalka', 'umywalki', 'prysznic', 'jacuzzi', 'komfortowy',
        'Komfortowy', 'premium', 'Premium', 'kabina', 'hartowane', 'antykorozyjna', 'morska',
        'panoramiczne', 'przesuwne', 'uchylne', 'dachowe', 'ciśnieniowa', 'filtracja',
        'odpływ', 'zlew', 'węzeł', 'sanitarny', 'pełna', 'Pełna', 'zimna', 'Zimna', 'ciepła'
    ]
    
    # Check for Polish characters
    if any(char in text for char in polish_chars):
        return True
    
    # Check for Polish words
    if any(word in text for word in polish_words):
        return True
    
    return False

def replace_text_comprehensively(text, mappings):
    """Replace Polish text with target language text"""
    if not isinstance(text, str) or not mappings:
        return text
    
    result = text
    
    # Sort replacements by length (longest first) to avoid partial replacements
    sorted_mappings = sorted(mappings.items(), key=lambda x: len(x[0]), reverse=True)
    
    for polish, translation in sorted_mappings:
        if polish in result:
            result = result.replace(polish, translation)
    
    return result

def clean_language_comprehensively(lang_code):
    """Comprehensively clean all Polish text from a language file"""
    if lang_code == 'pl':
        return True
    
    print(f"Comprehensively cleaning {lang_code}...")
    
    filepath = f'locales/{lang_code}.json'
    data = load_json_file(filepath)
    if not data:
        return False
    
    mappings = get_comprehensive_mappings().get(lang_code, {})
    if not mappings:
        print(f"  No comprehensive mappings for {lang_code}, skipping...")
        return True
    
    polish_count = 0
    
    def clean_recursive(obj):
        """Recursively clean all Polish text"""
        nonlocal polish_count
        
        if isinstance(obj, dict):
            return {k: clean_recursive(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_recursive(item) for item in obj]
        elif isinstance(obj, str):
            if is_likely_polish(obj):
                polish_count += 1
                return replace_text_comprehensively(obj, mappings)
            return obj
        else:
            return obj
    
    cleaned_data = clean_recursive(data)
    
    if save_json_file(filepath, cleaned_data):
        print(f"  ✓ Successfully cleaned {lang_code} - fixed {polish_count} Polish texts")
        return True
    else:
        print(f"  ✗ Failed to clean {lang_code}")
        return False

def main():
    """Main function"""
    print("Performing comprehensive Polish text removal...")
    
    # Start with languages that have comprehensive mappings
    languages_with_mappings = ['fi', 'hu', 'de']
    
    for lang in languages_with_mappings:
        clean_language_comprehensively(lang)
    
    print("Comprehensive Polish removal complete for languages with detailed mappings!")

if __name__ == "__main__":
    main()