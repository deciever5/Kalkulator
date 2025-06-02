"""Adjusted labor pricing and added permanent costs markup and labor profit margin to StructuralCalculations class."""
"""
Structural Calculations Module
Provides engineering calculations for container modifications and structural analysis
"""

import math
from typing import Dict, List, Any, Tuple
import pandas as pd
from datetime import datetime

# Cache lookup tables - Enhanced with all container types
BASE_COSTS = {
    "10ft Compact": 6000,
    "20ft Standard": 8000,
    "20ft High Cube": 9000,
    "40ft Standard": 12000,
    "40ft High Cube": 14000,
    "20ft Refrigerated": 15000,
    "Multi-unit Container": 25000,
    "Custom Size Container": 18000,
    "Refurbished Container": 6500
}

USE_CASE_MULTIPLIERS = {
    'Office Space': 1.5,
    'Residential': 2.0,
    'Storage': 1.0,
    'Workshop': 1.3,
    'Retail': 1.8,
    'Restaurant': 2.2,
    'Medical': 2.5,
    'Laboratory': 3.0
}

FINISH_COSTS = {
    'Basic': 0,
    'Standard': 3000,
    'Premium': 8000,
    'Luxury': 15000
}

def calculate_container_cost(config):
    """Calculate container cost based on configuration - comprehensive pricing"""
    
    # Enhanced base costs
    enhanced_base_costs = {
        "10ft Compact": 6000,
        "20ft Standard": 8000,
        "20ft High Cube": 9000,
        "40ft Standard": 12000,
        "40ft High Cube": 14000,
        "20ft Refrigerated": 15000,
        "Multi-unit Container": 25000,
        "Custom Size Container": 18000,
        "Refurbished Container": 6500
    }
    
    base_cost = enhanced_base_costs.get(config.get('container_type', '20ft Standard'), 8000)
    multiplier = USE_CASE_MULTIPLIERS.get(config.get('main_purpose', 'Storage'), 1.0)

    # Calculate modifications cost efficiently
    modifications_cost = 0

    # Construction material costs
    construction_material_costs = {
        'steel': 0,  # Base price
        'aluminum': 3500,  # Premium for aluminum
        'composite': 5000   # Highest premium for composite
    }
    construction_material = config.get('construction_material', 'steel').lower()
    if any(key in construction_material.lower() for key in construction_material_costs.keys()):
        for key, cost in construction_material_costs.items():
            if key in construction_material.lower():
                modifications_cost += cost
                break

    # Environment costs
    environment_costs = {
        'indoor': 0,
        'outdoor_standard': 500,
        'outdoor_extreme': 2000,
        'industrial': 1500,
        'construction': 1200,
        'agricultural': 800,
        'marine': 2500
    }
    environment = config.get('environment', '').lower()
    for key, cost in environment_costs.items():
        if key in environment.lower():
            modifications_cost += cost
            break

    # Finish level costs
    finish_level_costs = {
        'basic': 0,
        'shell': 2000,
        'standard': 4000,
        'comfort': 8000,
        'luxury': 15000,
        'specialist': 20000
    }
    finish_level = config.get('finish_level', '').lower()
    for key, cost in finish_level_costs.items():
        if key in finish_level.lower():
            modifications_cost += cost
            break

    # Flooring costs
    flooring_costs = {
        'none': 0,
        'plywood': 800,
        'anti_slip': 1200,
        'laminate': 1500,
        'vinyl': 1800,
        'carpet': 1000,
        'epoxy': 2500,
        'concrete': 3000,
        'hardwood': 3500
    }
    flooring = config.get('flooring', '').lower()
    for key, cost in flooring_costs.items():
        if key in flooring.lower():
            modifications_cost += cost
            break

    # Climate zone adjustments
    climate_zone_costs = {
        'northern_europe': 1500,  # Extra insulation needed
        'central_europe': 800,
        'southern_europe': 300,
        'continental': 1200,
        'maritime': 1000,
        'mountain': 2000,
        'tropical': 1800
    }
    climate_zone = config.get('climate_zone', '').lower()
    for key, cost in climate_zone_costs.items():
        if key in climate_zone.lower():
            modifications_cost += cost
            break

    # Insulation costs based on level
    insulation_costs = {
        'basic': 1500,
        'standard': 2500,
        'premium': 4000,
        'extreme': 6000
    }
    insulation = config.get('insulation', '').lower()
    for key, cost in insulation_costs.items():
        if key in insulation.lower():
            modifications_cost += cost
            break

    # Windows costs - enhanced
    window_count_costs = {
        'none': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5
    }
    num_windows_str = config.get('num_windows', 'none').lower()
    num_windows = 0
    for key, count in window_count_costs.items():
        if key in num_windows_str:
            num_windows = count
            break

    window_type_costs = {
        'standard': 600,
        'panoramic': 1200,
        'sliding': 800,
        'tilt': 750,
        'security': 900,
        'energy_efficient': 1000,
        'skylight': 1500
    }
    
    window_types = config.get('window_types', [])
    if isinstance(window_types, str):
        window_types = [window_types]
    
    total_window_cost = 0
    for window_type in window_types:
        for key, cost in window_type_costs.items():
            if key in window_type.lower():
                total_window_cost += cost
                break
    
    modifications_cost += num_windows * (total_window_cost if total_window_cost > 0 else 600)

    # Lighting system costs
    lighting_costs = {
        'none': 0,
        'basic_led': 800,
        'energy_efficient': 1200,
        'exterior': 1500,
        'emergency': 2000,
        'smart': 2500
    }
    lighting = config.get('lighting', '').lower()
    for key, cost in lighting_costs.items():
        if key in lighting.lower():
            modifications_cost += cost
            break

    # Ventilation system costs
    ventilation_costs = {
        'none': 0,
        'gravity': 300,
        'wall_fans': 800,
        'mechanical': 1500,
        'heat_recovery': 2500,
        'split_ac': 3000,
        'central_ac': 5000,
        'industrial': 4000
    }
    ventilation = config.get('ventilation', '').lower()
    for key, cost in ventilation_costs.items():
        if key in ventilation.lower():
            modifications_cost += cost
            break

    # Roof modifications costs
    roof_mod_costs = {
        'none': 0,
        'insulation': 1200,
        'skylight': 2500,
        'fans': 1000,
        'solar': 8000,
        'antennas': 500,
        'sloped': 3000,
        'terrace': 5000,
        'snow_removal': 800
    }
    roof_mods = config.get('roof_modifications', '').lower()
    for key, cost in roof_mod_costs.items():
        if key in roof_mods.lower():
            modifications_cost += cost
            break

    # Electrical system costs
    electrical_costs = {
        'none': 0,
        'preparation': 500,
        'basic': 1200,
        'standard': 1800,
        'extended': 3000,
        'industrial': 3500,
        'it_server': 4500,
        'smart': 5000
    }
    electrical = config.get('electrical_system', '').lower()
    for key, cost in electrical_costs.items():
        if key in electrical.lower():
            modifications_cost += cost
            break

    # Plumbing system costs
    plumbing_costs = {
        'none': 0,
        'preparation': 800,
        'cold_water': 1500,
        'hot_cold_water': 2000,
        'basic_sanitary': 2500,
        'standard_sanitary': 3500,
        'comfort_sanitary': 4500,
        'premium_sanitary': 7000,
        'industrial': 5000
    }
    plumbing = config.get('plumbing_system', '').lower()
    for key, cost in plumbing_costs.items():
        if key in plumbing.lower():
            modifications_cost += cost
            break

    # HVAC system costs
    hvac_costs = {
        'none': 0,
        'electric_heaters': 1200,
        'electric_heating': 1800,
        'heat_pump': 5500,
        'gas_heating': 3000,
        'split_ac': 3000,
        'vrv_vrf': 8000,
        'underfloor_heating': 4000,
        'central_ac': 6000
    }
    hvac = config.get('hvac_system', '').lower()
    for key, cost in hvac_costs.items():
        if key in hvac.lower():
            modifications_cost += cost
            break

    # Interior layout costs
    interior_layout_costs = {
        'open_space': 0,
        'partitioned': 2000,
        'built_in_furniture': 4000,
        'custom_layout': 3500,
        'mezzanine': 6000
    }
    interior_layout = config.get('interior_layout', '').lower()
    for key, cost in interior_layout_costs.items():
        if key in interior_layout.lower():
            modifications_cost += cost
            break

    # Security systems costs
    security_costs = {
        'none': 0,
        'basic': 800,
        'standard': 1500,
        'extended': 2500,
        'high': 4000,
        'maximum': 8000,
        'industrial': 6000
    }
    security = config.get('security_systems', '').lower()
    for key, cost in security_costs.items():
        if key in security.lower():
            modifications_cost += cost
            break

    # Exterior cladding costs
    cladding_costs = {
        'none': 0,
        'trapezoidal': 1500,
        'cassette': 2000,
        'vinyl_siding': 2500,
        'structural_plaster': 3000,
        'wood_cladding': 3500,
        'composite_panels': 4000,
        'clinker_brick': 5000,
        'natural_stone': 6000
    }
    cladding = config.get('exterior_cladding', '').lower()
    for key, cost in cladding_costs.items():
        if key in cladding.lower():
            modifications_cost += cost
            break

    # Additional openings costs
    additional_openings_costs = {
        'none': 0,
        'windows': 1500,
        'doors': 1200,
        'garage_door': 2500,
        'loading_dock': 4000,
        'ventilation': 800,
        'skylights': 2000,
        'custom': 2000
    }
    additional_openings = config.get('additional_openings', '').lower()
    for key, cost in additional_openings_costs.items():
        if key in additional_openings.lower():
            modifications_cost += cost
            break

    # Fire safety systems costs
    fire_safety_costs = {
        'none': 0,
        'basic': 500,
        'standard': 1500,
        'extended': 3000,
        'full': 5000
    }
    fire_systems = config.get('fire_systems', '').lower()
    for key, cost in fire_safety_costs.items():
        if key in fire_systems.lower():
            modifications_cost += cost
            break

    # Accessibility costs
    accessibility_costs = {
        'standard': 0,
        'ramp': 1200,
        'lift': 8000,
        'full_ada': 5000
    }
    accessibility = config.get('accessibility', '').lower()
    for key, cost in accessibility_costs.items():
        if key in accessibility.lower():
            modifications_cost += cost
            break

    # Paint and finish costs
    paint_costs = {
        'standard': 800,
        'extended': 1200,
        'marine': 2000,
        'industrial': 1500,
        'premium': 2500
    }
    paint_finish = config.get('paint_finish', '').lower()
    for key, cost in paint_costs.items():
        if key in paint_finish.lower():
            modifications_cost += cost
            break

    # Transport type costs
    transport_costs = {
        'standard': 0,
        'special': 1500,
        'crane': 2000,
        'multi_container': 800
    }
    transport_type = config.get('transport_type', '').lower()
    for key, cost in transport_costs.items():
        if key in transport_type.lower():
            modifications_cost += cost
            break

    # Installation costs
    installation_costs = {
        'none': 0,
        'basic': 1200,
        'standard': 2000,
        'full': 3500
    }
    installation = config.get('installation', '').lower()
    for key, cost in installation_costs.items():
        if key in installation.lower():
            modifications_cost += cost
            break

    # Equipment costs
    office_equipment_costs = {
        'none': 0,
        'basic': 2000,
        'standard': 4000,
        'full': 8000
    }
    office_equipment = config.get('office_equipment', '').lower()
    for key, cost in office_equipment_costs.items():
        if key in office_equipment.lower():
            modifications_cost += cost
            break

    appliances_costs = {
        'none': 0,
        'basic': 1500,
        'standard': 3000,
        'full': 6000
    }
    appliances = config.get('appliances', '').lower()
    for key, cost in appliances_costs.items():
        if key in appliances.lower():
            modifications_cost += cost
            break

    it_systems_costs = {
        'none': 0,
        'basic': 1000,
        'standard': 2500,
        'advanced': 5000
    }
    it_systems = config.get('it_systems', '').lower()
    for key, cost in it_systems_costs.items():
        if key in it_systems.lower():
            modifications_cost += cost
            break

    # Calculate delivery costs based on delivery zone
    delivery_cost = calculate_delivery_cost(config.get('delivery_zone', 'Local'), config.get('container_type', '20ft Standard'))

    # Calculate material costs (base + modifications)
    material_cost = base_cost + modifications_cost
    
    # Calculate labor cost (varies by complexity)
    labor_hours = calculate_labor_hours(config)
    labor_cost = calculate_labor_cost(labor_hours)
    
    # Calculate subtotal (materials + labor)
    subtotal_materials_labor = material_cost + labor_cost
    
    # Apply use case complexity multiplier
    subtotal_with_multiplier = subtotal_materials_labor * multiplier
    
    # Add operating costs (45% markup on materials + labor as per company policy)
    operating_costs = subtotal_with_multiplier * 0.45
    
    # Add profit margin (additional 20% on total before delivery)
    profit_margin = (subtotal_with_multiplier + operating_costs) * 0.20
    
    # Calculate subtotal before delivery
    subtotal_before_delivery = subtotal_with_multiplier + operating_costs + profit_margin
    
    # Add delivery cost
    total_cost = subtotal_before_delivery + delivery_cost

    return {
        'base_cost': base_cost,
        'modifications_cost': modifications_cost,
        'material_cost': material_cost,
        'labor_cost': labor_cost,
        'labor_hours': labor_hours,
        'use_case_multiplier': multiplier,
        'subtotal_materials_labor': subtotal_materials_labor,
        'subtotal_with_multiplier': subtotal_with_multiplier,
        'operating_costs': operating_costs,
        'profit_margin': profit_margin,
        'subtotal_before_delivery': subtotal_before_delivery,
        'delivery_cost': delivery_cost,
        'total_cost': total_cost
    }

