**Secure AI Assistant (Hudson)**

A security-first conversational AI assistant designed to safely handle user interactions by enforcing guardrails, policy controls, and audit logging before any request reaches the language model.

The project focuses on defending against prompt injection, role abuse, and adversarial inputs, while still allowing legitimate cybersecurity and educational queries.

**Overview**

Hudson is built using an enterprise-style modular architecture.
It provides a modern, full-screen Gemini-inspired web interface while internally applying zero-trust principles to AI prompt handling.

All user input is treated as untrusted and must pass security validation before being processed by the model.

**Key Capabilities**

Prompt injection and jailbreak prevention

Adversarial and obfuscation-based attack detection

Role-based policy enforcement and rate limiting

Secure session handling

Enterprise-grade audit logging

Gemini-inspired full-screen UI

Real AI responses powered by Groq using Llama 3.1

**Repository Structure**
<img width="564" height="622" alt="image" src="https://github.com/user-attachments/assets/1f61b046-65a7-439e-8584-f9687d747c04" />


**Architecture Overview**
User Interface
      ↓
Backend API (Flask)
      ↓
Guardrails & Policy Engine
      ↓ (validated only)
LLM Gateway (Groq)
      ↓
Sanitized AI Response


The language model is never exposed directly to user input.

**Audit Logging**
All security-relevant events are logged for monitoring and compliance:
Attack classification
Policy decision (ALLOW / BLOCK)
ession-level traceability
imestamped forensic records
aw user prompts are never stored.

**How to Run the Project**

**Prerequisites**

Python 3.9+
pip
Valid Groq API key

Modern web browser

**STEPS**
1. Clone the Repository
git clone https://github.com/<your-username>/secure-ai-assistant-hudson.git
cd secure-ai-assistant-hudson

2. Create and Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate   # Linux / macOS


(Windows: venv\Scripts\activate)

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file (or export variables):

GROQ_API_KEY=your_groq_api_key_here
FLASK_ENV=production


⚠️ Do not commit API keys to GitHub.

5. Start the Backend Server
python backend/app.py


Backend runs at:

http://127.0.0.1:5000

6. Launch the Frontend

Open the UI in your browser:

frontend/index.html


or

xdg-open frontend/index.html   # Linux
open frontend/index.html       # macOS

7. Verify Audit Logging

Interact with the chatbot and inspect logs:

logging/security.log


(or equivalent audit log file)

Blocked and allowed decisions should appear as structured entries.

8. Run Tests (Optional)
pytest


Validates:

Prompt injection detection

Adversarial filtering

Normal chat functionality

Design Philosophy

AI security is API security.
Every prompt is an attack surface.

This project applies defense-in-depth, least privilege, and secure-by-design principles to AI systems.
