from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from guardrails.prompt_analyzer import PromptAnalyzer
from guardrails.adversarial_detector import AdversarialDetector
from guardrails.policy_engine import PolicyEngine
from llm_gateway.groq_client import GroqClient
from logging.security_logger import SecurityLogger
from config import Config
from session_manager import SessionManager

app = Flask(__name__)
CORS(app)

# Initialize components
config = Config()
security_logger = SecurityLogger()
session_manager = SessionManager()
prompt_analyzer = PromptAnalyzer()
adversarial_detector = AdversarialDetector()
policy_engine = PolicyEngine()
groq_client = GroqClient(config.GROQ_API_KEY)

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('../frontend', filename)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = request.headers.get('X-Session-ID', 'anonymous')
        client_ip = request.remote_addr
        
        # Log user interaction
        security_logger.log_user_interaction(client_ip, session_id, message)
        
        # Security checks
        if not prompt_analyzer.is_safe(message):
            security_logger.log_security_violation(client_ip, 'PROMPT_INJECTION', message)
            return jsonify({'response': "I'm sorry, but I can't process that request."})
        
        if adversarial_detector.detect_attack(message):
            security_logger.log_security_violation(client_ip, 'ADVERSARIAL_ATTACK', message)
            return jsonify({'response': "I'm sorry, but I can't process that request."})
        
        if not policy_engine.check_policy(message, session_id):
            security_logger.log_security_violation(client_ip, 'POLICY_VIOLATION', message)
            return jsonify({'response': "I'm sorry, but I can't process that request."})
        
        # Get AI response
        response = groq_client.get_response(message)
        
        # Update session
        session_manager.update_session(session_id, message, response)
        
        # Log successful interaction
        security_logger.log_successful_interaction(client_ip, session_id, len(response))
        
        return jsonify({'response': response})
        
    except Exception as e:
        security_logger.log_error(str(e))
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)