def calculate_labor_hours(config):
    """Calculate total labor hours needed based on configuration"""
    
    base_hours = 40  # Base setup hours
    modification_hours = 0
    
    # Window installation hours
    num_windows_str = config.get('num_windows', 'none').lower()
    window_count = 0
    if 'one' in num_windows_str:
        window_count = 1
    elif 'two' in num_windows_str:
        window_count = 2
    elif 'three' in num_windows_str:
        window_count = 3
    elif 'four' in num_windows_str:
        window_count = 4
    elif 'five' in num_windows_str:
        window_count = 5
    
    modification_hours += window_count * 6  # 6 hours per window
    
    # Electrical system hours
    electrical = config.get('electrical_system', '').lower()
    if 'basic' in electrical:
        modification_hours += 16
    elif 'standard' in electrical:
        modification_hours += 24
    elif 'extended' in electrical or 'industrial' in electrical:
        modification_hours += 40
    elif 'smart' in electrical:
        modification_hours += 48
    
    # Plumbing system hours
    plumbing = config.get('plumbing_system', '').lower()
    if 'preparation' in plumbing:
        modification_hours += 8
    elif 'cold_water' in plumbing:
        modification_hours += 16
    elif 'hot_cold' in plumbing:
        modification_hours += 24
    elif 'sanitary' in plumbing:
        if 'basic' in plumbing:
            modification_hours += 32
        elif 'standard' in plumbing:
            modification_hours += 40
        elif 'comfort' in plumbing or 'premium' in plumbing:
            modification_hours += 56
    elif 'industrial' in plumbing:
        modification_hours += 48
    
    # HVAC system hours
    hvac = config.get('hvac_system', '').lower()
    if 'electric_heaters' in hvac:
        modification_hours += 8
    elif 'electric_heating' in hvac:
        modification_hours += 16
    elif 'split_ac' in hvac:
        modification_hours += 24
    elif 'heat_pump' in hvac:
        modification_hours += 32
    elif 'central_ac' in hvac or 'vrv_vrf' in hvac:
        modification_hours += 48
    elif 'underfloor_heating' in hvac:
        modification_hours += 40
    
    # Insulation hours
    insulation = config.get('insulation', '').lower()
    if 'basic' in insulation:
        modification_hours += 16
    elif 'standard' in insulation:
        modification_hours += 24
    elif 'premium' in insulation:
        modification_hours += 32
    elif 'extreme' in insulation:
        modification_hours += 48
    
    # Interior layout complexity
    interior = config.get('interior_layout', '').lower()
    if 'partitioned' in interior:
        modification_hours += 16
    elif 'built_in_furniture' in interior:
        modification_hours += 32
    elif 'custom_layout' in interior:
        modification_hours += 24
    elif 'mezzanine' in interior:
        modification_hours += 48
    
    # Additional systems
    if config.get('lighting', '').lower() not in ['none', '']:
        modification_hours += 8
    
    if config.get('ventilation', '').lower() not in ['none', '']:
        modification_hours += 12
    
    if config.get('security_systems', '').lower() not in ['none', '']:
        modification_hours += 16
    
    if config.get('fire_systems', '').lower() not in ['none', '']:
        modification_hours += 12
    
    # Exterior modifications
    if config.get('exterior_cladding', '').lower() not in ['none', '']:
        modification_hours += 24
    
    if config.get('additional_openings', '').lower() not in ['none', '']:
        modification_hours += 16
    
    # Installation complexity
    installation = config.get('installation', '').lower()
    if 'standard' in installation:
        modification_hours += 16
    elif 'full' in installation:
        modification_hours += 32
    
    return base_hours + modification_hours

