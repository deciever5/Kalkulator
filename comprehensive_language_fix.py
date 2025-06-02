#!/usr/bin/env python3
"""
Comprehensive Language Fix
Properly translates all missing translation keys for all languages
"""

import json
import os

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

def get_translations_by_language():
    """Get all proper translations organized by language"""
    return {
        'de': {
            "special_notes_systems": "Besondere Hinweise - Systeme",
            "describe_system_requirements": "Beschreiben Sie zusätzliche Systemanforderungen...",
            "system_requirements_placeholder": "z.B. Besondere Lüftungsanforderungen, zusätzliche Steckdosen, spezielle Installationen",
            "interior_layout": "Innenaufteilung",
            "security_systems": "Sicherheits- und Alarmsysteme",
            "exterior_cladding": "Außenverkleidung",
            "additional_openings": "Zusätzliche Öffnungen und Modifikationen",
            "fire_safety_systems": "Brandschutzsysteme",
            "accessibility_features": "Barrierefreiheit und Ergonomie",
            "paint_finish": "Lackierung und Außenveredelung",
            "special_notes_modifications": "Besondere Hinweise - Modifikationen",
            "describe_modification_requirements": "Beschreiben Sie zusätzliche Modifikationsanforderungen...",
            "modification_requirements_placeholder": "z.B. Spezielle RAL-Farben, ungewöhnliche Öffnungsgrößen, zusätzliche Strukturverstärkungen",
            "delivery_zone": "Lieferzone",
            "transport_type": "Transportart",
            "assembly_installation": "Montage und Installation",
            "office_equipment": "Büro-/Innenausstattung",
            "appliances": "Haushaltsgeräte (für Wohncontainer)",
            "it_multimedia": "IT- und Multimedia-Systeme",
            "special_notes_general": "Besondere Hinweise - Allgemein",
            "describe_general_requirements": "Beschreiben Sie alle zusätzlichen Anforderungen, Spezifikationen oder Projektbeschränkungen...",
            "general_requirements_placeholder": "z.B. Besondere Fertigstellungstermine, Zertifizierungsanforderungen, Budgetbeschränkungen",
            "interior_layout_options": {
                "open_space": "Offener Raum (keine Trennwände)",
                "partitioned": "Aufgeteilt (1-3 Räume)",
                "built_in_furniture": "Einbaumöbel (maßgeschneiderte Ausstattung)",
                "custom_layout": "Individuelle Aufteilung (Sonderplanung)",
                "mezzanine": "Zwischengeschoss (vergrößerte Fläche)"
            },
            "security_systems_options": {
                "none": "Keine zusätzliche Sicherheit (Standardschlösser)",
                "basic": "Grundausstattung (verstärkte Schlösser, Fenstergitter)",
                "standard": "Standard (Alarm, Sensoren, Sirene)",
                "extended": "Erweitert (Überwachung, Bewegungs-/Vibrationssensoren)",
                "high": "Hoch (IP-CCTV, Zutrittskontrolle, Gegensprechanlage)",
                "maximum": "Maximum (Tresor, Biometrie, Zentral-Überwachung)",
                "industrial": "Industriell (ATEX, Gassysteme, Panikraum)"
            },
            "exterior_cladding_options": {
                "none": "Keine Verkleidung (Standard-Containerblech)",
                "trapezoidal": "Trapezblech (T18, T35, T55)",
                "cassette": "Kassettenblech (flach, geprägt)",
                "vinyl_siding": "Vinyl-Siding (Holzimitat, modern)",
                "structural_plaster": "Strukturputz (Silikon, Acryl)",
                "wood_cladding": "Holzverkleidung (Thermo, exotisch)",
                "composite_panels": "Verbundplatten (HPL, Dibond)",
                "clinker_brick": "Klinkerziegel (Sicht-, Fassade)",
                "natural_stone": "Natur-/Kunststein"
            },
            "additional_openings_options": {
                "none": "Keine zusätzlichen Öffnungen (Standardtüren)",
                "windows": "Zusätzliche Fenster (1-4 Stück)",
                "doors": "Zusätzliche Türen (Service, Notfall)",
                "garage_door": "Garagentor (Sektional, Rolltor)",
                "loading_dock": "Laderampe (Hydraulikplattform)",
                "ventilation": "Lüftungsöffnungen (Gitter, Lamellen)",
                "skylights": "Dachfenster/Oberlichter",
                "custom": "Sonderöffnungen (ungewöhnliche Größen)"
            },
            "fire_safety_options": {
                "none": "Keine Brandschutzsysteme",
                "basic": "Grundausstattung (Feuerlöscher, Rauchmelder)",
                "standard": "Standard (Alarmanlage, Notbeleuchtung)",
                "extended": "Erweitert (Sprinkleranlage, Evakuierung)",
                "full": "Vollsystem (Gaslöschung, Überwachung)"
            },
            "accessibility_options": {
                "standard": "Standardzugang (15-20cm Schwelle)",
                "ramp": "Rampe (rollstuhlgerecht)",
                "lift": "Hydrauliklift (behindertengerecht)",
                "full_ada": "Vollständige ADA-Compliance (breite Türen, Haltegriffe)"
            },
            "paint_finish_options": {
                "standard": "Standardbeschichtung C2 (RAL 7035 - hellgrau)",
                "extended": "Erweiterte Beschichtung C3 (verbesserte Haltbarkeit)",
                "marine": "Marinebeschichtung C5M (Küstenumgebungen)",
                "industrial": "Industriebeschichtung C4 (aggressive Umgebungen)",
                "premium": "Premium (spezielle RAL-Farben, Texturen)"
            },
            "delivery_zone_options": {
                "local": "Lokal (bis 50km)",
                "regional": "Regional (50-200km)",
                "national": "National (ganzes Land)",
                "central_europe": "Mitteleuropa (DE, CZ, SK, AT)",
                "western_europe": "Westeuropa (FR, NL, BE, LU)",
                "international": "International (außerhalb Europas)"
            },
            "transport_type_options": {
                "standard": "Standardtransport (13,6m Sattelauflieger)",
                "special": "Spezialtransport (Schwertransport)",
                "crane": "Krantransport (Montage vor Ort)",
                "multi_container": "Mehrcontainertransport (2+ Einheiten)"
            },
            "assembly_options": {
                "none": "Keine Montage (nur Lieferung)",
                "basic": "Grundmontage (Positionierung, Ausrichtung)",
                "standard": "Standardmontage (Anschlüsse, Tests)",
                "full": "Vollmontage (komplette Installation)"
            },
            "office_equipment_options": {
                "none": "Keine Ausstattung (leerer Container)",
                "basic": "Grundausstattung (Schreibtisch, Stühle, Schrank)",
                "standard": "Standardausstattung (Möbelset, Beleuchtung)",
                "full": "Vollausstattung (komplette Büroeinrichtung)"
            },
            "appliances_options": {
                "none": "Keine Haushaltsgeräte",
                "basic": "Grundausstattung (Kühlschrank, Mikrowelle)",
                "standard": "Standardausstattung (Küchenset, Waschmaschine)",
                "full": "Vollausstattung (komplette Haushaltsgeräte)"
            },
            "it_systems_options": {
                "none": "Keine IT-Systeme",
                "basic": "Grundausstattung (Internet, WiFi)",
                "standard": "Standardausstattung (Netzwerk, Telefonie)",
                "advanced": "Erweitert (Serverraum, Sicherheit)"
            }
        },
        'fr': {
            "special_notes_systems": "Notes spéciales - Systèmes",
            "describe_system_requirements": "Décrivez les exigences système supplémentaires...",
            "system_requirements_placeholder": "ex. Exigences de ventilation spéciales, prises supplémentaires, installations spécialisées",
            "interior_layout": "Aménagement intérieur",
            "security_systems": "Systèmes de sécurité et d'alarme",
            "exterior_cladding": "Revêtement extérieur",
            "additional_openings": "Ouvertures supplémentaires et modifications",
            "fire_safety_systems": "Systèmes de sécurité incendie",
            "accessibility_features": "Accessibilité et ergonomie",
            "paint_finish": "Peinture et finition extérieure",
            "special_notes_modifications": "Notes spéciales - Modifications",
            "describe_modification_requirements": "Décrivez les exigences de modification supplémentaires...",
            "modification_requirements_placeholder": "ex. Couleurs RAL spéciales, tailles d'ouverture non standard, renforts structurels supplémentaires",
            "delivery_zone": "Zone de livraison",
            "transport_type": "Type de transport",
            "assembly_installation": "Assemblage et installation",
            "office_equipment": "Équipement de bureau/intérieur",
            "appliances": "Appareils électroménagers (pour conteneurs résidentiels)",
            "it_multimedia": "Systèmes informatiques et multimédia",
            "special_notes_general": "Notes spéciales - Général",
            "describe_general_requirements": "Décrivez toutes les exigences supplémentaires, spécifications ou contraintes de projet...",
            "general_requirements_placeholder": "ex. Délais de réalisation spéciaux, exigences de certification, contraintes budgétaires",
            "interior_layout_options": {
                "open_space": "Espace ouvert (sans cloisons)",
                "partitioned": "Cloisonné (1-3 pièces)",
                "built_in_furniture": "Mobilier intégré (aménagement sur mesure)",
                "custom_layout": "Aménagement personnalisé (conception sur mesure)",
                "mezzanine": "Mezzanine/étage (espace agrandi)"
            },
            "security_systems_options": {
                "none": "Aucune sécurité supplémentaire (serrures standard)",
                "basic": "De base (serrures renforcées, barreaux de fenêtre)",
                "standard": "Standard (alarme, capteurs, sirène)",
                "extended": "Étendu (surveillance, capteurs de mouvement/vibration)",
                "high": "Élevé (CCTV IP, contrôle d'accès, interphone)",
                "maximum": "Maximum (coffre-fort, biométrie, surveillance centrale)",
                "industrial": "Industriel (ATEX, systèmes à gaz, salle de panique)"
            },
            "exterior_cladding_options": {
                "none": "Sans bardage (tôle de conteneur standard)",
                "trapezoidal": "Tôle trapézoïdale (T18, T35, T55)",
                "cassette": "Tôle cassette (plate, embossée)",
                "vinyl_siding": "Bardage vinyle (imitation bois, moderne)",
                "structural_plaster": "Enduit structurel (silicone, acrylique)",
                "wood_cladding": "Bardage bois (thermo, exotique)",
                "composite_panels": "Panneaux composites (HPL, dibond)",
                "clinker_brick": "Brique de clinker (parement, façade)",
                "natural_stone": "Pierre naturelle/artificielle"
            },
            "additional_openings_options": {
                "none": "Pas d'ouvertures supplémentaires (portes standard)",
                "windows": "Fenêtres supplémentaires (1-4 pièces)",
                "doors": "Portes supplémentaires (service, urgence)",
                "garage_door": "Porte de garage (sectionnelle, roulante)",
                "loading_dock": "Quai de chargement (plateforme hydraulique)",
                "ventilation": "Ouvertures de ventilation (grilles, persiennes)",
                "skylights": "Fenêtres de toit/puits de lumière",
                "custom": "Ouvertures personnalisées (tailles non standard)"
            },
            "fire_safety_options": {
                "none": "Pas de systèmes de sécurité incendie",
                "basic": "De base (extincteur, détecteur de fumée)",
                "standard": "Standard (système d'alarme, éclairage d'urgence)",
                "extended": "Étendu (système de sprinkler, évacuation)",
                "full": "Système complet (suppression de gaz, surveillance)"
            },
            "accessibility_options": {
                "standard": "Accès standard (seuil 15-20cm)",
                "ramp": "Rampe (accessible en fauteuil roulant)",
                "lift": "Élévateur hydraulique (accès handicapés)",
                "full_ada": "Conformité ADA complète (portes larges, barres d'appui)"
            },
            "paint_finish_options": {
                "standard": "Revêtement standard C2 (RAL 7035 - gris clair)",
                "extended": "Revêtement étendu C3 (durabilité améliorée)",
                "marine": "Revêtement marin C5M (environnements côtiers)",
                "industrial": "Revêtement industriel C4 (environnements agressifs)",
                "premium": "Premium (couleurs RAL spéciales, textures)"
            },
            "delivery_zone_options": {
                "local": "Local (jusqu'à 50km)",
                "regional": "Régional (50-200km)",
                "national": "National (tout le pays)",
                "central_europe": "Europe centrale (DE, CZ, SK, AT)",
                "western_europe": "Europe de l'Ouest (FR, NL, BE, LU)",
                "international": "International (hors Europe)"
            },
            "transport_type_options": {
                "standard": "Transport standard (semi-remorque 13,6m)",
                "special": "Transport spécial (charge surdimensionnée)",
                "crane": "Transport avec grue (assemblage sur site)",
                "multi_container": "Transport multi-conteneurs (2+ unités)"
            },
            "assembly_options": {
                "none": "Pas d'assemblage (livraison seulement)",
                "basic": "Assemblage de base (positionnement, nivellement)",
                "standard": "Assemblage standard (connexions, tests)",
                "full": "Assemblage complet (installation complète)"
            },
            "office_equipment_options": {
                "none": "Pas d'équipement (conteneur vide)",
                "basic": "De base (bureau, chaises, armoire)",
                "standard": "Standard (ensemble de meubles, éclairage)",
                "full": "Complet (aménagement de bureau complet)"
            },
            "appliances_options": {
                "none": "Pas d'appareils électroménagers",
                "basic": "De base (réfrigérateur, micro-ondes)",
                "standard": "Standard (ensemble cuisine, lave-linge)",
                "full": "Complet (appareils électroménagers complets)"
            },
            "it_systems_options": {
                "none": "Pas de systèmes informatiques",
                "basic": "De base (internet, WiFi)",
                "standard": "Standard (réseau, téléphonie)",
                "advanced": "Avancé (salle serveur, sécurité)"
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
    print("Fixing translations for German and French languages...")
    
    all_translations = get_translations_by_language()
    
    # Update specific languages that need fixing
    for lang_code, translations in all_translations.items():
        update_language_file(lang_code, translations)
    
    print("Language-specific translation fix complete!")

if __name__ == "__main__":
    main()