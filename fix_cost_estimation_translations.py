#!/usr/bin/env python3
"""
Fix Cost Estimation Translations
Replaces all long AI-generated text with simple, clean translations for cost estimation section
"""

import json
import os
from typing import Dict

def load_json_file(filepath: str) -> Dict:
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filepath: str, data: Dict) -> bool:
    """Save JSON file with proper formatting"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def get_proper_cost_translations() -> Dict[str, Dict[str, str]]:
    """Get proper simple translations for all cost estimation keys"""
    return {
        'en': {
            'estimate_title': '💰 Project Cost Estimate',
            'cost_breakdown_title': 'Cost Breakdown:',
            'base_container_line': 'Base container:',
            'modifications_equipment_line': 'Modifications and equipment:',
            'total_cost_line': 'TOTAL COST:',
            'important_warning': '⚠️ Important:',
            'preliminary_estimate_full': 'This is a preliminary estimate. Final price depends on detailed specifications, current material prices and availability. Contact our team for an accurate quote.',
            'configuration_saved_success': '✅ Configuration saved successfully!'
        },
        'de': {
            'estimate_title': '💰 Projektkostenschätzung',
            'cost_breakdown_title': 'Kostenaufschlüsselung:',
            'base_container_line': 'Basis-Container:',
            'modifications_equipment_line': 'Änderungen und Ausstattung:',
            'total_cost_line': 'GESAMTKOSTEN:',
            'important_warning': '⚠️ Wichtig:',
            'preliminary_estimate_full': 'Dies ist eine vorläufige Schätzung. Der endgültige Preis hängt von detaillierten Spezifikationen, aktuellen Materialpreisen und Verfügbarkeit ab. Kontaktieren Sie unser Team für ein genaues Angebot.',
            'configuration_saved_success': '✅ Konfiguration erfolgreich gespeichert!'
        },
        'es': {
            'estimate_title': '💰 Estimación de Costos del Proyecto',
            'cost_breakdown_title': 'Desglose de Costos:',
            'base_container_line': 'Contenedor base:',
            'modifications_equipment_line': 'Modificaciones y equipamiento:',
            'total_cost_line': 'COSTO TOTAL:',
            'important_warning': '⚠️ Importante:',
            'preliminary_estimate_full': 'Esta es una estimación preliminar. El precio final depende de especificaciones detalladas, precios actuales de materiales y disponibilidad. Contacte nuestro equipo para una cotización precisa.',
            'configuration_saved_success': '✅ Configuración guardada con éxito!'
        },
        'fr': {
            'estimate_title': '💰 Estimation des Coûts du Projet',
            'cost_breakdown_title': 'Répartition des Coûts:',
            'base_container_line': 'Conteneur de base:',
            'modifications_equipment_line': 'Modifications et équipement:',
            'total_cost_line': 'COÛT TOTAL:',
            'important_warning': '⚠️ Important:',
            'preliminary_estimate_full': 'Ceci est une estimation préliminaire. Le prix final dépend des spécifications détaillées, des prix actuels des matériaux et de la disponibilité. Contactez notre équipe pour un devis précis.',
            'configuration_saved_success': '✅ Configuration sauvegardée avec succès!'
        },
        'it': {
            'estimate_title': '💰 Stima dei Costi del Progetto',
            'cost_breakdown_title': 'Ripartizione dei Costi:',
            'base_container_line': 'Container base:',
            'modifications_equipment_line': 'Modifiche e attrezzature:',
            'total_cost_line': 'COSTO TOTALE:',
            'important_warning': '⚠️ Importante:',
            'preliminary_estimate_full': 'Questa è una stima preliminare. Il prezzo finale dipende dalle specifiche dettagliate, dai prezzi attuali dei materiali e dalla disponibilità. Contatta il nostro team per un preventivo accurato.',
            'configuration_saved_success': '✅ Configurazione salvata con successo!'
        },
        'nl': {
            'estimate_title': '💰 Projectkostenschatting',
            'cost_breakdown_title': 'Kostenverdeling:',
            'base_container_line': 'Basis container:',
            'modifications_equipment_line': 'Wijzigingen en uitrusting:',
            'total_cost_line': 'TOTALE KOSTEN:',
            'important_warning': '⚠️ Belangrijk:',
            'preliminary_estimate_full': 'Dit is een voorlopige schatting. De definitieve prijs hangt af van gedetailleerde specificaties, huidige materiaalprijzen en beschikbaarheid. Neem contact op met ons team voor een nauwkeurige offerte.',
            'configuration_saved_success': '✅ Configuratie succesvol opgeslagen!'
        },
        'sv': {
            'estimate_title': '💰 Projektkostnadsuppskattning',
            'cost_breakdown_title': 'Kostnadsfördelning:',
            'base_container_line': 'Bascontainer:',
            'modifications_equipment_line': 'Modifieringar och utrustning:',
            'total_cost_line': 'TOTALKOSTNAD:',
            'important_warning': '⚠️ Viktigt:',
            'preliminary_estimate_full': 'Detta är en preliminär uppskattning. Slutpriset beror på detaljerade specifikationer, aktuella materialpriser och tillgänglighet. Kontakta vårt team för en exakt offert.',
            'configuration_saved_success': '✅ Konfiguration sparad framgångsrikt!'
        },
        'fi': {
            'estimate_title': '💰 Projektin Kustannusarvio',
            'cost_breakdown_title': 'Kustannusjaottelu:',
            'base_container_line': 'Peruskontti:',
            'modifications_equipment_line': 'Muutokset ja varusteet:',
            'total_cost_line': 'KOKONAISKUSTANNUS:',
            'important_warning': '⚠️ Tärkeää:',
            'preliminary_estimate_full': 'Tämä on alustava arvio. Lopullinen hinta riippuu yksityiskohtaisista spesifikaatioista, nykyisistä materiaalihinnoista ja saatavuudesta. Ota yhteyttä tiimiimme tarkan tarjouksen saamiseksi.',
            'configuration_saved_success': '✅ Konfiguraatio tallennettu onnistuneesti!'
        },
        'cs': {
            'estimate_title': '💰 Odhad Nákladů Projektu',
            'cost_breakdown_title': 'Rozpis Nákladů:',
            'base_container_line': 'Základní kontejner:',
            'modifications_equipment_line': 'Úpravy a vybavení:',
            'total_cost_line': 'CELKOVÉ NÁKLADY:',
            'important_warning': '⚠️ Důležité:',
            'preliminary_estimate_full': 'Toto je předběžný odhad. Konečná cena závisí na podrobných specifikacích, aktuálních cenách materiálů a dostupnosti. Pro přesnou nabídku kontaktujte náš tým.',
            'configuration_saved_success': '✅ Konfigurace úspěšně uložena!'
        },
        'sk': {
            'estimate_title': '💰 Odhad Nákladov Projektu',
            'cost_breakdown_title': 'Rozpis Nákladov:',
            'base_container_line': 'Základný kontajner:',
            'modifications_equipment_line': 'Úpravy a vybavenie:',
            'total_cost_line': 'CELKOVÉ NÁKLADY:',
            'important_warning': '⚠️ Dôležité:',
            'preliminary_estimate_full': 'Toto je predbežný odhad. Konečná cena závisí od podrobných špecifikácií, aktuálnych cien materiálov a dostupnosti. Pre presnú ponuku kontaktujte náš tím.',
            'configuration_saved_success': '✅ Konfigurácia úspešne uložená!'
        },
        'hu': {
            'estimate_title': '💰 Projekt Költségbecslés',
            'cost_breakdown_title': 'Költséglebontás:',
            'base_container_line': 'Alap konténer:',
            'modifications_equipment_line': 'Módosítások és felszerelés:',
            'total_cost_line': 'TELJES KÖLTSÉG:',
            'important_warning': '⚠️ Fontos:',
            'preliminary_estimate_full': 'Ez egy előzetes becslés. A végső ár a részletes specifikációktól, az aktuális anyagáraktól és a rendelkezésre állástól függ. Pontos ajánlatért lépjen kapcsolatba csapatunkkal.',
            'configuration_saved_success': '✅ Konfiguráció sikeresen elmentve!'
        },
        'uk': {
            'estimate_title': '💰 Кошторис Проекту',
            'cost_breakdown_title': 'Розбивка Витрат:',
            'base_container_line': 'Базовий контейнер:',
            'modifications_equipment_line': 'Модифікації та обладнання:',
            'total_cost_line': 'ЗАГАЛЬНА ВАРТІСТЬ:',
            'important_warning': '⚠️ Важливо:',
            'preliminary_estimate_full': 'Це попередня оцінка. Остаточна ціна залежить від детальних специфікацій, поточних цін на матеріали та наявності. Зверніться до нашої команди для точного кошторису.',
            'configuration_saved_success': '✅ Конфігурацію успішно збережено!'
        },
        'pl': {
            'estimate_title': '💰 Szacunkowa Wycena Projektu',
            'cost_breakdown_title': 'Podział Kosztów:',
            'base_container_line': 'Kontener bazowy:',
            'modifications_equipment_line': 'Modyfikacje i wyposażenie:',
            'total_cost_line': 'CAŁKOWITY KOSZT:',
            'important_warning': '⚠️ Ważne:',
            'preliminary_estimate_full': 'To wstępne szacowanie. Ostateczna cena zależy od szczegółowych specyfikacji, aktualnych cen materiałów i dostępności. Dla dokładnej wyceny skontaktuj się z naszym zespołem.',
            'configuration_saved_success': '✅ Konfiguracja zapisana pomyślnie!'
        }
    }

def fix_language_cost_translations(lang_code: str, translations: Dict[str, str]) -> bool:
    """Fix cost estimation translations for a specific language"""
    filepath = f'locales/{lang_code}.json'
    
    if not os.path.exists(filepath):
        print(f"  ❌ File not found: {filepath}")
        return False
    
    # Load existing translations
    data = load_json_file(filepath)
    
    # Ensure cost_estimation section exists
    if 'cost_estimation' not in data:
        data['cost_estimation'] = {}
    
    # Update all cost estimation translations
    for key, value in translations.items():
        data['cost_estimation'][key] = value
    
    # Save the file
    return save_json_file(filepath, data)

def fix_all_languages():
    """Fix cost estimation translations for all languages"""
    cost_translations = get_proper_cost_translations()
    
    for lang_code, translations in cost_translations.items():
        print(f"Processing {lang_code}...")
        
        if fix_language_cost_translations(lang_code, translations):
            print(f"  ✅ Updated {lang_code} cost estimation translations")
        else:
            print(f"  ❌ Failed to update {lang_code}")

def main():
    """Main function"""
    print("🔧 Fixing Cost Estimation Translations")
    print("=" * 50)
    
    fix_all_languages()
    
    print("\n✅ Cost estimation translation fixes completed!")
    print("\nNow the save configuration will show:")
    print("• Simple, clean cost breakdown format")
    print("• No long AI analysis or explanations")
    print("• Consistent format matching Polish across all languages")
    print("• Proper currency and business terminology")

if __name__ == "__main__":
    main()