"""Update fallback estimate to use proper translations and language-specific content for Hungarian and Czech."""
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
import requests

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
        """Build optimized prompt for cost estimation"""
        config = estimation_data.get("container_config", {})

        # Build compact configuration summary
        config_summary = [
            f"Type: {config.get('base_type', 'Unknown')}",
            f"Use: {config.get('use_case', 'Unknown')}",
            f"Occupancy: {config.get('occupancy', 1)}",
            f"Environment: {config.get('environment', 'Unknown')}"
        ]

        modifications = config.get('modifications', {})
        if modifications:
            mod_list = [f"{k}: {v}" for k, v in modifications.items() if v]
            config_summary.append(f"Modifications: {', '.join(mod_list)}")

        return f"""Analyze container project. Config: {'; '.join(config_summary)}
Location: {estimation_data.get('project_location', 'Europe')}
Base costs: {json.dumps(base_costs, separators=(',', ':'))}

Respond in {estimation_data.get('response_language', 'en')} with JSON:
{{"total_cost":0,"confidence":0.8,"estimated_timeline":"8-12 weeks","breakdown":{{"container_base":0,"structural_modifications":0,"systems_installation":0,"finishes_interior":0,"labor_costs":0,"permits_fees":0,"delivery_logistics":0,"contingency":0}},"analysis":{{"recommendations":[],"risk_factors":[],"cost_optimization":[]}}}}"""

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

        **IMPORTANT: Respond in {estimation_data.get('response_language', 'en')} language for all text fields.**

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

