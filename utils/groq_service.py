"""Groq AI service updated to use supported model llama-3.1-8b-instant."""
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
                model="llama-3.1-8b-instant",
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
                model="llama-3.1-8b-instant",
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
                json_str = response.split('```json')[1].split('