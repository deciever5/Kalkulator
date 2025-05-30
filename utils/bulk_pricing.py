"""
Bulk Pricing Module for Multiple Container Projects
Handles volume discounts and multi-container project calculations
"""

import streamlit as st
from typing import Dict, List, Any, Tuple
import pandas as pd

class BulkPricingCalculator:
    """Calculator for bulk container pricing with volume discounts"""
    
    def __init__(self):
        self.volume_discounts = {
            2: 0.05,   # 5% discount for 2+ containers
            5: 0.08,   # 8% discount for 5+ containers
            10: 0.12,  # 12% discount for 10+ containers
            20: 0.15,  # 15% discount for 20+ containers
            50: 0.18,  # 18% discount for 50+ containers
            100: 0.22  # 22% discount for 100+ containers
        }
        
        self.bulk_logistics_savings = {
            2: 0.03,   # 3% logistics savings for 2+ containers
            5: 0.06,   # 6% logistics savings for 5+ containers
            10: 0.10,  # 10% logistics savings for 10+ containers
            20: 0.12,  # 12% logistics savings for 20+ containers
            50: 0.15,  # 15% logistics savings for 50+ containers
            100: 0.18  # 18% logistics savings for 100+ containers
        }
    
    def calculate_volume_discount(self, quantity: int) -> float:
        """Calculate volume discount percentage based on quantity"""
        discount = 0.0
        for min_qty, disc in sorted(self.volume_discounts.items(), reverse=True):
            if quantity >= min_qty:
                discount = disc
                break
        return discount
    
    def calculate_logistics_savings(self, quantity: int) -> float:
        """Calculate logistics savings percentage for bulk orders"""
        savings = 0.0
        for min_qty, save in sorted(self.bulk_logistics_savings.items(), reverse=True):
            if quantity >= min_qty:
                savings = save
                break
        return savings
    
    def calculate_bulk_pricing(self, containers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate bulk pricing for multiple containers"""
        if not containers:
            return {"error": "No containers provided"}
        
        total_quantity = len(containers)
        individual_costs = []
        total_base_cost = 0
        
        # Calculate individual container costs
        for i, container in enumerate(containers):
            from utils.calculations import calculate_container_cost
            cost = calculate_container_cost(container)
            individual_costs.append({
                "container_id": i + 1,
                "type": container.get("container_type", "Unknown"),
                "use_case": container.get("main_purpose", "Unknown"),
                "individual_cost": cost,
                "modifications": self._count_modifications(container)
            })
            total_base_cost += cost
        
        # Apply volume discounts
        volume_discount_rate = self.calculate_volume_discount(total_quantity)
        logistics_savings_rate = self.calculate_logistics_savings(total_quantity)
        
        # Calculate discounts
        volume_discount_amount = total_base_cost * volume_discount_rate
        logistics_savings_amount = total_base_cost * logistics_savings_rate
        total_discount = volume_discount_amount + logistics_savings_amount
        
        # Final pricing
        final_total = total_base_cost - total_discount
        cost_per_container = final_total / total_quantity if total_quantity > 0 else 0
        
        # Calculate project timeline for bulk order
        timeline = self._calculate_bulk_timeline(total_quantity, containers)
        
        return {
            "total_quantity": total_quantity,
            "individual_costs": individual_costs,
            "pricing_summary": {
                "total_base_cost": total_base_cost,
                "volume_discount_rate": volume_discount_rate,
                "volume_discount_amount": volume_discount_amount,
                "logistics_savings_rate": logistics_savings_rate,
                "logistics_savings_amount": logistics_savings_amount,
                "total_discount": total_discount,
                "final_total": final_total,
                "cost_per_container": cost_per_container,
                "savings_percentage": (total_discount / total_base_cost * 100) if total_base_cost > 0 else 0
            },
            "project_timeline": timeline,
            "bulk_benefits": self._get_bulk_benefits(total_quantity)
        }
    
    def _count_modifications(self, container: Dict[str, Any]) -> int:
        """Count the number of modifications for a container"""
        modifications = 0
        
        # Count various modifications
        if container.get("num_windows", 0) > 0:
            modifications += 1
        if container.get("num_doors", 0) > 0:
            modifications += 1
        if container.get("electrical_system", False):
            modifications += 1
        if container.get("plumbing_system", False):
            modifications += 1
        if container.get("hvac_system", False):
            modifications += 1
        if container.get("insulation", False):
            modifications += 1
        if container.get("interior_finishing", False):
            modifications += 1
        if container.get("flooring_upgrade", False):
            modifications += 1
        
        return modifications
    
    def _calculate_bulk_timeline(self, quantity: int, containers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate project timeline for bulk orders"""
        # Base timeline factors
        base_weeks = 8
        additional_weeks_per_10_containers = 2
        complexity_factor = sum(self._count_modifications(c) for c in containers) / len(containers)
        
        # Calculate timeline
        production_weeks = base_weeks + (quantity // 10) * additional_weeks_per_10_containers
        if complexity_factor > 3:
            production_weeks += 2
        
        # Parallel processing benefits for bulk orders
        if quantity >= 10:
            production_weeks *= 0.9  # 10% time reduction for parallel processing
        if quantity >= 20:
            production_weeks *= 0.85  # 15% total reduction for large orders
        
        return {
            "total_weeks": int(production_weeks),
            "phases": {
                "design_and_permits": "2-3 weeks",
                "material_procurement": "1-2 weeks",
                "production": f"{int(production_weeks - 4)} weeks",
                "quality_control": "1 week",
                "delivery": "1-2 weeks"
            },
            "parallel_production": quantity >= 5,
            "batch_delivery": quantity >= 10
        }
    
    def _get_bulk_benefits(self, quantity: int) -> List[str]:
        """Get list of bulk order benefits"""
        benefits = []
        
        if quantity >= 2:
            benefits.append("Volume pricing discounts")
            benefits.append("Reduced per-unit logistics costs")
        
        if quantity >= 5:
            benefits.append("Priority production scheduling")
            benefits.append("Dedicated project manager")
        
        if quantity >= 10:
            benefits.append("Parallel production capabilities")
            benefits.append("Batch delivery coordination")
            benefits.append("Extended warranty coverage")
        
        if quantity >= 20:
            benefits.append("Custom design consultation")
            benefits.append("On-site installation support")
        
        if quantity >= 50:
            benefits.append("Executive account management")
            benefits.append("Flexible payment terms")
            benefits.append("Training and documentation")
        
        return benefits

def render_bulk_pricing_interface():
    """Render the bulk pricing interface"""
    st.markdown("## 📦 Bulk Container Pricing Calculator")
    st.markdown("Configure multiple containers and get volume pricing discounts")
    
    # Initialize session state for bulk containers
    if 'bulk_containers' not in st.session_state:
        st.session_state.bulk_containers = []
    
    # Container configuration section
    with st.expander("Add New Container to Bulk Order", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            container_type = st.selectbox(
                "Container Type",
                ["20ft Standard", "40ft Standard", "40ft High Cube", 
                 "20ft Double Door", "40ft Double Door", "40ft HC Double Door", 
                 "Custom Size"],
                key="bulk_container_type"
            )
            
            main_purpose = st.selectbox(
                "Main Purpose",
                ["Office Space", "Residential", "Storage", "Workshop", 
                 "Retail", "Restaurant", "Medical", "Laboratory"],
                key="bulk_main_purpose"
            )
        
        with col2:
            quantity = st.number_input(
                "Quantity of This Configuration",
                min_value=1, max_value=100, value=1,
                key="bulk_quantity"
            )
            
            if st.button("Add to Bulk Order", type="primary"):
                container_config = {
                    "container_type": container_type,
                    "main_purpose": main_purpose,
                    "num_windows": st.session_state.get("bulk_windows", 0),
                    "num_doors": st.session_state.get("bulk_doors", 0),
                    "electrical_system": st.session_state.get("bulk_electrical", False),
                    "plumbing_system": st.session_state.get("bulk_plumbing", False),
                    "hvac_system": st.session_state.get("bulk_hvac", False),
                    "insulation": st.session_state.get("bulk_insulation", False)
                }
                
                # Add multiple containers based on quantity
                for _ in range(quantity):
                    st.session_state.bulk_containers.append(container_config.copy())
                
                st.success(f"Added {quantity} containers to bulk order")
                st.rerun()
    
    # Display current bulk order
    if st.session_state.bulk_containers:
        st.markdown("### Current Bulk Order")
        
        # Calculate bulk pricing
        calculator = BulkPricingCalculator()
        bulk_result = calculator.calculate_bulk_pricing(st.session_state.bulk_containers)
        
        # Display summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Containers",
                bulk_result["total_quantity"]
            )
        
        with col2:
            st.metric(
                "Total Savings",
                f"€{bulk_result['pricing_summary']['total_discount']:,.0f}",
                f"{bulk_result['pricing_summary']['savings_percentage']:.1f}%"
            )
        
        with col3:
            st.metric(
                "Final Total",
                f"€{bulk_result['pricing_summary']['final_total']:,.0f}"
            )
        
        # Detailed breakdown
        st.markdown("#### Pricing Breakdown")
        
        pricing_data = {
            "Item": [
                "Base Cost (All Containers)",
                f"Volume Discount ({bulk_result['pricing_summary']['volume_discount_rate']*100:.1f}%)",
                f"Logistics Savings ({bulk_result['pricing_summary']['logistics_savings_rate']*100:.1f}%)",
                "Final Total"
            ],
            "Amount (€)": [
                f"{bulk_result['pricing_summary']['total_base_cost']:,.0f}",
                f"-{bulk_result['pricing_summary']['volume_discount_amount']:,.0f}",
                f"-{bulk_result['pricing_summary']['logistics_savings_amount']:,.0f}",
                f"{bulk_result['pricing_summary']['final_total']:,.0f}"
            ]
        }
        
        st.table(pd.DataFrame(pricing_data))
        
        # Bulk benefits
        st.markdown("#### Bulk Order Benefits")
        for benefit in bulk_result["bulk_benefits"]:
            st.markdown(f"✅ {benefit}")
        
        # Clear bulk order
        if st.button("Clear Bulk Order", type="secondary"):
            st.session_state.bulk_containers = []
            st.rerun()
    
    else:
        st.info("Add containers to your bulk order to see pricing calculations")