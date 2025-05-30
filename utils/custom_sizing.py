"""
Custom Container Sizing Module
Handles custom dimensions and specifications for non-standard containers
"""

import streamlit as st
from typing import Dict, Any, Tuple
import math

class CustomContainerCalculator:
    """Calculator for custom-sized containers"""
    
    def __init__(self):
        # Base pricing per square meter/foot
        self.base_price_per_sqm = 450  # EUR per square meter
        self.custom_fabrication_multiplier = 1.3  # 30% premium for custom work
        
        # Material costs
        self.steel_cost_per_kg = 2.8  # EUR per kg
        self.steel_density = 7850  # kg/m³
        self.wall_thickness = 0.002  # 2mm standard wall thickness
        
        # Engineering requirements
        self.min_length = 3.0  # meters
        self.max_length = 15.0  # meters
        self.min_width = 2.0   # meters
        self.max_width = 4.0   # meters
        self.min_height = 2.0  # meters
        self.max_height = 4.0  # meters
    
    def validate_dimensions(self, length: float, width: float, height: float) -> Dict[str, Any]:
        """Validate custom container dimensions"""
        errors = []
        warnings = []
        
        # Check minimum dimensions
        if length < self.min_length:
            errors.append(f"Length must be at least {self.min_length}m")
        if width < self.min_width:
            errors.append(f"Width must be at least {self.min_width}m")
        if height < self.min_height:
            errors.append(f"Height must be at least {self.min_height}m")
        
        # Check maximum dimensions
        if length > self.max_length:
            errors.append(f"Length cannot exceed {self.max_length}m")
        if width > self.max_width:
            errors.append(f"Width cannot exceed {self.max_width}m")
        if height > self.max_height:
            errors.append(f"Height cannot exceed {self.max_height}m")
        
        # Transportation warnings
        if length > 12.2:
            warnings.append("Length > 12.2m requires special transport permits")
        if width > 2.44:
            warnings.append("Width > 2.44m requires special transport permits")
        if height > 2.9:
            warnings.append("Height > 2.9m requires special transport permits")
        
        # Structural warnings
        aspect_ratio = length / width if width > 0 else 0
        if aspect_ratio > 6:
            warnings.append("High aspect ratio may require additional structural support")
        
        area = length * width
        if area > 35:
            warnings.append("Large floor area may require foundation engineering")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def calculate_custom_specifications(self, length: float, width: float, height: float) -> Dict[str, Any]:
        """Calculate specifications for custom container"""
        # Basic calculations
        floor_area = length * width
        internal_volume = length * width * height
        
        # Wall areas for material calculation
        wall_area = 2 * (length * height + width * height)
        roof_area = length * width
        floor_area_calc = length * width
        total_surface_area = wall_area + roof_area + floor_area_calc
        
        # Weight calculations
        steel_volume = total_surface_area * self.wall_thickness
        estimated_weight = steel_volume * self.steel_density
        
        # Payload calculation (conservative estimate)
        max_payload = min(25000, (floor_area * 1000))  # kg
        
        return {
            "dimensions": {
                "length": length,
                "width": width,
                "height": height,
                "internal_length": length - 0.1,  # Account for wall thickness
                "internal_width": width - 0.1,
                "internal_height": height - 0.1
            },
            "areas_and_volumes": {
                "floor_area": floor_area,
                "internal_volume": internal_volume,
                "wall_area": wall_area,
                "total_surface_area": total_surface_area
            },
            "weight_specifications": {
                "estimated_weight": estimated_weight,
                "max_payload": max_payload,
                "steel_volume": steel_volume
            }
        }
    
    def calculate_custom_pricing(self, length: float, width: float, height: float, 
                               modifications: Dict[str, Any] = None) -> Dict[str, Any]:
        """Calculate pricing for custom container"""
        specs = self.calculate_custom_specifications(length, width, height)
        
        # Base container cost
        floor_area = specs["areas_and_volumes"]["floor_area"]
        base_cost = floor_area * self.base_price_per_sqm
        
        # Custom fabrication premium
        custom_premium = base_cost * (self.custom_fabrication_multiplier - 1)
        
        # Material costs
        steel_cost = specs["weight_specifications"]["steel_volume"] * self.steel_density * self.steel_cost_per_kg
        
        # Engineering and design costs
        engineering_cost = base_cost * 0.15  # 15% of base cost
        
        # Transport cost calculation
        transport_cost = self._calculate_transport_cost(length, width, height)
        
        # Modification costs
        modification_cost = 0
        if modifications:
            modification_cost = self._calculate_modification_costs(modifications, specs)
        
        # Total cost
        total_cost = (base_cost + custom_premium + steel_cost + 
                     engineering_cost + transport_cost + modification_cost)
        
        return {
            "cost_breakdown": {
                "base_container_cost": base_cost,
                "custom_fabrication_premium": custom_premium,
                "material_costs": steel_cost,
                "engineering_design": engineering_cost,
                "transport_costs": transport_cost,
                "modifications": modification_cost,
                "total_cost": total_cost
            },
            "pricing_notes": [
                "Custom containers require 30% premium over standard pricing",
                "Engineering design and structural calculations included",
                "Special transport arrangements may be required",
                "Lead time: 12-16 weeks for custom fabrication"
            ]
        }
    
    def _calculate_transport_cost(self, length: float, width: float, height: float) -> float:
        """Calculate transport costs for custom container"""
        base_transport = 1200  # EUR base transport cost
        
        # Special permit costs
        permit_cost = 0
        if length > 12.2 or width > 2.44 or height > 2.9:
            permit_cost = 800
        
        # Oversized transport multiplier
        oversized_multiplier = 1.0
        if length > 13 or width > 3 or height > 3:
            oversized_multiplier = 1.5
        
        return (base_transport + permit_cost) * oversized_multiplier
    
    def _calculate_modification_costs(self, modifications: Dict[str, Any], 
                                    specs: Dict[str, Any]) -> float:
        """Calculate costs for modifications on custom container"""
        # Base modification costs with custom container premium
        custom_mod_multiplier = 1.2  # 20% premium for modifications on custom containers
        
        total_mod_cost = 0
        
        # Window costs
        if modifications.get("windows", 0) > 0:
            total_mod_cost += modifications["windows"] * 900 * custom_mod_multiplier
        
        # Door costs
        if modifications.get("doors", 0) > 0:
            total_mod_cost += modifications["doors"] * 1200 * custom_mod_multiplier
        
        # System costs
        floor_area = specs["areas_and_volumes"]["floor_area"]
        
        if modifications.get("electrical", False):
            total_mod_cost += (floor_area * 180) * custom_mod_multiplier
        
        if modifications.get("plumbing", False):
            total_mod_cost += (floor_area * 220) * custom_mod_multiplier
        
        if modifications.get("hvac", False):
            total_mod_cost += (floor_area * 280) * custom_mod_multiplier
        
        return total_mod_cost

