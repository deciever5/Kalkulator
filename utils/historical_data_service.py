"""
Historical Data Service for KAN-BUD Container Calculator
Integrates 2-year historical calculation results for improved pricing accuracy
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import streamlit as st
from utils.database import DatabaseManager

class HistoricalDataService:
    """Service for handling historical project data and improving cost accuracy"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.historical_data = None
        self.load_historical_data()
    
    def load_historical_data(self):
        """Load historical data from database or initialize if empty"""
        try:
            if self.db and self.db.engine:
                # Try to load existing historical data
                query = "SELECT COUNT(*) FROM historical_projects"
                with self.db.engine.connect() as conn:
                    result = conn.execute(query).fetchone()
                    if result[0] == 0:
                        # If no data exists, create sample structure for data import
                        self.initialize_sample_structure()
        except Exception as e:
            st.warning(f"Historical data initialization: {str(e)}")
            self.initialize_sample_structure()
    
    def initialize_sample_structure(self):
        """Initialize sample data structure for KAN-BUD historical data import"""
        # This creates a template for importing your 2-year historical data
        sample_data = {
            'project_date': [],
            'container_type': [],
            'use_case': [],
            'location': [],
            'actual_cost': [],
            'estimated_cost': [],
            'materials_cost': [],
            'labor_cost': [],
            'delivery_cost': [],
            'modifications': [],
            'project_duration_days': [],
            'customer_satisfaction': []
        }
        self.historical_data = pd.DataFrame(sample_data)
    
    def import_historical_projects(self, file_path: str = None, data: List[Dict] = None) -> bool:
        """
        Import your 2-year historical calculation results
        Accepts either file path (CSV/Excel) or direct data list
        """
        try:
            if file_path:
                # Load from file (CSV or Excel)
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_path.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file_path)
                else:
                    st.error("Unsupported file format. Please use CSV or Excel.")
                    return False
            elif data:
                df = pd.DataFrame(data)
            else:
                st.error("No data provided for import.")
                return False
            
            # Validate required columns
            required_columns = ['project_date', 'container_type', 'use_case', 'actual_cost']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"Missing required columns: {missing_columns}")
                return False
            
            # Data cleaning and validation
            df = self.clean_historical_data(df)
            
            # Save to database
            if self.db and self.db.engine:
                data_records = df.to_dict('records')
                success = self.db.insert_historical_data(data_records)
                if success:
                    st.success(f"Successfully imported {len(data_records)} historical projects!")
                    self.historical_data = df
                    return True
            
            return False
            
        except Exception as e:
            st.error(f"Error importing historical data: {str(e)}")
            return False
    
    def clean_historical_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate historical data"""
        
        # Convert date column
        df['project_date'] = pd.to_datetime(df['project_date'], errors='coerce')
        
        # Remove rows with invalid dates
        df = df.dropna(subset=['project_date'])
        
        # Ensure numeric columns are properly formatted
        numeric_columns = ['actual_cost', 'estimated_cost', 'materials_cost', 
                          'labor_cost', 'delivery_cost', 'project_duration_days']
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Fill missing values with reasonable defaults
        df['estimated_cost'] = df['estimated_cost'].fillna(df['actual_cost'])
        df['customer_satisfaction'] = df['customer_satisfaction'].fillna(4)  # Default good rating
        
        # Standardize container types
        df['container_type'] = df['container_type'].str.strip()
        
        return df
    
    def get_historical_accuracy_metrics(self, container_type: str = None, 
                                      use_case: str = None) -> Dict[str, Any]:
        """Calculate accuracy metrics from historical data"""
        
        if not self.has_historical_data():
            return {}
        
        historical_data = self.get_filtered_historical_data(container_type, use_case)
        
        if historical_data.empty:
            return {}
        
        # Calculate accuracy metrics
        estimated = historical_data['estimated_cost'].dropna()
        actual = historical_data['actual_cost'].dropna()
        
        if len(estimated) == 0 or len(actual) == 0:
            return {}
        
        # Align the data (same length)
        min_length = min(len(estimated), len(actual))
        estimated = estimated.head(min_length)
        actual = actual.head(min_length)
        
        # Calculate metrics
        percentage_errors = ((estimated - actual) / actual * 100).abs()
        
        metrics = {
            'mean_absolute_error': float(np.mean(np.abs(estimated - actual))),
            'mean_percentage_error': float(np.mean(percentage_errors)),
            'accuracy_within_10_percent': float(np.mean(percentage_errors <= 10) * 100),
            'accuracy_within_20_percent': float(np.mean(percentage_errors <= 20) * 100),
            'overestimate_tendency': float(np.mean(estimated > actual) * 100),
            'underestimate_tendency': float(np.mean(estimated < actual) * 100),
            'sample_size': int(len(estimated)),
            'confidence_score': min(1.0, max(0.3, len(estimated) / 50))  # More data = higher confidence
        }
        
        return metrics
    
    def get_cost_adjustment_factor(self, container_type: str, use_case: str, 
                                 base_estimate: float) -> Dict[str, Any]:
        """Get adjustment factor based on historical accuracy"""
        
        historical_data = self.get_filtered_historical_data(container_type, use_case)
        
        if historical_data.empty or len(historical_data) < 3:
            return {
                'adjustment_factor': 1.0,
                'confidence': 0.3,
                'reason': 'Insufficient historical data',
                'recommended_range': {'min': base_estimate * 0.8, 'max': base_estimate * 1.2}
            }
        
        # Calculate historical ratio of actual to estimated costs
        estimated = historical_data['estimated_cost'].dropna()
        actual = historical_data['actual_cost'].dropna()
        
        if len(estimated) == 0 or len(actual) == 0:
            return {
                'adjustment_factor': 1.0,
                'confidence': 0.3,
                'reason': 'Missing cost data',
                'recommended_range': {'min': base_estimate * 0.8, 'max': base_estimate * 1.2}
            }
        
        # Calculate ratios
        ratios = actual / estimated
        mean_ratio = float(np.mean(ratios))
        std_ratio = float(np.std(ratios))
        
        # Calculate confidence based on data consistency
        confidence = max(0.3, min(1.0, 1.0 - (std_ratio / mean_ratio) if mean_ratio > 0 else 0.3))
        
        # Recommended range
        margin = std_ratio * 1.96  # 95% confidence interval
        min_estimate = base_estimate * max(0.5, mean_ratio - margin)
        max_estimate = base_estimate * min(2.0, mean_ratio + margin)
        
        return {
            'adjustment_factor': mean_ratio,
            'confidence': confidence,
            'reason': f'Based on {len(ratios)} similar historical projects',
            'recommended_range': {'min': min_estimate, 'max': max_estimate},
            'historical_variance': std_ratio,
            'data_points': int(len(ratios))
        }
    
    def get_seasonal_adjustments(self, project_month: int) -> Dict[str, float]:
        """Get seasonal cost adjustments based on historical data"""
        
        if not self.has_historical_data():
            return {}
        
        try:
            # Extract month from historical data
            historical_data = self.historical_data.copy()
            historical_data['month'] = historical_data['project_date'].dt.month
            
            # Calculate average costs by month
            monthly_costs = historical_data.groupby('month')['actual_cost'].mean()
            
            if len(monthly_costs) < 6:  # Need at least 6 months of data
                return {}
            
            # Calculate seasonal factors (relative to annual average)
            annual_average = monthly_costs.mean()
            seasonal_factors = (monthly_costs / annual_average).to_dict()
            
            return {
                'factor': seasonal_factors.get(project_month, 1.0),
                'monthly_factors': seasonal_factors,
                'confidence': min(1.0, len(monthly_costs) / 12),
                'data_source': 'KAN-BUD historical projects'
            }
            
        except Exception as e:
            st.warning(f"Error calculating seasonal adjustments: {str(e)}")
            return {}
    
    def get_regional_cost_factors(self, project_location: str) -> Dict[str, float]:
        """Get regional cost adjustment factors"""
        
        if not self.has_historical_data():
            return {}
        
        try:
            historical_data = self.historical_data.copy()
            
            # Group by location and calculate average costs
            location_costs = historical_data.groupby('location')['actual_cost'].agg(['mean', 'count'])
            
            if len(location_costs) < 2:  # Need at least 2 locations for comparison
                return {}
            
            # Calculate regional factors
            base_cost = location_costs['mean'].mean()
            location_factors = (location_costs['mean'] / base_cost).to_dict()
            
            # Find closest match for project location
            project_factor = 1.0
            for location, factor in location_factors.items():
                if project_location.lower() in location.lower() or location.lower() in project_location.lower():
                    project_factor = factor
                    break
            
            return {
                'factor': project_factor,
                'all_factors': location_factors,
                'confidence': min(1.0, len(location_costs) / 5),
                'matched_location': project_location
            }
            
        except Exception as e:
            st.warning(f"Error calculating regional factors: {str(e)}")
            return {}
    
    def get_filtered_historical_data(self, container_type: str = None, 
                                   use_case: str = None) -> pd.DataFrame:
        """Get filtered historical data based on criteria"""
        
        if not self.has_historical_data():
            return pd.DataFrame()
        
        data = self.historical_data.copy()
        
        if container_type:
            data = data[data['container_type'].str.contains(container_type, case=False, na=False)]
        
        if use_case:
            data = data[data['use_case'].str.contains(use_case, case=False, na=False)]
        
        return data
    
    def has_historical_data(self) -> bool:
        """Check if historical data is available"""
        return (self.historical_data is not None and 
                not self.historical_data.empty and 
                len(self.historical_data) > 0)
    
    def get_data_upload_template(self) -> pd.DataFrame:
        """Get template for uploading your historical data"""
        
        template_data = {
            'project_date': ['2023-01-15', '2023-02-20', '2023-03-10'],
            'container_type': ['40ft Standard', '20ft Standard', '40ft High Cube'],
            'use_case': ['Office Space', 'Workshop', 'Residential'],
            'location': ['Kąkolewo', 'Poznań', 'Warszawa'],
            'actual_cost': [45000, 25000, 55000],
            'estimated_cost': [42000, 27000, 52000],
            'materials_cost': [28000, 16000, 33000],
            'labor_cost': [12000, 7000, 15000],
            'delivery_cost': [3000, 1500, 4000],
            'modifications': ['{"windows": 4, "electrical": true}', 
                           '{"doors": 2, "hvac": true}',
                           '{"windows": 6, "electrical": true, "plumbing": true}'],
            'project_duration_days': [45, 30, 60],
            'customer_satisfaction': [5, 4, 5]
        }
        
        return pd.DataFrame(template_data)
    
    def analyze_cost_trends(self, months_back: int = 24) -> Dict[str, Any]:
        """Analyze cost trends from historical data"""
        
        if not self.has_historical_data():
            return {}
        
        cutoff_date = datetime.now() - timedelta(days=months_back * 30)
        recent_data = self.historical_data[
            self.historical_data['project_date'] >= cutoff_date
        ].copy()
        
        if recent_data.empty:
            return {}
        
        # Calculate trends
        recent_data = recent_data.sort_values('project_date')
        
        # Monthly cost trends
        recent_data['year_month'] = recent_data['project_date'].dt.to_period('M')
        monthly_trends = recent_data.groupby('year_month')['actual_cost'].mean()
        
        if len(monthly_trends) < 3:
            return {}
        
        # Calculate trend direction
        recent_months = monthly_trends.tail(6)
        trend_slope = np.polyfit(range(len(recent_months)), recent_months.values, 1)[0]
        
        return {
            'trend_direction': 'increasing' if trend_slope > 0 else 'decreasing',
            'monthly_change_rate': float(trend_slope),
            'latest_average_cost': float(recent_months.iloc[-1]),
            'cost_volatility': float(monthly_trends.std()),
            'data_period': f'{months_back} months',
            'confidence': min(1.0, len(monthly_trends) / 12)
        }