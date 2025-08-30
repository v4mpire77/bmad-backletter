"""
Gemini AI Service for advanced contract analysis
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import google.generativeai as genai
from ..config import settings

logger = logging.getLogger(__name__)


@dataclass
class GeminiAnalysisResult:
    """Result from Gemini AI analysis"""
    summary: str
    key_terms: List[str]
    risk_factors: List[str]
    recommendations: List[str]
    confidence_score: float
    raw_response: Dict[str, Any]


@dataclass
class GeminiChatResponse:
    """Response from Gemini chat interaction"""
    response: str
    suggestions: List[str]
    follow_up_questions: List[str]


class GeminiService:
    """Service for interacting with Google's Gemini AI"""

    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.model_name = settings.gemini_model
        self.max_tokens = settings.gemini_max_tokens
        self.temperature = settings.gemini_temperature

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"Gemini service initialized with model: {self.model_name}")
        else:
            self.model = None
            logger.warning("Gemini API key not configured. Service will be unavailable.")

    def is_available(self) -> bool:
        """Check if Gemini service is available"""
        return self.model is not None

    def analyze_contract(self, contract_text: str, analysis_type: str = "general") -> Optional[GeminiAnalysisResult]:
        """
        Analyze contract text using Gemini AI

        Args:
            contract_text: The contract text to analyze
            analysis_type: Type of analysis ("general", "risk", "compliance", "financial")

        Returns:
            GeminiAnalysisResult or None if service unavailable
        """
        if not self.is_available():
            logger.error("Gemini service not available - API key not configured")
            return None

        try:
            # Create analysis prompt based on type
            prompt = self._create_analysis_prompt(contract_text, analysis_type)

            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
                top_p=0.9,
                top_k=40
            )

            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )

            # Parse and structure the response
            return self._parse_analysis_response(response, contract_text)

        except Exception as e:
            logger.error(f"Error analyzing contract with Gemini: {e}")
            return None

    def chat_about_contract(self, message: str, contract_context: Optional[str] = None) -> Optional[GeminiChatResponse]:
        """
        Interactive chat about contract-related questions

        Args:
            message: User's question or message
            contract_context: Optional contract text for context

        Returns:
            GeminiChatResponse or None if service unavailable
        """
        if not self.is_available():
            logger.error("Gemini service not available - API key not configured")
            return None

        try:
            # Create chat prompt
            prompt = self._create_chat_prompt(message, contract_context)

            # Generate response
            response = self.model.generate_content(prompt)

            # Parse chat response
            return self._parse_chat_response(response)

        except Exception as e:
            logger.error(f"Error in Gemini chat: {e}")
            return None

    def summarize_contract(self, contract_text: str, max_length: int = 500) -> Optional[str]:
        """
        Generate a concise summary of the contract

        Args:
            contract_text: Contract text to summarize
            max_length: Maximum length of summary in words

        Returns:
            Summary string or None if service unavailable
        """
        if not self.is_available():
            return None

        try:
            prompt = f"""
            Please provide a concise summary of the following contract in approximately {max_length} words or less.
            Focus on the key terms, obligations, rights, and important clauses:

            {contract_text[:10000]}  # Limit input to avoid token limits
            """

            response = self.model.generate_content(prompt)
            return response.text.strip() if response else None

        except Exception as e:
            logger.error(f"Error summarizing contract: {e}")
            return None

    def _create_analysis_prompt(self, contract_text: str, analysis_type: str) -> str:
        """Create analysis prompt based on type"""

        base_prompt = f"""
        You are an expert legal contract analyst. Analyze the following contract text and provide detailed insights.

        Contract Text:
        {contract_text[:15000]}  # Limit to avoid token limits

        """

        if analysis_type == "risk":
            return base_prompt + """
            Please provide a comprehensive risk analysis including:
            1. Overall risk level (Low, Medium, High, Critical)
            2. Key risk factors identified
            3. Specific recommendations to mitigate risks
            4. Critical clauses that need attention
            5. Compliance gaps or concerns

            Format your response as JSON with the following structure:
            {
                "risk_level": "string",
                "key_risks": ["risk1", "risk2"],
                "recommendations": ["rec1", "rec2"],
                "critical_clauses": ["clause1", "clause2"],
                "compliance_concerns": ["concern1", "concern2"]
            }
            """

        elif analysis_type == "compliance":
            return base_prompt + """
            Focus on GDPR and data protection compliance:
            1. Data processing activities identified
            2. Privacy compliance gaps
            3. Required GDPR clauses assessment
            4. Data subject rights considerations
            5. Recommendations for compliance improvement

            Format as JSON:
            {
                "data_processing": ["activity1", "activity2"],
                "compliance_gaps": ["gap1", "gap2"],
                "gdpr_clauses": ["clause1", "clause2"],
                "recommendations": ["rec1", "rec2"]
            }
            """

        elif analysis_type == "financial":
            return base_prompt + """
            Analyze financial aspects and implications:
            1. Financial commitments and obligations
            2. Payment terms and conditions
            3. Financial risk factors
            4. Cost implications
            5. Financial recommendations

            Format as JSON:
            {
                "financial_commitments": ["commitment1", "commitment2"],
                "payment_terms": ["term1", "term2"],
                "financial_risks": ["risk1", "risk2"],
                "recommendations": ["rec1", "rec2"]
            }
            """

        else:  # general analysis
            return base_prompt + """
            Provide a comprehensive general analysis including:
            1. Contract type and purpose
            2. Key parties and their roles
            3. Major obligations and rights
            4. Important terms and conditions
            5. Potential areas of concern
            6. Overall assessment

            Format as JSON:
            {
                "contract_type": "string",
                "key_parties": ["party1", "party2"],
                "major_obligations": ["obligation1", "obligation2"],
                "important_terms": ["term1", "term2"],
                "areas_of_concern": ["concern1", "concern2"],
                "overall_assessment": "string"
            }
            """

    def _create_chat_prompt(self, message: str, contract_context: Optional[str]) -> str:
        """Create chat prompt with context"""

        if contract_context:
            return f"""
            You are a legal contract analysis assistant. Use the following contract context to help answer the user's question.

            Contract Context:
            {contract_context[:8000]}

            User Question: {message}

            Please provide:
            1. A direct answer to the question
            2. Relevant contract clauses or sections that support your answer
            3. Any additional considerations or caveats
            4. Suggested follow-up questions if appropriate

            Format as JSON:
            {{
                "answer": "string",
                "relevant_clauses": ["clause1", "clause2"],
                "additional_considerations": ["consideration1", "consideration2"],
                "follow_up_questions": ["question1", "question2"]
            }}
            """
        else:
            return f"""
            You are a legal contract analysis assistant. Answer the user's question about contracts and legal matters.

            User Question: {message}

            Provide a helpful, accurate response about contract law and analysis.
            """

    def _parse_analysis_response(self, response: Any, contract_text: str) -> GeminiAnalysisResult:
        """Parse Gemini analysis response into structured format"""

        try:
            # Extract text from response
            response_text = response.text if hasattr(response, 'text') else str(response)

            # Try to parse as JSON first
            try:
                parsed_data = json.loads(response_text)
            except json.JSONDecodeError:
                # If not JSON, create structured response from text
                parsed_data = self._extract_insights_from_text(response_text)

            # Extract key components
            summary = parsed_data.get('overall_assessment', parsed_data.get('summary', 'Analysis completed'))
            key_terms = parsed_data.get('important_terms', parsed_data.get('key_terms', []))
            risk_factors = parsed_data.get('key_risks', parsed_data.get('risk_factors', []))
            recommendations = parsed_data.get('recommendations', [])

            # Calculate confidence based on response completeness
            confidence_score = min(len(parsed_data) / 10, 1.0)

            return GeminiAnalysisResult(
                summary=summary,
                key_terms=key_terms if isinstance(key_terms, list) else [key_terms],
                risk_factors=risk_factors if isinstance(risk_factors, list) else [risk_factors],
                recommendations=recommendations if isinstance(recommendations, list) else [recommendations],
                confidence_score=confidence_score,
                raw_response=parsed_data
            )

        except Exception as e:
            logger.error(f"Error parsing Gemini response: {e}")
            return GeminiAnalysisResult(
                summary="Analysis completed with limited structure",
                key_terms=[],
                risk_factors=["Unable to parse detailed risks"],
                recommendations=["Review analysis manually"],
                confidence_score=0.3,
                raw_response={"error": str(e), "raw_text": str(response)}
            )

    def _parse_chat_response(self, response: Any) -> GeminiChatResponse:
        """Parse Gemini chat response"""

        try:
            response_text = response.text if hasattr(response, 'text') else str(response)

            # Try to parse as JSON
            try:
                parsed_data = json.loads(response_text)
                return GeminiChatResponse(
                    response=parsed_data.get('answer', response_text),
                    suggestions=parsed_data.get('additional_considerations', []),
                    follow_up_questions=parsed_data.get('follow_up_questions', [])
                )
            except json.JSONDecodeError:
                # Return as plain text response
                return GeminiChatResponse(
                    response=response_text,
                    suggestions=[],
                    follow_up_questions=[]
                )

        except Exception as e:
            logger.error(f"Error parsing chat response: {e}")
            return GeminiChatResponse(
                response="Sorry, I encountered an error processing your request.",
                suggestions=[],
                follow_up_questions=[]
            )

    def _extract_insights_from_text(self, text: str) -> Dict[str, Any]:
        """Extract structured insights from plain text response"""

        # Simple extraction logic - can be enhanced with better NLP
        lines = text.split('\n')
        insights = {
            "summary": text[:500] + "..." if len(text) > 500 else text,
            "key_terms": [],
            "risk_factors": [],
            "recommendations": []
        }

        # Basic keyword extraction
        risk_keywords = ["risk", "concern", "issue", "problem", "critical", "warning"]
        rec_keywords = ["recommend", "suggest", "consider", "should", "advise"]

        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in risk_keywords):
                insights["risk_factors"].append(line.strip())
            elif any(keyword in line_lower for keyword in rec_keywords):
                insights["recommendations"].append(line.strip())

        return insights


# Global instance
gemini_service = GeminiService()
