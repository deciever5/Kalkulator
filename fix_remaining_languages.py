#!/usr/bin/env python3
"""
Fix Remaining Languages
Replaces Polish text with proper translations for all remaining languages
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

def get_translations_for_remaining_languages():
    """Get translations for all remaining languages"""
    return {
        'nl': {
            "special_notes_systems": "Speciale opmerkingen - Systemen",
            "describe_system_requirements": "Beschrijf aanvullende systeemvereisten...",
            "system_requirements_placeholder": "bijv. Speciale ventilatievereisten, extra stopcontacten, gespecialiseerde installaties",
            "interior_layout": "Binnenindeling",
            "security_systems": "Beveiligings- en alarmsystemen",
            "exterior_cladding": "Gevelbekleding",
            "additional_openings": "Aanvullende openingen en modificaties",
            "fire_safety_systems": "Brandveiligheidssystemen",
            "accessibility_features": "Toegankelijkheid en ergonomie",
            "paint_finish": "Schilderwerk en buitenafwerking",
            "special_notes_modifications": "Speciale opmerkingen - Modificaties",
            "describe_modification_requirements": "Beschrijf aanvullende modificatievereisten...",
            "modification_requirements_placeholder": "bijv. Speciale RAL-kleuren, niet-standaard openingsafmetingen, aanvullende structurele versterkingen",
            "delivery_zone": "Leveringszone",
            "transport_type": "Transporttype",
            "assembly_installation": "Montage en installatie",
            "office_equipment": "Kantoor-/interieuruitrusting",
            "appliances": "Huishoudelijke apparaten (voor wooncontainers)",
            "it_multimedia": "IT- en multimediasystemen",
            "special_notes_general": "Speciale opmerkingen - Algemeen",
            "describe_general_requirements": "Beschrijf alle aanvullende vereisten, specificaties of projectbeperkingen...",
            "general_requirements_placeholder": "bijv. Speciale voltooiingsdeadlines, certificeringsvereisten, budgetbeperkingen",
            "interior_layout_options": {
                "open_space": "Open ruimte (geen scheidingswanden)",
                "partitioned": "Verdeeld (1-3 kamers)",
                "built_in_furniture": "Ingebouwde meubels (maatwerk inrichting)",
                "custom_layout": "Aangepaste indeling (maatwerk ontwerp)",
                "mezzanine": "Mezzanine/verdieping (vergroot oppervlak)"
            },
            "security_systems_options": {
                "none": "Geen extra beveiliging (standaardsloten)",
                "basic": "Basis (versterkte sloten, tralies voor ramen)",
                "standard": "Standaard (alarm, sensoren, sirene)",
                "extended": "Uitgebreid (bewaking, bewegings-/trillingsensoren)",
                "high": "Hoog (IP CCTV, toegangscontrole, intercom)",
                "maximum": "Maximum (kluis, biometrie, centrale bewaking)",
                "industrial": "Industrieel (ATEX, gassystemen, paniekkamer)"
            },
            "exterior_cladding_options": {
                "none": "Geen bekleding (standaard containerplaat)",
                "trapezoidal": "Trapeziumplaat (T18, T35, T55)",
                "cassette": "Cassetteplaat (vlak, reliëf)",
                "vinyl_siding": "Vinyl gevelbekleding (houtimitatie, modern)",
                "structural_plaster": "Structuurpleister (siliconen, acryl)",
                "wood_cladding": "Houten bekleding (thermo, exotisch)",
                "composite_panels": "Composietpanelen (HPL, dibond)",
                "clinker_brick": "Klinkers (voorgevel, facade)",
                "natural_stone": "Natuurlijke/kunstmatige steen"
            },
            "additional_openings_options": {
                "none": "Geen extra openingen (standaarddeuren)",
                "windows": "Extra ramen (1-4 stuks)",
                "doors": "Extra deuren (service, nooduitgang)",
                "garage_door": "Garagedeur (sectionaal, rol)",
                "loading_dock": "Laadplatform (hydraulisch platform)",
                "ventilation": "Ventilatieopeningen (roosters, lamellen)",
                "skylights": "Dakramen/lichtkoepels",
                "custom": "Aangepaste openingen (niet-standaard afmetingen)"
            },
            "fire_safety_options": {
                "none": "Geen brandveiligheidssystemen",
                "basic": "Basis (brandblusser, rookmelder)",
                "standard": "Standaard (alarmsysteem, noodverlichting)",
                "extended": "Uitgebreid (sprinklersysteem, evacuatie)",
                "full": "Volledig systeem (gasonderdrukking, bewaking)"
            },
            "accessibility_options": {
                "standard": "Standaardtoegang (15-20cm drempel)",
                "ramp": "Oprit (rolstoeltoegankelijk)",
                "lift": "Hydraulische lift (toegang voor gehandicapten)",
                "full_ada": "Volledige ADA-compliance (brede deuren, handgrepen)"
            },
            "paint_finish_options": {
                "standard": "Standaardbekleding C2 (RAL 7035 - lichtgrijs)",
                "extended": "Uitgebreide bekleding C3 (verbeterde duurzaamheid)",
                "marine": "Marine bekleding C5M (kustomgevingen)",
                "industrial": "Industriële bekleding C4 (agressieve omgevingen)",
                "premium": "Premium (speciale RAL-kleuren, texturen)"
            },
            "delivery_zone_options": {
                "local": "Lokaal (tot 50km)",
                "regional": "Regionaal (50-200km)",
                "national": "Nationaal (hele land)",
                "central_europe": "Midden-Europa (DE, CZ, SK, AT)",
                "western_europe": "West-Europa (FR, NL, BE, LU)",
                "international": "Internationaal (buiten Europa)"
            },
            "transport_type_options": {
                "standard": "Standaardtransport (13,6m oplegger)",
                "special": "Speciaal transport (oversized lading)",
                "crane": "Kraantransport (montage ter plaatse)",
                "multi_container": "Multi-containertransport (2+ eenheden)"
            },
            "assembly_options": {
                "none": "Geen montage (alleen levering)",
                "basic": "Basismontage (positionering, waterpassing)",
                "standard": "Standaardmontage (aansluitingen, tests)",
                "full": "Volledige montage (complete installatie)"
            },
            "office_equipment_options": {
                "none": "Geen uitrusting (lege container)",
                "basic": "Basis (bureau, stoelen, kast)",
                "standard": "Standaard (meubelset, verlichting)",
                "full": "Volledig (complete kantoorinrichting)"
            },
            "appliances_options": {
                "none": "Geen huishoudelijke apparaten",
                "basic": "Basis (koelkast, magnetron)",
                "standard": "Standaard (keukensset, wasmachine)",
                "full": "Volledig (complete huishoudelijke apparaten)"
            },
            "it_systems_options": {
                "none": "Geen IT-systemen",
                "basic": "Basis (internet, WiFi)",
                "standard": "Standaard (netwerk, telefonie)",
                "advanced": "Geavanceerd (serverruimte, beveiliging)"
            }
        },
        'it': {
            "special_notes_systems": "Note speciali - Sistemi",
            "describe_system_requirements": "Descrivi i requisiti di sistema aggiuntivi...",
            "system_requirements_placeholder": "es. Requisiti di ventilazione speciali, prese aggiuntive, installazioni specializzate",
            "interior_layout": "Layout interno",
            "security_systems": "Sistemi di sicurezza e allarme",
            "exterior_cladding": "Rivestimento esterno",
            "additional_openings": "Aperture aggiuntive e modifiche",
            "fire_safety_systems": "Sistemi di sicurezza antincendio",
            "accessibility_features": "Accessibilità ed ergonomia",
            "paint_finish": "Verniciatura e finitura esterna",
            "special_notes_modifications": "Note speciali - Modifiche",
            "describe_modification_requirements": "Descrivi i requisiti di modifica aggiuntivi...",
            "modification_requirements_placeholder": "es. Colori RAL speciali, dimensioni di apertura non standard, rinforzi strutturali aggiuntivi",
            "delivery_zone": "Zona di consegna",
            "transport_type": "Tipo di trasporto",
            "assembly_installation": "Assemblaggio e installazione",
            "office_equipment": "Attrezzature per ufficio/interni",
            "appliances": "Elettrodomestici (per container residenziali)",
            "it_multimedia": "Sistemi IT e multimediali",
            "special_notes_general": "Note speciali - Generale",
            "describe_general_requirements": "Descrivi tutti i requisiti aggiuntivi, specifiche o vincoli del progetto...",
            "general_requirements_placeholder": "es. Scadenze speciali, requisiti di certificazione, vincoli di budget",
            "interior_layout_options": {
                "open_space": "Spazio aperto (senza partizioni)",
                "partitioned": "Partizionato (1-3 stanze)",
                "built_in_furniture": "Mobili incorporati (allestimento su misura)",
                "custom_layout": "Layout personalizzato (design su misura)",
                "mezzanine": "Mezzanino/piano (spazio aumentato)"
            },
            "security_systems_options": {
                "none": "Nessuna sicurezza aggiuntiva (serrature standard)",
                "basic": "Base (serrature rinforzate, barre alle finestre)",
                "standard": "Standard (allarme, sensori, sirena)",
                "extended": "Esteso (monitoraggio, sensori di movimento/vibrazione)",
                "high": "Alto (CCTV IP, controllo accessi, citofono)",
                "maximum": "Massimo (cassaforte, biometria, monitoraggio centrale)",
                "industrial": "Industriale (ATEX, sistemi a gas, stanza del panico)"
            },
            "exterior_cladding_options": {
                "none": "Nessun rivestimento (lamiera container standard)",
                "trapezoidal": "Lamiera trapezoidale (T18, T35, T55)",
                "cassette": "Lamiera a cassetta (piatta, goffrata)",
                "vinyl_siding": "Rivestimento in vinile (imitazione legno, moderno)",
                "structural_plaster": "Intonaco strutturale (silicone, acrilico)",
                "wood_cladding": "Rivestimento in legno (termo, esotico)",
                "composite_panels": "Pannelli compositi (HPL, dibond)",
                "clinker_brick": "Mattoni clinker (faccia a vista, facciata)",
                "natural_stone": "Pietra naturale/artificiale"
            },
            "additional_openings_options": {
                "none": "Nessuna apertura aggiuntiva (porte standard)",
                "windows": "Finestre aggiuntive (1-4 pezzi)",
                "doors": "Porte aggiuntive (servizio, emergenza)",
                "garage_door": "Porta garage (sezionale, avvolgibile)",
                "loading_dock": "Banchina di carico (piattaforma idraulica)",
                "ventilation": "Aperture di ventilazione (griglie, persiane)",
                "skylights": "Finestre da tetto/lucernari",
                "custom": "Aperture personalizzate (dimensioni non standard)"
            },
            "fire_safety_options": {
                "none": "Nessun sistema di sicurezza antincendio",
                "basic": "Base (estintore, rilevatore di fumo)",
                "standard": "Standard (sistema di allarme, illuminazione di emergenza)",
                "extended": "Esteso (sistema sprinkler, evacuazione)",
                "full": "Sistema completo (soppressione gas, monitoraggio)"
            },
            "accessibility_options": {
                "standard": "Accesso standard (soglia 15-20cm)",
                "ramp": "Rampa (accessibile in sedia a rotelle)",
                "lift": "Sollevatore idraulico (accesso disabili)",
                "full_ada": "Piena conformità ADA (porte larghe, maniglioni)"
            },
            "paint_finish_options": {
                "standard": "Rivestimento standard C2 (RAL 7035 - grigio chiaro)",
                "extended": "Rivestimento esteso C3 (durata migliorata)",
                "marine": "Rivestimento marino C5M (ambienti costieri)",
                "industrial": "Rivestimento industriale C4 (ambienti aggressivi)",
                "premium": "Premium (colori RAL speciali, texture)"
            },
            "delivery_zone_options": {
                "local": "Locale (fino a 50km)",
                "regional": "Regionale (50-200km)",
                "national": "Nazionale (tutto il paese)",
                "central_europe": "Europa centrale (DE, CZ, SK, AT)",
                "western_europe": "Europa occidentale (FR, NL, BE, LU)",
                "international": "Internazionale (fuori Europa)"
            },
            "transport_type_options": {
                "standard": "Trasporto standard (semirimorchio 13,6m)",
                "special": "Trasporto speciale (carico fuori misura)",
                "crane": "Trasporto con gru (assemblaggio in loco)",
                "multi_container": "Trasporto multi-container (2+ unità)"
            },
            "assembly_options": {
                "none": "Nessun assemblaggio (solo consegna)",
                "basic": "Assemblaggio base (posizionamento, livellamento)",
                "standard": "Assemblaggio standard (collegamenti, test)",
                "full": "Assemblaggio completo (installazione completa)"
            },
            "office_equipment_options": {
                "none": "Nessuna attrezzatura (container vuoto)",
                "basic": "Base (scrivania, sedie, armadio)",
                "standard": "Standard (set di mobili, illuminazione)",
                "full": "Completo (allestimento ufficio completo)"
            },
            "appliances_options": {
                "none": "Nessun elettrodomestico",
                "basic": "Base (frigorifero, microonde)",
                "standard": "Standard (set cucina, lavatrice)",
                "full": "Completo (elettrodomestici completi)"
            },
            "it_systems_options": {
                "none": "Nessun sistema IT",
                "basic": "Base (internet, WiFi)",
                "standard": "Standard (rete, telefonia)",
                "advanced": "Avanzato (sala server, sicurezza)"
            }
        },
        'es': {
            "special_notes_systems": "Notas especiales - Sistemas",
            "describe_system_requirements": "Describa los requisitos adicionales del sistema...",
            "system_requirements_placeholder": "ej. Requisitos especiales de ventilación, tomas adicionales, instalaciones especializadas",
            "interior_layout": "Distribución interior",
            "security_systems": "Sistemas de seguridad y alarma",
            "exterior_cladding": "Revestimiento exterior",
            "additional_openings": "Aberturas adicionales y modificaciones",
            "fire_safety_systems": "Sistemas de seguridad contra incendios",
            "accessibility_features": "Accesibilidad y ergonomía",
            "paint_finish": "Pintura y acabado exterior",
            "special_notes_modifications": "Notas especiales - Modificaciones",
            "describe_modification_requirements": "Describa los requisitos de modificación adicionales...",
            "modification_requirements_placeholder": "ej. Colores RAL especiales, tamaños de abertura no estándar, refuerzos estructurales adicionales",
            "delivery_zone": "Zona de entrega",
            "transport_type": "Tipo de transporte",
            "assembly_installation": "Montaje e instalación",
            "office_equipment": "Equipamiento de oficina/interior",
            "appliances": "Electrodomésticos (para contenedores residenciales)",
            "it_multimedia": "Sistemas informáticos y multimedia",
            "special_notes_general": "Notas especiales - General",
            "describe_general_requirements": "Describa todos los requisitos adicionales, especificaciones o limitaciones del proyecto...",
            "general_requirements_placeholder": "ej. Plazos especiales de finalización, requisitos de certificación, limitaciones presupuestarias",
            "interior_layout_options": {
                "open_space": "Espacio abierto (sin particiones)",
                "partitioned": "Dividido (1-3 habitaciones)",
                "built_in_furniture": "Muebles incorporados (equipamiento a medida)",
                "custom_layout": "Distribución personalizada (diseño a medida)",
                "mezzanine": "Entreplanta/piso (espacio ampliado)"
            },
            "security_systems_options": {
                "none": "Sin seguridad adicional (cerraduras estándar)",
                "basic": "Básico (cerraduras reforzadas, rejas en ventanas)",
                "standard": "Estándar (alarma, sensores, sirena)",
                "extended": "Ampliado (monitoreo, sensores de movimiento/vibración)",
                "high": "Alto (CCTV IP, control de acceso, intercomunicador)",
                "maximum": "Máximo (caja fuerte, biometría, monitoreo central)",
                "industrial": "Industrial (ATEX, sistemas de gas, habitación de pánico)"
            },
            "exterior_cladding_options": {
                "none": "Sin revestimiento (chapa de contenedor estándar)",
                "trapezoidal": "Chapa trapezoidal (T18, T35, T55)",
                "cassette": "Chapa de casete (plana, grabada)",
                "vinyl_siding": "Revestimiento de vinilo (imitación madera, moderno)",
                "structural_plaster": "Yeso estructural (silicona, acrílico)",
                "wood_cladding": "Revestimiento de madera (termo, exótico)",
                "composite_panels": "Paneles compuestos (HPL, dibond)",
                "clinker_brick": "Ladrillo clínker (cara vista, fachada)",
                "natural_stone": "Piedra natural/artificial"
            },
            "additional_openings_options": {
                "none": "Sin aberturas adicionales (puertas estándar)",
                "windows": "Ventanas adicionales (1-4 piezas)",
                "doors": "Puertas adicionales (servicio, emergencia)",
                "garage_door": "Puerta de garaje (seccional, enrollable)",
                "loading_dock": "Muelle de carga (plataforma hidráulica)",
                "ventilation": "Aberturas de ventilación (rejillas, persianas)",
                "skylights": "Ventanas de techo/claraboyas",
                "custom": "Aberturas personalizadas (tamaños no estándar)"
            },
            "fire_safety_options": {
                "none": "Sin sistemas de seguridad contra incendios",
                "basic": "Básico (extintor, detector de humo)",
                "standard": "Estándar (sistema de alarma, iluminación de emergencia)",
                "extended": "Ampliado (sistema de rociadores, evacuación)",
                "full": "Sistema completo (supresión de gas, monitoreo)"
            },
            "accessibility_options": {
                "standard": "Acceso estándar (umbral 15-20cm)",
                "ramp": "Rampa (accesible en silla de ruedas)",
                "lift": "Elevador hidráulico (acceso para discapacitados)",
                "full_ada": "Cumplimiento completo ADA (puertas anchas, barras de apoyo)"
            },
            "paint_finish_options": {
                "standard": "Revestimiento estándar C2 (RAL 7035 - gris claro)",
                "extended": "Revestimiento extendido C3 (durabilidad mejorada)",
                "marine": "Revestimiento marino C5M (entornos costeros)",
                "industrial": "Revestimiento industrial C4 (entornos agresivos)",
                "premium": "Premium (colores RAL especiales, texturas)"
            },
            "delivery_zone_options": {
                "local": "Local (hasta 50km)",
                "regional": "Regional (50-200km)",
                "national": "Nacional (todo el país)",
                "central_europe": "Europa Central (DE, CZ, SK, AT)",
                "western_europe": "Europa Occidental (FR, NL, BE, LU)",
                "international": "Internacional (fuera de Europa)"
            },
            "transport_type_options": {
                "standard": "Transporte estándar (semirremolque 13,6m)",
                "special": "Transporte especial (carga sobredimensionada)",
                "crane": "Transporte con grúa (montaje en sitio)",
                "multi_container": "Transporte multi-contenedor (2+ unidades)"
            },
            "assembly_options": {
                "none": "Sin montaje (solo entrega)",
                "basic": "Montaje básico (posicionamiento, nivelación)",
                "standard": "Montaje estándar (conexiones, pruebas)",
                "full": "Montaje completo (instalación completa)"
            },
            "office_equipment_options": {
                "none": "Sin equipamiento (contenedor vacío)",
                "basic": "Básico (escritorio, sillas, armario)",
                "standard": "Estándar (conjunto de muebles, iluminación)",
                "full": "Completo (equipamiento de oficina completo)"
            },
            "appliances_options": {
                "none": "Sin electrodomésticos",
                "basic": "Básico (refrigerador, microondas)",
                "standard": "Estándar (conjunto de cocina, lavadora)",
                "full": "Completo (electrodomésticos completos)"
            },
            "it_systems_options": {
                "none": "Sin sistemas informáticos",
                "basic": "Básico (internet, WiFi)",
                "standard": "Estándar (red, telefonía)",
                "advanced": "Avanzado (sala de servidores, seguridad)"
            }
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
    print("Fixing translations for Dutch, Italian, and Spanish...")
    
    all_translations = get_translations_for_remaining_languages()
    
    # Update specific languages that need fixing
    for lang_code, translations in all_translations.items():
        update_language_file(lang_code, translations)
    
    print("Translation fix for Dutch, Italian, and Spanish complete!")

if __name__ == "__main__":
    main()