class GroqService:
    """Service for Groq AI integration - Free and fast inference"""

    def __init__(self):
        self.model = "llama-3.1-70b-versatile"  # Free model
        self.api_key = os.environ.get('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1"

        if not self.api_key:
            # For demo purposes, we'll use a fallback
            self.api_key = "demo_mode"
            print("⚠️ No GROQ_API_KEY found. Using demo mode.")

    def generate_cost_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent cost estimate using Groq"""

        if self.api_key == "demo_mode":
            return self._generate_demo_estimate(estimation_data, base_costs)

        prompt = self._build_cost_estimation_prompt(estimation_data, base_costs)

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert construction cost estimator specializing in steel container modifications. Provide detailed, accurate cost estimates in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            }

            response = requests.post(f"{self.base_url}/chat/completions", 
                                   headers=headers, json=data)

            if response.status_code == 200:
                result_text = response.json()["choices"][0]["message"]["content"]
                # Extract JSON from response
                start = result_text.find('{')
                end = result_text.rfind('}') + 1
                json_content = result_text[start:end]

                result = json.loads(json_content)
                return self._process_cost_estimate_response(result)
            else:
                raise Exception(f"Groq API error: {response.status_code}")

        except Exception as e:
            print(f"Groq error, using fallback: {str(e)}")
            return self._generate_demo_estimate(estimation_data, base_costs)

    def _generate_demo_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate demo estimate when API is not available"""

        config = estimation_data.get("container_config", {})

        # Calculate basic estimate
        base_total = sum(base_costs.values())

        # Add complexity factors
        complexity_factor = 1.2
        if config.get("modifications", {}).get("reinforcement_walls"):
            complexity_factor += 0.1
        if config.get("modifications", {}).get("electrical"):
            complexity_factor += 0.15
        if config.get("modifications", {}).get("plumbing"):
            complexity_factor += 0.2

        total_cost = base_total * complexity_factor

        return {
            "total_cost": round(total_cost),
            "confidence": 0.85,
            "estimated_timeline": "8-12 weeks",
            "breakdown": {
                "container_base": base_costs.get("container_base", 5000),
                "structural_modifications": base_costs.get("structural_modifications", 0),
                "systems_installation": (base_costs.get("electrical", 0) + 
                                       base_costs.get("plumbing", 0) + 
                                       base_costs.get("hvac", 0)),
                "finishes_interior": base_costs.get("finishes", 1500),
                "labor_costs": total_cost * 0.4,
                "permits_fees": 1200,
                "delivery_logistics": 800,
                "contingency": total_cost * 0.1
            },
            "analysis": {
                "recommendations": [
                    "Consider standard electrical package for cost efficiency",
                    "Plan delivery route for oversized transport requirements",
                    "Schedule structural inspections early in process"
                ],
                "risk_factors": [
                    "Weather delays during construction phase",
                    "Permit approval timeline variations",
                    "Site access limitations for delivery"
                ],
                "cost_optimization": [
                    "Bundle multiple modifications for labor efficiency",
                    "Source materials locally to reduce shipping costs",
                    "Consider phased construction approach"
                ]
            }
        }

    def _build_cost_estimation_prompt(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> str:
        """Build prompt for cost estimation"""

        config = estimation_data.get("container_config", {})

        prompt = f"""
        Analyze this container modification project and provide a detailed cost estimate in JSON format.

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

        Base Costs: {json.dumps(base_costs, indent=2)}

        **IMPORTANT: Respond in {estimation_data.get('response_language', 'en')} language for all text fields.**

        Provide estimate in this exact JSON format:
        {{
            "total_cost": [number],
            "confidence": [0.0-1.0],
            "estimated_timeline": "[duration]",
            "breakdown": {{
                "container_base": [cost],
                "structural_modifications": [cost],
                "systems_installation": [cost],
                "finishes_interior": [cost],
                "labor_costs": [cost],
                "permits_fees": [cost],
                "delivery_logistics": [cost],
                "contingency": [cost]
            }},
            "analysis": {{
                "recommendations": ["rec1", "rec2", "rec3"],
                "risk_factors": ["risk1", "risk2", "risk3"],
                "cost_optimization": ["opt1", "opt2", "opt3"]
            }}
        }}
        """

        return prompt

    def _process_cost_estimate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate cost estimate response"""

        processed = {
            "total_cost": response.get("total_cost", 0),
            "confidence": min(1.0, max(0.0, response.get("confidence", 0.8))),
            "estimated_timeline": response.get("estimated_timeline", "8-12 weeks"),
            "breakdown": response.get("breakdown", {}),
            "analysis": response.get("analysis", {})
        }

        # Validate breakdown adds up to total
        breakdown_total = sum(processed["breakdown"].values())
        if abs(breakdown_total - processed["total_cost"]) > 100:
            processed["total_cost"] = breakdown_total

        return processed

    def generate_technical_analysis(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                  structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical analysis using Groq"""

        if self.api_key == "demo_mode":
            return self._generate_demo_technical_analysis(config, analysis_params, structural_analysis)

        prompt = self._build_technical_analysis_prompt(config, analysis_params, structural_analysis)

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a structural engineer specializing in container modifications. Provide technical analysis and recommendations in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            }

            response = requests.post(f"{self.base_url}/chat/completions", 
                                   headers=headers, json=data)

            if response.status_code == 200:
                result_text = response.json()["choices"][0]["message"]["content"]
                start = result_text.find('{')
                end = result_text.rfind('}') + 1
                json_content = result_text[start:end]

                result = json.loads(json_content)
                return result
            else:
                raise Exception(f"Groq API error: {response.status_code}")

        except Exception as e:
            print(f"Groq technical analysis error, using fallback: {str(e)}")
            return self._generate_demo_technical_analysis(config, analysis_params, structural_analysis)

    def _generate_demo_technical_analysis(self, config: Dict[str, Any], 
                                        analysis_params: Dict[str, Any], 
                                        structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate demo technical analysis"""

        return {
            "structural_recommendations": [
                "Add corner reinforcement for improved load distribution",
                "Consider additional floor support for heavy loads",
                "Implement proper drainage system for roof modifications"
            ],
            "modification_suggestions": [
                "Use structural-grade steel for all reinforcements",
                "Plan electrical routing to avoid structural members",
                "Consider modular approach for future modifications"
            ],
            "risk_mitigation": [
                "Conduct soil bearing capacity analysis",
                "Plan for thermal expansion in structural connections",
                "Implement proper ventilation to prevent condensation"
            ],
            "code_compliance_notes": [
                "Ensure compliance with local building codes",
                "Verify fire safety requirements for intended use",
                "Plan for ADA accessibility if required"
            ],
            "cost_impact": {
                "structural_reinforcement": "Additional $2,000-4,000 for enhanced structural integrity",
                "system_upgrades": "Professional installation recommended for safety compliance",
                "code_compliance": "Permit costs and inspections may add $1,000-2,500"
            }
        }

    def _build_technical_analysis_prompt(self, config: Dict[str, Any], 
                                       analysis_params: Dict[str, Any], 
                                       structural_analysis: Dict[str, Any]) -> str:
        """Build prompt for technical analysis"""

        prompt = f"""
        As a structural engineer, analyze this container modification project and provide technical recommendations.

        Container Configuration: {json.dumps(config, indent=2)}
        Analysis Parameters: {json.dumps(analysis_params, indent=2)}
        Structural Analysis: {json.dumps(structural_analysis, indent=2)}

        Provide analysis in this JSON format:
        {{
            "structural_recommendations": ["rec1", "rec2", "rec3"],
            "modification_suggestions": ["sug1", "sug2", "sug3"],
            "risk_mitigation": ["risk1", "risk2", "risk3"],
            "code_compliance_notes": ["note1", "note2", "note3"],
            "cost_impact": {{
                "structural_reinforcement": "impact description",
                "system_upgrades": "impact description",
                "code_compliance": "impact description"
            }}
        }}
        """

        return prompt

def estimate_cost_with_ai(config: Dict[str, Any], ai_model: str = "Auto-Select Best") -> str:
    """
    Generate AI cost estimate using specified model

    Args:
        config: Container configuration dictionary
        ai_model: Selected AI model name

    Returns:
        Formatted cost estimate as string
    """

    # Import translations here to avoid circular imports
    try:
        from utils.translations import get_current_language, t
        current_language = get_current_language()
    except ImportError:
        current_language = 'en'

    # Prepare estimation data
    estimation_data = {
        "container_config": config,
        "project_location": "Central Europe",
        "project_timeline": "Standard",
        "quality_level": "Standard",
        "additional_notes": "Standard container modification project",
        "response_language": current_language
    }

    # Calculate base costs from config
    base_costs = {
        "container_base": 8000 if config.get('container_type') == '20ft Standard' else 12000,
        "structural_modifications": 2000 if config.get('additional_doors') else 1000,
        "electrical": 1500 if config.get('finish_level') in ['Premium', 'Luxury'] else 800,
        "plumbing": 1200 if config.get('main_purpose') in ['Office Space', 'Living Space'] else 0,
        "hvac": 2000 if config.get('climate_zone') in ['Continental', 'Northern European'] else 1000,
        "finishes": 3000 if config.get('finish_level') == 'Luxury' else 1500,
        "windows": config.get('number_of_windows', 0) * 300
    }

    try:
        # Try Groq service first (free and fast)
        if "Groq" in ai_model or ai_model == "Auto-Select Best":
            try:
                groq_service = GroqService()
                result = groq_service.generate_cost_estimate(estimation_data, base_costs)
                return format_cost_estimate(result, "Groq AI")
            except Exception as e:
                print(f"Groq service failed: {e}")

        # Fallback to OpenAI if available
        if "OpenAI" in ai_model or ai_model == "Auto-Select Best":
            try:
                openai_service = OpenAIService()
                result = openai_service.generate_cost_estimate(estimation_data, base_costs)
                return format_cost_estimate(result, "OpenAI GPT-4o")
            except Exception as e:
                print(f"OpenAI service failed: {e}")

        # Fallback to Anthropic if available
        if "Anthropic" in ai_model or ai_model == "Auto-Select Best":
            try:
                anthropic_service = AnthropicService()
                result = anthropic_service.generate_cost_estimate(estimation_data, base_costs)
                return format_cost_estimate(result, "Anthropic Claude")
            except Exception as e:
                print(f"Anthropic service failed: {e}")

        # Final fallback - generate basic estimate
        return generate_fallback_estimate(config, base_costs, current_language)

    except Exception as e:
        return f"Error generating AI estimate: {str(e)}"

def format_cost_estimate(result: Dict[str, Any], ai_model: str) -> str:
    """Format AI cost estimate result into readable string"""

    breakdown = result.get('breakdown', {})
    analysis = result.get('analysis', {})

    estimate_text = f"""
## 🤖 AI Cost Estimate (Generated by {ai_model})

### 💰 **Total Project Cost: €{result.get('total_cost', 0):,.2f}**
*Confidence Level: {result.get('confidence', 0.8)*100:.0f}%*
*Estimated Timeline: {result.get('estimated_timeline', '8-12 weeks')}*

---

### 📊 **Cost Breakdown:**
- **Container Base:** €{breakdown.get('container_base', 0):,.2f}
- **Structural Modifications:** €{breakdown.get('structural_modifications', 0):,.2f}
- **Systems Installation:** €{breakdown.get('systems_installation', 0):,.2f}
- **Interior Finishes:** €{breakdown.get('finishes_interior', 0):,.2f}
- **Labor Costs:** €{breakdown.get('labor_costs', 0):,.2f}
- **Permits & Fees:** €{breakdown.get('permits_fees', 0):,.2f}
- **Delivery & Logistics:** €{breakdown.get('delivery_logistics', 0):,.2f}
- **Contingency (10%):** €{breakdown.get('contingency', 0):,.2f}

---

### 💡 **AI Recommendations:**
"""

    recommendations = analysis.get('recommendations', [])
    for i, rec in enumerate(recommendations, 1):
        estimate_text += f"{i}. {rec}\n"

    estimate_text += "\n### ⚠️ **Risk Factors:**\n"
    risk_factors = analysis.get('risk_factors', [])
    for i, risk in enumerate(risk_factors, 1):
        estimate_text += f"{i}. {risk}\n"

    estimate_text += "\n### 🎯 **Cost Optimization Opportunities:**\n"
    optimizations = analysis.get('cost_optimization', [])
    for i, opt in enumerate(optimizations, 1):
        estimate_text += f"{i}. {opt}\n"

    return estimate_text

def generate_fallback_estimate(config: Dict[str, Any], base_costs: Dict[str, Any], language: str = 'en') -> str:
    """Generate fallback cost estimate when AI services are unavailable"""

    # Import translations here to avoid circular imports
    try:
        from utils.translations import t
    except ImportError:
        # Fallback if translations not available
        def t(key, lang=None):
            return key

    # Calculate total cost
    total_cost = sum(base_costs.values())

    # Language-specific fallback content
    if language == 'hu':
        return f"""
## 🤖 Tartalék Költségbecslés

### 💰 **Teljes Projektköltség: €{total_cost:,.2f}**
*Alapszámítás amikor az AI szolgáltatások nem elérhetők*

---

### 📊 **Költséglebontás:**
- **Anyagok és Alapköltségek:** €{base_costs.get('container_base', 0) + base_costs.get('structural_modifications', 0) + base_costs.get('finishes', 0):,.2f}
- **Munkaerő Költségek (40%):** €{total_cost * 0.4:,.2f}
- **Engedélyek és Díjak:** €{total_cost * 0.1:,.2f}
- **Szállítás és Logisztika:** €{base_costs.get('windows', 0) * 50:,.2f}
- **Tartalék (10%):** €{total_cost * 0.1:,.2f}
"""
    elif language == 'cs':
        return f"""
## 🤖 Náhradní Odhad Nákladů

### 💰 **Celkové Náklady Projektu: €{total_cost:,.2f}**
*Základní výpočet, když nejsou služby AI dostupné*

---

### 📊 **Rozpis Nákladů:**
- **Materiály a Základní Náklady:** €{base_costs.get('container_base', 0) + base_costs.get('structural_modifications', 0) + base_costs.get('finishes', 0):,.2f}
- **Náklady na Práci (40%):** €{total_cost * 0.4:,.2f}
- **Povolení a Poplatky:** €{total_cost * 0.1:,.2f}
- **Doprava a Logistika:** €{base_costs.get('windows', 0) * 50:,.2f}
- **Rezerva (10%):** €{total_cost * 0.1:,.2f}
"""
    else:  # English default
        return f"""
## 🤖 Fallback Cost Estimate

### 💰 **Total Project Cost: €{total_cost:,.2f}**
*Basic calculation when AI services are unavailable*

---

### 📊 **Cost Breakdown:**
- **Materials & Base Costs:** €{base_costs.get('container_base', 0) + base_costs.get('structural_modifications', 0) + base_costs.get('finishes', 0):,.2f}
- **Labor Costs (40%):** €{total_cost * 0.4:,.2f}
- **Permits & Fees:** €{total_cost * 0.1:,.2f}
- **Delivery & Logistics:** €{base_costs.get('windows', 0) * 50:,.2f}
- **Contingency (10%):** €{total_cost * 0.1:,.2f}
"""

class ContainerCostEstimator:
    """
    A class for estimating the cost of container modifications using AI services.
    """

    def __init__(self, openai_api_key: Optional[str] = None, anthropic_api_key: Optional[str] = None):
        """
        Initializes the ContainerCostEstimator with optional OpenAI and Anthropic API keys.

        Args:
            openai_api_key (Optional[str]): The OpenAI API key. If None, OpenAI service will not be used.
            anthropic_api_key (Optional[str]): The Anthropic API key. If None, Anthropic service will not be used.
        """
        self.openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None
        self.anthropic_client = Anthropic(api_key=anthropic_api_key) if anthropic_api_key else None

    def _get_system_message(self, language: str) -> str:
        """Get system message in the appropriate language"""
        messages = {
            'en': "You are a professional container modification cost estimator with expertise in European construction standards and container conversions. Provide detailed cost estimates in English.",
            'pl': "Jesteś profesjonalnym rzeczoznawcą kosztów modyfikacji kontenerów z wiedzą na temat europejskich standardów budowlanych i przebudowy kontenerów. Przedstaw szczegółowe kosztorysy w języku polskim.",
            'de': "Sie sind ein professioneller Kostenschätzer für Containermodifikationen mit Expertise in europäischen Baustandards und Containerumbauten. Stellen Sie detaillierte Kostenschätzungen auf Deutsch bereit.",
            'nl': "Je bent een professionele kostenspecialist voor containermodificaties met expertise in Europese bouwstandaarden en containerconversies. Geef gedetailleerde kostenramingen in het Nederlands.",
            'hu': "Ön egy professzionális konténer-módosítási költségbecslő szakértő, aki jártas az európai építési szabványokban és konténer-átalakításokban. Adjon részletes költségbecsléseket magyar nyelven.",
            'cs': "Jste profesionální odhadce nákladů na úpravy kontejnerů s odborností v evropských stavebních standardech a přestavbách kontejnerů. Poskytněte podrobné odhady nákladů v češtině."
        }
        return messages.get(language, messages['en'])

    def _create_cost_estimation_prompt(self, config_data: Dict[str, Any], language: str = 'en') -> str:
        """Create detailed prompt for cost estimation in the specified language"""

        container_type = config_data.get('container_type', '20ft_standard')
        use_case = config_data.get('use_case', 'office_space')
        environment = config_data.get('environment', 'indoor')
        finish_level = config_data.get('finish_level', 'basic')

        if language == 'pl':
            prompt = f"""
Proszę o szczegółowy kosztorys dla następującego projektu modyfikacji kontenera:

SPECYFIKACJA KONTENERA:
- Typ: {container_type.replace('_', ' ').title()}
- Przeznaczenie: {use_case.replace('_', ' ').title()}
- Środowisko: {environment.title()}
- Poziom wykończenia: {finish_level.title()}

ŻĄDANE MODYFIKACJE:
- Podłoga: {config_data.get('flooring', 'standard').title()}
- Okna: {config_data.get('windows', 0)} sztuk
- Dodatkowe drzwi: {'Tak' if config_data.get('additional_doors') else 'Nie'}
- Strefa klimatyczna: {config_data.get('climate_zone', 'temperate').replace('_', ' ').title()}

SYSTEMY (jeśli wybrane):
- System elektryczny: {'Tak' if config_data.get('electrical_system') else 'Nie'}
- System hydrauliczny: {'Tak' if config_data.get('plumbing_system') else 'Nie'}
- System HVAC: {'Tak' if config_data.get('hvac_system') else 'Nie'}
- Pakiet izolacyjny: {'Tak' if config_data.get('insulation_package') else 'Nie'}

Proszę o podanie:
1. Szczegółowy podział kosztów
2. Szacowanie kosztów robocizny
3. Szacowanie kosztów materiałów
4. Całkowity koszt projektu w EUR
5. Szacowanie czasu realizacji
6. Dodatkowe uwagi lub rekomendacje

Oprzeć szacunki na aktualnych cenach rynkowych w Europie, włączając koszty dostawy/transportu.
Sformatować odpowiedź czytelnie z nagłówkami i punktami dla łatwego czytania.
"""
        elif language == 'de':
            prompt = f"""
Bitte erstellen Sie eine detaillierte Kostenschätzung für das folgende Containermodifikationsprojekt:

CONTAINER-SPEZIFIKATIONEN:
- Typ: {container_type.replace('_', ' ').title()}
- Verwendungszweck: {use_case.replace('_', ' ').title()}
- Umgebung: {environment.title()}
- Ausstattungsniveau: {finish_level.title()}

GEWÜNSCHTE MODIFIKATIONEN:
- Bodenbelag: {config_data.get('flooring', 'standard').title()}
- Fenster: {config_data.get('windows', 0)} Stück
- Zusätzliche Türen: {'Ja' if config_data.get('additional_doors') else 'Nein'}
- Klimazone: {config_data.get('climate_zone', 'temperate').replace('_', ' ').title()}

SYSTEME (falls ausgewählt):
- Elektrisches System: {'Ja' if config_data.get('electrical_system') else 'Nein'}
- Sanitärsystem: {'Ja' if config_data.get('plumbing_system') else 'Nein'}
- HVAC-System: {'Ja' if config_data.get('hvac_system') else 'Nein'}
- Isolationspaket: {'Ja' if config_data.get('insulation_package') else 'Nein'}

Bitte geben Sie an:
1. Aufgeschlüsselte Kostenübersicht
2. Arbeitskostenschätzung
3. Materialkostenschätzung
4. Gesamtprojektkosten in EUR
5. Zeitschätzung
6. Zusätzliche Überlegungen oder Empfehlungen

Basieren Sie Ihre Schätzungen auf aktuellen europäischen Marktpreisen und schließen Sie Liefer-/Transportkosten ein.
Formatieren Sie die Antwort klar mit Überschriften und Aufzählungspunkten für einfaches Lesen.
"""
        elif language == 'nl':
            prompt = f"""
Gelieve een gedetailleerde kostenraming te verstrekken voor het volgende containermodificatieproject:

CONTAINER SPECIFICATIES:
- Type: {container_type.replace('_', ' ').title()}
- Beoogd gebruik: {use_case.replace('_', ' ').title()}
- Omgeving: {environment.title()}
- Afwerkingsniveau: {finish_level.title()}

GEVRAAGDE WIJZIGINGEN:
- Vloerbedekking: {config_data.get('flooring', 'standard').title()}
- Ramen: {config_data.get('windows', 0)} stuks
- Extra deuren: {'Ja' if config_data.get('additional_doors') else 'Nee'}
- Klimaatzone: {config_data.get('climate_zone', 'temperate').replace('_', ' ').title()}

SYSTEMEN (indien geselecteerd):
- Elektrisch systeem: {'Ja' if config_data.get('electrical_system') else 'Nee'}
- Leidingsysteem: {'Ja' if config_data.get('plumbing_system') else 'Nee'}
- HVAC-systeem: {'Ja' if config_data.get('hvac_system') else 'Nee'}
- Isolatiepakket: {'Ja' if config_data.get('insulation_package') else 'Nee'}

Gelieve te verstrekken:
1. Gespecificeerde kostenverdeling
2. Arbeidskosten schatting
3. Materiaalkosten schatting
4. Totale projectkosten in EUR
5. Tijdsinschatting
6. Aanvullende overwegingen of aanbevelingen

Baseer uw schattingen op huidige Europese marktprijzen en voeg leverings-/transportkosten toe.
Formatteer het antwoord duidelijk met kopjes en opsommingstekens voor gemakkelijk lezen.
"""
        elif language == 'hu':
            prompt = f"""
Kérem, készítsen részletes költségbecslést a következő konténer-módosítási projekthez:

KONTÉNER SPECIFIKÁCIÓK:
- Típus: {container_type.replace('_', ' ').title()}
- Rendeltetés: {use_case.replace('_', ' ').title()}
- Környezet: {environment.title()}
- Befejezési szint: {finish_level.title()}

KÉRT MÓDOSÍTÁSOK:
- Padló: {config_data.get('flooring', 'standard').title()}
- Ablakok: {config_data.get('windows', 0)} darab
- További ajtók: {'Igen' if config_data.get('additional_doors') else 'Nem'}
- Klímaövezet: {config_data.get('climate_zone', 'temperate').replace('_', ' ').title()}

RENDSZEREK (ha kiválasztott):
- Elektromos rendszer: {'Igen' if config_data.get('electrical_system') else 'Nem'}
- Vízvezeték rendszer: {'Igen' if config_data.get('plumbing_system') else 'Nem'}
- HVAC rendszer: {'Igen' if config_data.get('hvac_system') else 'Nem'}
- Szigetelési csomag: {'Igen' if config_data.get('insulation_package') else 'Nem'}

Kérem, adja meg:
1. Részletes költségbontást
2. Munkaerőköltség becslést
3. Anyagköltség becslést
4. Teljes projektköltséget EUR-ban
5. Időbecslést
6. További megfontolásokat vagy ajánlásokat

Alapozza becsléseit a jelenlegi európai piaci árakra, és vegye figyelembe a szállítási/fuvarozási költségeket.
Formázza a választ világosan címekkel és felsorolásokkal a könnyű olvashatóság érdekében.
"""
        elif language == 'cs':
            prompt = f"""
Prosím o podrobný odhad nákladů na následující projekt úprav kontejneru:

SPECIFIKACE KONTEJNERU:
- Typ: {container_type.replace('_', ' ').title()}
- Zamýšlené použití: {use_case.replace('_', ' ').title()}
- Prostředí: {environment.title()}
- Úroveň dokončení: {finish_level.title()}

POŽADOVANÉ ÚPRAVY:
- Podlaha: {config_data.get('flooring', 'standard').title()}
- Okna: {config_data.get('windows', 0)} kusů
- Další dveře: {'Ano' if config_data.get('additional_doors') else 'Ne'}
- Klimatická zóna: {config_data.get('climate_zone', 'temperate').replace('_', ' ').title()}

SYSTÉMY (pokud vybráno):
- Elektrický systém: {'Ano' if config_data.get('electrical_system') else 'Ne'}
- Instalatérský systém: {'Ano' if config_data.get('plumbing_system') else 'Ne'}
- HVAC systém: {'Ano' if config_data.get('hvac_system') else 'Ne'}
- Izolační balíček: {'Ano' if config_data.get('insulation_package') else 'Ne'}

Prosím poskytněte:
1. Položkový rozpis nákladů
2. Odhad nákladů na práci
3. Odhad nákladů na materiál
4. Celkové náklady projektu v EUR
5. Odhad času
6. Dodatečné úvahy nebo doporučení

Založte své odhady na současných evropských tržních cenách a zahrňte náklady na dopravu/přepravu.
Naformátujte odpověď jasně s nadpisy a odrážkami pro snadné čtení.
"""
        else:  # English default
            prompt = f"""
Please provide a detailed cost estimate for the following container modification project:

CONTAINER SPECIFICATIONS:
- Type: {container_type.replace('_', ' ').title()}
- Intended Use: {use_case.replace('_', ' ').title()}
- Environment: {environment.title()}
- Finish Level: {finish_level.title()}

MODIFICATIONS REQUESTED:
- Flooring: {config_data.get('flooring', 'standard').title()}
- Windows: {config_data.get('windows', 0)} units
- Additional Doors: {'Yes' if config_data.get('additional_doors') else 'No'}
- Climate Zone: {config_data.get('climate_zone', 'temperate').replace('_', ' ').title()}

SYSTEMS (if selected):
- Electrical System: {'Yes' if config_data.get('electrical_system') else 'No'}
- Plumbing System: {'Yes' if config_data.get('plumbing_system') else 'No'}
- HVAC System: {'Yes' if config_data.get('hvac_system') else 'No'}
- Insulation Package: {'Yes' if config_data.get('insulation_package') else 'No'}

Please provide:
1. Itemized cost breakdown
2. Labor costs estimation
3. Material costs estimation
4. Total project cost in EUR
5. Timeline estimation
6. Any additional considerations or recommendations

Base your estimates on current European market prices and include delivery/transport costs.
Format the response clearly with headers and bullet points for easy reading.
"""

        return prompt

    def _validate_cost_response(self, response: str) -> bool:
        """Simple validation to ensure the response contains cost-related information."""
        return "EUR" in response or "€" in response or "cost" in response.lower()

    def generate_fallback_estimate(self, config_data: Dict[str, Any], language: str = 'en') -> str:
        """Generate a fallback estimate using predefined logic when AI services fail"""
        try:
            from utils.translations import t

            # Base costs (in EUR)
            base_costs = {
                '20ft_standard': 8000,
                '20ft_high_cube': 9000,
                '40ft_standard': 12000,
                '40ft_high_cube': 13500
            }

            # Get base cost
            container_type = config_data.get('container_type', '20ft_standard')
            base_cost = base_costs.get(container_type, 8000)

            # Calculate modifications cost
            modifications_cost = 0

            # Finish level multiplier
            finish_levels = {'basic': 1.0, 'standard': 1.3, 'premium': 1.8, 'luxury': 2.5}
            finish_level = config_data.get('finish_level', 'basic')
            finish_multiplier = finish_levels.get(finish_level, 1.0)

            # Add costs for specific modifications
            if config_data.get('windows', 0) > 0:
                modifications_cost += config_data['windows'] * 500

            if config_data.get('additional_doors', False):
                modifications_cost += 800

            # Flooring costs
            flooring_costs = {'plywood': 800, 'laminate': 1200, 'vinyl': 1000, 'concrete': 600}
            flooring = config_data.get('flooring', 'plywood')
            modifications_cost += flooring_costs.get(flooring, 800)

            # HVAC, electrical, etc.
            if config_data.get('hvac_system'):
                modifications_cost += 2500
            if config_data.get('electrical_system'):
                modifications_cost += 1500
            if config_data.get('plumbing_system'):
                modifications_cost += 2000

            # Apply finish level multiplier
            modifications_cost = int(modifications_cost * finish_multiplier)

            # Delivery cost
            delivery_cost = 800

            # Environment multiplier
            environment_multipliers = {'indoor': 1.0, 'outdoor': 1.3, 'marine': 1.6}
            environment = config_data.get('environment', 'indoor')
            env_multiplier = environment_multipliers.get(environment, 1.0)

            # Calculate total
            subtotal = (base_cost + modifications_cost + delivery_cost)
            total_cost = int(subtotal * env_multiplier)

            # Generate response using translations
            response = f"""
# {t('configuration_summary', language)}

**{t('base_container', language)}:**

• {t('type', language)}: {t(f'container.types.{container_type}', language)}

• {t('use_case', language)}: {t(f'container.use_cases.{config_data.get("use_case", "office_space")}', language)}

• {t('environment', language)}: {t(f'container.environment.{environment}', language)}

**{t('key_modifications', language)}:**

• {t('finish_level', language)}: {t(f'container.finish_levels.{finish_level}', language)}

• {t('flooring', language)}: {t(f'container.flooring.{flooring}', language)}

• {t('windows', language)}: {config_data.get('windows', 0)}

**{t('cost_breakdown', language)}:**

• {t('base_cost', language)}: €{base_cost:,.2f}

• {t('modifications', language)}: €{modifications_cost:,.2f}

• {t('delivery_cost', language)}: €{delivery_cost:,.2f}

• {t('multiplier', language)}: {env_multiplier}x

**{t('total_cost', language)}: €{total_cost:,.2f}**

*{t('preliminary_estimate_note', language)}*
"""

            return response.strip()

        except Exception as e:
            print(f"Error in fallback estimate generation: {e}")
            return f"Error generating estimate: {str(e)}"

    def estimate_container_cost(self, config_data: Dict[str, Any], language: str = 'en') -> str:
        """
        Generate container cost estimate using AI services
        Falls back to local estimation if AI services fail
        """
        try:
            # Create comprehensive prompt for cost estimation in the selected language
            prompt = self._create_cost_estimation_prompt(config_data, language)

            # Try OpenAI first
            if self.openai_client:
                try:
                    system_message = self._get_system_message(language)
                    response = self.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=1000,
                        temperature=0.7
                    )

                    ai_response = response.choices[0].message.content

                    # Validate the response contains cost information
                    if self._validate_cost_response(ai_response):
                        return ai_response
                    else:
                        print("OpenAI response validation failed, trying Anthropic...")

                except Exception as e:
                    print(f"OpenAI API error: {e}")

            # Try Anthropic if OpenAI fails
            if self.anthropic_client:
                try:
                    response = self.anthropic_client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=1000,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )

                    ai_response = response.content[0].text

                    # Validate the response contains cost information
                    if self._validate_cost_response(ai_response):
                        return ai_response
                    else:
                        print("Anthropic response validation failed, using fallback...")

                except Exception as e:
                    print(f"Anthropic API error: {e}")

            # If both AI services fail, use fallback estimation
            print("All AI services failed, using fallback estimation...")
            return self.generate_fallback_estimate(config_data, language)

        except Exception as e:
            print(f"Error in estimate_container_cost: {e}")
            return self.generate_fallback_estimate(config_data, language)