def calculate_labor_cost(total_hours):
    """Calculate labor cost with mixed skill rates and profit margin"""
    
    # Labor rate distribution (Polish market rates in EUR/hour)
    basic_hours = total_hours * 0.4      # 40% basic work at €12/hour
    skilled_hours = total_hours * 0.4    # 40% skilled work at €15/hour  
    specialist_hours = total_hours * 0.2 # 20% specialist work at €18/hour
    
    labor_cost = (basic_hours * 12 + skilled_hours * 15 + specialist_hours * 18)
    
    # Add 17% profit margin on labor as per company policy
    labor_cost_with_profit = labor_cost * 1.17
    
    return labor_cost_with_profit

def calculate_delivery_cost(delivery_zone, container_type):
    """Calculate delivery cost based on zone and container type"""

    # Base delivery costs by zone (in EUR)
    zone_costs = {
        'Local': 800,           # Poland local (do 100km)
        'Poland': 1200,         # Poland nationwide
        'Central_Europe': 2500, # Germany, Czech Republic, Slovakia, Austria
        'Western_Europe': 3500, # France, Netherlands, Belgium, Luxembourg
        'Northern_Europe': 4000, # Denmark, Sweden, Norway, Finland
        'Southern_Europe': 4200, # Italy, Spain, Portugal, Greece
        'Eastern_Europe': 3200,  # Hungary, Romania, Bulgaria, Croatia
        'UK_Ireland': 4500,     # United Kingdom, Ireland
        'International': 6500   # Outside Europe
    }

    base_delivery = zone_costs.get(delivery_zone, 800)

    # Container size multipliers
    size_multipliers = {
        "20ft Standard": 1.0,
        "40ft Standard": 1.4,
        "40ft High Cube": 1.5,
        "20ft Refrigerated": 1.2
    }

    multiplier = size_multipliers.get(container_type, 1.0)

    return base_delivery * multiplier

