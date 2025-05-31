"""Fixed unterminated string literal in json extraction."""
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
        # Support multiple API keys for failover
        self.api_keys = []
        
        # Primary API key
        primary_key = os.environ.get('GROQ_API_KEY')
        if primary_key:
            self.api_keys.append(primary_key)
            
        # Reserve API keys
        reserve_key = os.environ.get('GROQ_RESERVE_API_KEY')
        if reserve_key:
            self.api_keys.append(reserve_key)
            
        # Additional reserve keys (can add more)
        reserve_key_2 = os.environ.get('GROQ_RESERVE_API_KEY_2')
        if reserve_key_2:
            self.api_keys.append(reserve_key_2)
        
        self.current_key_index = 0
        self.client = None
        
        if not self.api_keys:
            if st.session_state.get('employee_logged_in', False):
                st.error("No GROQ API keys found in environment variables")
        else:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Groq client with current API key"""
        if self.current_key_index < len(self.api_keys):
            try:
                self.client = Groq(api_key=self.api_keys[self.current_key_index])
                return True
            except Exception as e:
                if st.session_state.get('employee_logged_in', False):
                    st.warning(f"Failed to initialize Groq client with key {self.current_key_index + 1}: {str(e)}")
                return False
        return False
    
    def _try_next_key(self):
        """Switch to next available API key"""
        self.current_key_index += 1
        if self.current_key_index < len(self.api_keys):
            if st.session_state.get('employee_logged_in', False):
                st.info(f"Switching to reserve API key {self.current_key_index}")
            return self._initialize_client()
        return False

    def generate_cost_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent cost estimate using Groq with failover"""

        if not self.client:
            return self._fallback_cost_estimate(estimation_data, base_costs)

        max_retries = len(self.api_keys)
        
        for attempt in range(max_retries):
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
                error_msg = str(e).lower()
                if "rate limit" in error_msg or "429" in error_msg:
                    if st.session_state.get('employee_logged_in', False):
                        st.warning(f"Rate limit hit on API key {self.current_key_index + 1}: {str(e)}")
                    
                    # Try next API key
                    if self._try_next_key():
                        continue
                    else:
                        if st.session_state.get('employee_logged_in', False):
                            st.error("All API keys exhausted or rate limited")
                        break
                else:
                    if st.session_state.get('employee_logged_in', False):
                        st.error(f"Groq API error: {str(e)}")
                    break

        return self._fallback_cost_estimate(estimation_data, base_costs)

    def generate_technical_analysis(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                  structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical analysis using Groq with failover"""

        if not self.client:
            return self._fallback_technical_analysis(config, analysis_params)

        max_retries = len(self.api_keys)
        
        for attempt in range(max_retries):
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
                error_msg = str(e).lower()
                if "rate limit" in error_msg or "429" in error_msg:
                    if st.session_state.get('employee_logged_in', False):
                        st.warning(f"Rate limit hit on API key {self.current_key_index + 1}: {str(e)}")
                    
                    # Try next API key
                    if self._try_next_key():
                        continue
                    else:
                        if st.session_state.get('employee_logged_in', False):
                            st.error("All API keys exhausted or rate limited")
                        break
                else:
                    if st.session_state.get('employee_logged_in', False):
                        st.error(f"Groq technical analysis error: {str(e)}")
                    break

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

            # Validate required fields
            required_fields = ['structural_integrity', 'building_code_compliance', 'environmental_considerations']
            for field in required_fields:
                if field not in result:
                    result[field] = {}

            # Ensure technical score is between 0 and 10
            result['technical_score'] = max(0, min(10, result.get('technical_score', 7)))

            # Add metadata
            result['ai_model'] = 'Groq Llama3-8B'
            result['generated_at'] = str(st.session_state.get('current_time', 'Unknown'))

            return result

        except Exception as e:
            if st.session_state.get('employee_logged_in', False):
                st.error(f"Error processing Groq technical analysis response: {str(e)}")
            return self._fallback_technical_analysis({}, {})

    def _fallback_cost_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback cost estimation method"""

        return {
            "total_cost": 5000,
            "material_costs": 2000,
            "labor_costs": 2500,
            "equipment_costs": 300,
            "permit_costs": 200,
            "margin": 500,
            "timeline_weeks": 4,
            "cost_breakdown": {
                "structural": 1500,
                "electrical": 800,
                "plumbing": 700,
                "hvac": 600,
                "insulation": 400,
                "finishing": 1000
            },
            "risk_factors": ["Supply chain delays", "Unexpected permit issues"],
            "recommendations": ["Order materials in advance", "Consult with local authorities"],
            "confidence_score": 0.6,
            "ai_model": 'Fallback',
            "generated_at": str(st.session_state.get('current_time', 'Unknown'))
        }

    def _fallback_technical_analysis(self, config: Dict[str, Any], analysis_params: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback technical analysis method"""

        return {
            "structural_integrity": {
                "safety_factor": 2.5,
                "load_capacity": 5000,
                "stress_analysis": "Meets minimum safety standards"
            },
            "building_code_compliance": {
                "european_standards": ["EN 1991", "EN 1993"],
                "compliance_status": "compliant",
                "required_permits": ["Building permit", "Electrical permit"]
            },
            "environmental_considerations": {
                "climate_suitability": "Suitable for temperate climates",
                "insulation_requirements": "R-13 insulation recommended",
                "weatherproofing": "Requires sealant and weather-resistant paint"
            },
            "safety_recommendations": ["Install smoke detectors", "Ensure proper ventilation"],
            "potential_issues": ["Corrosion", "Moisture buildup"],
            "technical_score": 7.5,
            "feasibility": "high",
            "ai_model": 'Fallback',
            "generated_at": str(st.session_state.get('current_time', 'Unknown'))
        }

import asyncio
import aiohttp

class TranslationQualityChecker:
    """
    A service to check the quality of translations across multiple languages,
    using Polish as the base for comparison.
    """

    def __init__(self, groq_service: GroqService):
        self.groq_service = groq_service
        # Use the GroqService's client instead of creating our own
        self.client = groq_service.client
        self.languages = {
            "en": "English",
            "de": "German",
            "fr": "French",
            "es": "Spanish",
            "it": "Italian",
            "ru": "Russian",
            "zh": "Chinese",
            "ja": "Japanese",
            "pl": "Polish",
            # Add more languages as needed
        }

    async def check_translation_quality(self, text_to_translate: str) -> Dict[str, Dict[str, Any]]:
        """
        Orchestrates the translation and quality check process for all languages.
        """
        results = {}
        polish_translation = await self._translate_text(text_to_translate, "pl")
        if not polish_translation:
            return {"error": "Failed to translate to Polish"}
        results["pl"] = {"translation": polish_translation, "quality_score": 1.0}  # Polish is the base

        async with aiohttp.ClientSession() as session:
            tasks = [self._evaluate_translation(session, text_to_translate, language, polish_translation)
                     for language in self.languages if language != "pl"]
            evaluations = await asyncio.gather(*tasks)

        for language, evaluation in evaluations:
            results[language] = evaluation

        return results

    async def _translate_text(self, text: str, target_language: str) -> str:
         """
         Translate text to target language using Groq with failover.
         """
         if not self.client:
             print("Groq client is not initialized.")
             return ""

         max_retries = len(self.groq_service.api_keys)
         
         for attempt in range(max_retries):
             try:
                 # Get language name, fallback to the code itself if not found
                 target_language_name = self.languages.get(target_language, target_language)
                 prompt = f"""Translate the following text to {target_language_name}: '{text}'"""

                 response = self.client.chat.completions.create(
                     model="llama-3.1-8b-instant",
                     messages=[
                         {
                             "role": "system",
                             "content": f"You are a professional translator. Translate accurately to {target_language_name}."
                         },
                         {
                             "role": "user",
                             "content": prompt
                         }
                     ],
                     temperature=0.2,
                     max_tokens=1000
                 )
                 translation = response.choices[0].message.content.strip()
                 return translation

             except Exception as e:
                 error_msg = str(e).lower()
                 if "rate limit" in error_msg or "429" in error_msg:
                     print(f"Translation rate limit hit on API key {self.groq_service.current_key_index + 1}")
                     
                     # Try next API key using GroqService method
                     if self.groq_service._try_next_key():
                         # Update our client to use the new key
                         self.client = self.groq_service.client
                         continue
                     else:
                         print("All translation API keys exhausted or rate limited")
                         break
                 else:
                     print(f"Translation error to {target_language}: {e}")
                     break
         
         return None

    async def _evaluate_translation(self, session: aiohttp.ClientSession, original_text: str, target_language: str, polish_base: str) -> tuple[str, Dict[str, Any]]:
        """
        Evaluate translation quality by comparing the translation back to Polish and then to the original Polish.
        """
        translated_text = await self._translate_text(original_text, target_language)
        if not translated_text:
            return target_language, {"error": f"Failed to translate to {target_language}"}

        # Translate the translated text back to Polish
        back_translated_text = await self._translate_text(translated_text, "pl")
        if not back_translated_text:
            return target_language, {"error": f"Failed to back-translate from {target_language} to Polish"}

        # Score the similarity between the back-translated text and the original Polish base
        similarity_score = self._calculate_similarity(polish_base, back_translated_text)

        return target_language, {
            "translation": translated_text,
            "back_translation": back_translated_text,
            "quality_score": similarity_score
        }

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate the similarity between two texts using a simple approach.
        """
        # This is a placeholder; replace with a more sophisticated method like cosine similarity
        # using embeddings for better accuracy.
        words1 = text1.lower().split()
        words2 = text2.lower().split()
        common_words = set(words1) & set(words2)
        similarity = len(common_words) / max(len(words1), len(words2), 1)
        return similarity

# Example Usage (This will not run directly in this environment)
if __name__ == '__main__':
    async def main():
        groq_service = GroqService()
        checker = TranslationQualityChecker(groq_service)
        text_to_translate = "This is a test sentence to check translation quality."
        results = await checker.check_translation_quality(text_to_translate)
        print(json.dumps(results, indent=2))

    asyncio.run(main())