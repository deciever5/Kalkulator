"""
Simple Storage System for KAN-BUD Container Calculator
Works without external database dependencies using session state
"""

import streamlit as st
import pandas as pd
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

import streamlit as st
from typing import Dict, List, Any, Optional
from datetime import datetime

class SimpleStorageManager:
    """Simple storage manager using Streamlit session state"""
    
    def __init__(self):
        # Initialize storage in session state
        if 'storage_data' not in st.session_state:
            st.session_state.storage_data = {
                'historical_projects': [],
                'user_projects': [],
                'customers': [],
                'quotes': [],
                'material_prices': {},
                'settings': {}
            }
    
    def save_user_project(self, user_id: str, project_name: str, 
                         config: Dict[str, Any], estimate: Dict[str, Any] = None,
                         analysis: Dict[str, Any] = None) -> Optional[int]:
        """Save user project configuration and results"""
        
        project_data = {
            'id': len(st.session_state.storage_data['user_projects']) + 1,
            'user_id': user_id,
            'project_name': project_name,
            'container_config': config,
            'cost_estimate': estimate or {},
            'technical_analysis': analysis or {},
            'status': 'draft',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        st.session_state.storage_data['user_projects'].append(project_data)
        return project_data['id']
    
    def get_user_projects(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all projects for a user"""
        
        user_projects = []
        for project in st.session_state.storage_data['user_projects']:
            if project.get('user_id') == user_id:
                user_projects.append(project)
        
        return sorted(user_projects, key=lambda x: x['created_at'], reverse=True)
    
    def save_customer(self, customer_data: Dict[str, Any]) -> Optional[int]:
        """Save customer information"""
        
        customer = {
            'id': len(st.session_state.storage_data['customers']) + 1,
            'created_at': datetime.now(),
            **customer_data
        }
        
        st.session_state.storage_data['customers'].append(customer)
        return customer['id']
    
    def save_quote(self, quote_data: Dict[str, Any]) -> bool:
        """Save generated quote"""
        
        quote = {
            'id': len(st.session_state.storage_data['quotes']) + 1,
            'created_at': datetime.now(),
            **quote_data
        }
        
        st.session_state.storage_data['quotes'].append(quote)
        return True
    
    def add_historical_project(self, project_data: Dict[str, Any]) -> bool:
        """Add historical project data"""
        
        project = {
            'id': len(st.session_state.storage_data['historical_projects']) + 1,
            'imported_at': datetime.now(),
            **project_data
        }
        
        st.session_state.storage_data['historical_projects'].append(project)
        return True
    
    def get_historical_pricing_data(self, container_type: str, use_case: str, 
                                  months_back: int = 24) -> Dict[str, Any]:
        """Get historical pricing data for more accurate estimates"""
        
        cutoff_date = datetime.now() - timedelta(days=months_back * 30)
        
        # Filter historical data
        relevant_projects = []
        for project in st.session_state.storage_data['historical_projects']:
            project_date = project.get('project_date')
            if isinstance(project_date, str):
                try:
                    project_date = datetime.fromisoformat(project_date)
                except:
                    continue
            elif not isinstance(project_date, datetime):
                continue
            
            if (project_date >= cutoff_date and 
                container_type.lower() in project.get('container_type', '').lower() and
                use_case.lower() in project.get('use_case', '').lower()):
                relevant_projects.append(project)
        
        if not relevant_projects:
            return {}
        
        # Calculate metrics
        costs = [p.get('actual_cost', 0) for p in relevant_projects if p.get('actual_cost')]
        materials = [p.get('materials_cost', 0) for p in relevant_projects if p.get('materials_cost')]
        labor = [p.get('labor_cost', 0) for p in relevant_projects if p.get('labor_cost')]
        durations = [p.get('project_duration_days', 0) for p in relevant_projects if p.get('project_duration_days')]
        
        if costs:
            return {
                'avg_cost': sum(costs) / len(costs),
                'min_cost': min(costs),
                'max_cost': max(costs),
                'avg_materials': sum(materials) / len(materials) if materials else 0,
                'avg_labor': sum(labor) / len(labor) if labor else 0,
                'avg_duration': sum(durations) / len(durations) if durations else 0,
                'project_count': len(relevant_projects),
                'confidence': min(1.0, len(relevant_projects) / 10)
            }
        
        return {}
    
    def get_current_material_prices(self) -> Dict[str, float]:
        """Get current material prices"""
        return st.session_state.storage_data.get('material_prices', {})
    
    def update_material_price(self, material: str, price: float):
        """Update material price"""
        st.session_state.storage_data['material_prices'][material] = price
    
    def get_all_historical_projects(self) -> List[Dict[str, Any]]:
        """Get all historical projects"""
        return st.session_state.storage_data.get('historical_projects', [])
    
    def clear_historical_data(self):
        """Clear all historical data"""
        st.session_state.storage_data['historical_projects'] = []
    
    def import_historical_data(self, data: List[Dict[str, Any]]) -> bool:
        """Import historical data from list"""
        try:
            for project in data:
                self.add_historical_project(project)
            return True
        except Exception as e:
            st.error(f"Error importing data: {str(e)}")
            return False
    
    def get_storage_stats(self) -> Dict[str, int]:
        """Get storage statistics"""
        return {
            'historical_projects': len(st.session_state.storage_data.get('historical_projects', [])),
            'user_projects': len(st.session_state.storage_data.get('user_projects', [])),
            'customers': len(st.session_state.storage_data.get('customers', [])),
            'quotes': len(st.session_state.storage_data.get('quotes', []))
        }