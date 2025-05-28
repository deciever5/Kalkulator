"""
Database Module for KAN-BUD Container Calculator
Handles user data, historical projects, and pricing accuracy improvements
"""

import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List, Any, Optional
import json
from datetime import datetime, timedelta

class DatabaseManager:
    """Database manager for KAN-BUD container calculation system"""
    
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        if not self.database_url:
            st.error("DATABASE_URL not configured")
            return
        
        try:
            self.engine = create_engine(self.database_url)
            self.initialize_tables()
        except Exception as e:
            st.error(f"Database connection failed: {str(e)}")
            self.engine = None
    
    def initialize_tables(self):
        """Create necessary tables for the KAN-BUD system"""
        
        tables_sql = """
        -- Historical project data table
        CREATE TABLE IF NOT EXISTS historical_projects (
            id SERIAL PRIMARY KEY,
            project_date DATE NOT NULL,
            container_type VARCHAR(50) NOT NULL,
            use_case VARCHAR(100) NOT NULL,
            location VARCHAR(100),
            actual_cost DECIMAL(12,2) NOT NULL,
            estimated_cost DECIMAL(12,2),
            materials_cost DECIMAL(12,2),
            labor_cost DECIMAL(12,2),
            delivery_cost DECIMAL(12,2),
            modifications JSONB,
            project_duration_days INTEGER,
            customer_satisfaction INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Material pricing history
        CREATE TABLE IF NOT EXISTS material_prices (
            id SERIAL PRIMARY KEY,
            material_name VARCHAR(100) NOT NULL,
            price_per_unit DECIMAL(10,4) NOT NULL,
            unit VARCHAR(20) NOT NULL,
            supplier VARCHAR(100),
            price_date DATE NOT NULL,
            region VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Labor rates by region and skill
        CREATE TABLE IF NOT EXISTS labor_rates (
            id SERIAL PRIMARY KEY,
            skill_level VARCHAR(50) NOT NULL,
            hourly_rate DECIMAL(8,2) NOT NULL,
            region VARCHAR(50) NOT NULL,
            effective_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- User projects and configurations
        CREATE TABLE IF NOT EXISTS user_projects (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(100),
            project_name VARCHAR(200) NOT NULL,
            container_config JSONB NOT NULL,
            cost_estimate JSONB,
            technical_analysis JSONB,
            quote_data JSONB,
            status VARCHAR(50) DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Customer data
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            company VARCHAR(200),
            email VARCHAR(150),
            phone VARCHAR(50),
            address TEXT,
            preferred_language VARCHAR(10) DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Quotes and proposals
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            quote_number VARCHAR(50) UNIQUE NOT NULL,
            customer_id INTEGER REFERENCES customers(id),
            project_id INTEGER REFERENCES user_projects(id),
            total_amount DECIMAL(12,2) NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            valid_until DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Market data and trends
        CREATE TABLE IF NOT EXISTS market_data (
            id SERIAL PRIMARY KEY,
            data_type VARCHAR(50) NOT NULL,
            value DECIMAL(12,4) NOT NULL,
            unit VARCHAR(20),
            region VARCHAR(50),
            data_date DATE NOT NULL,
            source VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Create indexes for better performance
        CREATE INDEX IF NOT EXISTS idx_historical_projects_date ON historical_projects(project_date);
        CREATE INDEX IF NOT EXISTS idx_material_prices_date ON material_prices(price_date);
        CREATE INDEX IF NOT EXISTS idx_user_projects_user ON user_projects(user_id);
        CREATE INDEX IF NOT EXISTS idx_quotes_customer ON quotes(customer_id);
        """
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text(tables_sql))
                conn.commit()
        except SQLAlchemyError as e:
            st.error(f"Failed to initialize database tables: {str(e)}")
    
    def insert_historical_data(self, data: List[Dict[str, Any]]) -> bool:
        """Insert historical project data for improved pricing accuracy"""
        
        if not self.engine:
            return False
        
        try:
            df = pd.DataFrame(data)
            df.to_sql('historical_projects', self.engine, if_exists='append', index=False)
            return True
        except Exception as e:
            st.error(f"Failed to insert historical data: {str(e)}")
            return False
    
    def get_historical_pricing_data(self, container_type: str, use_case: str, 
                                  months_back: int = 24) -> Dict[str, Any]:
        """Get historical pricing data for more accurate estimates"""
        
        if not self.engine:
            return {}
        
        cutoff_date = datetime.now() - timedelta(days=months_back * 30)
        
        query = """
        SELECT 
            AVG(actual_cost) as avg_cost,
            MIN(actual_cost) as min_cost,
            MAX(actual_cost) as max_cost,
            AVG(materials_cost) as avg_materials,
            AVG(labor_cost) as avg_labor,
            AVG(project_duration_days) as avg_duration,
            COUNT(*) as project_count
        FROM historical_projects 
        WHERE container_type = :container_type 
        AND use_case = :use_case 
        AND project_date >= :cutoff_date
        """
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), {
                    'container_type': container_type,
                    'use_case': use_case,
                    'cutoff_date': cutoff_date
                }).fetchone()
                
                if result and result[6] > 0:  # project_count > 0
                    return {
                        'avg_cost': float(result[0]) if result[0] else 0,
                        'min_cost': float(result[1]) if result[1] else 0,
                        'max_cost': float(result[2]) if result[2] else 0,
                        'avg_materials': float(result[3]) if result[3] else 0,
                        'avg_labor': float(result[4]) if result[4] else 0,
                        'avg_duration': float(result[5]) if result[5] else 0,
                        'project_count': int(result[6]),
                        'confidence': min(1.0, int(result[6]) / 10)  # Higher confidence with more projects
                    }
        except Exception as e:
            st.error(f"Failed to get historical pricing data: {str(e)}")
        
        return {}
    
    def get_current_material_prices(self) -> Dict[str, float]:
        """Get current material prices for accurate cost calculation"""
        
        if not self.engine:
            return {}
        
        query = """
        SELECT DISTINCT ON (material_name) 
            material_name, price_per_unit, unit
        FROM material_prices 
        ORDER BY material_name, price_date DESC
        """
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query)).fetchall()
                return {row[0]: float(row[1]) for row in result}
        except Exception as e:
            st.error(f"Failed to get material prices: {str(e)}")
            return {}
    
    def save_user_project(self, user_id: str, project_name: str, 
                         config: Dict[str, Any], estimate: Dict[str, Any] = None,
                         analysis: Dict[str, Any] = None) -> Optional[int]:
        """Save user project configuration and results"""
        
        if not self.engine:
            return None
        
        query = """
        INSERT INTO user_projects (user_id, project_name, container_config, cost_estimate, technical_analysis)
        VALUES (:user_id, :project_name, :config, :estimate, :analysis)
        RETURNING id
        """
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), {
                    'user_id': user_id,
                    'project_name': project_name,
                    'config': json.dumps(config),
                    'estimate': json.dumps(estimate) if estimate else None,
                    'analysis': json.dumps(analysis) if analysis else None
                }).fetchone()
                conn.commit()
                return result[0] if result else None
        except Exception as e:
            st.error(f"Failed to save project: {str(e)}")
            return None
    
    def get_user_projects(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all projects for a user"""
        
        if not self.engine:
            return []
        
        query = """
        SELECT id, project_name, container_config, cost_estimate, 
               technical_analysis, status, created_at
        FROM user_projects 
        WHERE user_id = :user_id 
        ORDER BY created_at DESC
        """
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), {'user_id': user_id}).fetchall()
                
                projects = []
                for row in result:
                    projects.append({
                        'id': row[0],
                        'project_name': row[1],
                        'container_config': json.loads(row[2]) if row[2] else {},
                        'cost_estimate': json.loads(row[3]) if row[3] else {},
                        'technical_analysis': json.loads(row[4]) if row[4] else {},
                        'status': row[5],
                        'created_at': row[6]
                    })
                
                return projects
        except Exception as e:
            st.error(f"Failed to get user projects: {str(e)}")
            return []
    
    def save_customer(self, customer_data: Dict[str, Any]) -> Optional[int]:
        """Save customer information"""
        
        if not self.engine:
            return None
        
        query = """
        INSERT INTO customers (name, company, email, phone, address, preferred_language)
        VALUES (:name, :company, :email, :phone, :address, :language)
        RETURNING id
        """
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), customer_data).fetchone()
                conn.commit()
                return result[0] if result else None
        except Exception as e:
            st.error(f"Failed to save customer: {str(e)}")
            return None
    
    def save_quote(self, quote_data: Dict[str, Any]) -> bool:
        """Save generated quote"""
        
        if not self.engine:
            return False
        
        query = """
        INSERT INTO quotes (quote_number, customer_id, project_id, total_amount, valid_until)
        VALUES (:quote_number, :customer_id, :project_id, :total_amount, :valid_until)
        """
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text(query), quote_data)
                conn.commit()
                return True
        except Exception as e:
            st.error(f"Failed to save quote: {str(e)}")
            return False
    
    def get_market_trends(self, data_type: str, months_back: int = 12) -> List[Dict[str, Any]]:
        """Get market trend data for analysis"""
        
        if not self.engine:
            return []
        
        cutoff_date = datetime.now() - timedelta(days=months_back * 30)
        
        query = """
        SELECT value, data_date, region, unit
        FROM market_data 
        WHERE data_type = :data_type 
        AND data_date >= :cutoff_date 
        ORDER BY data_date DESC
        """
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), {
                    'data_type': data_type,
                    'cutoff_date': cutoff_date
                }).fetchall()
                
                return [{'value': float(row[0]), 'date': row[1], 'region': row[2], 'unit': row[3]} 
                       for row in result]
        except Exception as e:
            st.error(f"Failed to get market trends: {str(e)}")
            return []