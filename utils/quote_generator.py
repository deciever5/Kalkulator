"""
Quote Generator Module
Generates professional quotes and proposals for container projects
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd

class QuoteGenerator:
    """Professional quote and proposal generator"""
    
    def __init__(self):
        self.company_info = {
            "name": "Steel Container Solutions",
            "address": "123 Industrial Drive, Construction City, ST 12345",
            "phone": "(555) 123-4567",
            "email": "quotes@steelcontainersolutions.com",
            "website": "www.steelcontainersolutions.com",
            "license": "Contractor License #123456"
        }
        
        # Base rates and factors
        self.base_rates = {
            "labor_rate": 85,  # per hour
            "overhead_factor": 0.15,  # 15%
            "profit_factor": 0.20,  # 20%
            "tax_rate": 0.0875,  # 8.75%
        }
        
        # Standard warranty and terms
        self.standard_terms = [
            "Payment terms: 50% deposit upon contract signing, 50% upon completion",
            "Prices valid for 30 days from quote date",
            "Work to be completed in accordance with local building codes",
            "Customer responsible for obtaining necessary permits unless specified",
            "Final pricing subject to site inspection and permit requirements",
            "Changes to scope of work may affect pricing and timeline",
            "Warranty: 1 year on workmanship, manufacturer warranty on materials"
        ]
    
    def generate_quote(self, quote_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive professional quote"""
        
        # Generate quote number
        quote_number = self._generate_quote_number()
        
        # Calculate detailed costs
        cost_breakdown = self._calculate_detailed_costs(quote_data)
        
        # Generate timeline
        timeline = self._generate_project_timeline(quote_data)
        
        # Prepare quote structure
        quote = {
            "quote_number": quote_number,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "valid_until": self._calculate_validity_date(quote_data),
            "customer": quote_data.get("customer", {}),
            "project": quote_data.get("project", {}),
            "container_config": quote_data.get("container_config", {}),
            "cost_breakdown": cost_breakdown,
            "subtotal": cost_breakdown.get("subtotal", 0),
            "tax": cost_breakdown.get("tax", 0),
            "total_cost": cost_breakdown.get("total", 0),
            "timeline": timeline,
            "terms_conditions": self._generate_terms_conditions(quote_data),
            "warranty": self._generate_warranty_terms(quote_data),
            "payment_schedule": self._generate_payment_schedule(quote_data),
            "exclusions": self._generate_exclusions(quote_data),
            "assumptions": self._generate_assumptions(quote_data)
        }
        
        return quote
    
    def _generate_quote_number(self) -> str:
        """Generate unique quote number"""
        date_part = datetime.now().strftime("%Y%m")
        time_part = datetime.now().strftime("%H%M")
        return f"SCS-{date_part}-{time_part}"
    
    def _calculate_validity_date(self, quote_data: Dict[str, Any]) -> str:
        """Calculate quote validity expiration date"""
        quote_params = quote_data.get("quote_params", {})
        validity_period = quote_params.get("validity_period", "30 days")
        
        if "30" in validity_period:
            days = 30
        elif "60" in validity_period:
            days = 60
        elif "90" in validity_period:
            days = 90
        else:
            days = 30  # Default
        
        valid_until = datetime.now() + timedelta(days=days)
        return valid_until.strftime("%Y-%m-%d")
    
    def _calculate_detailed_costs(self, quote_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed cost breakdown"""
        
        config = quote_data.get("container_config", {})
        services = quote_data.get("services", {})
        quote_params = quote_data.get("quote_params", {})
        
        # Base costs
        base_costs = self._get_base_costs(config)
        
        # Service costs
        service_costs = self._calculate_service_costs(services, config)
        
        # Apply adjustments
        profit_margin = quote_params.get("profit_margin", 0.20)
        contingency = quote_params.get("contingency", 0.10)
        discount = quote_params.get("discount", 0.0)
        
        # Calculate breakdown
        breakdown = {}
        
        # Container and base modifications
        breakdown["container_base"] = {
            "description": f"{config.get('base_type', 'Container')} with basic modifications",
            "quantity": 1,
            "unit_cost": base_costs["container_base"],
            "total": base_costs["container_base"]
        }
        
        # Structural modifications
        if base_costs.get("structural_modifications", 0) > 0:
            breakdown["structural_modifications"] = {
                "description": "Structural reinforcements and modifications",
                "quantity": 1,
                "unit_cost": base_costs["structural_modifications"],
                "total": base_costs["structural_modifications"]
            }
        
        # Systems installation
        systems_cost = (base_costs.get("electrical", 0) + 
                       base_costs.get("plumbing", 0) + 
                       base_costs.get("hvac", 0))
        
        if systems_cost > 0:
            breakdown["systems_installation"] = {
                "description": "Electrical, plumbing, and HVAC systems",
                "quantity": 1,
                "unit_cost": systems_cost,
                "total": systems_cost
            }
        
        # Insulation and finishes
        finish_cost = base_costs.get("insulation", 0) + base_costs.get("finishes", 0)
        if finish_cost > 0:
            breakdown["finishes_interior"] = {
                "description": "Insulation and interior finishes",
                "quantity": 1,
                "unit_cost": finish_cost,
                "total": finish_cost
            }
        
        # Labor costs
        total_material_cost = sum(item["total"] for item in breakdown.values())
        labor_cost = total_material_cost * 0.40  # 40% of materials
        
        breakdown["labor_costs"] = {
            "description": "Professional installation and labor",
            "quantity": 1,
            "unit_cost": labor_cost,
            "total": labor_cost
        }
        
        # Service costs
        if service_costs.get("delivery", 0) > 0:
            breakdown["delivery_logistics"] = {
                "description": f"Delivery within {services.get('delivery_distance', 50)} miles",
                "quantity": 1,
                "unit_cost": service_costs["delivery"],
                "total": service_costs["delivery"]
            }
        
        if service_costs.get("permits", 0) > 0:
            breakdown["permits_fees"] = {
                "description": "Permit assistance and fees",
                "quantity": 1,
                "unit_cost": service_costs["permits"],
                "total": service_costs["permits"]
            }
        
        if service_costs.get("site_prep", 0) > 0:
            breakdown["site_preparation"] = {
                "description": "Site preparation and foundation work",
                "quantity": 1,
                "unit_cost": service_costs["site_prep"],
                "total": service_costs["site_prep"]
            }
        
        # Calculate subtotal
        subtotal = sum(item["total"] for item in breakdown.values())
        
        # Apply profit margin
        subtotal_with_profit = subtotal * (1 + profit_margin)
        
        # Apply contingency
        contingency_amount = subtotal_with_profit * contingency
        breakdown["contingency"] = {
            "description": f"Contingency ({contingency*100:.0f}%)",
            "quantity": 1,
            "unit_cost": contingency_amount,
            "total": contingency_amount
        }
        
        # Calculate new subtotal
        subtotal_final = subtotal_with_profit + contingency_amount
        
        # Apply discount
        discount_amount = subtotal_final * discount
        if discount_amount > 0:
            breakdown["discount"] = {
                "description": f"Discount ({discount*100:.0f}%)",
                "quantity": 1,
                "unit_cost": -discount_amount,
                "total": -discount_amount
            }
            subtotal_final -= discount_amount
        
        # Calculate tax
        tax_amount = subtotal_final * self.base_rates["tax_rate"]
        
        return {
            "breakdown": breakdown,
            "subtotal": subtotal_final,
            "tax": tax_amount,
            "total": subtotal_final + tax_amount
        }
    
    def _get_base_costs(self, config: Dict[str, Any]) -> Dict[str, float]:
        """Calculate base costs for container and modifications"""
        
        base_type = config.get('base_type', '40ft Standard')
        modifications = config.get('modifications', {})
        
        # Container base costs - Polish market
        container_costs = {
            "20ft Standard": 3000,
            "40ft Standard": 4200,
            "40ft High Cube": 4500,
            "45ft High Cube": 5000,
            "48ft Standard": 5500,
            "53ft Standard": 6000
        }
        
        costs = {
            "container_base": container_costs.get(base_type, 5000)
        }
        
        # Structural modifications
        structural_cost = 0
        if modifications.get('reinforcement_walls'):
            structural_cost += 2000
        if modifications.get('reinforcement_roof'):
            structural_cost += 1500
        if modifications.get('reinforcement_floor'):
            structural_cost += 1800
        if modifications.get('additional_support'):
            structural_cost += 2500
        
        # Openings
        structural_cost += modifications.get('windows', 0) * 800
        structural_cost += max(0, modifications.get('doors', 1) - 1) * 1200
        structural_cost += modifications.get('skylights', 0) * 1500
        structural_cost += modifications.get('vents', 0) * 200
        
        if structural_cost > 0:
            costs["structural_modifications"] = structural_cost
        
        # Systems
        if modifications.get('electrical'):
            costs["electrical"] = 3500
        
        if modifications.get('plumbing'):
            costs["plumbing"] = 4000
        
        if modifications.get('hvac'):
            costs["hvac"] = 2500
        
        # Insulation
        if modifications.get('insulation'):
            # Estimate based on container size
            area_factors = {
                "20ft Standard": 600,
                "40ft Standard": 1000,
                "40ft High Cube": 1100,
                "45ft High Cube": 1200,
                "48ft Standard": 1200,
                "53ft Standard": 1300
            }
            insulation_area = area_factors.get(base_type, 1000)
            costs["insulation"] = insulation_area * 1.50
        
        # Finishes
        finish_level = modifications.get('finish_level', 'Basic')
        finish_multipliers = {
            'Basic': 1500,
            'Standard': 3000,
            'Premium': 6000,
            'Luxury': 12000
        }
        costs["finishes"] = finish_multipliers.get(finish_level, 1500)
        
        return costs
    
    def _calculate_service_costs(self, services: Dict[str, Any], 
                               config: Dict[str, Any]) -> Dict[str, float]:
        """Calculate costs for additional services"""
        
        costs = {}
        
        # Delivery
        if services.get("delivery", False):
            distance = services.get("delivery_distance", 50)
            base_delivery = 800
            if distance > 50:
                costs["delivery"] = base_delivery + (distance - 50) * 8  # $8 per mile over 50
            else:
                costs["delivery"] = base_delivery
        
        # Installation
        if services.get("installation", False):
            costs["installation"] = 2500  # Professional installation service
        
        # Permits
        if services.get("permits", False):
            costs["permits"] = 1200  # Permit assistance and fees
        
        # Site preparation
        if services.get("site_prep", False):
            costs["site_prep"] = 3500  # Basic site preparation
        
        # Utilities
        if services.get("utilities", False):
            costs["utilities"] = 2800  # Utility connections
        
        # Maintenance package
        if services.get("maintenance", False):
            costs["maintenance"] = 1500  # Annual maintenance package
        
        return costs
    
    def _generate_project_timeline(self, quote_data: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
        """Generate detailed project timeline"""
        
        config = quote_data.get("container_config", {})
        services = quote_data.get("services", {})
        modifications = config.get("modifications", {})
        
        timeline = {}
        
        # Phase 1: Design and Engineering
        design_weeks = 2
        if any([modifications.get('reinforcement_walls'), 
                modifications.get('reinforcement_roof'),
                modifications.get('additional_support')]):
            design_weeks = 3
        
        timeline["design_engineering"] = {
            "duration": f"{design_weeks} weeks",
            "description": "Design development, engineering calculations, permit applications"
        }
        
        # Phase 2: Procurement
        timeline["procurement"] = {
            "duration": "1-2 weeks",
            "description": "Material procurement and container preparation"
        }
        
        # Phase 3: Site Preparation
        if services.get("site_prep", False):
            timeline["site_preparation"] = {
                "duration": "1 week",
                "description": "Site preparation and foundation installation"
            }
        
        # Phase 4: Fabrication
        fab_weeks = 2
        if modifications.get('windows', 0) > 2 or modifications.get('doors', 1) > 2:
            fab_weeks = 3
        
        timeline["fabrication"] = {
            "duration": f"{fab_weeks} weeks",
            "description": "Container modifications, structural work, openings"
        }
        
        # Phase 5: Delivery and Installation
        delivery_weeks = 1
        if services.get("installation", False):
            delivery_weeks = 2
        
        timeline["delivery_installation"] = {
            "duration": f"{delivery_weeks} weeks",
            "description": "Delivery, positioning, and basic installation"
        }
        
        # Phase 6: Systems Installation
        systems_weeks = 2
        system_count = sum([1 for sys in ['electrical', 'plumbing', 'hvac'] 
                           if modifications.get(sys, False)])
        if system_count > 1:
            systems_weeks = 3
        
        timeline["systems"] = {
            "duration": f"{systems_weeks} weeks",
            "description": "Electrical, plumbing, and HVAC installation"
        }
        
        # Phase 7: Finishes
        finish_weeks = 1
        finish_level = modifications.get('finish_level', 'Basic')
        if finish_level in ['Premium', 'Luxury']:
            finish_weeks = 3
        elif finish_level == 'Standard':
            finish_weeks = 2
        
        timeline["finishes"] = {
            "duration": f"{finish_weeks} weeks",
            "description": "Interior finishes, flooring, final details"
        }
        
        # Phase 8: Testing and Commissioning
        timeline["commissioning"] = {
            "duration": "1 week",
            "description": "System testing, inspections, final walkthrough"
        }
        
        return timeline
    
    def _generate_terms_conditions(self, quote_data: Dict[str, Any]) -> List[str]:
        """Generate terms and conditions"""
        
        quote_params = quote_data.get("quote_params", {})
        services = quote_data.get("services", {})
        
        terms = self.standard_terms.copy()
        
        # Customize payment terms
        payment_terms = quote_params.get("payment_terms", "50% deposit, 50% completion")
        terms[0] = f"Payment terms: {payment_terms}"
        
        # Customize validity period
        validity = quote_params.get("validity_period", "30 days")
        terms[1] = f"Prices valid for {validity} from quote date"
        
        # Add service-specific terms
        if services.get("delivery", False):
            terms.append("Delivery included within specified radius; additional charges apply beyond")
        
        if services.get("permits", False):
            terms.append("Permit assistance included; customer responsible for permit fees and approvals")
        
        if services.get("warranty", False):
            warranty_period = services.get("warranty_period", "1 year")
            terms.append(f"Extended warranty: {warranty_period} on all work and materials")
        
        # Add special terms
        special_terms = quote_data.get("special_terms", "")
        if special_terms:
            terms.append(f"Special conditions: {special_terms}")
        
        return terms
    
    def _generate_warranty_terms(self, quote_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate warranty information"""
        
        services = quote_data.get("services", {})
        
        warranty = {
            "workmanship": "1 year warranty on all installation and fabrication work",
            "materials": "Manufacturer warranty on all materials and components",
            "structural": "5 year warranty on structural modifications and reinforcements"
        }
        
        if services.get("warranty", False):
            warranty_period = services.get("warranty_period", "2 years")
            warranty["extended"] = f"Extended {warranty_period} comprehensive warranty on all work"
        
        return warranty
    
    def _generate_payment_schedule(self, quote_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed payment schedule"""
        
        quote_params = quote_data.get("quote_params", {})
        payment_terms = quote_params.get("payment_terms", "50% deposit, 50% completion")
        total_cost = quote_data.get("cost_breakdown", {}).get("total", 0)
        
        schedule = {}
        
        if "50%" in payment_terms and "deposit" in payment_terms:
            schedule["deposit"] = {
                "percentage": 50,
                "amount": total_cost * 0.5,
                "due": "Upon contract signing",
                "description": "Project initiation and material procurement"
            }
            schedule["final"] = {
                "percentage": 50,
                "amount": total_cost * 0.5,
                "due": "Upon project completion",
                "description": "Final payment after inspection and approval"
            }
        
        elif "30%" in payment_terms:
            schedule["deposit"] = {
                "percentage": 30,
                "amount": total_cost * 0.3,
                "due": "Upon contract signing",
                "description": "Project initiation"
            }
            schedule["progress"] = {
                "percentage": 40,
                "amount": total_cost * 0.4,
                "due": "At 50% completion",
                "description": "Progress payment"
            }
            schedule["final"] = {
                "percentage": 30,
                "amount": total_cost * 0.3,
                "due": "Upon completion",
                "description": "Final payment"
            }
        
        elif "Net 30" in payment_terms:
            schedule["full_payment"] = {
                "percentage": 100,
                "amount": total_cost,
                "due": "Net 30 days from completion",
                "description": "Full payment due within 30 days"
            }
        
        return schedule
    
    def _generate_exclusions(self, quote_data: Dict[str, Any]) -> List[str]:
        """Generate list of exclusions"""
        
        services = quote_data.get("services", {})
        
        exclusions = []
        
        if not services.get("permits", False):
            exclusions.append("Building permits and associated fees")
        
        if not services.get("site_prep", False):
            exclusions.append("Site preparation and excavation work")
        
        if not services.get("utilities", False):
            exclusions.append("Utility connections and hook-ups")
        
        if not services.get("delivery", False):
            exclusions.append("Transportation and delivery")
        
        # Standard exclusions
        exclusions.extend([
            "Soil testing and geotechnical analysis",
            "Environmental assessments or remediation",
            "Landscaping and site restoration",
            "Temporary utilities during construction",
            "Security and temporary fencing",
            "Changes in scope or design modifications",
            "Unforeseen site conditions or subsurface issues"
        ])
        
        return exclusions
    
    def _generate_assumptions(self, quote_data: Dict[str, Any]) -> List[str]:
        """Generate project assumptions"""
        
        config = quote_data.get("container_config", {})
        project = quote_data.get("project", {})
        
        assumptions = [
            "Site is accessible for delivery vehicles and equipment",
            "Site has adequate space for construction activities",
            "Standard soil conditions suitable for proposed foundation",
            "No environmental hazards or contamination present",
            "Customer will provide necessary site access and utilities",
            "Work to be performed during standard business hours",
            "Weather conditions will not significantly delay construction"
        ]
        
        # Use case specific assumptions
        use_case = config.get("use_case", "")
        if "Residential" in use_case:
            assumptions.append("Structure meets local residential building codes")
        elif "Office" in use_case:
            assumptions.append("Structure meets commercial building code requirements")
        
        # Location specific
        location = project.get("location", "")
        if location:
            assumptions.append(f"Local building codes and regulations for {location} apply")
        
        return assumptions
    
    def export_quote_pdf(self, quote: Dict[str, Any]) -> str:
        """Export quote to PDF format (placeholder for future implementation)"""
        # This would integrate with a PDF generation library
        # For now, return a success message
        return f"Quote {quote.get('quote_number', 'N/A')} ready for PDF export"
    
    def save_quote_template(self, quote_data: Dict[str, Any], template_name: str) -> bool:
        """Save quote configuration as template"""
        # This would save to a database or file system
        # For now, return success
        return True
    
    def load_quote_template(self, template_name: str) -> Dict[str, Any]:
        """Load quote template"""
        # This would load from saved templates
        # For now, return empty template
        return {}
