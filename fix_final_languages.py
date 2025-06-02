#!/usr/bin/env python3
"""
Fix Final Languages
Completes the translation fix for Czech, Slovak, Hungarian, Swedish, Finnish, and Ukrainian
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

def get_translations_for_final_languages():
    """Get translations for the final group of languages"""
    return {
        'cs': {
            "special_notes_systems": "Speciální poznámky - Systémy",
            "describe_system_requirements": "Popište další systémové požadavky...",
            "system_requirements_placeholder": "např. Speciální požadavky na ventilaci, další zásuvky, specializované instalace",
            "interior_layout": "Vnitřní uspořádání",
            "security_systems": "Bezpečnostní a poplašné systémy",
            "exterior_cladding": "Vnější obklad",
            "additional_openings": "Další otvory a úpravy",
            "fire_safety_systems": "Požární bezpečnostní systémy",
            "accessibility_features": "Přístupnost a ergonomie",
            "paint_finish": "Malování a vnější úprava",
            "special_notes_modifications": "Speciální poznámky - Úpravy",
            "describe_modification_requirements": "Popište další požadavky na úpravy...",
            "modification_requirements_placeholder": "např. Speciální RAL barvy, nestandardní velikosti otvorů, další konstrukční posílení",
            "delivery_zone": "Dodací zóna",
            "transport_type": "Typ dopravy",
            "assembly_installation": "Montáž a instalace",
            "office_equipment": "Kancelářské/interiérové vybavení",
            "appliances": "Spotřebiče (pro obytné kontejnery)",
            "it_multimedia": "IT a multimediální systémy",
            "special_notes_general": "Speciální poznámky - Obecné",
            "describe_general_requirements": "Popište všechny další požadavky, specifikace nebo omezení projektu...",
            "general_requirements_placeholder": "např. Speciální termíny dokončení, certifikační požadavky, rozpočtová omezení",
            "interior_layout_options": {
                "open_space": "Otevřený prostor (bez příček)",
                "partitioned": "Rozdělený (1-3 místnosti)",
                "built_in_furniture": "Vestavěný nábytek (vybavení na míru)",
                "custom_layout": "Vlastní uspořádání (design na míru)",
                "mezzanine": "Mezipatro/patro (zvětšený prostor)"
            },
            "security_systems_options": {
                "none": "Žádná další bezpečnost (standardní zámky)",
                "basic": "Základní (posílené zámky, mříže na okna)",
                "standard": "Standardní (alarm, senzory, siréna)",
                "extended": "Rozšířený (monitoring, pohybové/vibrační senzory)",
                "high": "Vysoký (IP CCTV, kontrola přístupu, interkom)",
                "maximum": "Maximální (trezor, biometrie, centrální monitoring)",
                "industrial": "Průmyslový (ATEX, plynové systémy, panikový pokoj)"
            },
            "exterior_cladding_options": {
                "none": "Bez obkladu (standardní kontejnerový plech)",
                "trapezoidal": "Trapézový plech (T18, T35, T55)",
                "cassette": "Kazetový plech (plochý, reliéfní)",
                "vinyl_siding": "Vinylový obklad (imitace dřeva, moderní)",
                "structural_plaster": "Strukturální omítka (silikonová, akrylová)",
                "wood_cladding": "Dřevěný obklad (termo, exotický)",
                "composite_panels": "Kompozitní panely (HPL, dibond)",
                "clinker_brick": "Klinkové cihly (líc, fasáda)",
                "natural_stone": "Přírodní/umělý kámen"
            },
            "additional_openings_options": {
                "none": "Žádné další otvory (standardní dveře)",
                "windows": "Další okna (1-4 kusy)",
                "doors": "Další dveře (servis, nouzové)",
                "garage_door": "Garážová vrata (sekční, rolovací)",
                "loading_dock": "Nakládací rampa (hydraulická plošina)",
                "ventilation": "Ventilační otvory (mřížky, žaluzie)",
                "skylights": "Střešní okna/světlíky",
                "custom": "Vlastní otvory (nestandardní velikosti)"
            },
            "fire_safety_options": {
                "none": "Žádné požární bezpečnostní systémy",
                "basic": "Základní (hasicí přístroj, detektor kouře)",
                "standard": "Standardní (alarmový systém, nouzové osvětlení)",
                "extended": "Rozšířený (sprinklerový systém, evakuace)",
                "full": "Úplný systém (plynové potlačení, monitoring)"
            },
            "accessibility_options": {
                "standard": "Standardní přístup (práh 15-20cm)",
                "ramp": "Rampa (přístupná pro vozíčkáře)",
                "lift": "Hydraulický výtah (přístup pro zdravotně postižené)",
                "full_ada": "Plná shoda s ADA (široké dveře, madla)"
            },
            "paint_finish_options": {
                "standard": "Standardní nátěr C2 (RAL 7035 - světle šedá)",
                "extended": "Rozšířený nátěr C3 (zlepšená trvanlivost)",
                "marine": "Námořní nátěr C5M (pobřežní prostředí)",
                "industrial": "Průmyslový nátěr C4 (agresivní prostředí)",
                "premium": "Premium (speciální RAL barvy, textury)"
            },
            "delivery_zone_options": {
                "local": "Místní (do 50km)",
                "regional": "Regionální (50-200km)",
                "national": "Národní (celá země)",
                "central_europe": "Střední Evropa (DE, CZ, SK, AT)",
                "western_europe": "Západní Evropa (FR, NL, BE, LU)",
                "international": "Mezinárodní (mimo Evropu)"
            },
            "transport_type_options": {
                "standard": "Standardní doprava (13,6m návěs)",
                "special": "Speciální doprava (nadrozměrný náklad)",
                "crane": "Doprava s jeřábem (montáž na místě)",
                "multi_container": "Multi-kontejnerová doprava (2+ jednotky)"
            },
            "assembly_options": {
                "none": "Bez montáže (pouze dodání)",
                "basic": "Základní montáž (umístění, vyrovnání)",
                "standard": "Standardní montáž (připojení, testy)",
                "full": "Úplná montáž (kompletní instalace)"
            },
            "office_equipment_options": {
                "none": "Bez vybavení (prázdný kontejner)",
                "basic": "Základní (stůl, židle, skříň)",
                "standard": "Standardní (nábytkový set, osvětlení)",
                "full": "Úplný (kompletní kancelářské vybavení)"
            },
            "appliances_options": {
                "none": "Bez spotřebičů",
                "basic": "Základní (lednice, mikrovlnka)",
                "standard": "Standardní (kuchyňský set, pračka)",
                "full": "Úplný (kompletní domácí spotřebiče)"
            },
            "it_systems_options": {
                "none": "Bez IT systémů",
                "basic": "Základní (internet, WiFi)",
                "standard": "Standardní (síť, telefonie)",
                "advanced": "Pokročilý (serverovna, bezpečnost)"
            }
        },
        'sk': {
            "special_notes_systems": "Špeciálne poznámky - Systémy",
            "describe_system_requirements": "Opíšte ďalšie systémové požiadavky...",
            "system_requirements_placeholder": "napr. Špeciálne požiadavky na vetranie, ďalšie zásuvky, špecializované inštalácie",
            "interior_layout": "Vnútorné usporiadanie",
            "security_systems": "Bezpečnostné a poplašné systémy",
            "exterior_cladding": "Vonkajší obklad",
            "additional_openings": "Ďalšie otvory a úpravy",
            "fire_safety_systems": "Požiarne bezpečnostné systémy",
            "accessibility_features": "Prístupnosť a ergonómia",
            "paint_finish": "Maľovanie a vonkajšia úprava",
            "special_notes_modifications": "Špeciálne poznámky - Úpravy",
            "describe_modification_requirements": "Opíšte ďalšie požiadavky na úpravy...",
            "modification_requirements_placeholder": "napr. Špeciálne RAL farby, neštandardné veľkosti otvorov, ďalšie konštrukčné posilnenie",
            "delivery_zone": "Dodacia zóna",
            "transport_type": "Typ dopravy",
            "assembly_installation": "Montáž a inštalácia",
            "office_equipment": "Kancelárske/interiérové vybavenie",
            "appliances": "Spotrebiče (pre obytné kontajnery)",
            "it_multimedia": "IT a multimediálne systémy",
            "special_notes_general": "Špeciálne poznámky - Všeobecné",
            "describe_general_requirements": "Opíšte všetky ďalšie požiadavky, špecifikácie alebo obmedzenia projektu...",
            "general_requirements_placeholder": "napr. Špeciálne termíny dokončenia, certifikačné požiadavky, rozpočtové obmedzenia"
        },
        'hu': {
            "special_notes_systems": "Speciális megjegyzések - Rendszerek",
            "describe_system_requirements": "Írja le a további rendszerkövetelményeket...",
            "system_requirements_placeholder": "pl. Speciális szellőzési követelmények, további aljzatok, specializált telepítések",
            "interior_layout": "Belső elrendezés",
            "security_systems": "Biztonsági és riasztórendszerek",
            "exterior_cladding": "Külső burkolat",
            "additional_openings": "További nyílások és módosítások",
            "fire_safety_systems": "Tűzbiztonsági rendszerek",
            "accessibility_features": "Akadálymentesítés és ergonómia",
            "paint_finish": "Festés és külső wykończenie",
            "special_notes_modifications": "Speciális megjegyzések - Módosítások",
            "describe_modification_requirements": "Írja le a további módosítási követelményeket...",
            "modification_requirements_placeholder": "pl. Speciális RAL színek, nem szabványos nyílásméret, további szerkezeti megerősítések",
            "delivery_zone": "Szállítási zóna",
            "transport_type": "Szállítás típusa",
            "assembly_installation": "Összeszerelés és telepítés",
            "office_equipment": "Irodai/belső berendezés",
            "appliances": "Háztartási gépek (lakókonténerekhez)",
            "it_multimedia": "IT és multimédia rendszerek",
            "special_notes_general": "Speciális megjegyzések - Általános",
            "describe_general_requirements": "Írja le az összes további követelményt, specifikációt vagy projektkorlátozást...",
            "general_requirements_placeholder": "pl. Speciális befejezési határidők, tanúsítási követelmények, költségvetési korlátok"
        },
        'sv': {
            "special_notes_systems": "Speciella anteckningar - System",
            "describe_system_requirements": "Beskriv ytterligare systemkrav...",
            "system_requirements_placeholder": "t.ex. Speciella ventilationskrav, extra uttag, specialiserade installationer",
            "interior_layout": "Inredningslayout",
            "security_systems": "Säkerhets- och larmsystem",
            "exterior_cladding": "Fasadbeklädnad",
            "additional_openings": "Ytterligare öppningar och modifieringar",
            "fire_safety_systems": "Brandsäkerhetssystem",
            "accessibility_features": "Tillgänglighet och ergonomi",
            "paint_finish": "Målning och ytterfinish",
            "special_notes_modifications": "Speciella anteckningar - Modifieringar",
            "describe_modification_requirements": "Beskriv ytterligare modifieringskrav...",
            "modification_requirements_placeholder": "t.ex. Speciella RAL-färger, icke-standardiserade öppningsstorlekar, ytterligare strukturförstärkningar",
            "delivery_zone": "Leveranszon",
            "transport_type": "Transporttyp",
            "assembly_installation": "Montering och installation",
            "office_equipment": "Kontors-/inredningsutrustning",
            "appliances": "Hushållsapparater (för bostadscontainrar)",
            "it_multimedia": "IT- och multimediasystem",
            "special_notes_general": "Speciella anteckningar - Allmänt",
            "describe_general_requirements": "Beskriv alla ytterligare krav, specifikationer eller projektbegränsningar...",
            "general_requirements_placeholder": "t.ex. Speciella slutdatum, certifieringskrav, budgetbegränsningar"
        },
        'fi': {
            "special_notes_systems": "Erityishuomautukset - Järjestelmät",
            "describe_system_requirements": "Kuvaile lisäjärjestelmävaatimukset...",
            "system_requirements_placeholder": "esim. Erityiset ilmanvaihtovaatimukset, lisäpistorasiat, erikoisasennukset",
            "interior_layout": "Sisätilojen layout",
            "security_systems": "Turvallisuus- ja hälytysjärjestelmät",
            "exterior_cladding": "Ulkoverhoilu",
            "additional_openings": "Lisäaukot ja muutokset",
            "fire_safety_systems": "Paloturvallisuusjärjestelmät",
            "accessibility_features": "Esteettömyys ja ergonomia",
            "paint_finish": "Maalaus ja ulkoviimeistely",
            "special_notes_modifications": "Erityishuomautukset - Muutokset",
            "describe_modification_requirements": "Kuvaile lisämuutosvaatimukset...",
            "modification_requirements_placeholder": "esim. Erityiset RAL-värit, epästandardit aukkokoot, lisärakenteelliset vahvistukset",
            "delivery_zone": "Toimitusvyöhyke",
            "transport_type": "Kuljetustyyppi",
            "assembly_installation": "Kokoaminen ja asennus",
            "office_equipment": "Toimisto-/sisustusvarusteet",
            "appliances": "Kodinkoneet (asuinkonteille)",
            "it_multimedia": "IT- ja multimediajärjestelmät",
            "special_notes_general": "Erityishuomautukset - Yleinen",
            "describe_general_requirements": "Kuvaile kaikki lisävaatimukset, spesifikaatiot tai projektin rajoitukset...",
            "general_requirements_placeholder": "esim. Erityiset valmistumispäivämäärät, sertifiointivaatimukset, budjettirajoitukset"
        },
        'uk': {
            "special_notes_systems": "Спеціальні примітки - Системи",
            "describe_system_requirements": "Опишіть додаткові системні вимоги...",
            "system_requirements_placeholder": "напр. Спеціальні вимоги до вентиляції, додаткові розетки, спеціалізовані установки",
            "interior_layout": "Внутрішнє планування",
            "security_systems": "Системи безпеки та сигналізації",
            "exterior_cladding": "Зовнішнє облицювання",
            "additional_openings": "Додаткові отвори та модифікації",
            "fire_safety_systems": "Системи пожежної безпеки",
            "accessibility_features": "Доступність та эргономіка",
            "paint_finish": "Фарбування та зовнішня обробка",
            "special_notes_modifications": "Спеціальні примітки - Модифікації",
            "describe_modification_requirements": "Опишіть додаткові вимоги до модифікацій...",
            "modification_requirements_placeholder": "напр. Спеціальні кольори RAL, нестандартні розміри отворів, додаткові структурні підсилення",
            "delivery_zone": "Зона доставки",
            "transport_type": "Тип транспорту",
            "assembly_installation": "Збирання та встановлення",
            "office_equipment": "Офісне/внутрішнє обладнання",
            "appliances": "Побутова техніка (для житлових контейнерів)",
            "it_multimedia": "ІТ та мультимедійні системи",
            "special_notes_general": "Спеціальні примітки - Загальні",
            "describe_general_requirements": "Опишіть всі додаткові вимоги, специфікації або обмеження проекту...",
            "general_requirements_placeholder": "напр. Спеціальні терміни завершення, вимоги до сертифікації, бюджетні обмеження"
        }
    }

def update_language_file(lang_code, translations):
    """Update a specific language file with translations"""
    filepath = f'locales/{lang_code}.json'
    print(f"Updating {lang_code}...")
    
    data = load_json_file(filepath)
    if not data:
        return False
    
    # Update all translation keys
    for key, value in translations.items():
        data[key] = value
    
    if save_json_file(filepath, data):
        print(f"  ✓ Successfully updated {lang_code}")
        return True
    else:
        print(f"  ✗ Failed to update {lang_code}")
        return False

def main():
    """Main function"""
    print("Fixing translations for Czech, Slovak, Hungarian, Swedish, Finnish, and Ukrainian...")
    
    all_translations = get_translations_for_final_languages()
    
    # Update final group of languages
    for lang_code, translations in all_translations.items():
        update_language_file(lang_code, translations)
    
    print("Final language translation fix complete!")
    print("All 13 languages should now have proper translations!")

if __name__ == "__main__":
    main()