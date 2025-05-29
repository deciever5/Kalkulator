"""
Database Management Module for KAN-BUD Container Sales Calculator
Handles historical data storage and retrieval for improved pricing accuracy
"""

import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Dict, List, Any, Optional

Base = declarative_base()

# Historical projects removed as not needed at this stage

class CustomerData(Base):
    """Store customer information and preferences"""
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    company = Column(String(255))
    email = Column(String(255), unique=True)
    phone = Column(String(50))
    address = Column(Text)
    preferred_language = Column(String(10), default='en')
    customer_type = Column(String(100))
    credit_rating = Column(String(50))
    typical_project_size = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProjectQuotes(Base):
    """Store generated quotes and their outcomes"""
    __tablename__ = 'project_quotes'
    
    id = Column(Integer, primary_key=True)
    quote_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer)
    container_config = Column(JSON, nullable=False)
    estimated_cost = Column(Float, nullable=False)
    quote_date = Column(DateTime, default=datetime.utcnow)
    valid_until = Column(DateTime)
    status = Column(String(50), default='pending')  # pending, accepted, rejected, expired
    actual_final_cost = Column(Float)
    project_completed = Column(Boolean, default=False)
    ai_model_used = Column(String(50))
    accuracy_score = Column(Float)
    notes = Column(Text)

class MarketData(Base):
    """Store market pricing data for better estimates"""
    __tablename__ = 'market_data'
    
    id = Column(Integer, primary_key=True)
    material_type = Column(String(100), nullable=False)
    price_per_unit = Column(Float, nullable=False)
    unit_type = Column(String(50), nullable=False)
    supplier = Column(String(255))
    location = Column(String(255))
    date_recorded = Column(DateTime, default=datetime.utcnow)
    currency = Column(String(10), default='EUR')
    quality_grade = Column(String(50))

