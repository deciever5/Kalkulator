"""
AI Services Module
Integrates with OpenAI and Anthropic APIs for intelligent cost estimation and technical analysis
"""

import os
import json
import sys
from typing import Dict, List, Any, Optional
from openai import OpenAI
import anthropic
from anthropic import Anthropic

class OpenAIService:
    """Service for OpenAI GPT-4o integration"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
        self.model = "gpt-4o"
        self.api_key = os.environ.get('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_cost_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent cost estimate using GPT-4o"""
        
        prompt = self._build_cost_estimation_prompt(estimation_data, base_costs)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert construction cost estimator specializing in steel container modifications. Provide detailed, accurate cost estimates in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            return self._process_cost_estimate_response(result)
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def generate_technical_analysis(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                  structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical analysis and recommendations"""
        
        prompt = self._build_technical_analysis_prompt(config, analysis_params, structural_analysis)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a structural engineer specializing in container modifications. Provide technical analysis and recommendations in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            raise Exception(f"OpenAI technical analysis error: {str(e)}")
    
    def _build_cost_estimation_prompt(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> str:
        """Build prompt for cost estimation"""
        
        config = estimation_data.get("container_config", {})
        
        prompt = f"""
        Analyze the following container modification project and provide a detailed cost estimate in JSON format.

        **Container Configuration:**
        - Base Type: {config.get('base_type', 'Unknown')}
        - Use Case: {config.get('use_case', 'Unknown')}
        - Occupancy: {config.get('occupancy', 1)} people
        - Environment: {config.get('environment', 'Unknown')}

        **Modifications Required:**
        {json.dumps(config.get('modifications', {}), indent=2)}

        **Project Parameters:**
        - Location: {estimation_data.get('project_location', 'Unknown')}
        - Timeline: {estimation_data.get('project_timeline', 'Unknown')}
        - Quality Level: {estimation_data.get('quality_level', 'Standard')}
        - Additional Notes: {estimation_data.get('additional_notes', 'None')}

        **Base Cost Calculations:**
        {json.dumps(base_costs, indent=2)}

        Please provide a comprehensive cost estimate with the following JSON structure:
        {{
            "total_cost": 0,
            "confidence": 0.0,
            "estimated_timeline": "weeks",
            "breakdown": {{
                "container_base": 0,
                "structural_modifications": 0,
                "systems_installation": 0,
                "finishes_interior": 0,
                "labor_costs": 0,
                "permits_fees": 0,
                "delivery_logistics": 0,
                "contingency": 0
            }},
            "analysis": {{
                "recommendations": ["recommendation1", "recommendation2"],
                "risk_factors": ["risk1", "risk2"],
                "cost_optimization": ["optimization1", "optimization2"]
            }}
        }}

        Consider current market conditions, regional pricing variations, and the specific requirements of the project.
        """
        
        return prompt
    
    def _build_technical_analysis_prompt(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                       structural_analysis: Dict[str, Any]) -> str:
        """Build prompt for technical analysis"""
        
        prompt = f"""
        Perform a technical analysis of this container modification project and provide recommendations in JSON format.

        **Container Configuration:**
        {json.dumps(config, indent=2)}

        **Analysis Parameters:**
        {json.dumps(analysis_params, indent=2)}

        **Structural Analysis Results:**
        {json.dumps(structural_analysis, indent=2)}

        Please provide technical recommendations with the following JSON structure:
        {{
            "structural_recommendations": ["recommendation1", "recommendation2"],
            "modification_suggestions": ["suggestion1", "suggestion2"],
            "risk_mitigation": ["mitigation1", "mitigation2"],
            "code_compliance_notes": ["note1", "note2"],
            "cost_impact": {{
                "structural_reinforcement": "impact description",
                "system_upgrades": "impact description",
                "code_compliance": "impact description"
            }}
        }}

        Focus on structural integrity, code compliance, and practical implementation considerations.
        """
        
        return prompt
    
    def _process_cost_estimate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate cost estimate response"""
        
        # Ensure required fields exist
        processed = {
            "total_cost": response.get("total_cost", 0),
            "confidence": min(1.0, max(0.0, response.get("confidence", 0.8))),
            "estimated_timeline": response.get("estimated_timeline", "8-12 weeks"),
            "breakdown": response.get("breakdown", {}),
            "analysis": response.get("analysis", {})
        }
        
        # Validate breakdown adds up to total
        breakdown_total = sum(processed["breakdown"].values())
        if abs(breakdown_total - processed["total_cost"]) > 100:  # Allow small rounding differences
            # Adjust total to match breakdown
            processed["total_cost"] = breakdown_total
        
        return processed

class AnthropicService:
    """Service for Anthropic Claude integration"""
    
    def __init__(self):
        #the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
        self.model = "claude-3-5-sonnet-20241022"
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable must be set")
        
        self.client = Anthropic(api_key=self.api_key)
    
    def generate_cost_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent cost estimate using Claude"""
        
        prompt = self._build_cost_estimation_prompt(estimation_data, base_costs)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract JSON from response
            content = response.content[0].text
            # Find JSON content between curly braces
            start = content.find('{')
            end = content.rfind('}') + 1
            json_content = content[start:end]
            
            result = json.loads(json_content)
            return self._process_cost_estimate_response(result)
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def generate_technical_analysis(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                  structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical analysis using Claude"""
        
        prompt = self._build_technical_analysis_prompt(config, analysis_params, structural_analysis)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract JSON from response
            content = response.content[0].text
            start = content.find('{')
            end = content.rfind('}') + 1
            json_content = content[start:end]
            
            result = json.loads(json_content)
            return result
            
        except Exception as e:
            raise Exception(f"Anthropic technical analysis error: {str(e)}")
    
    def _build_cost_estimation_prompt(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> str:
        """Build prompt for cost estimation with Claude"""
        
        config = estimation_data.get("container_config", {})
        
        prompt = f"""
        As an expert construction cost estimator specializing in steel container modifications, analyze the following project and provide a detailed cost estimate.

        Container Configuration:
        - Base Type: {config.get('base_type', 'Unknown')}
        - Use Case: {config.get('use_case', 'Unknown')}
        - Occupancy: {config.get('occupancy', 1)} people
        - Environment: {config.get('environment', 'Unknown')}
        - Modifications: {json.dumps(config.get('modifications', {}), indent=2)}

        Project Parameters:
        - Location: {estimation_data.get('project_location', 'Unknown')}
        - Timeline: {estimation_data.get('project_timeline', 'Unknown')}
        - Quality Level: {estimation_data.get('quality_level', 'Standard')}
        - Additional Notes: {estimation_data.get('additional_notes', 'None')}

        Base Cost Calculations:
        {json.dumps(base_costs, indent=2)}

        Provide your analysis in the following JSON format:
        {{
            "total_cost": [total project cost in USD],
            "confidence": [confidence level 0.0-1.0],
            "estimated_timeline": "[project duration]",
            "breakdown": {{
                "container_base": [base container cost],
                "structural_modifications": [structural work cost],
                "systems_installation": [electrical/plumbing/HVAC cost],
                "finishes_interior": [interior finishes cost],
                "labor_costs": [total labor cost],
                "permits_fees": [permits and fees],
                "delivery_logistics": [delivery and logistics],
                "contingency": [contingency amount]
            }},
            "analysis": {{
                "recommendations": ["specific recommendation 1", "specific recommendation 2"],
                "risk_factors": ["potential risk 1", "potential risk 2"],
                "cost_optimization": ["optimization opportunity 1", "optimization opportunity 2"]
            }}
        }}

        Consider current market conditions, regional pricing variations, material costs, labor rates, and project complexity. Be specific and practical in your recommendations.
        """
        
        return prompt
    
    def _build_technical_analysis_prompt(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                       structural_analysis: Dict[str, Any]) -> str:
        """Build prompt for technical analysis with Claude"""
        
        prompt = f"""
        As a structural engineer specializing in container modifications, analyze this project and provide technical recommendations.

        Container Configuration:
        {json.dumps(config, indent=2)}

        Analysis Parameters:
        {json.dumps(analysis_params, indent=2)}

        Structural Analysis Results:
        {json.dumps(structural_analysis, indent=2)}

        Provide your technical analysis in the following JSON format:
        {{
            "structural_recommendations": ["specific structural recommendation 1", "specific structural recommendation 2"],
            "modification_suggestions": ["modification suggestion 1", "modification suggestion 2"],
            "risk_mitigation": ["risk mitigation strategy 1", "risk mitigation strategy 2"],
            "code_compliance_notes": ["compliance note 1", "compliance note 2"],
            "cost_impact": {{
                "structural_reinforcement": "detailed impact description",
                "system_upgrades": "detailed impact description",
                "code_compliance": "detailed impact description"
            }}
        }}

        Focus on structural integrity, building code compliance, safety factors, and practical implementation. Consider the specific use case and environmental conditions.
        """
        
        return prompt
    
    def _process_cost_estimate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate cost estimate response from Claude"""
        
        # Ensure required fields exist
        processed = {
            "total_cost": response.get("total_cost", 0),
            "confidence": min(1.0, max(0.0, response.get("confidence", 0.8))),
            "estimated_timeline": response.get("estimated_timeline", "8-12 weeks"),
            "breakdown": response.get("breakdown", {}),
            "analysis": response.get("analysis", {})
        }
        
        # Validate breakdown adds up to total
        breakdown_total = sum(processed["breakdown"].values())
        if abs(breakdown_total - processed["total_cost"]) > 100:  # Allow small rounding differences
            # Adjust total to match breakdown
            processed["total_cost"] = breakdown_total
        
        return processed
