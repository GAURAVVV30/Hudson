import re
import string
from typing import Dict, List

class AdversarialDetector:
    def __init__(self):
        self.evasion_patterns = [
            # Encoding evasion
            r'\\x[0-9a-fA-F]{2}',  # Hex encoding
            r'\\u[0-9a-fA-F]{4}',  # Unicode encoding
            r'%[0-9a-fA-F]{2}',    # URL encoding
            r'&#x?[0-9a-fA-F]+;',  # HTML entities
            
            # Character substitution
            r'[^\w\s]{3,}',        # Excessive special characters
            r'(.)\1{5,}',          # Repeated characters
        ]
        
        self.adversarial_indicators = [
            'base64',
            'decode',
            'encode',
            'rot13',
            'cipher',
            'obfuscate',
            'unicode',
            'ascii'
        ]
    
    def detect_attack(self, message: str) -> bool:
        """Detect adversarial attacks in message"""
        return (
            self._detect_encoding_evasion(message) or
            self._detect_character_manipulation(message) or
            self._detect_obfuscation(message) or
            self._detect_payload_injection(message)
        )
    
    def _detect_encoding_evasion(self, message: str) -> bool:
        """Detect encoding-based evasion attempts"""
        for pattern in self.evasion_patterns:
            if re.search(pattern, message):
                return True
        
        # Check for excessive URL encoding
        url_encoded_chars = len(re.findall(r'%[0-9a-fA-F]{2}', message))
        if url_encoded_chars > 3:
            return True
        
        # Check for HTML entity abuse
        html_entities = len(re.findall(r'&#x?[0-9a-fA-F]+;', message))
        if html_entities > 2:
            return True
        
        return False
    
    def _detect_character_manipulation(self, message: str) -> bool:
        """Detect character-based manipulation"""
        # Check special character ratio
        special_chars = sum(1 for c in message if c in string.punctuation)
        if len(message) > 0 and special_chars / len(message) > 0.4:
            return True
        
        # Check for excessive whitespace manipulation
        whitespace_chars = sum(1 for c in message if c.isspace())
        if len(message) > 0 and whitespace_chars / len(message) > 0.3:
            return True
        
        # Check for repeated character patterns
        if re.search(r'(.)\1{10,}', message):
            return True
        
        return False
    
    def _detect_obfuscation(self, message: str) -> bool:
        """Detect obfuscation attempts"""
        message_lower = message.lower()
        
        # Check for obfuscation keywords
        obfuscation_count = sum(1 for indicator in self.adversarial_indicators 
                               if indicator in message_lower)
        if obfuscation_count >= 2:
            return True
        
        # Check for leetspeak patterns
        leetspeak_patterns = [
            r'[4@]dm[1i]n',
            r'[5$]y[5$]t[3e]m',
            r'[8b]yp[4@][5$][5$]',
            r'[0o]v[3e]rr[1i]d[3e]'
        ]
        
        for pattern in leetspeak_patterns:
            if re.search(pattern, message_lower):
                return True
        
        return False
    
    def _detect_payload_injection(self, message: str) -> bool:
        """Detect payload injection attempts"""
        # Check for script-like patterns
        script_patterns = [
            r'<script[^>]*>',
            r'javascript:',
            r'eval\s*\(',
            r'exec\s*\(',
            r'system\s*\(',
            r'shell_exec\s*\('
        ]
        
        for pattern in script_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        
        # Check for SQL injection patterns
        sql_patterns = [
            r'union\s+select',
            r'drop\s+table',
            r'insert\s+into',
            r'delete\s+from',
            r'update\s+set'
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        
        return False
    
    def get_attack_type(self, message: str) -> List[str]:
        """Identify types of attacks detected"""
        attack_types = []
        
        if self._detect_encoding_evasion(message):
            attack_types.append("ENCODING_EVASION")
        
        if self._detect_character_manipulation(message):
            attack_types.append("CHARACTER_MANIPULATION")
        
        if self._detect_obfuscation(message):
            attack_types.append("OBFUSCATION")
        
        if self._detect_payload_injection(message):
            attack_types.append("PAYLOAD_INJECTION")
        
        return attack_types