#!/usr/bin/env python3
"""
Fix English Translation File
Corrects the Polish content that was incorrectly merged into English translations
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

def fix_english_translations():
    """Fix the English translation file"""
    
    # Load English file
    en_data = load_json_file('locales/en.json')
    if not en_data:
        return False
    
    # Correct translations for key sections
    corrections = {
        "electrical_system": "Electrical System",
        "plumbing_system": "Plumbing System", 
        "hvac_system": "HVAC System",
        "configure_container": "Configure Your Container",
        "simple_process_2_steps": "Simple process in 2 easy steps",
        "step_1_configuration": "Step 1: Configuration",
        "choose_container_type": "Choose container type and modifications",
        "step_2_ai_estimation": "Step 2: AI Estimation",
        "ai_analyzes_configuration": "AI analyzes your configuration and provides cost estimates",
        "send_inquiry_button": "Send Inquiry",
        "why_kan_bud": "Why KAN-BUD?",
        "precise_quotes": "Precise Quotes",
        "ai_historical_data": "AI analysis with historical data",
        "european_climate_standards": "European climate standards",
        "transparent_calculations": "Transparent calculations",
        "fast_realization": "Fast Realization",
        "hundreds_of_projects": "Hundreds of completed projects",
        "own_machinery": "Own machinery park",
        "poland_center": "Central location in Poland",
        "full_service": "Full Service",
        "design_execution": "From design to execution",
        "transport_assembly": "Transport and assembly",
        "after_sales_support": "After-sales support",
        "contact_us": "Contact us",
        "address": "Address",
        "phone": "Phone",
        "email": "Email",
        "working_hours": "Working hours",
        "mon_fri": "Mon-Fri 8:00-17:00"
    }
    
    # Apply corrections
    for key, value in corrections.items():
        if key in en_data:
            en_data[key] = value
    
    # Fix nested structures
    if "window_types" in en_data:
        en_data["window_types"] = {
            "standard": "Standard (double glazing)",
            "energy_efficient": "Energy efficient (triple glazing)",
            "security": "Security (tempered glass)",
            "marine_grade": "Marine grade (anti-corrosion)"
        }
    
    if "lighting" in en_data:
        en_data["lighting"] = {
            "none": "No lighting",
            "basic": "Basic LED",
            "energy_efficient": "Energy efficient LED with sensors",
            "exterior": "Exterior lighting (floodlights)",
            "emergency": "Emergency lighting (battery backup)",
            "smart": "Smart system (controlled lighting)"
        }
    
    # Save corrected data
    return save_json_file('locales/en.json', en_data)

def main():
    """Main function"""
    print("Fixing English translation file...")
    
    if fix_english_translations():
        print("Successfully fixed English translations")
    else:
        print("Failed to fix English translations")

if __name__ == "__main__":
    main()