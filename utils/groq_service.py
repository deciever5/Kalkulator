"""
Groq AI Service Module
Integrates with Groq API for intelligent cost estimation and technical analysis
"""

import os
import json
import streamlit as st
from typing import Dict, Any, List
from groq import Groq

class GroqService:
    """Service for Groq AI integration"""
    
    def __init__(self):
        self.api_key = os.environ.get('GROQ_API_KEY')
        if not self.api_key:
            if st.session_state.get('employee_logged_in', False):
                st.error("GROQ_API_KEY not found in environment variables")
            self.client = None
        else:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                if st.session_state.get('employee_logged_in', False):
                    st.error(f"Failed to initialize Groq client: {str(e)}")
                self.client = None
    
    def generate_cost_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent cost estimate using Groq"""
        
        if not self.client:
            return self._fallback_cost_estimate(estimation_data, base_costs)
        
        try:
            prompt = self._build_cost_estimation_prompt(estimation_data, base_costs)
            
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert container modification cost estimator. Provide accurate cost estimates in JSON format with detailed breakdowns."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            return self._process_cost_estimate_response(result)
            
        except Exception as e:
            if st.session_state.get('employee_logged_in', False):
                st.error(f"Groq API error: {str(e)}")
            return self._fallback_cost_estimate(estimation_data, base_costs)
    
    def generate_technical_analysis(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                  structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical analysis using Groq"""
        
        if not self.client:
            return self._fallback_technical_analysis(config, analysis_params)
        
        try:
            prompt = self._build_technical_analysis_prompt(config, analysis_params, structural_analysis)
            
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a structural engineer specializing in container modifications. Provide technical analysis in JSON format with safety recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=3000
            )
            
            result = response.choices[0].message.content
            return self._process_technical_analysis_response(result)
            
        except Exception as e:
            if st.session_state.get('employee_logged_in', False):
                st.error(f"Groq technical analysis error: {str(e)}")
            return self._fallback_technical_analysis(config, analysis_params)
    
    def _build_cost_estimation_prompt(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> str:
        """Build prompt for cost estimation with Groq"""
        
        return f"""
        Analyze this container modification project and provide accurate cost estimates in EUR.
        
        Project Details:
        - Container Type: {estimation_data.get('container_type', 'Unknown')}
        - Use Case: {estimation_data.get('use_case', 'Unknown')}
        - Location: Europe (Poland)
        - Climate Zone: {estimation_data.get('climate_zone', 'Central European')}
        
        Modifications Required:
        {json.dumps(estimation_data.get('modifications', {}), indent=2)}
        
        Base Cost Information:
        {json.dumps(base_costs, indent=2)}
        
        Please provide a detailed cost breakdown in JSON format with:
        {{
            "total_cost": <number>,
            "material_costs": <number>,
            "labor_costs": <number>,
            "equipment_costs": <number>,
            "permit_costs": <number>,
            "margin": <number>,
            "timeline_weeks": <number>,
            "cost_breakdown": {{
                "structural": <number>,
                "electrical": <number>,
                "plumbing": <number>,
                "hvac": <number>,
                "insulation": <number>,
                "finishing": <number>
            }},
            "risk_factors": ["factor1", "factor2"],
            "recommendations": ["rec1", "rec2"],
            "confidence_score": <0-1>
        }}
        
        Consider European building standards, material costs, and labor rates in Poland.
        """
    
    def _build_technical_analysis_prompt(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                       structural_analysis: Dict[str, Any]) -> str:
        """Build prompt for technical analysis with Groq"""
        
        return f"""
        Perform technical analysis for this container modification project according to European standards.
        
        Container Configuration:
        {json.dumps(config, indent=2)}
        
        Analysis Parameters:
        {json.dumps(analysis_params, indent=2)}
        
        Structural Analysis Results:
        {json.dumps(structural_analysis, indent=2)}
        
        Provide technical analysis in JSON format:
        {{
            "structural_integrity": {{
                "safety_factor": <number>,
                "load_capacity": <number>,
                "stress_analysis": "description"
            }},
            "building_code_compliance": {{
                "european_standards": ["EN 1991", "EN 1993"],
                "compliance_status": "compliant/non-compliant",
                "required_permits": ["permit1", "permit2"]
            }},
            "environmental_considerations": {{
                "climate_suitability": "description",
                "insulation_requirements": "description",
                "weatherproofing": "description"
            }},
            "safety_recommendations": ["rec1", "rec2"],
            "potential_issues": ["issue1", "issue2"],
            "technical_score": <0-10>,
            "feasibility": "high/medium/low"
        }}
        
        Focus on European climate conditions and Polish building regulations.
        """
    
    def _process_cost_estimate_response(self, response: str) -> Dict[str, Any]:
        """Process and validate cost estimate response from Groq"""
        
        try:
            # Extract JSON from response
            if '```json' in response:
                json_str = response.split('```json')[1].split('```')[0].strip()
            elif '{' in response and '}' in response:
                start = response.find('{')
                end = response.rfind('}') + 1
                json_str = response[start:end]
            else:
                raise ValueError("No valid JSON found in response")
            
            result = json.loads(json_str)
            
            # Validate required fields
            required_fields = ['total_cost', 'material_costs', 'labor_costs', 'timeline_weeks']
            for field in required_fields:
                if field not in result:
                    result[field] = 0
            
            # Ensure confidence score is between 0 and 1
            result['confidence_score'] = max(0, min(1, result.get('confidence_score', 0.7)))
            
            # Add metadata
            result['ai_model'] = 'Groq Llama3-8B'
            result['generated_at'] = str(st.session_state.get('current_time', 'Unknown'))
            
            return result
            
        except Exception as e:
            if st.session_state.get('employee_logged_in', False):
                st.error(f"Error processing Groq response: {str(e)}")
            return self._fallback_cost_estimate({}, {})
    
    def _process_technical_analysis_response(self, response: str) -> Dict[str, Any]:
        """Process and validate technical analysis response from Groq"""
        
        try:
            # Extract JSON from response
            if '```json' in response:
                json_str = response.split('```json')[1].split('```')[0].strip()
            elif '{' in response and '}' in response:
                start = response.find('{')
                end = response.rfind('}') + 1
                json_str = response[start:end]
            else:
                raise ValueError("No valid JSON found in response")
            
            result = json.loads(json_str)
            
            # Add metadata
            result['ai_model'] = 'Groq Llama3-8B'
            result['analysis_date'] = str(st.session_state.get('current_time', 'Unknown'))
            
            return result
            
        except Exception as e:
            if st.session_state.get('employee_logged_in', False):
                st.error(f"Error processing Groq technical analysis: {str(e)}")
            return self._fallback_technical_analysis({}, {})
    
    def _fallback_cost_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback cost estimation when AI is unavailable"""
        
        # Basic calculation based on container type and modifications
        base_cost = base_costs.get('base_container_cost', 5000)
        modifications = estimation_data.get('modifications', {})
        
        # Simple cost multipliers
        total_cost = base_cost
        if modifications.get('windows', 0) > 0:
            total_cost += modifications['windows'] * 500
        if modifications.get('doors', 0) > 1:
            total_cost += (modifications['doors'] - 1) * 800
        if modifications.get('electrical', False):
            total_cost += 2000
        if modifications.get('plumbing', False):
            total_cost += 3000
        if modifications.get('hvac', False):
            total_cost += 4000
        if modifications.get('insulation', False):
            total_cost += 1500
        
        return {
            'total_cost': total_cost,
            'material_costs': total_cost * 0.6,
            'labor_costs': total_cost * 0.3,
            'equipment_costs': total_cost * 0.05,
            'margin': total_cost * 0.05,
            'timeline_weeks': 4,
            'confidence_score': 0.6,
            'ai_model': 'Fallback Calculation',
            'cost_breakdown': {
                'structural': total_cost * 0.3,
                'electrical': total_cost * 0.2,
                'plumbing': total_cost * 0.15,
                'hvac': total_cost * 0.2,
                'insulation': total_cost * 0.1,
                'finishing': total_cost * 0.05
            },
            'risk_factors': ['Standard project risks'],
            'recommendations': ['Follow standard procedures']
        }
    
    def _fallback_technical_analysis(self, config: Dict[str, Any], analysis_params: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback technical analysis when AI is unavailable"""
        
        return {
            'structural_integrity': {
                'safety_factor': 2.0,
                'load_capacity': 'Standard container load capacity',
                'stress_analysis': 'Basic structural analysis completed'
            },
            'building_code_compliance': {
                'european_standards': ['EN 1991-1-1', 'EN 1993-1-1'],
                'compliance_status': 'requires_review',
                'required_permits': ['Building permit', 'Electrical permit']
            },
            'environmental_considerations': {
                'climate_suitability': 'Suitable for Central European climate',
                'insulation_requirements': 'Standard insulation recommended',
                'weatherproofing': 'Standard weatherproofing required'
            },
            'safety_recommendations': [
                'Ensure proper structural reinforcement',
                'Follow electrical safety standards',
                'Implement proper ventilation'
            ],
            'potential_issues': [
                'Condensation in cold weather',
                'Thermal bridging at connections'
            ],
            'technical_score': 7,
            'feasibility': 'medium',
            'ai_model': 'Fallback Analysis'
        }