"""
Security module for detecting and handling malicious or jailbreak attempts.
Validates user input and protects the chatbot from exploitation.
"""

import re
import logging
from typing import Tuple, Optional
from src.config.system_prompt import (
    JAILBREAK_KEYWORDS,
    SUSPICIOUS_PATTERNS,
    OUTSIDE_SCOPE_TOPICS,
    SAFETY_RESPONSES
)

logger = logging.getLogger(__name__)


class SecurityValidator:
    """Validates queries for security threats and jailbreak attempts."""
    
    def __init__(self):
        """Initialize security validator with compiled regex patterns."""
        self.jailbreak_keywords = [kw.lower() for kw in JAILBREAK_KEYWORDS]
        self.suspicious_patterns = [re.compile(pattern) for pattern in SUSPICIOUS_PATTERNS]
        self.outside_scope_topics = [topic.lower() for topic in OUTSIDE_SCOPE_TOPICS]
    
    def validate_query(self, query: str) -> Tuple[bool, Optional[str]]:
        """
        Validate user query for security threats.
        
        Args:
            query (str): User query to validate
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, threat_description)
                - is_valid: True if query is safe, False if threat detected
                - threat_description: Description of threat if detected, None otherwise
        """
        if not query or not isinstance(query, str):
            return False, "Invalid query format"
        
        query_lower = query.lower().strip()
        
        # Check for empty query
        if len(query_lower) < 2:
            return False, "Query too short"
        
        # Check for jailbreak keywords
        for keyword in self.jailbreak_keywords:
            if keyword in query_lower:
                logger.warning(f"Jailbreak attempt detected: keyword '{keyword}' found in query")
                return False, "jailbreak_detected"
        
        # Check for suspicious patterns
        for pattern in self.suspicious_patterns:
            if pattern.search(query):
                logger.warning(f"Suspicious pattern detected in query: {pattern.pattern}")
                return False, "suspicious_pattern_detected"
        
        # Check for outside scope topics
        for topic in self.outside_scope_topics:
            if topic in query_lower:
                logger.info(f"Query about outside scope topic: {topic}")
                return False, "outside_scope"
        
        # If all checks pass, query is valid
        return True, None
    
    def is_jailbreak_attempt(self, query: str) -> bool:
        """Quick check if query is a jailbreak attempt."""
        is_valid, threat_type = self.validate_query(query)
        return not is_valid and threat_type == "jailbreak_detected"
    
    def is_suspicious(self, query: str) -> bool:
        """Quick check if query has suspicious patterns."""
        is_valid, threat_type = self.validate_query(query)
        return not is_valid and threat_type == "suspicious_pattern_detected"
    
    def is_outside_scope(self, query: str) -> bool:
        """Quick check if query is outside chatbot's scope."""
        is_valid, threat_type = self.validate_query(query)
        return not is_valid and threat_type == "outside_scope"
    
    def get_safety_response(self, threat_type: Optional[str]) -> str:
        """
        Get appropriate safety response for threat type.
        
        Args:
            threat_type (str): Type of threat detected
            
        Returns:
            str: Safe response to send to user
        """
        if threat_type in SAFETY_RESPONSES:
            return SAFETY_RESPONSES[threat_type]
        
        return SAFETY_RESPONSES.get("outside_scope", "I'm here to help with Nintendo support!")
    
    def sanitize_query(self, query: str) -> str:
        """
        Clean up query while preserving meaning.
        
        Args:
            query (str): Raw user query
            
        Returns:
            str: Sanitized query
        """
        # Remove excessive whitespace
        query = re.sub(r'\s+', ' ', query).strip()
        
        # Remove any dangerous characters but keep safe punctuation
        safe_chars = re.sub(r'[^a-zA-Z0-9\s\?\!\.\,\-\(\)&]', '', query)
        
        return safe_chars.strip()


def validate_and_sanitize(query: str) -> Tuple[bool, str]:
    """
    Convenience function to validate and sanitize a query.
    
    Args:
        query (str): User query to process
        
    Returns:
        Tuple[bool, str]: (is_valid, processed_query)
            - is_valid: True if query passed security validation
            - processed_query: Sanitized query if valid, or safety response if invalid
    """
    validator = SecurityValidator()
    is_valid, threat_type = validator.validate_query(query)
    
    if not is_valid:
        safety_response = validator.get_safety_response(threat_type)
        logger.warning(f"Query blocked due to: {threat_type}")
        return False, safety_response
    
    sanitized_query = validator.sanitize_query(query)
    return True, sanitized_query
