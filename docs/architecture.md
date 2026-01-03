# Hudson Architecture

## Overview
Hudson is a secure AI chatbot gateway built with enterprise-grade security features and modular architecture.

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Frontend     │    │     Backend     │    │   LLM Gateway   │
│                 │    │                 │    │                 │
│  - HTML/CSS/JS  │◄──►│  - Flask API    │◄──►│  - Groq Client  │
│  - Gemini UI    │    │  - Session Mgmt │    │  - LangChain    │
│  - Chat Logic   │    │  - Config       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Guardrails    │
                       │                 │
                       │ - Prompt Analyzer│
                       │ - Adversarial Det│
                       │ - Policy Engine │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    Logging      │
                       │                 │
                       │ - Security Logs │
                       │ - Audit Trails  │
                       │ - Error Tracking│
                       └─────────────────┘
```

## Components

### Frontend Layer
- **Technology**: HTML5, CSS3, JavaScript
- **Design**: Gemini-inspired UI with Google color palette
- **Features**: Real-time chat, responsive design, smooth animations

### Backend Layer
- **Technology**: Flask, Python
- **Components**:
  - `app.py`: Main Flask application
  - `config.py`: Configuration management
  - `session_manager.py`: Session handling and rate limiting

### Guardrails Layer
- **Prompt Analyzer**: Detects prompt injection attempts
- **Adversarial Detector**: Identifies evasion and obfuscation attacks
- **Policy Engine**: Enforces rate limits and content policies

### LLM Gateway Layer
- **Groq Client**: Direct API integration with Groq
- **LangChain Pipeline**: Context-aware message processing

### Logging Layer
- **Security Logger**: Comprehensive audit and security logging
- **Log Files**: Separate logs for audit, security, and errors

## Security Features

### Multi-Layer Protection
1. **Input Validation**: Length and format checking
2. **Pattern Matching**: Regex-based attack detection
3. **Behavioral Analysis**: Suspicious activity monitoring
4. **Rate Limiting**: Request throttling per IP/session
5. **Content Filtering**: Policy-based content restrictions

### Audit & Compliance
- Complete audit trails for all interactions
- Security incident logging with anonymized data
- Performance monitoring and error tracking
- Session management with timeout handling

## Data Flow

1. **User Input** → Frontend validation
2. **API Request** → Backend receives and logs
3. **Security Check** → Guardrails analyze message
4. **Policy Check** → Rate limits and content policies
5. **LLM Processing** → Groq API call via gateway
6. **Response Filter** → Output sanitization
7. **Audit Log** → Complete interaction logging
8. **User Response** → Secure delivery to frontend

## Scalability

### Horizontal Scaling
- Stateless backend design
- Session data can be externalized
- Load balancer compatible

### Performance Optimization
- Async request handling
- Connection pooling for LLM API
- Efficient logging with rotation

### Monitoring
- Health check endpoints
- Performance metrics
- Security dashboards