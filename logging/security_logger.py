import logging
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any

class SecurityLogger:
    def __init__(self):
        self.setup_loggers()
    
    def setup_loggers(self):
        """Setup security and audit loggers"""
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # Setup audit logger
        self.audit_logger = logging.getLogger('hudson_audit')
        self.audit_logger.setLevel(logging.INFO)
        
        audit_handler = logging.FileHandler('logs/hudson_audit.log')
        audit_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        audit_handler.setFormatter(audit_formatter)
        self.audit_logger.addHandler(audit_handler)
        
        # Setup security logger
        self.security_logger = logging.getLogger('hudson_security')
        self.security_logger.setLevel(logging.WARNING)
        
        security_handler = logging.FileHandler('logs/hudson_security.log')
        security_formatter = logging.Formatter(
            '%(asctime)s | SECURITY_ALERT | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        security_handler.setFormatter(security_formatter)
        self.security_logger.addHandler(security_handler)
        
        # Setup error logger
        self.error_logger = logging.getLogger('hudson_errors')
        self.error_logger.setLevel(logging.ERROR)
        
        error_handler = logging.FileHandler('logs/hudson_errors.log')
        error_formatter = logging.Formatter(
            '%(asctime)s | ERROR | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        error_handler.setFormatter(error_formatter)
        self.error_logger.addHandler(error_handler)
        
        # Log system startup
        self.audit_logger.info("Hudson Security Logger initialized")
    
    def log_user_interaction(self, client_ip: str, session_id: str, message: str):
        """Log user interaction"""
        message_hash = hashlib.sha256(message.encode()).hexdigest()[:16]
        self.audit_logger.info(
            f"USER_INTERACTION | IP: {client_ip} | SESSION: {session_id} | "
            f"MSG_HASH: {message_hash} | MSG_LEN: {len(message)}"
        )
    
    def log_security_violation(self, client_ip: str, violation_type: str, message: str):
        """Log security violation"""
        message_hash = hashlib.sha256(message.encode()).hexdigest()[:16]
        message_sample = message[:50].replace('\n', ' ').replace('\r', ' ')
        
        self.security_logger.warning(
            f"VIOLATION: {violation_type} | IP: {client_ip} | "
            f"MSG_HASH: {message_hash} | SAMPLE: {message_sample}..."
        )
    
    def log_successful_interaction(self, client_ip: str, session_id: str, response_length: int):
        """Log successful interaction"""
        self.audit_logger.info(
            f"SUCCESS | IP: {client_ip} | SESSION: {session_id} | "
            f"RESP_LEN: {response_length}"
        )
    
    def log_api_call(self, success: bool, response_time: int = 0, error: str = None):
        """Log API call to LLM"""
        if success:
            self.audit_logger.info(f"API_CALL | SUCCESS | RESPONSE_TIME: {response_time}ms")
        else:
            self.audit_logger.error(f"API_CALL | FAILED | ERROR: {error}")
    
    def log_rate_limit_exceeded(self, client_ip: str, limit_type: str):
        """Log rate limit exceeded"""
        self.security_logger.warning(
            f"RATE_LIMIT_EXCEEDED | IP: {client_ip} | TYPE: {limit_type}"
        )
    
    def log_policy_violation(self, client_ip: str, policy_type: str, details: str):
        """Log policy violation"""
        self.security_logger.warning(
            f"POLICY_VIOLATION | IP: {client_ip} | TYPE: {policy_type} | DETAILS: {details}"
        )
    
    def log_system_event(self, event_type: str, details: Dict[str, Any]):
        """Log system event"""
        details_str = json.dumps(details, separators=(',', ':'))
        self.audit_logger.info(f"SYSTEM_EVENT | TYPE: {event_type} | DETAILS: {details_str}")
    
    def log_error(self, error_message: str, error_type: str = "GENERAL"):
        """Log error"""
        self.error_logger.error(f"TYPE: {error_type} | MESSAGE: {error_message}")
    
    def log_session_created(self, client_ip: str, session_id: str):
        """Log session creation"""
        self.audit_logger.info(f"SESSION_CREATED | IP: {client_ip} | SESSION: {session_id}")
    
    def log_session_expired(self, session_id: str):
        """Log session expiration"""
        self.audit_logger.info(f"SESSION_EXPIRED | SESSION: {session_id}")
    
    def log_ip_blocked(self, client_ip: str, reason: str):
        """Log IP blocking"""
        self.security_logger.warning(f"IP_BLOCKED | IP: {client_ip} | REASON: {reason}")
    
    def log_suspicious_activity(self, client_ip: str, activity_type: str, details: str):
        """Log suspicious activity"""
        self.security_logger.warning(
            f"SUSPICIOUS_ACTIVITY | IP: {client_ip} | TYPE: {activity_type} | DETAILS: {details}"
        )
    
    def get_log_stats(self) -> Dict[str, int]:
        """Get logging statistics"""
        stats = {
            'total_interactions': 0,
            'security_violations': 0,
            'errors': 0,
            'blocked_ips': 0
        }
        
        try:
            # Count lines in each log file
            for log_file, stat_key in [
                ('logs/hudson_audit.log', 'total_interactions'),
                ('logs/hudson_security.log', 'security_violations'),
                ('logs/hudson_errors.log', 'errors')
            ]:
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        stats[stat_key] = sum(1 for line in f)
        except Exception as e:
            self.log_error(f"Error getting log stats: {e}")
        
        return stats