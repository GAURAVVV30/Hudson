import json
import subprocess
import time
from typing import Optional

class GroqClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"
        self.max_tokens = 500
        self.temperature = 0.7
    
    def get_response(self, message: str, system_prompt: str = None) -> str:
        """Get response from Groq API"""
        try:
            start_time = time.time()
            
            # Prepare system prompt
            if not system_prompt:
                system_prompt = "You are Hudson, a helpful AI assistant. Provide natural, conversational responses."
            
            # Prepare payload
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            # Make API call using curl
            curl_cmd = [
                'curl', '-s', '-X', 'POST',
                self.base_url,
                '-H', f'Authorization: Bearer {self.api_key}',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps(payload)
            ]
            
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
            response_time = int((time.time() - start_time) * 1000)
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    response_data = json.loads(result.stdout)
                    
                    if 'choices' in response_data and len(response_data['choices']) > 0:
                        content = response_data['choices'][0]['message']['content']
                        return self._sanitize_response(content)
                    
                    elif 'error' in response_data:
                        error_msg = response_data['error'].get('message', 'Unknown error')
                        return f"I'm having trouble with the AI service: {error_msg}"
                
                except json.JSONDecodeError:
                    return "I received an invalid response from the AI service."
            
            return "I'm having trouble connecting to the AI service right now."
            
        except subprocess.TimeoutExpired:
            return "The AI service is taking too long to respond. Please try again."
        except Exception as e:
            return "I'm having trouble connecting to the AI service right now."
    
    def _sanitize_response(self, response: str) -> str:
        """Sanitize AI response to ensure safety"""
        # Remove any potential harmful content
        sanitized = response.strip()
        
        # Check for system information leakage
        forbidden_phrases = [
            'system prompt',
            'internal instructions',
            'my training',
            'my guidelines',
            'i am programmed',
            'my creators',
            'openai',
            'anthropic'
        ]
        
        response_lower = sanitized.lower()
        for phrase in forbidden_phrases:
            if phrase in response_lower:
                return "I'd be happy to help you with that topic. What specific aspect interests you?"
        
        # Ensure response doesn't contain harmful instructions
        if self._contains_harmful_content(sanitized):
            return "I can't provide information that could be harmful. Is there something else I can help you with?"
        
        return sanitized
    
    def _contains_harmful_content(self, response: str) -> bool:
        """Check if response contains harmful content"""
        harmful_patterns = [
            r'(?i)how to (hack|crack|exploit)',
            r'(?i)(create|make|build).*(malware|virus|trojan)',
            r'(?i)(bypass|circumvent).*(security|authentication)',
            r'(?i)(illegal|unlawful|criminal) (activity|action)'
        ]
        
        import re
        for pattern in harmful_patterns:
            if re.search(pattern, response):
                return True
        
        return False
    
    def test_connection(self) -> bool:
        """Test connection to Groq API"""
        try:
            test_response = self.get_response("Hello")
            return len(test_response) > 0 and "trouble connecting" not in test_response
        except:
            return False
    
    def get_model_info(self) -> dict:
        """Get information about the current model"""
        return {
            'model': self.model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'provider': 'Groq'
        }