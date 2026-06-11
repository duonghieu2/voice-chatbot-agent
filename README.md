# Voice Chatbot Agent for Ride-Hailing & Food Delivery (E2E Prototype)

Welcome to the **Voice Chatbot Agent** project, a premium end-to-end prototype designed for simulating, validating, and demonstrating voice-based customer support interactions in Ride-Hailing (Đặt xe) and Food Delivery (Đặt đồ ăn) domains.

This codebase integrates a complete **E2E Voice Pipeline**:
1. **Audio Input**: Live microphone recording or file upload via a premium Web UI.
2. **ASR (Speech-to-Text)**: Local Whisper Tiny/Large inference with Vietnamese accent and error normalization.
3. **LLM Chatbot Agent & Tool Calling**: Gemini 3.1 Flash-Lite with 2-Stage native tool calling.
4. **Backend Mock Database**: In-memory database with state isolation.
5. **Text-to-Speech (TTS)**: Server-side Microsoft Edge TTS with high-quality neural voices.

---

## 📂 Project Architecture & Directory Layout

The project structure is organized as follows:

```text
voice-chatbot-agent/
├── app/                        # Main FastAPI application
│   ├── core/                   # System configurations and schemas
│   │   ├── config.py           # Global settings using Pydantic Settings
│   │   └── tools.py            # Core JSON schemas for Gemini Tool Calling
│   ├── database/               # Data-storage and initialization files
│   │   ├── mock_backend_data.json   # 53 mock records seed database (Rides, Food Orders, Payments)
│   │   ├── mock_backend_schema.json # JSON Schema validator for the mock backend
│   │   ├── mock_db.py          # State-isolated In-Memory Mock Database
│   │   └── prompts.json        # 20 curated customer support Vietnamese utterances
│   ├── routers/                # FastAPI Router Modules
│   │   ├── chatbot.py          # End-to-End Voice API & Edge TTS routes
│   │   └── tools.py            # REST API endpoints for mock tools
│   ├── schemas/                # Pydantic validation models
│   ├── services/               # Core business services
│   │   ├── agent_service.py    # Live Gemini 3.1 Agent & Vietnamese Normalization
│   │   ├── asr_service.py      # Real Whisper ASR inference (In-Memory Processing)
│   │   └── tool_service.py     # Backend functions invoked by Agent to access database
│   ├── static/                 # Premium Web UI Dashboard assets
│   │   ├── index.html          # HTML5 SPA structure
│   │   ├── app.js              # Frontend logic (recorder, waves, pipeline stepper, TTS play)
│   │   ├── style.css           # Glassmorphic premium CSS styling
│   │   └── samples/            # 20 preloaded audio samples (.mp3)
│   └── main.py                 # FastAPI Application Entrypoint
├── docs/                       # Technical Specifications & Reports
│   ├── asr_evaluation_report.md  # Quantification of WER/CER, Latency & downstream accuracy
│   ├── google_colab_guide.md   # Deployment and GPU evaluation guide on Google Colab
│   ├── mock_backend_data_design.md  # Mock database seed dataset layout
│   ├── prompts_dataset.md      # Analysis of 20 conversational prompts
│   ├── test_specification.md   # Testing matrix and test isolation details
│   └── tool_calling_specs.md   # Specifications of Gemini-compatible tools
├── tests/                      # Automated test suite
│   ├── audio_samples/          # 20 audio recordings for offline baseline testing
│   ├── test_api.py             # API Integration tests for Voice & Tool endpoints
│   ├── test_mock_db.py         # Mock database logic verification
│   └── test_services.py        # ASR, Agent, and Tool services verification
├── colab_run.py                # Google Colab helper script (install, evaluate, test, serve)
├── evaluate_asr.py             # Script to evaluate ASR baseline on CPU/GPU
├── generate_audio.py           # Script to generate multilingual TTS samples
├── test_end_to_end.py          # E2E integration test script (calls real Gemini API)
├── pyproject.toml              # Project dependencies & tool configurations
└── uv.lock                     # Locked dependencies managed by UV
```

---

## 🛠️ Setup & Installation

This project utilizes the ultra-fast Python package manager **`uv`**. Follow these instructions to setup your local environment:

### Prerequisites
Make sure Python 3.10+ is installed on your computer.

### 1. Synchronize Dependencies
Sync the virtual environment and install all packages locked in `uv.lock` by running:
```bash
uv sync
```
This command automatically creates a `.venv` virtual environment in your project directory and installs all required development and core libraries.

### 2. Configure Environment Variables
Create a local `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL_NAME=gemini-3.1-flash-lite
USE_MOCK_ASR=False
WHISPER_MODEL_NAME=base
```
*Note: If `GEMINI_API_KEY` is missing or when running automated unit tests, the system automatically falls back to an offline rule-based regex engine to prevent API billing and allow offline development.*

### 3. Generate Audio Samples
To generate the 20 `.mp3` test samples under `app/static/samples/` using Microsoft Edge's Neural Voices, run:
```bash
uv run python generate_audio.py
```

---

## 🛡️ Offline Fallback & Testing Isolation

To ensure maximum reliability, cost efficiency, and ease of development, this prototype implements a **deterministic offline fallback mechanism**:
* **Automatic Detection**: If the `GEMINI_API_KEY` is not set in the environment (or is left empty), the agent service (`agent_service.py`) dynamically switches to a local rule-based regex engine.
* **Testing Isolation**: When running unit tests via `pytest` (detected via `"pytest" in sys.modules`), the system overrides API calls and uses the offline regex engine automatically. This allows you to run the entire test suite in under **1 second** offline without consuming Gemini API tokens or risking rate limit errors.
* **Accent & Spacing Robustness**: The offline engine is integrated with a Vietnamese accent stripper (`strip_accents`) and a whitespace normalizer, enabling robust intent matching and entity extraction even when Whisper transcribes text with speech errors.

---

## 🚀 Running the Server Locally

To launch the FastAPI development server, run:
```bash
uv run uvicorn app.main:app --reload
```
Once started, you can explore:
* **Premium Web UI Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Swagger UI Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc UI Docs: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Testing & Verification

We provide both automated unit tests (using Pytest) and a live end-to-end integration script.

### 1. Automated Test Suite (Pytest)
Run the entire suite of 25 unit and integration tests. The database writes are isolated during tests to ensure zero seed data corruption:
```bash
uv run pytest -v
```

### 2. Live End-to-End Integration Test
To run the E2E integration test against the real Gemini API for 5 main customer support scenarios (driver late, missing food, refund request, payment error, human escalation):
```bash
uv run python test_end_to_end.py
```

### 3. ASR Performance Evaluation
To run the offline Whisper ASR transcription quality evaluation (generates WER/CER and Downstream Agent Accuracy report):
```bash
uv run python evaluate_asr.py
```

---

## ☁️ Google Colab (GPU Execution)

To run the project on Google Colab's GPU (Tesla T4) for fast Whisper inference and public web sharing, refer to:
* **Guide**: [docs/google_colab_guide.md](file:///c:/Users/Administrator/Developer/Intern_VSF/voice-chatbot-agent/docs/google_colab_guide.md)
* **Automation Command**: `!python colab_run.py --install` -> `!python colab_run.py --server`
