import time
from typing import Dict, List
from collections import defaultdict

class PolicyEngine:
    def __init__(self):
        self.rate_limits = defaultdict(list)
        self.blocked_ips = set()
        self.session_limits = defaultdict(int)
        
        # Policy configurations
        self.MAX_REQUESTS_PER_MINUTE = 10
        self.MAX_REQUESTS_PER_HOUR = 100
        self.MAX_MESSAGE_LENGTH = 1000
        self.MAX_SESSIONS_PER_IP = 5
        self.BLOCKED_KEYWORDS = [
            'hack', 'crack', 'exploit', 'vulnerability',
            'malware', 'virus', 'trojan', 'backdoor'
        ]
    
    def check_policy(self, message: str, session_id: str, client_ip: str = None) -> bool:
        """Check if message complies with all policies"""
        return (
            self._check_rate_limit(client_ip) and
            self._check_message_length(message) and
            self._check_content_policy(message) and
            self._check_session_limit(client_ip) and
            not self._is_ip_blocked(client_ip)
        )
    
    def _check_rate_limit(self, client_ip: str) -> bool:
        """Check rate limiting policies"""
        if not client_ip:
            return True
        
        current_time = time.time()
        
        # Clean old entries
        self.rate_limits[client_ip] = [
            timestamp for timestamp in self.rate_limits[client_ip]
            if current_time - timestamp < 3600  # Keep last hour
        ]
        
        # Check per-minute limit
        recent_requests = [
            timestamp for timestamp in self.rate_limits[client_ip]
            if current_time - timestamp < 60
        ]
        
        if len(recent_requests) >= self.MAX_REQUESTS_PER_MINUTE:
            return False
        
        # Check per-hour limit
        if len(self.rate_limits[client_ip]) >= self.MAX_REQUESTS_PER_HOUR:
            return False
        
        # Add current request
        self.rate_limits[client_ip].append(current_time)
        return True
    
    def _check_message_length(self, message: str) -> bool:
        """Check message length policy"""
        return len(message) <= self.MAX_MESSAGE_LENGTH
    
    def _check_content_policy(self, message: str) -> bool:
        """Check content policy compliance"""
        message_lower = message.lower()
        
        # Check for blocked keywords in context
        blocked_count = 0
        for keyword in self.BLOCKED_KEYWORDS:
            if keyword in message_lower:
                blocked_count += 1
        
        # Allow educational questions but block if too many suspicious keywords
        if blocked_count >= 3:
            return False
        
        # Check for explicit harmful intent
        harmful_phrases = [
            'how to hack',
            'create malware',
            'exploit vulnerability',
            'bypass security',
            'crack password'
        ]
        
        for phrase in harmful_phrases:
            if phrase in message_lower:
                return False
        
        return True
    
    def _check_session_limit(self, client_ip: str) -> bool:
        """Check session limit per IP"""
        if not client_ip:
            return True
        
        return self.session_limits[client_ip] < self.MAX_SESSIONS_PER_IP
    
    def _is_ip_blocked(self, client_ip: str) -> bool:
        """Check if IP is blocked"""
        return client_ip in self.blocked_ips
    
    def block_ip(self, client_ip: str, reason: str = "Policy violation"):
        """Block an IP address"""
        self.blocked_ips.add(client_ip)
    
    def unblock_ip(self, client_ip: str):
        """Unblock an IP address"""
        self.blocked_ips.discard(client_ip)
    
    def increment_session_count(self, client_ip: str):
        """Increment session count for IP"""
        self.session_limits[client_ip] += 1
    
    def decrement_session_count(self, client_ip: str):
        """Decrement session count for IP"""
        if self.session_limits[client_ip] > 0:
            self.session_limits[client_ip] -= 1
    
    def get_policy_status(self, client_ip: str) -> Dict:
        """Get policy status for IP"""
        current_time = time.time()
        
        # Clean old entries
        if client_ip in self.rate_limits:
            self.rate_limits[client_ip] = [
                timestamp for timestamp in self.rate_limits[client_ip]
                if current_time - timestamp < 3600
            ]
        
        recent_requests = [
            timestamp for timestamp in self.rate_limits.get(client_ip, [])
            if current_time - timestamp < 60
        ]
        
        return {
            'requests_last_minute': len(recent_requests),
            'requests_last_hour': len(self.rate_limits.get(client_ip, [])),
            'active_sessions': self.session_limits.get(client_ip, 0),
            'is_blocked': client_ip in self.blocked_ips,
            'rate_limit_remaining': max(0, self.MAX_REQUESTS_PER_MINUTE - len(recent_requests))
        }