#!/usr/bin/env python3
"""
Comprehensive Translation Cleanup
Fixes ALL Polish text mixed into other language files with proper translations
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

def get_polish_to_language_mappings():
    """Get comprehensive mappings from Polish to each language"""
    return {
        'en': {
            # Common Polish words to English
            "Bez": "Without",
            "bez": "without",
            "Podstawowe": "Basic",
            "podstawowe": "basic",
            "Standardowe": "Standard",
            "standardowe": "standard",
            "Rozszerzone": "Extended",
            "rozszerzone": "extended",
            "Przemysłowe": "Industrial",
            "przemysłowe": "industrial",
            "Komfortowe": "Comfort",
            "komfortowe": "comfort",
            "Premium": "Premium",
            "premium": "premium",
            "Pełne": "Full",
            "pełne": "full",
            "Żadne": "None",
            "żadne": "none",
            "Przygotowanie": "Preparation",
            "przygotowanie": "preparation",
            "Instalacja": "Installation",
            "instalacja": "installation",
            "System": "System",
            "system": "system",
            "Montaż": "Assembly",
            "montaż": "assembly",
            "Transport": "Transport",
            "transport": "transport",
            "Dostawa": "Delivery",
            "dostawa": "delivery",
            "Wyposażenie": "Equipment",
            "wyposażenie": "equipment",
            "Sprzęt": "Appliances",
            "sprzęt": "appliances",
            "Przestrzeń otwarta": "Open space",
            "bez podziałów": "no partitions",
            "podwójne szyby": "double glazing",
            "potrójne szyby": "triple glazing",
            "instalacji elektrycznej": "electrical installation",
            "instalacji wodnej": "water installation",
            "przewody bez wyposażenia": "wiring without equipment",
            "rury bez armatury": "pipes without fixtures",
            "wzmocnione zamki": "reinforced locks",
            "kraty okienne": "window bars",
            "czujniki": "sensors",
            "syrena": "siren",
            "monitoring": "monitoring",
            "kontrola dostępu": "access control",
            "biometria": "biometrics",
            "centralne": "central",
            "sejf": "safe",
            "systemy gazowe": "gas systems",
            "panikowa": "panic",
            "blacha kontenerowa": "container sheet",
            "standardowa": "standard",
            "trapezoidalna": "trapezoidal",
            "kasetowa": "cassette",
            "płaska": "flat",
            "przetłaczana": "embossed",
            "winylowy": "vinyl",
            "imitacja drewna": "wood imitation",
            "nowoczesny": "modern",
            "strukturalny": "structural",
            "silikonowy": "silicone",
            "akrylowy": "acrylic",
            "drewniana": "wooden",
            "termo": "thermo",
            "egzotyczna": "exotic",
            "kompozytowe": "composite",
            "klinkierowa": "clinker",
            "lica": "face",
            "elewacyjna": "facade",
            "naturalny": "natural",
            "sztuczny": "artificial",
            "dodatkowych otworów": "additional openings",
            "drzwi": "doors",
            "okna": "windows",
            "sztuki": "pieces",
            "serwisowe": "service",
            "awaryjne": "emergency",
            "garażowa": "garage",
            "segmentowa": "sectional",
            "rolowana": "roller",
            "załadunkowa": "loading",
            "hydrauliczna": "hydraulic",
            "platforma": "platform",
            "wentylacyjne": "ventilation",
            "kratki": "grilles",
            "żaluzje": "louvers",
            "dachowe": "roof",
            "świetliki": "skylights",
            "niestandardowe": "custom",
            "nietypowe wymiary": "non-standard sizes",
            "przeciwpożarowych": "fire safety",
            "gaśnica": "extinguisher",
            "czujka dymu": "smoke detector",
            "alarmowy": "alarm",
            "oświetlenie awaryjne": "emergency lighting",
            "tryskacze": "sprinklers",
            "ewakuacja": "evacuation",
            "gazowe": "gas",
            "próg": "threshold",
            "podjazd": "ramp",
            "rampa": "ramp",
            "wózków inwalidzkich": "wheelchair",
            "winda": "lift",
            "hydrauliczna": "hydraulic",
            "niepełnosprawnych": "disabled",
            "zgodność": "compliance",
            "szerokie drzwi": "wide doors",
            "uchwyty": "grab bars",
            "powłoka": "coating",
            "szary jasny": "light gray",
            "ulepszona": "improved",
            "trwałość": "durability",
            "morska": "marine",
            "środowiska przybrzeżne": "coastal environments",
            "przemysłowa": "industrial",
            "agresywne": "aggressive",
            "specjalne kolory": "special colors",
            "tekstury": "textures",
            "lokalny": "local",
            "regionalny": "regional",
            "krajowy": "national",
            "cały kraj": "whole country",
            "środkowa": "central",
            "zachodnia": "western",
            "międzynarodowy": "international",
            "poza Europą": "outside Europe",
            "standardowy": "standard",
            "naczep": "semi-trailer",
            "specjalny": "special",
            "ponadgabarytowy": "oversized",
            "dźwigiem": "crane",
            "na miejscu": "on site",
            "wielokontenerowy": "multi-container",
            "jednostki": "units",
            "pozycjonowanie": "positioning",
            "poziomowanie": "leveling",
            "podłączenia": "connections",
            "testy": "tests",
            "kompletna": "complete",
            "pusty kontener": "empty container",
            "biurko": "desk",
            "krzesła": "chairs",
            "szafa": "cabinet",
            "komplet mebli": "furniture set",
            "kompletne wyposażenie": "complete equipment",
            "lodówka": "refrigerator",
            "mikrofalówka": "microwave",
            "zestaw kuchenny": "kitchen set",
            "pralka": "washing machine",
            "gospodarstwa domowego": "household",
            "internet": "internet",
            "sieć": "network",
            "telefonia": "telephony",
            "serwerownia": "server room",
            "bezpieczeństwo": "security"
        },
        'de': {
            "Bez": "Ohne",
            "bez": "ohne",
            "Podstawowe": "Grundlegend",
            "podstawowe": "grundlegend",
            "Standardowe": "Standard",
            "standardowe": "standard",
            "Rozszerzone": "Erweitert",
            "rozszerzone": "erweitert",
            "Przemysłowe": "Industriell",
            "przemysłowe": "industriell",
            "Przestrzeń otwarta": "Offener Raum",
            "bez podziałów": "keine Trennwände",
            "podwójne szyby": "Doppelverglasung",
            "potrójne szyby": "Dreifachverglasung",
            "instalacji elektrycznej": "Elektroinstallation",
            "instalacji wodnej": "Wasserinstallation",
            "przewody bez wyposażenia": "Verkabelung ohne Ausrüstung",
            "rury bez armatury": "Rohre ohne Armaturen",
            "wzmocnione zamki": "verstärkte Schlösser",
            "kraty okienne": "Fenstergitter"
        },
        'fr': {
            "Bez": "Sans",
            "bez": "sans",
            "Podstawowe": "De base",
            "podstawowe": "de base",
            "Standardowe": "Standard",
            "standardowe": "standard",
            "Rozszerzone": "Étendu",
            "rozszerzone": "étendu",
            "Przemysłowe": "Industriel",
            "przemysłowe": "industriel",
            "Przestrzeń otwarta": "Espace ouvert",
            "bez podziałów": "sans cloisons",
            "podwójne szyby": "double vitrage",
            "potrójne szyby": "triple vitrage",
            "instalacji elektrycznej": "installation électrique",
            "instalacji wodnej": "installation d'eau",
            "przewody bez wyposażenia": "câblage sans équipement",
            "rury bez armatury": "tuyaux sans raccords",
            "wzmocnione zamki": "serrures renforcées",
            "kraty okienne": "barreaux de fenêtre"
        },
        'nl': {
            "Bez": "Zonder",
            "bez": "zonder",
            "Podstawowe": "Basis",
            "podstawowe": "basis",
            "Standardowe": "Standaard",
            "standardowe": "standaard",
            "Rozszerzone": "Uitgebreid",
            "rozszerzone": "uitgebreid",
            "Przemysłowe": "Industrieel",
            "przemysłowe": "industrieel",
            "Przestrzeń otwarta": "Open ruimte",
            "bez podziałów": "geen scheidingswanden",
            "podwójne szyby": "dubbele beglazing",
            "potrójne szyby": "drievoudige beglazing",
            "instalacji elektrycznej": "elektrische installatie",
            "instalacji wodnej": "waterinstallatie",
            "przewody bez wyposażenia": "bedrading zonder uitrusting",
            "rury bez armatury": "leidingen zonder fittingen",
            "wzmocnione zamki": "verstevigde sloten",
            "kraty okienne": "tralies"
        },
        'it': {
            "Bez": "Senza",
            "bez": "senza",
            "Podstawowe": "Di base",
            "podstawowe": "di base",
            "Standardowe": "Standard",
            "standardowe": "standard",
            "Rozszerzone": "Esteso",
            "rozszerzone": "esteso",
            "Przemysłowe": "Industriale",
            "przemysłowe": "industriale",
            "Przestrzeń otwarta": "Spazio aperto",
            "bez podziałów": "senza partizioni",
            "podwójne szyby": "doppi vetri",
            "potrójne szyby": "tripli vetri",
            "instalacji elektrycznej": "impianto elettrico",
            "instalacji wodnej": "impianto idrico",
            "przewody bez wyposażenia": "cablaggio senza attrezzature",
            "rury bez armatury": "tubazioni senza raccordi",
            "wzmocnione zamki": "serrature rinforzate",
            "kraty okienne": "grate alle finestre"
        },
        'es': {
            "Bez": "Sin",
            "bez": "sin",
            "Podstawowe": "Básico",
            "podstawowe": "básico",
            "Standardowe": "Estándar",
            "standardowe": "estándar",
            "Rozszerzone": "Ampliado",
            "rozszerzone": "ampliado",
            "Przemysłowe": "Industrial",
            "przemysłowe": "industrial",
            "Przestrzeń otwarta": "Espacio abierto",
            "bez podziałów": "sin particiones",
            "podwójne szyby": "doble acristalamiento",
            "potrójne szyby": "triple acristalamiento",
            "instalacji elektrycznej": "instalación eléctrica",
            "instalacji wodnej": "instalación de agua",
            "przewody bez wyposażenia": "cableado sin equipos",
            "rury bez armatury": "tuberías sin accesorios",
            "wzmocnione zamki": "cerraduras reforzadas",
            "kraty okienne": "rejas de ventana"
        },
        'cs': {
            "Bez": "Bez",
            "bez": "bez",
            "Podstawowe": "Základní",
            "podstawowe": "základní",
            "Standardowe": "Standardní",
            "standardowe": "standardní",
            "Rozszerzone": "Rozšířený",
            "rozszerzone": "rozšířený",
            "Przemysłowe": "Průmyslový",
            "przemysłowe": "průmyslový",
            "Przestrzeń otwarta": "Otevřený prostor",
            "bez podziałów": "bez příček",
            "podwójne szyby": "dvojité zasklení",
            "potrójne szyby": "trojité zasklení",
            "instalacji elektrycznej": "elektrická instalace",
            "instalacji wodnej": "vodovodní instalace",
            "przewody bez wyposażenia": "kabeláž bez vybavení",
            "rury bez armatury": "potrubí bez armatur",
            "wzmocnione zamki": "zesílené zámky",
            "kraty okienne": "okenní mříže"
        },
        'sk': {
            "Bez": "Bez",
            "bez": "bez",
            "Podstawowe": "Základné",
            "podstawowe": "základné",
            "Standardowe": "Štandardné",
            "standardowe": "štandardné",
            "Rozszerzone": "Rozšírené",
            "rozszerzone": "rozšírené",
            "Przemysłowe": "Priemyselné",
            "przemysłowe": "priemyselné",
            "Przestrzeń otwarta": "Otvorený priestor",
            "bez podziałów": "bez priečok",
            "podwójne szyby": "dvojité zasklenie",
            "potrójne szyby": "trojité zasklenie"
        },
        'hu': {
            "Bez": "Nélkül",
            "bez": "nélkül",
            "Podstawowe": "Alapvető",
            "podstawowe": "alapvető",
            "Standardowe": "Szabványos",
            "standardowe": "szabványos",
            "Rozszerzone": "Kiterjesztett",
            "rozszerzone": "kiterjesztett",
            "Przemysłowe": "Ipari",
            "przemysłowe": "ipari",
            "Przestrzeń otwarta": "Nyitott tér",
            "bez podziałów": "válaszfalak nélkül",
            "podwójne szyby": "dupla üvegezés",
            "potrójne szyby": "tripla üvegezés"
        },
        'sv': {
            "Bez": "Utan",
            "bez": "utan",
            "Podstawowe": "Grundläggande",
            "podstawowe": "grundläggande",
            "Standardowe": "Standard",
            "standardowe": "standard",
            "Rozszerzone": "Utökad",
            "rozszerzone": "utökad",
            "Przemysłowe": "Industriell",
            "przemysłowe": "industriell",
            "Przestrzeń otwarta": "Öppet utrymme",
            "bez podziałów": "inga skiljeväggar",
            "podwójne szyby": "dubbelglas",
            "potrójne szyby": "trippelglas"
        },
        'fi': {
            "Bez": "Ilman",
            "bez": "ilman",
            "Podstawowe": "Perus",
            "podstawowe": "perus",
            "Standardowe": "Standardi",
            "standardowe": "standardi",
            "Rozszerzone": "Laajennettu",
            "rozszerzone": "laajennettu",
            "Przemysłowe": "Teollinen",
            "przemysłowe": "teollinen",
            "Przestrzeń otwarta": "Avoin tila",
            "bez podziałów": "ei väliseiniä",
            "podwójne szyby": "kaksinkertainen lasi",
            "potrójne szyby": "kolminkertainen lasi"
        },
        'uk': {
            "Bez": "Без",
            "bez": "без",
            "Podstawowe": "Базовий",
            "podstawowe": "базовий",
            "Standardowe": "Стандартний",
            "standardowe": "стандартний",
            "Rozszerzone": "Розширений",
            "rozszerzone": "розширений",
            "Przemysłowe": "Промисловий",
            "przemysłowe": "промисловий",
            "Przestrzeń otwarta": "Відкритий простір",
            "bez podziałów": "без перегородок",
            "podwójne szyby": "подвійне скління",
            "potrójne szyby": "потрійне скління"
        }
    }

def replace_polish_text(text, mappings):
    """Replace Polish text with appropriate language translation"""
    if not isinstance(text, str):
        return text
    
    result = text
    # Sort by length descending to replace longer phrases first
    for polish, translation in sorted(mappings.items(), key=lambda x: len(x[0]), reverse=True):
        if polish in result:
            result = result.replace(polish, translation)
    
    return result

def clean_language_file(lang_code):
    """Clean all Polish text from a language file"""
    if lang_code == 'pl':  # Skip Polish file
        return True
        
    print(f"Cleaning {lang_code}...")
    
    filepath = f'locales/{lang_code}.json'
    data = load_json_file(filepath)
    if not data:
        return False
    
    mappings = get_polish_to_language_mappings().get(lang_code, {})
    if not mappings:
        print(f"  No mappings defined for {lang_code}, skipping...")
        return True
    
    def clean_recursive(obj):
        """Recursively clean Polish text from nested structures"""
        if isinstance(obj, dict):
            return {k: clean_recursive(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_recursive(item) for item in obj]
        elif isinstance(obj, str):
            return replace_polish_text(obj, mappings)
        else:
            return obj
    
    cleaned_data = clean_recursive(data)
    
    if save_json_file(filepath, cleaned_data):
        print(f"  ✓ Successfully cleaned {lang_code}")
        return True
    else:
        print(f"  ✗ Failed to clean {lang_code}")
        return False

def main():
    """Main function"""
    print("Cleaning ALL Polish text from all language files...")
    
    languages = ['en', 'de', 'fr', 'nl', 'it', 'es', 'cs', 'sk', 'hu', 'sv', 'fi', 'uk']
    
    success_count = 0
    for lang in languages:
        if clean_language_file(lang):
            success_count += 1
    
    print(f"Comprehensive cleanup complete: {success_count}/{len(languages)} languages cleaned")

if __name__ == "__main__":
    main()