def render_custom_sizing_interface():
    """Render the custom container sizing interface"""
    st.markdown("## 📐 Custom Container Sizing")
    st.markdown("Design a container with your exact specifications")
    
    calculator = CustomContainerCalculator()
    
    # Dimension inputs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        length = st.number_input(
            "Length (meters)",
            min_value=3.0, max_value=15.0, value=6.0, step=0.1,
            help="Container length in meters"
        )
    
    with col2:
        width = st.number_input(
            "Width (meters)", 
            min_value=2.0, max_value=4.0, value=2.4, step=0.1,
            help="Container width in meters"
        )
    
    with col3:
        height = st.number_input(
            "Height (meters)",
            min_value=2.0, max_value=4.0, value=2.6, step=0.1,
            help="Container height in meters"
        )
    
    # Validate dimensions
    validation = calculator.validate_dimensions(length, width, height)
    
    if not validation["valid"]:
        for error in validation["errors"]:
            st.error(error)
        return
    
    # Show warnings
    for warning in validation["warnings"]:
        st.warning(warning)
    
    # Calculate specifications
    specs = calculator.calculate_custom_specifications(length, width, height)
    
    # Display specifications
    st.markdown("### Container Specifications")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Floor Area", f"{specs['areas_and_volumes']['floor_area']:.1f} m²")
        st.metric("Internal Volume", f"{specs['areas_and_volumes']['internal_volume']:.1f} m³")
    
    with col2:
        st.metric("Estimated Weight", f"{specs['weight_specifications']['estimated_weight']:.0f} kg")
        st.metric("Max Payload", f"{specs['weight_specifications']['max_payload']:.0f} kg")
    
    with col3:
        st.metric("Wall Area", f"{specs['areas_and_volumes']['wall_area']:.1f} m²")
        st.metric("Surface Area", f"{specs['areas_and_volumes']['total_surface_area']:.1f} m²")
    
    # Modifications
    st.markdown("### Modifications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_windows = st.number_input("Number of Windows", min_value=0, max_value=10, value=0)
        num_doors = st.number_input("Additional Doors", min_value=0, max_value=4, value=0)
    
    with col2:
        electrical = st.checkbox("Electrical System")
        plumbing = st.checkbox("Plumbing System")
        hvac = st.checkbox("HVAC System")
    
    # Calculate pricing
    modifications = {
        "windows": num_windows,
        "doors": num_doors,
        "electrical": electrical,
        "plumbing": plumbing,
        "hvac": hvac
    }
    
    pricing = calculator.calculate_custom_pricing(length, width, height, modifications)
    
    # Display pricing
    st.markdown("### Pricing Breakdown")
    
    cost_data = []
    for item, cost in pricing["cost_breakdown"].items():
        if item != "total_cost":
            cost_data.append({
                "Cost Item": item.replace("_", " ").title(),
                "Amount (€)": f"{cost:,.0f}"
            })
    
    st.table(cost_data)
    
    # Total cost
    st.markdown(f"### Total Cost: **€{pricing['cost_breakdown']['total_cost']:,.0f}**")
    
    # Pricing notes
    st.markdown("### Important Notes")
    for note in pricing["pricing_notes"]:
        st.info(note)