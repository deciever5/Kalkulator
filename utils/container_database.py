"""
Container Database Module
Provides standard container specifications and modification options
"""

import pandas as pd
from typing import Dict, List, Any

class ContainerDatabase:
    """Database of standard container specifications and modification options"""
    
    def __init__(self):
        self.container_types = self._initialize_container_types()
        self.modification_options = self._initialize_modifications()
        self.material_specs = self._initialize_materials()
        self.compliance_codes = self._initialize_compliance()
    
    def _initialize_container_types(self) -> Dict[str, Dict[str, Any]]:
        """Initialize standard container type specifications"""
        return {
            "20ft Standard": {
                "length": 20,
                "width": 8,
                "height": 8.5,
                "internal_length": 19.33,
                "internal_width": 7.7,
                "internal_height": 7.83,
                "weight": 5000,  # lbs
                "payload": 62000,  # lbs
                "volume": 1172,  # cubic feet
                "construction": "Corten steel",
                "floor": "Marine plywood",
                "doors": "Double doors (rear)"
            },
            "40ft Standard": {
                "length": 40,
                "width": 8,
                "height": 8.5,
                "internal_length": 39.33,
                "internal_width": 7.7,
                "internal_height": 7.83,
                "weight": 8000,  # lbs
                "payload": 67000,  # lbs
                "volume": 2372,  # cubic feet
                "construction": "Corten steel",
                "floor": "Marine plywood",
                "doors": "Double doors (rear)"
            },
            "40ft High Cube": {
                "length": 40,
                "width": 8,
                "height": 9.5,
                "internal_length": 39.33,
                "internal_width": 7.7,
                "internal_height": 8.83,
                "weight": 8500,  # lbs
                "payload": 66500,  # lbs
                "volume": 2694,  # cubic feet
                "construction": "Corten steel",
                "floor": "Marine plywood",
                "doors": "Double doors (rear)"
            },
            "45ft High Cube": {
                "length": 45,
                "width": 8,
                "height": 9.5,
                "internal_length": 44.33,
                "internal_width": 7.7,
                "internal_height": 8.83,
                "weight": 9000,  # lbs
                "payload": 66000,  # lbs
                "volume": 3030,  # cubic feet
                "construction": "Corten steel",
                "floor": "Marine plywood",
                "doors": "Double doors (rear)"
            },
            "48ft Standard": {
                "length": 48,
                "width": 8,
                "height": 8.5,
                "internal_length": 47.33,
                "internal_width": 7.7,
                "internal_height": 7.83,
                "weight": 9500,  # lbs
                "payload": 65500,  # lbs
                "volume": 2855,  # cubic feet
                "construction": "Corten steel",
                "floor": "Marine plywood",
                "doors": "Double doors (rear)"
            },
            "53ft Standard": {
                "length": 53,
                "width": 8,
                "height": 8.5,
                "internal_length": 52.33,
                "internal_width": 7.7,
                "internal_height": 7.83,
                "weight": 10500,  # lbs
                "payload": 64500,  # lbs
                "volume": 3154,  # cubic feet
                "construction": "Corten steel",
                "floor": "Marine plywood",
                "doors": "Double doors (rear)"
            }
        }
    
    def _initialize_modifications(self) -> Dict[str, Dict[str, Any]]:
        """Initialize modification options and specifications"""
        return {
            "windows": {
                "standard_window": {
                    "size": "3x4 ft",
                    "cost_per_unit": 800,
                    "material": "Double-pane glass",
                    "frame": "Aluminum",
                    "installation_hours": 4
                },
                "large_window": {
                    "size": "4x6 ft",
                    "cost_per_unit": 1200,
                    "material": "Double-pane glass",
                    "frame": "Aluminum",
                    "installation_hours": 6
                },
                "sliding_window": {
                    "size": "6x4 ft",
                    "cost_per_unit": 1500,
                    "material": "Double-pane glass",
                    "frame": "Aluminum",
                    "installation_hours": 5
                }
            },
            "doors": {
                "personnel_door": {
                    "size": "3x7 ft",
                    "cost_per_unit": 1200,
                    "material": "Steel",
                    "features": "Lock, weather stripping",
                    "installation_hours": 6
                },
                "double_door": {
                    "size": "6x7 ft",
                    "cost_per_unit": 2000,
                    "material": "Steel",
                    "features": "Lock, weather stripping",
                    "installation_hours": 8
                },
                "roll_up_door": {
                    "size": "8x8 ft",
                    "cost_per_unit": 3500,
                    "material": "Aluminum",
                    "features": "Electric opener",
                    "installation_hours": 12
                }
            },
            "insulation": {
                "spray_foam": {
                    "r_value": 6.5,
                    "cost_per_sqft": 1.50,
                    "thickness": "1 inch",
                    "fire_rating": "Class A"
                },
                "rigid_foam": {
                    "r_value": 5.0,
                    "cost_per_sqft": 1.20,
                    "thickness": "1 inch",
                    "fire_rating": "Class A"
                },
                "fiberglass_batt": {
                    "r_value": 3.5,
                    "cost_per_sqft": 0.80,
                    "thickness": "3.5 inches",
                    "fire_rating": "Class A"
                }
            },
            "electrical": {
                "basic_package": {
                    "description": "Outlets, switches, basic lighting",
                    "cost": 3500,
                    "amp_service": 100,
                    "includes": ["Panel", "Outlets", "Switches", "LED lighting"]
                },
                "standard_package": {
                    "description": "Enhanced electrical with HVAC support",
                    "cost": 5500,
                    "amp_service": 200,
                    "includes": ["Panel", "Outlets", "Switches", "LED lighting", "HVAC circuits"]
                },
                "premium_package": {
                    "description": "Full electrical with smart controls",
                    "cost": 8500,
                    "amp_service": 200,
                    "includes": ["Panel", "Outlets", "Switches", "LED lighting", "HVAC circuits", "Smart controls"]
                }
            },
            "plumbing": {
                "basic_package": {
                    "description": "Rough plumbing for utilities",
                    "cost": 4000,
                    "includes": ["Water supply", "Drain lines", "Vent stack"]
                },
                "bathroom_package": {
                    "description": "Complete bathroom installation",
                    "cost": 8500,
                    "includes": ["Toilet", "Sink", "Shower", "Water heater", "Plumbing"]
                },
                "kitchen_package": {
                    "description": "Kitchen plumbing installation",
                    "cost": 6500,
                    "includes": ["Kitchen sink", "Dishwasher prep", "Water lines"]
                }
            },
            "hvac": {
                "mini_split": {
                    "capacity": "12000 BTU",
                    "cost": 2500,
                    "efficiency": "SEER 16",
                    "coverage": "500 sq ft"
                },
                "packaged_unit": {
                    "capacity": "24000 BTU",
                    "cost": 4500,
                    "efficiency": "SEER 14",
                    "coverage": "1000 sq ft"
                },
                "heat_pump": {
                    "capacity": "18000 BTU",
                    "cost": 3500,
                    "efficiency": "SEER 15",
                    "coverage": "750 sq ft"
                }
            }
        }
    
    def _initialize_materials(self) -> Dict[str, Dict[str, Any]]:
        """Initialize material specifications and current pricing"""
        return {
            "steel": {
                "corten_steel": {
                    "grade": "A588",
                    "yield_strength": 50000,  # psi
                    "tensile_strength": 70000,  # psi
                    "cost_per_lb": 1.20,
                    "density": 0.284  # lb/cubic inch
                },
                "structural_steel": {
                    "grade": "A36",
                    "yield_strength": 36000,  # psi
                    "tensile_strength": 58000,  # psi
                    "cost_per_lb": 0.90,
                    "density": 0.284  # lb/cubic inch
                },
                "stainless_steel": {
                    "grade": "316L",
                    "yield_strength": 42000,  # psi
                    "tensile_strength": 84000,  # psi
                    "cost_per_lb": 3.50,
                    "density": 0.289  # lb/cubic inch
                }
            },
            "lumber": {
                "pressure_treated": {
                    "grade": "Southern Pine #2",
                    "cost_per_bf": 0.85,  # per board foot
                    "moisture_content": "19%",
                    "treatment": "ACQ"
                },
                "marine_plywood": {
                    "grade": "A/B",
                    "cost_per_sqft": 2.50,
                    "thickness": "3/4 inch",
                    "waterproof": True
                }
            },
            "concrete": {
                "standard_mix": {
                    "strength": 3000,  # psi
                    "cost_per_yard": 120,
                    "slump": "4-6 inches"
                },
                "high_strength": {
                    "strength": 4000,  # psi
                    "cost_per_yard": 140,
                    "slump": "4-6 inches"
                }
            }
        }
    
    def _initialize_compliance(self) -> Dict[str, Dict[str, Any]]:
        """Initialize building codes and compliance requirements"""
        return {
            "IBC": {
                "name": "International Building Code",
                "occupancy_classifications": {
                    "R-3": "Residential",
                    "B": "Business/Office",
                    "F-1": "Factory/Industrial",
                    "S-1": "Storage",
                    "M": "Mercantile"
                },
                "construction_types": {
                    "Type V-B": "Wood frame, non-fire rated",
                    "Type II-B": "Non-combustible, non-fire rated"
                },
                "requirements": {
                    "fire_separation": "Required for multi-unit",
                    "egress": "Two exits required over 500 sq ft occupant load > 49",
                    "accessibility": "ADA compliance required for commercial"
                }
            },
            "IRC": {
                "name": "International Residential Code",
                "applicable_to": "Single family residential",
                "requirements": {
                    "ceiling_height": "7.5 ft minimum",
                    "bedroom_area": "70 sq ft minimum",
                    "window_area": "8% of floor area minimum",
                    "egress": "Emergency egress required in bedrooms"
                }
            },
            "local_codes": {
                "setbacks": "Varies by jurisdiction",
                "permits": "Building permit typically required",
                "inspections": "Foundation, framing, electrical, plumbing, final",
                "zoning": "Check local zoning for container structures"
            }
        }
    
    def get_container_types(self) -> Dict[str, Dict[str, Any]]:
        """Get all available container types"""
        return self.container_types
    
    def get_container_specs(self, container_type: str) -> Dict[str, Any]:
        """Get specifications for a specific container type"""
        return self.container_types.get(container_type, {})
    
    def get_modification_options(self, category: str = None) -> Dict[str, Any]:
        """Get modification options, optionally filtered by category"""
        if category:
            return self.modification_options.get(category, {})
        return self.modification_options
    
    def get_material_specs(self, material_type: str = None) -> Dict[str, Any]:
        """Get material specifications"""
        if material_type:
            return self.material_specs.get(material_type, {})
        return self.material_specs
    
    def get_compliance_requirements(self, code: str = None) -> Dict[str, Any]:
        """Get building code and compliance requirements"""
        if code:
            return self.compliance_codes.get(code, {})
        return self.compliance_codes
    
    def calculate_container_area(self, container_type: str) -> Dict[str, float]:
        """Calculate various area measurements for a container"""
        specs = self.get_container_specs(container_type)
        if not specs:
            return {}
        
        return {
            "floor_area": specs["internal_length"] * specs["internal_width"],
            "wall_area": 2 * (specs["internal_length"] * specs["internal_height"] + 
                             specs["internal_width"] * specs["internal_height"]),
            "ceiling_area": specs["internal_length"] * specs["internal_width"],
            "total_internal_volume": specs["volume"]
        }
    
    def get_use_case_requirements(self, use_case: str) -> Dict[str, Any]:
        """Get specific requirements for different use cases"""
        requirements = {
            "Office Space": {
                "min_ceiling_height": 8.0,
                "min_area_per_person": 50,
                "required_systems": ["electrical", "hvac", "insulation"],
                "building_code": "IBC - Business (B)",
                "accessibility": "ADA required",
                "parking": "1 space per 300 sq ft"
            },
            "Residential Living": {
                "min_ceiling_height": 7.5,
                "min_bedroom_area": 70,
                "required_systems": ["electrical", "plumbing", "hvac", "insulation"],
                "building_code": "IRC or IBC - Residential (R-3)",
                "egress": "Emergency egress required",
                "window_area": "8% of floor area minimum"
            },
            "Workshop/Manufacturing": {
                "min_ceiling_height": 8.0,
                "min_area_per_person": 100,
                "required_systems": ["electrical", "ventilation"],
                "building_code": "IBC - Factory (F-1)",
                "ventilation": "Industrial ventilation required",
                "fire_protection": "Sprinkler system may be required"
            },
            "Storage/Warehouse": {
                "min_ceiling_height": 8.0,
                "required_systems": ["basic_electrical"],
                "building_code": "IBC - Storage (S-1)",
                "fire_protection": "Based on stored materials",
                "loading": "Consider loading dock access"
            },
            "Retail/Commercial": {
                "min_ceiling_height": 8.0,
                "min_area_per_person": 30,
                "required_systems": ["electrical", "hvac", "plumbing"],
                "building_code": "IBC - Mercantile (M)",
                "accessibility": "ADA required",
                "signage": "Consider signage requirements"
            }
        }
        
        return requirements.get(use_case, {})
