#!/usr/bin/env python3
"""
Add Missing Form Labels
Adds all missing form labels that appear in the configuration display
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

def get_missing_labels():
    """Get missing form labels for all languages"""
    return {
        'en': {
            "construction_material": "Construction Material",
            "insulation": "Insulation", 
            "destination": "Destination",
            "environment": "Environment",
            "finish_level": "Finish Level",
            "climate_zone": "Climate Zone",
            "windows": "Windows",
            "window_type": "Window Type",
            "lighting": "Lighting",
            "ventilation": "Ventilation",
            "roof_modifications": "Roof Modifications",
            "additional_systems_modifications": "Additional Systems and Modifications:",
            "interior_layout": "Interior Layout",
            "security": "Security",
            "exterior_cladding": "Exterior Cladding",
            "additional_openings": "Additional Openings",
            "fire_systems": "Fire Safety Systems",
            "accessibility": "Accessibility",
            "painting": "Painting",
            "delivery_zone": "Delivery Zone",
            "transport_type": "Transport Type",
            "assembly": "Assembly"
        },
        'es': {
            "construction_material": "Material de Construcción",
            "insulation": "Aislamiento",
            "destination": "Destino", 
            "environment": "Ambiente",
            "finish_level": "Nivel de Acabado",
            "climate_zone": "Zona Climática",
            "windows": "Ventanas",
            "window_type": "Tipo de Ventana",
            "lighting": "Iluminación",
            "ventilation": "Ventilación",
            "roof_modifications": "Modificaciones del Techo",
            "additional_systems_modifications": "Sistemas Adicionales y Modificaciones:",
            "interior_layout": "Distribución Interior",
            "security": "Seguridad",
            "exterior_cladding": "Revestimiento Exterior",
            "additional_openings": "Aberturas Adicionales",
            "fire_systems": "Sistemas Contra Incendios",
            "accessibility": "Accesibilidad",
            "painting": "Pintura",
            "delivery_zone": "Zona de Entrega",
            "transport_type": "Tipo de Transporte",
            "assembly": "Montaje"
        },
        'de': {
            "construction_material": "Konstruktionsmaterial",
            "insulation": "Isolierung",
            "destination": "Bestimmung",
            "environment": "Umgebung", 
            "finish_level": "Ausbaustufe",
            "climate_zone": "Klimazone",
            "windows": "Fenster",
            "window_type": "Fenstertyp",
            "lighting": "Beleuchtung",
            "ventilation": "Lüftung",
            "roof_modifications": "Dachmodifikationen",
            "additional_systems_modifications": "Zusätzliche Systeme und Modifikationen:",
            "interior_layout": "Innenaufteilung",
            "security": "Sicherheit",
            "exterior_cladding": "Außenverkleidung",
            "additional_openings": "Zusätzliche Öffnungen",
            "fire_systems": "Brandschutzsysteme",
            "accessibility": "Barrierefreiheit",
            "painting": "Lackierung",
            "delivery_zone": "Lieferzone",
            "transport_type": "Transportart",
            "assembly": "Montage"
        },
        'fr': {
            "construction_material": "Matériau de Construction",
            "insulation": "Isolation",
            "destination": "Destination",
            "environment": "Environnement",
            "finish_level": "Niveau de Finition",
            "climate_zone": "Zone Climatique",
            "windows": "Fenêtres",
            "window_type": "Type de Fenêtre",
            "lighting": "Éclairage",
            "ventilation": "Ventilation",
            "roof_modifications": "Modifications de Toit",
            "additional_systems_modifications": "Systèmes Supplémentaires et Modifications:",
            "interior_layout": "Aménagement Intérieur",
            "security": "Sécurité",
            "exterior_cladding": "Revêtement Extérieur",
            "additional_openings": "Ouvertures Supplémentaires",
            "fire_systems": "Systèmes Anti-Incendie",
            "accessibility": "Accessibilité",
            "painting": "Peinture",
            "delivery_zone": "Zone de Livraison",
            "transport_type": "Type de Transport",
            "assembly": "Assemblage"
        },
        'it': {
            "construction_material": "Materiale di Costruzione",
            "insulation": "Isolamento",
            "destination": "Destinazione",
            "environment": "Ambiente",
            "finish_level": "Livello di Finitura", 
            "climate_zone": "Zona Climatica",
            "windows": "Finestre",
            "window_type": "Tipo di Finestra",
            "lighting": "Illuminazione",
            "ventilation": "Ventilazione",
            "roof_modifications": "Modifiche al Tetto",
            "additional_systems_modifications": "Sistemi Aggiuntivi e Modifiche:",
            "interior_layout": "Layout Interno",
            "security": "Sicurezza",
            "exterior_cladding": "Rivestimento Esterno",
            "additional_openings": "Aperture Aggiuntive",
            "fire_systems": "Sistemi Antincendio",
            "accessibility": "Accessibilità",
            "painting": "Verniciatura",
            "delivery_zone": "Zona di Consegna",
            "transport_type": "Tipo di Trasporto",
            "assembly": "Assemblaggio"
        },
        'nl': {
            "construction_material": "Constructiemateriaal",
            "insulation": "Isolatie",
            "destination": "Bestemming",
            "environment": "Omgeving",
            "finish_level": "Afwerkingsniveau",
            "climate_zone": "Klimaatzone",
            "windows": "Ramen",
            "window_type": "Raamtype",
            "lighting": "Verlichting",
            "ventilation": "Ventilatie",
            "roof_modifications": "Dakmodificaties",
            "additional_systems_modifications": "Aanvullende Systemen en Modificaties:",
            "interior_layout": "Binnenindeling",
            "security": "Beveiliging",
            "exterior_cladding": "Gevelbekleding",
            "additional_openings": "Aanvullende Openingen",
            "fire_systems": "Brandbeveiligingssystemen",
            "accessibility": "Toegankelijkheid",
            "painting": "Schilderwerk",
            "delivery_zone": "Leveringszone",
            "transport_type": "Transporttype",
            "assembly": "Montage"
        },
        'cs': {
            "construction_material": "Konstrukční Materiál",
            "insulation": "Izolace",
            "destination": "Určení",
            "environment": "Prostředí",
            "finish_level": "Úroveň Dokončení",
            "climate_zone": "Klimatická Zóna",
            "windows": "Okna",
            "window_type": "Typ Okna",
            "lighting": "Osvětlení",
            "ventilation": "Ventilace",
            "roof_modifications": "Úpravy Střechy",
            "additional_systems_modifications": "Další Systémy a Úpravy:",
            "interior_layout": "Vnitřní Uspořádání",
            "security": "Bezpečnost",
            "exterior_cladding": "Vnější Obklad",
            "additional_openings": "Další Otvory",
            "fire_systems": "Požární Systémy",
            "accessibility": "Přístupnost",
            "painting": "Malování",
            "delivery_zone": "Dodací Zóna",
            "transport_type": "Typ Dopravy",
            "assembly": "Montáž"
        },
        'sk': {
            "construction_material": "Konštrukčný Materiál",
            "insulation": "Izolácia",
            "destination": "Určenie",
            "environment": "Prostredie",
            "finish_level": "Úroveň Dokončenia",
            "climate_zone": "Klimatická Zóna",
            "windows": "Okná",
            "window_type": "Typ Okna",
            "lighting": "Osvetlenie",
            "ventilation": "Ventilácia",
            "roof_modifications": "Úpravy Strechy",
            "additional_systems_modifications": "Ďalšie Systémy a Úpravy:",
            "interior_layout": "Vnútorné Usporiadanie",
            "security": "Bezpečnosť",
            "exterior_cladding": "Vonkajší Obklad",
            "additional_openings": "Ďalšie Otvory",
            "fire_systems": "Požiarne Systémy",
            "accessibility": "Prístupnosť",
            "painting": "Maľovanie",
            "delivery_zone": "Dodacia Zóna",
            "transport_type": "Typ Dopravy",
            "assembly": "Montáž"
        },
        'hu': {
            "construction_material": "Építőanyag",
            "insulation": "Szigetelés",
            "destination": "Rendeltetés",
            "environment": "Környezet",
            "finish_level": "Befejezési Szint",
            "climate_zone": "Klímazóna",
            "windows": "Ablakok",
            "window_type": "Ablaktípus",
            "lighting": "Világítás",
            "ventilation": "Szellőztetés",
            "roof_modifications": "Tetőmódosítások",
            "additional_systems_modifications": "További Rendszerek és Módosítások:",
            "interior_layout": "Belső Elrendezés",
            "security": "Biztonság",
            "exterior_cladding": "Külső Burkolat",
            "additional_openings": "További Nyílások",
            "fire_systems": "Tűzbiztonsági Rendszerek",
            "accessibility": "Akadálymentesítés",
            "painting": "Festés",
            "delivery_zone": "Szállítási Zóna",
            "transport_type": "Szállítás Típusa",
            "assembly": "Összeszerelés"
        },
        'sv': {
            "construction_material": "Konstruktionsmaterial",
            "insulation": "Isolering",
            "destination": "Destination",
            "environment": "Miljö",
            "finish_level": "Slutnivå",
            "climate_zone": "Klimatzon",
            "windows": "Fönster",
            "window_type": "Fönstertyp",
            "lighting": "Belysning",
            "ventilation": "Ventilation",
            "roof_modifications": "Takmodifieringar",
            "additional_systems_modifications": "Ytterligare System och Modifieringar:",
            "interior_layout": "Inredningslayout",
            "security": "Säkerhet",
            "exterior_cladding": "Fasadbeklädnad",
            "additional_openings": "Ytterligare Öppningar",
            "fire_systems": "Brandsäkerhetssystem",
            "accessibility": "Tillgänglighet",
            "painting": "Målning",
            "delivery_zone": "Leveranszon",
            "transport_type": "Transporttyp",
            "assembly": "Montering"
        },
        'fi': {
            "construction_material": "Rakennusmateriaali",
            "insulation": "Eristys",
            "destination": "Kohde",
            "environment": "Ympäristö",
            "finish_level": "Viimeistelytyötaso",
            "climate_zone": "Ilmastovyöhyke",
            "windows": "Ikkunat",
            "window_type": "Ikkunatyyppi",
            "lighting": "Valaistus",
            "ventilation": "Tuuletus",
            "roof_modifications": "Kattomuutokset",
            "additional_systems_modifications": "Lisäjärjestelmät ja Muutokset:",
            "interior_layout": "Sisätilojen Layout",
            "security": "Turvallisuus",
            "exterior_cladding": "Ulkoverhoilu",
            "additional_openings": "Lisäaukot",
            "fire_systems": "Paloturvallisuusjärjestelmät",
            "accessibility": "Esteettömyys",
            "painting": "Maalaus",
            "delivery_zone": "Toimitusvyöhyke",
            "transport_type": "Kuljetustyyppi",
            "assembly": "Kokoaminen"
        },
        'uk': {
            "construction_material": "Будівельний Матеріал",
            "insulation": "Ізоляція",
            "destination": "Призначення",
            "environment": "Середовище",
            "finish_level": "Рівень Оздоблення",
            "climate_zone": "Кліматична Зона",
            "windows": "Вікна",
            "window_type": "Тип Вікна",
            "lighting": "Освітлення",
            "ventilation": "Вентиляція",
            "roof_modifications": "Модифікації Даху",
            "additional_systems_modifications": "Додаткові Системи та Модифікації:",
            "interior_layout": "Внутрішнє Планування",
            "security": "Безпека",
            "exterior_cladding": "Зовнішнє Облицювання",
            "additional_openings": "Додаткові Отвори",
            "fire_systems": "Протипожежні Системи",
            "accessibility": "Доступність",
            "painting": "Фарбування",
            "delivery_zone": "Зона Доставки",
            "transport_type": "Тип Транспорту",
            "assembly": "Збирання"
        }
    }

def add_missing_labels_to_language(lang_code):
    """Add missing labels to a specific language file"""
    if lang_code == 'pl':
        return True  # Skip Polish base file
        
    print(f"Adding missing labels to {lang_code}...")
    
    filepath = f'locales/{lang_code}.json'
    data = load_json_file(filepath)
    if not data:
        return False
    
    missing_labels = get_missing_labels().get(lang_code, {})
    if not missing_labels:
        print(f"  No missing labels defined for {lang_code}")
        return True
    
    # Add missing labels at root level
    for key, value in missing_labels.items():
        data[key] = value
    
    if save_json_file(filepath, data):
        print(f"  ✓ Successfully added {len(missing_labels)} labels to {lang_code}")
        return True
    else:
        print(f"  ✗ Failed to update {lang_code}")
        return False

def main():
    """Main function"""
    print("Adding missing form labels to all language files...")
    
    languages = ['en', 'es', 'de', 'fr', 'it', 'nl', 'cs', 'sk', 'hu', 'sv', 'fi', 'uk']
    
    success_count = 0
    for lang in languages:
        if add_missing_labels_to_language(lang):
            success_count += 1
    
    print(f"Missing labels addition complete: {success_count}/{len(languages)} languages updated")

if __name__ == "__main__":
    main()