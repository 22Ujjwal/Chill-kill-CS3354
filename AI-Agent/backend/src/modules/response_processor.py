"""
Response processor for improving chatbot response quality.
Enhances formatting, tone, and overall helpfulness of responses.
"""

import re
import logging
from typing import Dict, Any, Optional
from src.config.system_prompt import RESPONSE_TEMPLATES

logger = logging.getLogger(__name__)


class ResponseProcessor:
    """Processes and enhances chatbot responses for better quality."""
    
    def __init__(self):
        """Initialize response processor."""
        self.templates = RESPONSE_TEMPLATES
    
    def process_response(
        self,
        response: str,
        query: str = "",
        context_docs: int = 0,
        conversation_turn: int = 1
    ) -> str:
        """
        Process and enhance a chatbot response.
        
        Args:
            response (str): Raw LLM response
            query (str): Original user query
            context_docs (int): Number of context documents retrieved
            conversation_turn (int): Which turn in conversation this is
            
        Returns:
            str: Enhanced response (concise and friendly)
        """
        if not response:
            return "Sorry, I couldn't generate a response. Try again! 🎮"
        
        # Clean up the response
        response = self._clean_response(response)
        
        # Truncate to reasonable length (max 500 chars for conciseness)
        response = self._truncate_response(response, max_length=500)
        
        # Enhance formatting
        response = self._improve_formatting(response)
        
        # Add personality
        response = self._add_personality(response, conversation_turn)
        
        # Ensure proper ending
        response = self._ensure_proper_ending(response)
        
        return response.strip()
    
    def _clean_response(self, response: str) -> str:
        """Remove artifacts and clean up response text."""
        # Remove markdown code blocks if present
        response = re.sub(r'```.*?```', '', response, flags=re.DOTALL)
        
        # Remove excessive newlines
        response = re.sub(r'\n\n\n+', '\n\n', response)
        
        # Remove leading/trailing whitespace
        response = response.strip()
        
        return response
    
    def _truncate_response(self, response: str, max_length: int = 500) -> str:
        """
        Truncate response to a reasonable length.
        Keeps it under max_length characters while preserving complete sentences.
        """
        if len(response) <= max_length:
            return response
        
        # Find last sentence ending before max_length
        truncated = response[:max_length]
        
        # Try to end at a sentence boundary
        last_period = truncated.rfind('.')
        last_newline = truncated.rfind('\n')
        
        # Use whichever is closer to the end
        last_boundary = max(last_period, last_newline)
        
        if last_boundary > max_length * 0.7:  # Only use boundary if it's reasonably far
            truncated = response[:last_boundary + 1]
        else:
            truncated = truncated + "..."
        
        return truncated.strip()
    
    def _improve_formatting(self, response: str) -> str:
        """Improve response formatting and readability."""
        # Convert markdown bold to more casual style
        response = re.sub(r'\*\*(.*?)\*\*', r'\1', response)
        response = re.sub(r'__(.*?)__', r'\1', response)
        
        # Ensure bullet points are clean
        response = re.sub(r'^\s*[\*\-]\s+', '• ', response, flags=re.MULTILINE)
        
        # Add proper spacing around lists
        response = re.sub(r'(\n•.*?)\n(?!\n|•)', r'\1\n', response)
        
        # Ensure numbers in lists are formatted properly
        response = re.sub(r'^\s*(\d+)\.\s+', r'\1. ', response, flags=re.MULTILINE)
        
        return response
    
    def _add_personality(self, response: str, turn: int) -> str:
        """Add friendly personality to response."""
        # Keep responses short and snappy
        # Only add emoji if it contains Nintendo-related words
        if any(word in response.lower() for word in ["switch", "game", "play", "nintendo", "pokemon"]):
            if "🎮" not in response:
                response += " 🎮"
        
        return response
    
    def _ensure_proper_ending(self, response: str) -> str:
        """Ensure response ends properly."""
        response = response.strip()
        
        # Ensure ends with punctuation
        if response and response[-1] not in ".!?":
            response += "."
        
        return response
    
    def _validate_and_fix_response(self, response: str) -> str:
        """Validate and fix common response issues."""
        # Check for incomplete sentences
        if response.endswith(("that", "the", "and", "or", "but", "a", "an", "...")):
            # Already truncated, so just return as is
            return response
        
        # Fix double punctuation
        response = re.sub(r'([.!?])\1+', r'\1', response)
        
        # Fix spacing around punctuation
        response = re.sub(r'\s+([.,!?])', r'\1', response)
        response = re.sub(r'([.,!?])([^ ])', r'\1 \2', response)
        
        return response
    
    def format_for_api(self, response: str, context_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format response for API return.
        
        Args:
            response (str): Processed response text
            context_info (Dict): Additional context information
            
        Returns:
            Dict: Formatted response object
        """
        return {
            "status": "success",
            "response": response,
            "context_documents_count": context_info.get("doc_count", 0),
            "context_length": context_info.get("context_length", 0),
            "confidence": context_info.get("confidence", 0.8),
            "helpful": None,  # User can rate this later
            "timestamp": context_info.get("timestamp", ""),
            "turn": context_info.get("turn", 1)
        }


def enhance_response(
    response: str,
    query: str = "",
    context_docs: int = 0,
    turn: int = 1
) -> str:
    """
    Convenience function to enhance response quality.
    
    Args:
        response (str): Raw response from LLM
        query (str): User's original query
        context_docs (int): Number of context documents used
        turn (int): Conversation turn number
        
    Returns:
        str: Enhanced response
    """
    processor = ResponseProcessor()
    return processor.process_response(response, query, context_docs, turn)


def is_response_quality_good(response: str) -> bool:
    """
    Quick quality check for response.
    
    Args:
        response (str): Response to check
        
    Returns:
        bool: True if response meets quality standards
    """
    if not response:
        return False
    
    # Check minimum length (shouldn't be too short)
    if len(response.strip()) < 10:
        return False
    
    # Check for incomplete sentences
    if response.strip().endswith(("the", "and", "or", "a", "an")):
        return False
    
    # Check for too many placeholder text
    if "[" in response and "]" in response:
        bracket_count = response.count("[")
        if bracket_count > 2:
            return False
    
    return True
