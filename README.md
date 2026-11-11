# Dual-Engine LLM Judge & Cost-Latency Optimizer

A cloud-deployed FastAPI application that integrates two Large Language Model (LLM) providers — Google Gemini and Groq — with evaluation and Redis-based caching to explore cost, latency, and response optimization.

## Live Deployment

- **Live API:** https://dual-engine-llm-optimizer.onrender.com
- **Interactive API Documentation:** https://dual-engine-llm-optimizer.onrender.com/docs
- **Health Check:** https://dual-engine-llm-optimizer.onrender.com/health
- **GitHub Repository:** https://github.com/jannamvaishnav19/dual-engine-llm-optimizer

## Project Overview

The Dual-Engine LLM Optimizer is designed to work with multiple LLM providers through a unified API.

It integrates Gemini and Groq, provides an evaluation endpoint, and uses Redis caching to reduce repeated processing for eligible requests.

The project demonstrates backend development, API integration, cloud deployment, authentication, and caching.

## Key Features

- **Dual LLM Integration:** Supports Google Gemini and Groq.
- **Unified API:** Interact with different LLM providers through FastAPI.
- **LLM Evaluation:** Provides an evaluation endpoint for comparing model outputs.
- **Redis Caching:** Uses Redis to cache eligible repeated requests.
- **API Authentication:** Protects API access using an API key.
- **Cloud Deployment:** Deployed using Render.
- **Interactive Documentation:** Swagger UI documentation through FastAPI.
- **Docker Support:** Containerized application deployment.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| Google Gemini | LLM provider |
| Groq | LLM provider |
| Upstash Redis | Caching |
| Docker | Containerization |
| Render | Cloud deployment |
| Git & GitHub | Version control |

## System Architecture

Client Request  
↓  
FastAPI Backend  
↓  
API Authentication  
↓  
LLM Provider Selection  
↓  
Gemini / Groq  
↓  
Evaluation and Response Processing  
↓  
Redis Caching  
↓  
API Response

*The exact execution and caching sequence depends on the configured application workflow.*

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Service information |
| GET | `/health` | Health check |
| POST | `/api/v1/chat` | Submit LLM requests |
| POST | `/api/v1/evaluate` | Evaluate model responses |

## Testing & Verification

The deployed application has been tested for:

- FastAPI health-check response.
- Successful Gemini API requests.
- Successful Groq API requests.
- Evaluation endpoint response.
- Redis cache-hit behavior on repeated requests.

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/jannamvaishnav19/dual-engine-llm-optimizer.git
cd dual-engine-llm-optimizer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

Windows:
```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file locally using the variable names expected by your application:

```env
API_KEY=your_application_api_key
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
REDIS_URL=your_redis_tls_connection_url
```

Never commit your `.env` file or expose API credentials.

### 5. Run the application

Use the Uvicorn command specified by your project's application entry point.

### 6. Open API documentation

```text
http://localhost:8000/docs
```

## Deployment

The application is deployed on Render using a GitHub-connected Blueprint configuration.

External services:
- Google AI Studio for Gemini API access.
- Groq Cloud for Groq API access.
- Upstash for Redis caching.

## Security

- API-key-based authentication.
- Environment-based secret management.
- No API credentials should be committed to GitHub.
- TLS-enabled Redis connection.

## Future Improvements

- Advanced model benchmarking.
- Detailed cost and latency analytics.
- More LLM provider integrations.
- Improved caching strategies.
- Monitoring and performance dashboards.
- Automated evaluation and reporting.

## Author

Developed as a portfolio project demonstrating practical skills in Python backend engineering, LLM integration, API development, caching, and cloud deployment.

---

**Project Status:** Deployed and core API functionality tested.