class DatabaseManager:
    """Main database management class"""
    
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable must be set")
        
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def add_historical_project(self, project_data: Dict[str, Any]) -> int:
        """Add a historical project for learning"""
        session = self.get_session()
        try:
            project = HistoricalProject(
                project_name=project_data['project_name'],
                container_type=project_data['container_type'],
                use_case=project_data['use_case'],
                modifications=project_data.get('modifications', {}),
                actual_cost=project_data['actual_cost'],
                estimated_cost=project_data.get('estimated_cost'),
                completion_date=project_data['completion_date'],
                location=project_data.get('location'),
                customer_type=project_data.get('customer_type'),
                project_size_category=project_data.get('project_size_category'),
                complexity_score=project_data.get('complexity_score'),
                material_costs=project_data.get('material_costs', {}),
                labor_hours=project_data.get('labor_hours'),
                timeline_weeks=project_data.get('timeline_weeks')
            )
            session.add(project)
            session.commit()
            project_id = project.id
            return project_id
        finally:
            session.close()
    
    def get_similar_projects(self, container_type: str, use_case: str, modifications: Dict) -> List[Dict]:
        """Find similar historical projects for pricing reference"""
        session = self.get_session()
        try:
            projects = session.query(HistoricalProject).filter(
                HistoricalProject.container_type == container_type,
                HistoricalProject.use_case == use_case
            ).order_by(HistoricalProject.completion_date.desc()).limit(10).all()
            
            result = []
            for project in projects:
                result.append({
                    'id': project.id,
                    'project_name': project.project_name,
                    'actual_cost': project.actual_cost,
                    'estimated_cost': project.estimated_cost,
                    'completion_date': project.completion_date,
                    'modifications': project.modifications,
                    'material_costs': project.material_costs,
                    'labor_hours': project.labor_hours,
                    'timeline_weeks': project.timeline_weeks,
                    'complexity_score': project.complexity_score
                })
            
            return result
        finally:
            session.close()
    
    def save_customer(self, customer_data: Dict[str, Any]) -> int:
        """Save customer information"""
        session = self.get_session()
        try:
            # Check if customer exists
            existing = session.query(CustomerData).filter(
                CustomerData.email == customer_data['email']
            ).first()
            
            if existing:
                # Update existing customer
                for key, value in customer_data.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                existing.updated_at = datetime.utcnow()
                session.commit()
                return existing.id
            else:
                # Create new customer
                customer = CustomerData(**customer_data)
                session.add(customer)
                session.commit()
                return customer.id
        finally:
            session.close()
    
    def save_quote(self, quote_data: Dict[str, Any]) -> str:
        """Save generated quote"""
        session = self.get_session()
        try:
            quote = ProjectQuotes(
                quote_number=quote_data['quote_number'],
                customer_id=quote_data.get('customer_id'),
                container_config=quote_data['container_config'],
                estimated_cost=quote_data['estimated_cost'],
                valid_until=quote_data.get('valid_until'),
                ai_model_used=quote_data.get('ai_model_used'),
                notes=quote_data.get('notes')
            )
            session.add(quote)
            session.commit()
            return quote.quote_number
        finally:
            session.close()
    
    def update_market_data(self, material_type: str, price: float, unit_type: str, 
                          supplier: str = None, location: str = None) -> None:
        """Update material market pricing data"""
        session = self.get_session()
        try:
            market_data = MarketData(
                material_type=material_type,
                price_per_unit=price,
                unit_type=unit_type,
                supplier=supplier,
                location=location
            )
            session.add(market_data)
            session.commit()
        finally:
            session.close()
    
    def get_market_prices(self, material_type: str = None) -> List[Dict]:
        """Get current market prices"""
        session = self.get_session()
        try:
            query = session.query(MarketData)
            if material_type:
                query = query.filter(MarketData.material_type == material_type)
            
            prices = query.order_by(MarketData.date_recorded.desc()).limit(20).all()
            
            result = []
            for price in prices:
                result.append({
                    'material_type': price.material_type,
                    'price_per_unit': price.price_per_unit,
                    'unit_type': price.unit_type,
                    'supplier': price.supplier,
                    'location': price.location,
                    'date_recorded': price.date_recorded,
                    'currency': price.currency
                })
            
            return result
        finally:
            session.close()
    
    def calculate_accuracy_metrics(self) -> Dict[str, float]:
        """Calculate pricing accuracy from historical data"""
        session = self.get_session()
        try:
            completed_quotes = session.query(ProjectQuotes).filter(
                ProjectQuotes.project_completed == True,
                ProjectQuotes.actual_final_cost.isnot(None)
            ).all()
            
            if not completed_quotes:
                return {'accuracy': 0.0, 'avg_variance': 0.0, 'total_projects': 0}
            
            accuracies = []
            variances = []
            
            for quote in completed_quotes:
                if quote.estimated_cost > 0:
                    variance = abs(quote.actual_final_cost - quote.estimated_cost) / quote.estimated_cost
                    accuracy = max(0, 1 - variance)
                    accuracies.append(accuracy)
                    variances.append(variance * 100)  # Convert to percentage
            
            return {
                'accuracy': sum(accuracies) / len(accuracies) if accuracies else 0.0,
                'avg_variance': sum(variances) / len(variances) if variances else 0.0,
                'total_projects': len(completed_quotes)
            }
        finally:
            session.close()
    
    def get_pricing_trends(self, days: int = 365) -> Dict[str, Any]:
        """Get pricing trends for the last specified days"""
        session = self.get_session()
        try:
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            projects = session.query(HistoricalProject).filter(
                HistoricalProject.completion_date >= cutoff_date
            ).all()
            
            trends = {
                'container_types': {},
                'use_cases': {},
                'avg_cost_per_month': {},
                'material_cost_trends': {}
            }
            
            for project in projects:
                # Container type trends
                if project.container_type not in trends['container_types']:
                    trends['container_types'][project.container_type] = []
                trends['container_types'][project.container_type].append(project.actual_cost)
                
                # Use case trends
                if project.use_case not in trends['use_cases']:
                    trends['use_cases'][project.use_case] = []
                trends['use_cases'][project.use_case].append(project.actual_cost)
            
            # Calculate averages
            for container_type, costs in trends['container_types'].items():
                trends['container_types'][container_type] = {
                    'avg_cost': sum(costs) / len(costs),
                    'min_cost': min(costs),
                    'max_cost': max(costs),
                    'project_count': len(costs)
                }
            
            for use_case, costs in trends['use_cases'].items():
                trends['use_cases'][use_case] = {
                    'avg_cost': sum(costs) / len(costs),
                    'min_cost': min(costs),
                    'max_cost': max(costs),
                    'project_count': len(costs)
                }
            
            return trends
        finally:
            session.close()