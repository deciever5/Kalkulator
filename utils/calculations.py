"""
Structural Calculations Module
Provides engineering calculations for container modifications and structural analysis
"""

import math
from typing import Dict, List, Any, Tuple
import pandas as pd
from datetime import datetime

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
        
        # Systems
        if modifications.get('electrical'):
            modification_costs += 3500  # Basic electrical package
        
        if modifications.get('plumbing'):
            modification_costs += 4000  # Basic plumbing package
        
        if modifications.get('hvac'):
            modification_costs += 2500  # Mini-split system
        
        if modifications.get('insulation'):
            # Calculate based on container size
            container_areas = self._get_container_areas(base_type)
            insulation_area = container_areas['wall_area'] + container_areas['ceiling_area']
            modification_costs += insulation_area * 1.50  # $1.50 per sq ft
        
        # Reinforcements
        if modifications.get('reinforcement_walls'):
            modification_costs += 2000
        
        if modifications.get('reinforcement_roof'):
            modification_costs += 1500
        
        if modifications.get('reinforcement_floor'):
            modification_costs += 1800
        
        if modifications.get('additional_support'):
            modification_costs += 2500
        
        # Labor costs (approximately 40% of material costs)
        labor_costs = (base_cost + modification_costs) * 0.4
        
        return {
            "base_container": base_cost,
            "modifications": modification_costs,
            "labor": labor_costs,
            "subtotal": base_cost + modification_costs + labor_costs,
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
        """Calculate design loads"""
        
        use_case = config.get('use_case', 'Office Space')
        occupancy = config.get('occupancy', 4)
        
        # Live loads based on use case
        live_load_mapping = {
            "Office Space": 50,  # psf
            "Residential Living": 40,
            "Workshop/Manufacturing": 125,
            "Storage/Warehouse": 125,
            "Retail/Commercial": 75
        }
        
        live_load = live_load_mapping.get(use_case, 50)
        
        # Dead loads (structure + finishes)
        dead_load = 15  # psf (basic structure)
        
        modifications = config.get('modifications', {})
        if modifications.get('insulation'):
            dead_load += 2  # Additional dead load for insulation
        
        if modifications.get('hvac'):
            dead_load += 5  # Additional dead load for HVAC
        
        # Environmental loads
        wind_load = analysis_params.get('wind_load', 90)  # mph
        snow_load = analysis_params.get('snow_load', 20)  # psf
        
        # Convert wind speed to pressure (simplified)
        wind_pressure = 0.00256 * (wind_load ** 2)  # psf
        
        return {
            "dead_load": dead_load,
            "live_load": live_load,
            "wind_load": wind_pressure,
            "snow_load": snow_load,
            "total_vertical": dead_load + live_load + snow_load,
            "wind_pressure": wind_pressure
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
        """Check building code compliance"""
        
        building_code = analysis_params.get('building_code', 'IBC (International Building Code)')
        use_case = config.get('use_case', 'Office Space')
        
        compliance_results = {
            "building_codes": {},
            "safety": {},
            "structural": {}
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
    
    def _get_required_drawings(self, config: Dict[str, Any], 
                             structural_results: Dict[str, Any]) -> List[str]:
        """Determine required engineering drawings"""
        
        drawings = ["Site Plan", "Foundation Plan", "Floor Plan"]
        
        modifications = config.get('modifications', {})
        
        if modifications.get('reinforcement_walls') or modifications.get('reinforcement_roof'):
            drawings.append("Structural Reinforcement Details")
        
        if modifications.get('electrical'):
            drawings.append("Electrical Plan")
        
        if modifications.get('plumbing'):
            drawings.append("Plumbing Plan")
        
        if modifications.get('hvac'):
            drawings.append("HVAC Plan")
        
        if structural_results.get("stress_ratio", 0) > 0.8:
            drawings.append("Structural Analysis Report")
        
        drawings.extend(["Sections and Details", "Construction Specifications"])
        
        return drawings
    
    def _get_professional_requirements(self, config: Dict[str, Any], 
                                     structural_results: Dict[str, Any]) -> List[str]:
        """Determine professional requirements"""
        
        requirements = []
        
        use_case = config.get('use_case', 'Office Space')
        
        # Structural engineer required for certain conditions
        if structural_results.get("stress_ratio", 0) > 0.7:
            requirements.append("Licensed Structural Engineer - Structural Analysis")
        
        if config.get('modifications', {}).get('reinforcement_walls') or config.get('modifications', {}).get('reinforcement_roof'):
            requirements.append("Licensed Structural Engineer - Reinforcement Design")
        
        # Other professionals
        if config.get('modifications', {}).get('electrical'):
            requirements.append("Licensed Electrician - Electrical Installation")
        
        if config.get('modifications', {}).get('plumbing'):
            requirements.append("Licensed Plumber - Plumbing Installation")
        
        if config.get('modifications', {}).get('hvac'):
            requirements.append("HVAC Contractor - System Installation")
        
        # Permits and inspections
        if use_case in ["Office Space", "Retail/Commercial", "Residential Living"]:
            requirements.append("Building Permit Required")
            requirements.append("Municipal Inspections Required")
        
        if structural_results.get("foundation_type") != "Concrete Pads":
            requirements.append("Foundation Engineering Review")
        
        return requirements
    
    def calculate_project_timeline(self, config: Dict[str, Any], 
                                 structural_results: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Calculate project timeline based on scope"""
        
        modifications = config.get('modifications', {})
        base_type = config.get('base_type', '40ft Standard')
        
        timeline = {}
        
        # Phase 1: Design and Permits
        design_weeks = 2
        if structural_results.get("stress_ratio", 0) > 0.7:
            design_weeks += 2  # Additional time for structural engineering
        
        timeline["Design_and_Permits"] = {
            "duration": f"{design_weeks} weeks",
            "description": "Design development, engineering, permit applications"
        }
        
        # Phase 2: Site Preparation
        site_prep_weeks = 1
        foundation_type = structural_results.get("foundation_type", "Concrete Pads")
        if foundation_type != "Concrete Pads":
            site_prep_weeks += 1
        
        timeline["Site_Preparation"] = {
            "duration": f"{site_prep_weeks} weeks",
            "description": f"Site preparation, {foundation_type.lower()} installation"
        }
        
        # Phase 3: Container Modifications
        mod_weeks = 2
        if modifications.get('windows', 0) > 2:
            mod_weeks += 1
        if modifications.get('reinforcement_walls') or modifications.get('reinforcement_roof'):
            mod_weeks += 2
        
        timeline["Container_Modifications"] = {
            "duration": f"{mod_weeks} weeks",
            "description": "Structural modifications, openings, reinforcements"
        }
        
        # Phase 4: Systems Installation
        systems_weeks = 2
        if modifications.get('electrical'):
            systems_weeks += 1
        if modifications.get('plumbing'):
            systems_weeks += 1
        if modifications.get('hvac'):
            systems_weeks += 1
        
        timeline["Systems_Installation"] = {
            "duration": f"{systems_weeks} weeks",
            "description": "Electrical, plumbing, HVAC installation"
        }
        
        # Phase 5: Finishes
        finish_weeks = 1
        if modifications.get('insulation'):
            finish_weeks += 1
        
        finish_level = modifications.get('finish_level', 'Basic')
        if finish_level in ['Premium', 'Luxury']:
            finish_weeks += 2
        
        timeline["Interior_Finishes"] = {
            "duration": f"{finish_weeks} weeks",
            "description": "Insulation, flooring, interior finishes"
        }
        
        # Phase 6: Final Inspections
        timeline["Final_Inspections"] = {
            "duration": "1 week",
            "description": "Final inspections, testing, commissioning"
        }
        
        return timeline