class StructuralCalculations:
    """Class for structural engineering calculations and analysis"""

    def __init__(self):
        # Material properties (typical values)
        self.steel_properties = {
            "corten_steel": {
                "yield_strength": 50000,  # psi
                "tensile_strength": 70000,  # psi
                "elastic_modulus": 29000000,  # psi
                "density": 490,  # lb/ft³
                "poisson_ratio": 0.3
            },
            "structural_steel": {
                "yield_strength": 36000,  # psi
                "tensile_strength": 58000,  # psi
                "elastic_modulus": 29000000,  # psi
                "density": 490,  # lb/ft³
                "poisson_ratio": 0.3
            }
        }

        # Load factors and safety factors
        self.load_factors = {
            "dead_load": 1.2,
            "live_load": 1.6,
            "wind_load": 1.0,
            "snow_load": 1.2,
            "seismic_load": 1.0
        }

        # Standard loading values
        self.standard_loads = {
            "office_live_load": 50,  # psf
            "residential_live_load": 40,  # psf
            "workshop_live_load": 125,  # psf
            "storage_live_load": 125,  # psf
        }

        # Base rates and factors - Polish market
        self.base_rates = {
            "labor_rates": {
                "basic_worker": 12,      # EUR per hour - basic construction worker
                "skilled_worker": 15,    # EUR per hour - skilled trades (electrical, plumbing)
                "specialist": 18,        # EUR per hour - specialist (welding, technical)
                "average_rate": 15       # EUR per hour - average rate for calculations
            },
            "permanent_costs_markup": 0.45,  # 45% on parts + labor
            "labor_profit_margin": 0.17,     # 17% profit on manual labor
            "overhead_factor": 0.15,         # 15%
            "tax_rate": 0.00,               # No VAT for B2B sales (23% VAT applies only for B2C)
        }

    def calculate_base_costs(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate base costs for container modifications"""

        base_type = config.get('base_type', '40ft Standard')
        use_case = config.get('use_case', 'Office Space')
        modifications = config.get('modifications', {})

        # Base container costs
        container_costs = {
            "20ft Standard": 3500,
            "40ft Standard": 5000,
            "40ft High Cube": 5500,
            "45ft High Cube": 6500,
            "48ft Standard": 7000,
            "53ft Standard": 7500
        }

        base_cost = container_costs.get(base_type, 5000)

        # Modification costs
        modification_costs = 0

        # Windows
        windows = modifications.get('windows', 0)
        modification_costs += windows * 800  # $800 per window

        # Additional doors
        doors = modifications.get('doors', 1)
        if doors > 1:
            modification_costs += (doors - 1) * 1200  # $1200 per additional door

        # Skylights
        skylights = modifications.get('skylights', 0)
        modification_costs += skylights * 1500  # $1500 per skylight

        # Ventilation
        vents = modifications.get('vents', 0)
        modification_costs += vents * 200  # $200 per vent

        # Systems with detailed options
        electrical_system = modifications.get('electrical_system', '')
        if electrical_system:
            electrical_costs = {
                'basic': 1200,
                'standard': 1800,
                'industrial': 3500,
                'smart': 5000
            }
            modification_costs += electrical_costs.get(electrical_system.lower(), 1800)

        plumbing_system = modifications.get('plumbing_system', '')
        if plumbing_system:
            plumbing_costs = {
                'basic': 2000,
                'standard': 2500,
                'full': 4500,
                'commercial': 7000
            }
            modification_costs += plumbing_costs.get(plumbing_system.lower(), 2500)

        hvac_system = modifications.get('hvac_system', '')
        if hvac_system:
            hvac_costs = {
                'basic': 1800,
                'split_air_conditioning': 3000,
                'central_air': 6000,
                'heat_pump': 5500,
                'industrial': 8000
            }
            modification_costs += hvac_costs.get(hvac_system.lower().replace(' ', '_'), 3000)

        # Insulation with levels
        insulation_level = modifications.get('insulation', '')
        if insulation_level:
            container_areas = self._get_container_areas(base_type)
            insulation_area = container_areas['wall_area'] + container_areas['ceiling_area']
            
            insulation_costs_per_sqft = {
                'basic': 1.20,
                'standard': 1.50,
                'premium': 2.00,
                'extreme': 2.80
            }
            cost_per_sqft = insulation_costs_per_sqft.get(insulation_level.lower(), 1.50)
            modification_costs += insulation_area * cost_per_sqft

        # Reinforcements
        if modifications.get('reinforcement_walls'):
            modification_costs += 2000

        if modifications.get('reinforcement_roof'):
            modification_costs += 1500

        if modifications.get('reinforcement_floor'):
            modification_costs += 1800

        if modifications.get('additional_support'):
            modification_costs += 2500

        # Total material cost
        total_material_cost = base_cost + modification_costs
        
        # Labor costs calculation using Polish rates
        # Estimate hours based on project complexity
        base_hours = 40  # Base hours for container setup
        mod_hours = 0

        # Add hours for modifications
        if modifications.get('windows', 0) > 0:
            mod_hours += modifications['windows'] * 8  # 8 hours per window
        if modifications.get('doors', 1) > 1:
            mod_hours += (modifications['doors'] - 1) * 6  # 6 hours per door
        if modifications.get('electrical'):
            mod_hours += 24  # 3 days for electrical
        if modifications.get('plumbing'):
            mod_hours += 32  # 4 days for plumbing
        if modifications.get('hvac'):
            mod_hours += 16  # 2 days for HVAC
        if modifications.get('insulation'):
            container_areas = self._get_container_areas(base_type)
            insulation_area = container_areas['wall_area'] + container_areas['ceiling_area']
            mod_hours += insulation_area / 25  # 25 sq ft per hour

        total_hours = base_hours + mod_hours

        # Calculate labor cost with mixed rates
        basic_hours = total_hours * 0.4      # 40% basic work
        skilled_hours = total_hours * 0.4    # 40% skilled work  
        specialist_hours = total_hours * 0.2 # 20% specialist work

        labor_cost = (basic_hours * self.base_rates["labor_rates"]["basic_worker"] + 
                     skilled_hours * self.base_rates["labor_rates"]["skilled_worker"] + 
                     specialist_hours * self.base_rates["labor_rates"]["specialist"])

        # Add 17% profit margin on labor
        labor_cost_with_profit = labor_cost * (1 + self.base_rates["labor_profit_margin"])

        # Calculate subtotal before permanent costs
        subtotal_before_permanent = base_cost + modification_costs + labor_cost_with_profit

        # Apply 45% permanent costs markup on parts + labor
        permanent_costs = subtotal_before_permanent * self.base_rates["permanent_costs_markup"]

        # Calculate subtotal
        subtotal = subtotal_before_permanent + permanent_costs

        return {
            "base_container": base_cost,
            "modifications": modification_costs,
            "labor": labor_cost_with_profit,
            "subtotal": subtotal,
            "materials_breakdown": {
                "container_base": base_cost,
                "structural_steel": modification_costs * 0.3,
                "electrical_materials": 3500 if modifications.get('electrical') else 0,
                "plumbing_materials": 4000 if modifications.get('plumbing') else 0,
                "hvac_materials": 2500 if modifications.get('hvac') else 0,
                "insulation_materials": insulation_area * 1.50 if modifications.get('insulation') else 0,
                "other_materials": modification_costs * 0.3
            }
        }

    def perform_structural_analysis(self, config: Dict[str, Any], 
                                  analysis_params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive structural analysis"""

        base_type = config.get('base_type', '40ft Standard')
        use_case = config.get('use_case', 'Office Space')
        modifications = config.get('modifications', {})

        # Get container dimensions
        container_specs = self._get_container_specs(base_type)
        safety_factor = analysis_params.get('safety_factor', 1.5)

        # Calculate loads
        loads = self._calculate_loads(config, analysis_params)

        # Perform structural calculations
        structural_results = self._analyze_structure(container_specs, loads, modifications, safety_factor)

        # Check compliance
        compliance = self._check_compliance(config, analysis_params, structural_results)

        # Calculate material requirements
        materials = self._calculate_material_requirements(config, structural_results)

        return {
            "load_ratio": structural_results["load_ratio"],
            "max_deflection": structural_results["max_deflection"],
            "deflection_limit": structural_results["deflection_limit"],
            "stress_ratio": structural_results["stress_ratio"],
            "foundation_required": structural_results["foundation_type"],
            "loads": loads,
            "structural_analysis": structural_results,
            "compliance": compliance,
            "materials": materials,
            "load_distribution": self._calculate_load_distribution(container_specs, loads),
            "stress_points": self._calculate_stress_points(container_specs, loads),
            "required_drawings": self._get_required_drawings(config, structural_results),
            "professional_requirements": self._get_professional_requirements(config, structural_results)
        }

    def _get_container_specs(self, base_type: str) -> Dict[str, float]:
        """Get container specifications"""
        specs = {
            "20ft Standard": {"length": 20, "width": 8, "height": 8.5, "wall_thickness": 0.075},
            "40ft Standard": {"length": 40, "width": 8, "height": 8.5, "wall_thickness": 0.075},
            "40ft High Cube": {"length": 40, "width": 8, "height": 9.5, "wall_thickness": 0.075},
            "45ft High Cube": {"length": 45, "width": 8, "height": 9.5, "wall_thickness": 0.075},
            "48ft Standard": {"length": 48, "width": 8, "height": 8.5, "wall_thickness": 0.075},
            "53ft Standard": {"length": 53, "width": 8, "height": 8.5, "wall_thickness": 0.075}
        }
        return specs.get(base_type, specs["40ft Standard"])

    def _get_container_areas(self, base_type: str) -> Dict[str, float]:
        """Calculate container surface areas"""
        specs = self._get_container_specs(base_type)

        return {
            "floor_area": specs["length"] * specs["width"],
            "wall_area": 2 * (specs["length"] * specs["height"] + specs["width"] * specs["height"]),
            "ceiling_area": specs["length"] * specs["width"],
            "total_surface": 2 * (specs["length"] * specs["width"]) + 
                           2 * (specs["length"] * specs["height"] + specs["width"] * specs["height"])
        }

    def _calculate_loads(self, config: Dict[str, Any], analysis_params: Dict[str, Any]) -> Dict[str, float]:
        """Calculate design loads according to European standards (EN 1991)"""

        use_case = config.get('use_case', 'Office Space')
        occupancy = config.get('occupancy', 4)

        # Live loads based on use case (EN 1991-1-1) - in kN/m²
        live_load_mapping = {
            "Office Space": 2.5,  # kN/m²
            "Residential Living": 2.0,
            "Workshop/Manufacturing": 5.0,
            "Storage/Warehouse": 7.5,
            "Retail/Commercial": 4.0
        }

        live_load = live_load_mapping.get(use_case, 2.5)

        # Dead loads (structure + finishes) - in kN/m²
        dead_load = 1.0  # kN/m² (basic structure)

        modifications = config.get('modifications', {})
        if modifications.get('insulation'):
            dead_load += 0.15  # Additional dead load for insulation

        if modifications.get('hvac'):
            dead_load += 0.25  # Additional dead load for HVAC

        # Environmental loads
        wind_load = analysis_params.get('wind_load', 120)  # km/h
        snow_load = analysis_params.get('snow_load', 1.5)  # kN/m²
        climate_zone = analysis_params.get('climate_zone', 'Umiarkowana (Europa Środkowa)')
        environmental_conditions = analysis_params.get('environmental_conditions', 'Standardowe')

        # Import European climate standards
        from .european_climate_standards import EuropeanClimateStandards
        climate_std = EuropeanClimateStandards()

        # Adjust loads based on European climate zones
        climate_factors = climate_std.get_climate_factors(climate_zone)
        env_factors = climate_std.get_environmental_factors(environmental_conditions)

        # Adjusted snow load based on climate zone
        adjusted_snow_load = climate_std.calculate_snow_load(snow_load, climate_zone)

        # Adjusted wind load based on climate zone  
        adjusted_wind_load = climate_std.calculate_wind_load(wind_load, climate_zone)

        # Convert wind speed to pressure (EN 1991-1-4) - in kN/m²
        wind_pressure = (adjusted_wind_load / 3.6) ** 2 * 0.0006  # kN/m²

        return {
            "dead_load": dead_load,
            "live_load": live_load,
            "wind_load": wind_pressure,
            "snow_load": adjusted_snow_load,
            "total_vertical": dead_load + live_load + adjusted_snow_load,
            "wind_pressure": wind_pressure,
            "climate_zone": climate_zone,
            "environmental_conditions": environmental_conditions,
            "climate_factors": climate_factors,
            "environmental_factors": env_factors
        }

    def _analyze_structure(self, container_specs: Dict[str, float], loads: Dict[str, float], 
                          modifications: Dict[str, Any], safety_factor: float) -> Dict[str, Any]:
        """Perform structural analysis calculations"""

        length = container_specs["length"]
        width = container_specs["width"]
        height = container_specs["height"]
        wall_thickness = container_specs["wall_thickness"]

        # Calculate section properties
        steel_props = self.steel_properties["corten_steel"]

        # Simplified beam analysis for roof loading
        total_load = loads["total_vertical"]  # psf
        beam_load = total_load * width  # plf (load per linear foot)

        # Maximum moment (simply supported beam)
        max_moment = beam_load * (length ** 2) / 8  # lb-ft
        max_moment *= 12  # Convert to lb-in

        # Section modulus of container frame (simplified)
        # Assume effective section modulus based on container construction
        section_modulus = 10.0  # in³ (conservative estimate)

        # Calculate stress
        max_stress = max_moment / section_modulus  # psi
        allowable_stress = steel_props["yield_strength"] / safety_factor

        stress_ratio = max_stress / allowable_stress

        # Deflection calculation
        moment_of_inertia = section_modulus * height / 2  # Approximate
        max_deflection = (5 * beam_load * (length * 12) ** 4) / (384 * steel_props["elastic_modulus"] * moment_of_inertia)
        max_deflection /= 12  # Convert to feet

        # Deflection limit (L/240 for live load)
        deflection_limit = length / 240

        # Load ratio (total load vs capacity)
        # Simplified capacity calculation
        area_capacity = steel_props["yield_strength"] * wall_thickness * width * 12  # Total capacity
        applied_load = total_load * length * width
        load_ratio = applied_load / area_capacity

        # Foundation requirements
        foundation_type = self._determine_foundation_type(loads, length, width)

        # Account for modifications that affect structural integrity
        modification_factor = 1.0

        if modifications.get('windows', 0) > 0:
            modification_factor += 0.1 * modifications['windows']  # Each window increases stress

        if modifications.get('doors', 0) > 1:
            modification_factor += 0.15 * (modifications['doors'] - 1)  # Additional doors

        if modifications.get('reinforcement_walls'):
            modification_factor *= 0.8  # Wall reinforcement reduces stress

        if modifications.get('reinforcement_roof'):
            modification_factor *= 0.85  # Roof reinforcement

        # Apply modification factor
        stress_ratio *= modification_factor
        load_ratio *= modification_factor

        return {
            "max_stress": max_stress,
            "allowable_stress": allowable_stress,
            "stress_ratio": stress_ratio,
            "max_deflection": max_deflection,
            "deflection_limit": deflection_limit,
            "load_ratio": load_ratio,
            "foundation_type": foundation_type,
            "modification_factor": modification_factor,
            "beam_analysis": {
                "max_moment": max_moment,
                "section_modulus": section_modulus,
                "moment_of_inertia": moment_of_inertia
            }
        }

    def _determine_foundation_type(self, loads: Dict[str, float], length: float, width: float) -> str:
        """Determine foundation requirements"""

        total_load = loads["total_vertical"] * length * width

        if total_load < 20000:
            return "Concrete Pads"
        elif total_load < 40000:
            return "Strip Foundation"
        elif total_load < 80000:
            return "Slab Foundation"
        else:
            return "Engineered Foundation"

    def _check_compliance(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                         structural_results: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
        """Check European building code compliance"""

        building_code = analysis_params.get('building_code', 'EN (European Norms)')
        use_case = config.get('use_case', 'Office Space')
        climate_zone = analysis_params.get('climate_zone', 'Umiarkowana (Europa Środkowa)')
        environmental_conditions = analysis_params.get('environmental_conditions', 'Standardowe')

        # Import European climate standards for compliance requirements
        from .european_climate_standards import EuropeanClimateStandards
        climate_std = EuropeanClimateStandards()

        # Get specific compliance requirements for climate zone and use case
        compliance_reqs = climate_std.get_compliance_requirements(climate_zone, use_case)

        compliance_results = {
            "european_standards": {},
            "climate_specific": {},
            "structural": {},
            "environmental": {}
        }

        # Structural compliance
        if structural_results["stress_ratio"] < 1.0:
            compliance_results["structural"]["Stress Check"] = "Pass"
        else:
            compliance_results["structural"]["Stress Check"] = "Fail"

        if structural_results["load_ratio"] < 1.0:
            compliance_results["structural"]["Load Check"] = "Pass"
        else:
            compliance_results["structural"]["Load Check"] = "Fail"

        if structural_results["max_deflection"] < structural_results["deflection_limit"]:
            compliance_results["structural"]["Deflection Check"] = "Pass"
        else:
            compliance_results["structural"]["Deflection Check"] = "Fail"

        # Safety requirements
        modifications = config.get('modifications', {})

        # Exit requirements
        if use_case in ["Office Space", "Retail/Commercial"] and config.get('occupancy', 1) > 49:
            if modifications.get('doors', 1) >= 2:
                compliance_results["safety"]["Emergency Exits"] = "Pass"
            else:
                compliance_results["safety"]["Emergency Exits"] = "Fail"
        else:
            compliance_results["safety"]["Emergency Exits"] = "Pass"

        # Ventilation
        if modifications.get('hvac') or modifications.get('vents', 0) > 0:
            compliance_results["safety"]["Ventilation"] = "Pass"
        else:
            compliance_results["safety"]["Ventilation"] = "Review Required"

        # Electrical safety
        if modifications.get('electrical'):
            compliance_results["safety"]["Electrical Code"] = "Pass"
        else:
            compliance_results["safety"]["Electrical Code"] = "N/A"

        # Building code specific checks
        if "IBC" in building_code:
            compliance_results["building_codes"]["IBC Structural"] = "Pass" if structural_results["stress_ratio"] < 1.0 else "Fail"
            compliance_results["building_codes"]["IBC Fire Safety"] = "Review Required"
            compliance_results["building_codes"]["IBC Accessibility"] = "Review Required" if use_case in ["Office Space", "Retail/Commercial"] else "N/A"

        return compliance_results

    def _calculate_material_requirements(self, config: Dict[str, Any], 
                                       structural_results: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Calculate detailed material requirements"""

        base_type = config.get('base_type', '40ft Standard')
        modifications = config.get('modifications', {})
        container_specs = self._get_container_specs(base_type)

        materials = {}

        # Base container
        materials["base_container"] = {
            "material": "Corten Steel Container",
            "quantity": "1 each",
            "specification": f"{base_type} ISO container"
        }

        # Structural reinforcements
        if modifications.get('reinforcement_walls'):
            materials["wall_reinforcement"] = {
                "material": "Structural Steel Angles",
                "quantity": "200 lbs",
                "specification": "A36 Steel, 3x3x1/4 angles"
            }

        if modifications.get('reinforcement_roof'):
            materials["roof_reinforcement"] = {
                "material": "Structural Steel Beams",
                "quantity": "150 lbs",
                "specification": "A36 Steel, W8x10 beams"
            }

        if modifications.get('additional_support'):
            materials["support_beams"] = {
                "material": "Steel Support Posts",
                "quantity": "4 each",
                "specification": "4x4 HSS posts, A500 Grade B"
            }

        # Windows and doors
        if modifications.get('windows', 0) > 0:
            materials["windows"] = {
                "material": "Aluminum Frame Windows",
                "quantity": f"{modifications['windows']} each",
                "specification": "Double-pane, thermally broken"
            }

        if modifications.get('doors', 1) > 1:
            materials["additional_doors"] = {
                "material": "Steel Personnel Doors",
                "quantity": f"{modifications['doors'] - 1} each",
                "specification": "3'x7', insulated, weather sealed"
            }

        # Insulation
        if modifications.get('insulation'):
            container_areas = self._get_container_areas(base_type)
            insulation_area = container_areas['wall_area'] + container_areas['ceiling_area']
            materials["insulation"] = {
                "material": "Spray Foam Insulation",
                "quantity": f"{insulation_area:.0f} sq ft",
                "specification": "Closed-cell, R-6.5 per inch"
            }

        # Foundation
        foundation_type = structural_results.get("foundation_type", "Concrete Pads")
        if foundation_type == "Concrete Pads":
            materials["foundation"] = {
                "material": "Concrete Pads",
                "quantity": "4 each",
                "specification": "3'x3'x1' concrete pads, 3000 psi"
            }
        elif foundation_type == "Strip Foundation":
            materials["foundation"] = {
                "material": "Strip Foundation",
                "quantity": f"{container_specs['length'] * 2 + container_specs['width'] * 2:.0f} lin ft",
                "specification": "12\"x8\" concrete strip, 3000 psi"
            }

        return materials

    def get_all_pricing_rates(self) -> Dict[str, Any]:
        """Get all pricing rates and factors used in calculations"""
        
        # Container base costs
        container_costs = {
            "20ft_standard": "€3,000 (2,500 + transport + 20% margin)",
            "40ft_standard": "€4,200 (3,500 + transport + 20% margin)",
            "40ft_high_cube": "€4,500 (3,750 + transport + 20% margin)",
            "45ft_high_cube": "€5,000 (4,167 + transport + 20% margin)",
            "48ft_standard": "€5,500 (4,583 + transport + 20% margin)",
            "53ft_standard": "€6,000 (5,000 + transport + 20% margin)"
        }
        
        # Modification costs
        modification_costs = {
            "window_per_unit": "€600 per window",
            "additional_door": "€900 per door", 
            "electrical_system": "€1,800 basic package",
            "plumbing_system": "€2,500 basic package",
            "hvac_system": "€3,000 mini-split system",
            "wall_reinforcement": "€2,000",
            "roof_reinforcement": "€1,500",
            "floor_reinforcement": "€1,800",
            "additional_support": "€2,500"
        }
        
        return {
            "labor_rates": {
                f"{role.replace('_', ' ').title()}": f"€{rate}/hour" 
                for role, rate in self.base_rates["labor_rates"].items()
            },
            "markup_rates": {
                "Permanent costs markup": f"{self.base_rates['permanent_costs_markup']*100:.0f}% on parts + labor",
                "Labor profit margin": f"{self.base_rates['labor_profit_margin']*100:.0f}% on manual labor",
                "Overhead factor": f"{self.base_rates['overhead_factor']*100:.0f}%"
            },
            "container_base_costs": container_costs,
            "modification_costs": modification_costs,
            "tax_rate": "VAT excluded for B2B sales (added at invoicing per applicable regulations)",
            "calculation_method": {
                "step_1": "Base container cost + transport + 20% margin",
                "step_2": "Add modification costs",
                "step_3": "Calculate labor hours and apply mixed rates",
                "step_4": "Add 17% profit margin on labor",
                "step_5": "Apply 45% permanent costs markup on (parts + labor)",
                "step_6": "Final price excluding VAT"
            }
        }

    def _calculate_load_distribution(self, container_specs: Dict[str, float], 
                                   loads: Dict[str, float]) -> Dict[str, Dict[str, List[float]]]:
        """Calculate load distribution for visualization"""

        length = container_specs["length"]
        width = container_specs["width"]

        # Create coordinate arrays for visualization
        x_coords = [i * length / 10 for i in range(11)]  # 11 points along length

        # Uniform load distribution
        uniform_load = [loads["total_vertical"]] * len(x_coords)

        # Wind load distribution (varies along height)
        wind_load = [loads["wind_pressure"] * (1 + i * 0.1) for i in range(len(x_coords))]

        return {
            "dead_load": {
                "x_coords": x_coords,
                "y_coords": [loads["dead_load"]] * len(x_coords)
            },
            "live_load": {
                "x_coords": x_coords,
                "y_coords": [loads["live_load"]] * len(x_coords)
            },
            "wind_load": {
                "x_coords": x_coords,
                "y_coords": wind_load
            },
            "total_load": {
                "x_coords": x_coords,
                "y_coords": uniform_load
            }
        }

    def _calculate_stress_points(self, container_specs: Dict[str, float], 
                               loads: Dict[str, float]) -> Dict[str, List[float]]:
        """Calculate stress distribution points for visualization"""

        length = container_specs["length"]
        width = container_specs["width"]

        # Create grid of stress points
        x_points = [i * length / 5 for i in range(6)]  # 6 points along length
        y_points = [i * width / 3 for i in range(4)]   # 4 points along width

        x_coords = []
        y_coords = []
        stress_values = []

        # Calculate stress at each point (simplified)
        max_stress = loads["total_vertical"] * 1.5  # Simplified stress calculation

        for x in x_points:
            for y in y_points:
                x_coords.append(x)
                y_coords.append(y)

                # Stress varies based on location (higher at corners and mid-span)
                distance_factor = abs(x - length/2) / (length/2)  # 0 at center, 1 at ends
                stress = max_stress * (0.5 + 0.5 * distance_factor)
                stress_values.append(stress)

        return {
            "x_coords": x_coords,
            "y_coords": y_coords,
            "stress_values": stress_values
        }