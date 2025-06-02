#!/usr/bin/env python3
"""
Rebuild Translations Properly
Uses Polish as base and creates proper translations for each language
"""

import json

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

def get_complete_translations():
    """Get complete proper translations for key sections"""
    
    translations = {
        'fi': {
            # Fire safety options
            "fire_safety_options": {
                "none": "Ei paloturvallisuusjärjestelmiä",
                "basic": "Perus (sammutin, savuilmaisin)",
                "standard": "Standardi (hälytysjärjestelmä, hätävalaistus)",
                "extended": "Laajennettu (sprinklerit, evakuointi)",
                "full": "Täysi järjestelmä (kaasunpoisto, valvonta)"
            },
            
            # Accessibility options
            "accessibility_options": {
                "standard": "Tavallinen pääsy (15-20cm kynnys)",
                "ramp": "Luiska (pyörätuolipääsy)",
                "lift": "Hydraulinen nostin (vammaispääsy)",
                "full_ada": "Täysi ADA-yhteensopivuus (leveät ovet, käsijohteet)"
            },
            
            # Paint finish options
            "paint_finish_options": {
                "standard": "Tavallinen pinnoite C2 (RAL 7035 - vaaleanharmaa)",
                "extended": "Laajennettu pinnoite C3 (parannettu kestävyys)",
                "marine": "Meriympäristön pinnoite C5M (rannikkoympäristöt)",
                "industrial": "Teollisuuspinnoite C4 (aggressiiviset ympäristöt)",
                "premium": "Premium (erikois RAL-värit, tekstuurit)"
            },
            
            # Delivery zone options
            "delivery_zone_options": {
                "local": "Paikallinen (enintään 50km)",
                "regional": "Alueellinen (50-200km)",
                "national": "Kansallinen (koko maa)",
                "central_europe": "Keski-Eurooppa (DE, CZ, SK, AT)",
                "western_europe": "Länsi-Eurooppa (FR, NL, BE, LU)",
                "international": "Kansainvälinen (Euroopan ulkopuolella)"
            },
            
            # Transport type options
            "transport_type_options": {
                "standard": "Tavallinen kuljetus (13,6m puoliperävaunu)",
                "special": "Erikoiskuljetus (ylimitoitettu kuorma)",
                "crane": "Nosturikuljetus (kokoaminen paikan päällä)",
                "multi_container": "Monikonttien kuljetus (2+ yksikköä)"
            },
            
            # Assembly options
            "assembly_options": {
                "none": "Ei kokoamista (vain toimitus)",
                "basic": "Peruskokoaminen (sijoittelu, tasoitus)",
                "standard": "Tavallinen kokoaminen (liitännät, testit)",
                "full": "Täysi kokoaminen (täydellinen asennus)"
            },
            
            # Office equipment options
            "office_equipment_options": {
                "none": "Ei varustusta (tyhjä kontti)",
                "basic": "Perus (pöytä, tuolit, kaappi)",
                "standard": "Standardi (huonekaluvalikoima, valaistus)",
                "full": "Täysi (täydellinen toimistovarustus)"
            },
            
            # Window types
            "window_types": {
                "standard": "Standardi (kaksinkertainen lasi)",
                "energy_efficient": "Energiatehokas (kolminkertainen lasi)",
                "security": "Turvallisuus (karkaistua lasia)",
                "marine_grade": "Meriluokka (korroosionkestävä)",
                "panoramic": "Panoraama-ikkunat",
                "sliding": "Liukuikkunat",
                "tilt": "Kääntöikkunat",
                "skylight": "Kattoikkunat"
            },
            
            # Lighting
            "lighting": {
                "none": "Ei valaistusta",
                "basic": "Perus LED",
                "basic_led": "Perus LED-valaistus",
                "energy_efficient": "Energiatehokas LED antureilla",
                "exterior": "Ulkovalaistus (valonheittimet)",
                "emergency": "Hätävalaistus (akkukäyttöinen)",
                "smart": "Älyjärjestelmä (ohjattu valaistus)"
            },
            
            # Electrical system
            "electrical_system": {
                "none": "Ei sähköasennusta",
                "preparation": "Valmistelu (johdotus ilman laitteita)",
                "basic": "Perus (valaistus + pistorasiat)",
                "standard": "Standardi (25A, valaistus, 8 pistorasiaa)",
                "extended": "Laajennettu (40A, teho, UPS, hätä)",
                "industrial": "Teollinen (63A, teho, jakokeskus)",
                "it_server": "IT/Palvelin (UPS, jäähdytys, valvonta)",
                "smart": "Älykäs (kotiautomaatio, KNX)"
            },
            
            # Plumbing system
            "plumbing_system": {
                "none": "Ei vesiasennus",
                "preparation": "Valmistelu (putket ilman kalustetta)",
                "basic": "Perus (pesuallas + viemäri)",
                "full": "Täysi (kylpyhuoneen valmistelu)",
                "commercial": "Kaupallinen luokka",
                "industrial": "Teollinen asennus (painevesi, suodatus)",
                "cold_water": "Kylmävesiasennus (pesuallas)",
                "hot_cold_water": "Kylmä + lämmin vesi (pesuallas, käsiallas)",
                "basic_sanitary": "Perus saniteettisolmu (WC + käsiallas)",
                "standard_sanitary": "Standardi solmu (WC + käsiallas + suihku)",
                "comfort_sanitary": "Mukavuussolmu (WC + käsiallas + kaappi)",
                "premium_sanitary": "Premium solmu (poreallas, bidee, 2 käsiallasta)"
            }
        },
        
        'hu': {
            # Fire safety options
            "fire_safety_options": {
                "none": "Nincs tűzbiztonsági rendszer",
                "basic": "Alapvető (tűzoltó, füstérzékelő)",
                "standard": "Szabványos (riasztórendszer, vészvilágítás)",
                "extended": "Kiterjesztett (sprinkler rendszer, evakuáció)",
                "full": "Teljes rendszer (gáznyomás, felügyelet)"
            },
            
            # Accessibility options
            "accessibility_options": {
                "standard": "Szabványos hozzáférés (15-20cm küszöb)",
                "ramp": "Rámpa (tolószékes hozzáférés)",
                "lift": "Hidraulikus lift (fogyatékos hozzáférés)",
                "full_ada": "Teljes ADA megfelelőség (széles ajtók, kapaszkodók)"
            },
            
            # Paint finish options
            "paint_finish_options": {
                "standard": "Szabványos bevonat C2 (RAL 7035 - világosszürke)",
                "extended": "Kiterjesztett bevonat C3 (javított tartósság)",
                "marine": "Tengeri bevonat C5M (parti környezetek)",
                "industrial": "Ipari bevonat C4 (agresszív környezetek)",
                "premium": "Prémium (speciális RAL színek, textúrák)"
            },
            
            # Delivery zone options
            "delivery_zone_options": {
                "local": "Helyi (legfeljebb 50km)",
                "regional": "Regionális (50-200km)",
                "national": "Nemzeti (egész ország)",
                "central_europe": "Közép-Európa (DE, CZ, SK, AT)",
                "western_europe": "Nyugat-Európa (FR, NL, BE, LU)",
                "international": "Nemzetközi (Európán kívül)"
            },
            
            # Transport type options
            "transport_type_options": {
                "standard": "Szabványos szállítás (13,6m félpótkocsi)",
                "special": "Speciális szállítás (túlméretes rakomány)",
                "crane": "Daruszállítás (helyszíni összeszerelés)",
                "multi_container": "Többkonténeres szállítás (2+ egység)"
            },
            
            # Assembly options
            "assembly_options": {
                "none": "Nincs összeszerelés (csak szállítás)",
                "basic": "Alapvető összeszerelés (pozicionálás, szintezés)",
                "standard": "Szabványos összeszerelés (csatlakozások, tesztek)",
                "full": "Teljes összeszerelés (komplett telepítés)"
            },
            
            # Office equipment options
            "office_equipment_options": {
                "none": "Nincs felszerelés (üres konténer)",
                "basic": "Alapvető (íróasztal, székek, szekrény)",
                "standard": "Szabványos (bútorkészlet, világítás)",
                "full": "Teljes (komplett irodai felszerelés)"
            },
            
            # Window types
            "window_types": {
                "standard": "Szabványos (dupla üvegezés)",
                "energy_efficient": "Energiatakarékos (tripla üvegezés)",
                "security": "Biztonság (edzett üveg)",
                "marine_grade": "Tengeri osztály (korróziógátló)",
                "panoramic": "Panoráma ablakok",
                "sliding": "Tolóablakok",
                "tilt": "Bukóablakok",
                "skylight": "Tetőablakok"
            },
            
            # Lighting
            "lighting": {
                "none": "Nincs világítás",
                "basic": "Alapvető LED",
                "basic_led": "Alapvető LED világítás",
                "energy_efficient": "Energiatakarékos LED érzékelőkkel",
                "exterior": "Külső világítás (reflektorok)",
                "emergency": "Vészvilágítás (akkumulátoros)",
                "smart": "Intelligens rendszer (vezérelt világítás)"
            },
            
            # Electrical system
            "electrical_system": {
                "none": "Nincs elektromos szerelés",
                "preparation": "Előkészítés (vezetékek berendezés nélkül)",
                "basic": "Alapvető (világítás + aljzatok)",
                "standard": "Szabványos (25A, világítás, 8 aljzat)",
                "extended": "Kiterjesztett (40A, erő, UPS, vészhelyzet)",
                "industrial": "Ipari (63A, erő, elosztószekrény)",
                "it_server": "IT/Szerver (UPS, hűtés, felügyelet)",
                "smart": "Intelligens (otthon automatizálás, KNX)"
            },
            
            # Plumbing system
            "plumbing_system": {
                "none": "Nincs vízszerelés",
                "preparation": "Előkészítés (csövek szerelvények nélkül)",
                "basic": "Alapvető (mosogató + lefolyó)",
                "full": "Teljes (fürdőszoba előkészítés)",
                "commercial": "Kereskedelmi osztály",
                "industrial": "Ipari telepítés (nyomásos, szűrés)",
                "cold_water": "Hidegvíz-szerelés (mosogató)",
                "hot_cold_water": "Hideg + meleg víz (mosogató, mosdó)",
                "basic_sanitary": "Alapvető szaniter csomópont (WC + mosdó)",
                "standard_sanitary": "Szabványos csomópont (WC + mosdó + zuhany)",
                "comfort_sanitary": "Kényelmes csomópont (WC + mosdó + kabin)",
                "premium_sanitary": "Prémium csomópont (jakuzzi, bidé, 2 mosdó)"
            }
        }
    }
    
    return translations

def rebuild_language_file(lang_code):
    """Rebuild a language file with proper translations"""
    if lang_code == 'pl':
        return True
        
    print(f"Rebuilding {lang_code} with proper translations...")
    
    filepath = f'locales/{lang_code}.json'
    data = load_json_file(filepath)
    if not data:
        return False
    
    translations = get_complete_translations().get(lang_code, {})
    if not translations:
        print(f"  No complete translations for {lang_code}")
        return True
    
    # Update with proper translations
    for key, value in translations.items():
        data[key] = value
    
    if save_json_file(filepath, data):
        print(f"  ✓ Successfully rebuilt {lang_code}")
        return True
    else:
        print(f"  ✗ Failed to rebuild {lang_code}")
        return False

def main():
    """Main function"""
    print("Rebuilding translation files with proper translations...")
    
    languages = ['fi', 'hu']
    
    for lang in languages:
        rebuild_language_file(lang)
    
    print("Translation rebuild complete!")

if __name__ == "__main__":
    main()