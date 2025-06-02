#!/usr/bin/env python3
"""
Final Translation Cleanup
Systematically replaces all remaining mixed Polish/English text with proper translations
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

def get_complete_replacement_maps():
    """Get complete replacement mappings for all problematic text patterns"""
    return {
        'fi': {
            # Complete Finnish translations
            "Ilman systemów przeciwpożarowych": "Ei paloturvallisuusjärjestelmiä",
            "Perus (gaśnica, czujka dymu)": "Perus (sammutin, savuilmaisin)",
            "Standardi (system alarmowy, valaistus hätä)": "Standardi (hälytysjärjestelmä, hätävalaistus)",
            "Laajennettu (tryskacze, ewakuacja)": "Laajennettu (sprinklerit, evakuointi)",
            "Pełny system (gazowe, valvonta)": "Täysi järjestelmä (kaasunpoisto, valvonta)",
            "Dostęp standardi (próg 15-20cm)": "Tavallinen pääsy (15-20cm kynnys)",
            "Podjazd/rampa (dla wózków inwalidzkich)": "Luiska (pyörätuolipääsy)",
            "Winda hydrauliczna (dostęp dla niepełnosprawnych)": "Hydraulinen nostin (vammaispääsy)",
            "Täysi zgodność ADA (szerokie drzwi, uchwyty)": "Täysi ADA-yhteensopivuus (leveät ovet, käsijohteet)",
            "Powłoka standardowa C2 (RAL 7035 - szary jasny)": "Tavallinen pinnoite C2 (RAL 7035 - vaaleanharmaa)",
            "Powłoka ulepszona C3 (lepsza trwałość)": "Laajennettu pinnoite C3 (parannettu kestävyys)",
            "Powłoka morska C5M (środowiska przybrzeżne)": "Meriympäristön pinnoite C5M (rannikkoympäristöt)",
            "Powłoka przemysłowa C4 (środowiska agresywne)": "Teollisuuspinnoite C4 (aggressiiviset ympäristöt)",
            "Premium (specjalne kolory RAL, tekstury)": "Premium (erikois RAL-värit, tekstuurit)",
            "Lokalny (do 50km)": "Paikallinen (enintään 50km)",
            "Regionalny (50-200km)": "Alueellinen (50-200km)",
            "Krajowy (cały kraj)": "Kansallinen (koko maa)",
            "Europa Środkowa (DE, CZ, SK, AT)": "Keski-Eurooppa (DE, CZ, SK, AT)",
            "Europa Zachodnia (FR, NL, BE, LU)": "Länsi-Eurooppa (FR, NL, BE, LU)",
            "Międzynarodowy (poza Europą)": "Kansainvälinen (Euroopan ulkopuolella)",
            "Transport standardi (naczep 13.6m)": "Tavallinen kuljetus (13,6m puoliperävaunu)",
            "Transport specjalny (ponadgabarytowy)": "Erikoiskuljetus (ylimitoitettu kuorma)",
            "Transport z dźwigiem (montaż na miejscu)": "Nosturikuljetus (kokoaminen paikan päällä)",
            "Transport wielokontenerowy (2+ jednostki)": "Monikonttien kuljetus (2+ yksikköä)",
            "Ilman montażu (tylko dostawa)": "Ei kokoamista (vain toimitus)",
            "Montaż perus (pozycjonowanie, poziomowanie)": "Peruskokoaminen (sijoittelu, tasoitus)",
            "Montaż standardi (podłączenia, testy)": "Tavallinen kokoaminen (liitännät, testit)",
            "Montaż pełny (kompletna instalacja)": "Täysi kokoaminen (täydellinen asennus)",
            "Ilman varustusta (pusty kontener)": "Ei varustusta (tyhjä kontti)",
            "Perus (biurko, krzesła, szafa)": "Perus (pöytä, tuolit, kaappi)",
            "Standardi (komplet mebli, valaistus)": "Standardi (huonekaluvalikoima, valaistus)",
            "Pełne (kompletne wyposażenie": "Täysi (täydellinen varustus",
            "systemów": "järjestelmiä",
            "przeciwpożarowych": "paloturvallisuus",
            "gaśnica": "sammutin",
            "czujka dymu": "savuilmaisin",
            "system alarmowy": "hälytysjärjestelmä",
            "oświetlenie awaryjne": "hätävalaistus",
            "tryskacze": "sprinklerit",
            "ewakuacja": "evakuointi",
            "gazowe": "kaasunpoisto",
            "monitoring": "valvonta",
            "dostęp": "pääsy",
            "próg": "kynnys",
            "podjazd": "luiska",
            "rampa": "luiska",
            "wózków inwalidzkich": "pyörätuoli",
            "winda hydrauliczna": "hydraulinen nostin",
            "niepełnosprawnych": "vammaiset",
            "zgodność": "yhteensopivuus",
            "szerokie drzwi": "leveät ovet",
            "uchwyty": "käsijohteet",
            "powłoka": "pinnoite",
            "standardowa": "tavallinen",
            "ulepszona": "laajennettu",
            "trwałość": "kestävyys",
            "morska": "meriympäristö",
            "środowiska": "ympäristöt",
            "przybrzeżne": "rannikko",
            "przemysłowa": "teollisuus",
            "agresywne": "aggressiiviset",
            "specjalne kolory": "erikoisvärit",
            "tekstury": "tekstuurit",
            "lokalny": "paikallinen",
            "regionalny": "alueellinen",
            "krajowy": "kansallinen",
            "cały kraj": "koko maa",
            "środkowa": "keski",
            "zachodnia": "länsi",
            "międzynarodowy": "kansainvälinen",
            "poza Europą": "Euroopan ulkopuolella",
            "transport": "kuljetus",
            "naczep": "puoliperävaunu",
            "specjalny": "erikois",
            "ponadgabarytowy": "ylimitoitettu",
            "dźwigiem": "nosturi",
            "montaż": "kokoaminen",
            "na miejscu": "paikan päällä",
            "wielokontenerowy": "monikontti",
            "jednostki": "yksikköä",
            "tylko dostawa": "vain toimitus",
            "pozycjonowanie": "sijoittelu",
            "poziomowanie": "tasoitus",
            "podłączenia": "liitännät",
            "testy": "testit",
            "kompletna instalacja": "täydellinen asennus",
            "wyposażenia": "varustusta",
            "pusty kontener": "tyhjä kontti",
            "biurko": "pöytä",
            "krzesła": "tuolit",
            "szafa": "kaappi",
            "komplet mebli": "huonekaluvalikoima",
            "kompletne wyposażenie": "täydellinen varustus"
        },
        
        'hu': {
            # Complete Hungarian translations
            "Ilman systemów przeciwpożarowych": "Nincs tűzbiztonsági rendszer",
            "Perus (gaśnica, czujka dymu)": "Alapvető (tűzoltó, füstérzékelő)",
            "Standardi (system alarmowy, valaistus hätä)": "Szabványos (riasztórendszer, vészvilágítás)",
            "Laajennettu (tryskacze, ewakuacja)": "Kiterjesztett (sprinkler rendszer, evakuáció)",
            "Pełny system (gazowe, valvonta)": "Teljes rendszer (gáznyomás, felügyelet)",
            "Dostęp standardi (próg 15-20cm)": "Szabványos hozzáférés (15-20cm küszöb)",
            "Podjazd/rampa (dla wózków inwalidzkich)": "Rámpa (tolószékes hozzáférés)",
            "Winda hydrauliczna (dostęp dla niepełnosprawnych)": "Hidraulikus lift (fogyatékos hozzáférés)",
            "Täysi zgodność ADA (szerokie drzwi, uchwyty)": "Teljes ADA megfelelőség (széles ajtók, kapaszkodók)",
            "Powłoka standardowa C2 (RAL 7035 - szary jasny)": "Szabványos bevonat C2 (RAL 7035 - világosszürke)",
            "Powłoka ulepszona C3 (lepsza trwałość)": "Kiterjesztett bevonat C3 (javított tartósság)",
            "Powłoka morska C5M (środowiska przybrzeżne)": "Tengeri bevonat C5M (parti környezetek)",
            "Powłoka przemysłowa C4 (środowiska agresywne)": "Ipari bevonat C4 (agresszív környezetek)",
            "Premium (specjalne kolory RAL, tekstury)": "Prémium (speciális RAL színek, textúrák)",
            "Lokalny (do 50km)": "Helyi (legfeljebb 50km)",
            "Regionalny (50-200km)": "Regionális (50-200km)",
            "Krajowy (cały kraj)": "Nemzeti (egész ország)",
            "Europa Środkowa (DE, CZ, SK, AT)": "Közép-Európa (DE, CZ, SK, AT)",
            "Europa Zachodnia (FR, NL, BE, LU)": "Nyugat-Európa (FR, NL, BE, LU)",
            "Międzynarodowy (poza Europą)": "Nemzetközi (Európán kívül)",
            "Transport standardi (naczep 13.6m)": "Szabványos szállítás (13,6m félpótkocsi)",
            "Transport specjalny (ponadgabarytowy)": "Speciális szállítás (túlméretes rakomány)",
            "Transport z dźwigiem (montaż na miejscu)": "Daruszállítás (helyszíni összeszerelés)",
            "Transport wielokontenerowy (2+ jednostki)": "Többkonténeres szállítás (2+ egység)",
            "Ilman montażu (tylko dostawa)": "Nincs összeszerelés (csak szállítás)",
            "Montaż perus (pozycjonowanie, poziomowanie)": "Alapvető összeszerelés (pozicionálás, szintezés)",
            "Montaż standardi (podłączenia, testy)": "Szabványos összeszerelés (csatlakozások, tesztek)",
            "Montaż pełny (kompletna instalacja)": "Teljes összeszerelés (komplett telepítés)",
            "Ilman varustusta (pusty kontener)": "Nincs felszerelés (üres konténer)",
            "Perus (biurko, krzesła, szafa)": "Alapvető (íróasztal, székek, szekrény)",
            "Standardi (komplet mebli, valaistus)": "Szabványos (bútorkészlet, világítás)",
            "Pełne (kompletne wyposażenie": "Teljes (komplett felszerelés"
        }
    }

def clean_mixed_text(text, replacements):
    """Clean mixed language text using comprehensive replacements"""
    if not isinstance(text, str):
        return text
    
    result = text
    
    # Sort by length descending to handle longer phrases first
    for old_text, new_text in sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True):
        if old_text in result:
            result = result.replace(old_text, new_text)
    
    return result

def clean_language_completely(lang_code):
    """Completely clean all mixed text from a language file"""
    if lang_code == 'pl':
        return True
        
    print(f"Final cleanup for {lang_code}...")
    
    filepath = f'locales/{lang_code}.json'
    data = load_json_file(filepath)
    if not data:
        return False
    
    replacements = get_complete_replacement_maps().get(lang_code, {})
    if not replacements:
        print(f"  No replacement map for {lang_code}")
        return True
    
    replacement_count = 0
    
    def clean_recursive(obj):
        """Recursively clean all text"""
        nonlocal replacement_count
        
        if isinstance(obj, dict):
            return {k: clean_recursive(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_recursive(item) for item in obj]
        elif isinstance(obj, str):
            original = obj
            cleaned = clean_mixed_text(obj, replacements)
            if cleaned != original:
                replacement_count += 1
            return cleaned
        else:
            return obj
    
    cleaned_data = clean_recursive(data)
    
    if save_json_file(filepath, cleaned_data):
        print(f"  ✓ Successfully cleaned {lang_code} - made {replacement_count} replacements")
        return True
    else:
        print(f"  ✗ Failed to clean {lang_code}")
        return False

def main():
    """Main function"""
    print("Performing final comprehensive cleanup of mixed-language text...")
    
    languages = ['fi', 'hu']
    
    for lang in languages:
        clean_language_completely(lang)
    
    print("Final cleanup complete!")

if __name__ == "__main__":
    main()