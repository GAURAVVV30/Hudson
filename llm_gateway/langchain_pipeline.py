from llm_gateway.groq_client import GroqClient
from typing import List, Dict, Any

class LangChainPipeline:
    def __init__(self, groq_client: GroqClient):
        self.groq_client = groq_client
        self.conversation_memory = []
    
    def process_message(self, message: str, context: Dict[str, Any] = None) -> str:
        """Process message through LangChain pipeline"""
        # Add context-aware processing
        enhanced_message = self._enhance_with_context(message, context)
        
        # Get response from Groq
        response = self.groq_client.get_response(enhanced_message)
        
        # Store in conversation memory
        self._update_memory(message, response)
        
        return response
    
    def _enhance_with_context(self, message: str, context: Dict[str, Any]) -> str:
        """Enhance message with context"""
        if not context:
            return message
        
        # Add relevant context to message
        if context.get('user_history'):
            return f"Context: Previous conversation topics. Current message: {message}"
        
        return message
    
    def _update_memory(self, message: str, response: str):
        """Update conversation memory"""
        self.conversation_memory.append({
            'message': message[:100],  # Truncate for privacy
            'response_length': len(response)
        })
        
        # Keep only last 5 interactions
        if len(self.conversation_memory) > 5:
            self.conversation_memory = self.conversation_memory[-5:]
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get conversation summary"""
        return {
            'total_interactions': len(self.conversation_memory),
            'recent_topics': [item['message'] for item in self.conversation_memory[-3:]]
        }