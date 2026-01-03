import time
import hashlib
from collections import defaultdict

class SessionManager:
    def __init__(self):
        self.sessions = defaultdict(dict)
        self.session_timestamps = {}
        self.message_counts = defaultdict(int)
    
    def create_session(self, session_id):
        """Create a new session"""
        self.sessions[session_id] = {
            'created_at': time.time(),
            'last_activity': time.time(),
            'message_count': 0,
            'conversation_history': []
        }
        self.session_timestamps[session_id] = time.time()
    
    def update_session(self, session_id, message, response):
        """Update session with new interaction"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        session = self.sessions[session_id]
        session['last_activity'] = time.time()
        session['message_count'] += 1
        session['conversation_history'].append({
            'timestamp': time.time(),
            'message': message[:100],  # Store only first 100 chars for privacy
            'response_length': len(response)
        })
        
        # Keep only last 10 interactions
        if len(session['conversation_history']) > 10:
            session['conversation_history'] = session['conversation_history'][-10:]
    
    def is_rate_limited(self, session_id, max_requests=10, window=60):
        """Check if session is rate limited"""
        current_time = time.time()
        
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        recent_messages = [
            msg for msg in session['conversation_history']
            if current_time - msg['timestamp'] < window
        ]
        
        return len(recent_messages) >= max_requests
    
    def cleanup_expired_sessions(self, timeout=3600):
        """Remove expired sessions"""
        current_time = time.time()
        expired_sessions = [
            sid for sid, timestamp in self.session_timestamps.items()
            if current_time - timestamp > timeout
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
            del self.session_timestamps[session_id]
    
    def get_session_stats(self, session_id):
        """Get session statistics"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        return {
            'message_count': session['message_count'],
            'duration': time.time() - session['created_at'],
            'last_activity': session['last_activity']
        }