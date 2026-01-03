import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import Config
from llm_gateway.groq_client import GroqClient
from guardrails.prompt_analyzer import PromptAnalyzer
from guardrails.policy_engine import PolicyEngine

class TestNormalChat(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.analyzer = PromptAnalyzer()
        self.policy_engine = PolicyEngine()
        # Note: GroqClient requires actual API key for testing
    
    def test_normal_conversation_flow(self):
        """Test normal conversation flow"""
        normal_messages = [
            "Hello, how are you?",
            "What is machine learning?",
            "Can you explain blockchain?",
            "How does encryption work?",
            "What are the benefits of AI?"
        ]
        
        for message in normal_messages:
            with self.subTest(message=message):
                # Should pass security checks
                self.assertTrue(self.analyzer.is_safe(message))
                self.assertTrue(self.policy_engine.check_policy(message, "test_session", "127.0.0.1"))
    
    def test_educational_security_questions(self):
        """Test that educational security questions are allowed"""
        educational_questions = [
            "What is cybersecurity?",
            "How does penetration testing work?",
            "What are common security vulnerabilities?",
            "Explain how firewalls protect networks",
            "What is ethical hacking?"
        ]
        
        for question in educational_questions:
            with self.subTest(question=question):
                self.assertTrue(self.analyzer.is_safe(question))
    
    def test_message_length_limits(self):
        """Test message length limits"""
        # Normal length message
        normal_message = "This is a normal length message"
        self.assertTrue(self.analyzer.is_safe(normal_message))
        
        # Very long message
        long_message = "A" * 1001
        self.assertFalse(self.analyzer.is_safe(long_message))
    
    def test_policy_compliance(self):
        """Test policy compliance for normal usage"""
        test_ip = "192.168.1.100"
        test_session = "test_session_123"
        
        # Normal message should pass policy
        normal_message = "Hello, can you help me?"
        self.assertTrue(self.policy_engine.check_policy(normal_message, test_session, test_ip))
        
        # Check rate limiting doesn't affect single request
        self.assertTrue(self.policy_engine._check_rate_limit(test_ip))
    
    def test_conversation_context(self):
        """Test conversation context handling"""
        messages = [
            "What is Python?",
            "Can you give me an example?",
            "How do I install it?",
            "What about libraries?"
        ]
        
        for i, message in enumerate(messages):
            with self.subTest(message=message, turn=i):
                self.assertTrue(self.analyzer.is_safe(message))
    
    def test_multilingual_support(self):
        """Test basic multilingual message handling"""
        multilingual_messages = [
            "Hola, ¿cómo estás?",  # Spanish
            "Bonjour, comment allez-vous?",  # French
            "Guten Tag, wie geht es Ihnen?",  # German
        ]
        
        for message in multilingual_messages:
            with self.subTest(message=message):
                # Should not be flagged as malicious
                self.assertTrue(self.analyzer.is_safe(message))

if __name__ == '__main__':
    unittest.main()