# speCTra
**Universal AI Gateway**

> Connect to OpenAI, Anthropic, Gemini, and more through a single, unified API.

![Dashboard Preview](frontend/public/vite.svg) 

## 🚀 Features

- **Universal API**: A Drop-in replacement for OpenAI's API. Use `client = OpenAI(base_url="http://localhost:8000/v1")` with any supported provider.
- **Multi-Provider Support**: 
  - **OpenAI** (GPT-3.5, GPT-4)
  - **Anthropic** (Claude 3 Opus/Sonnet/Haiku)
  - **Google Gemini** (Gemini Pro)
- **Advanced Routing**: Route requests dynamically based on model name or headers (`x-spectra-provider`).
- **Dashboard**: A beautiful, Dark Mode-first UI to manage API Keys and view usage analytics.
- **Secure**: Built-in API Key management and authentication.

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI, SQLModel, Uvicorn.
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Shadcn/UI.
- **Database**: SQLite (default) or PostgreSQL (via Docker).

## 🏁 Getting Started

### Prerequisites

- **Docker** (Recommended)
- *OR* Python 3.9+ and Node.js 18+ for local development.

### Option A: Run with Docker 🐳

Ensure you have Docker installed and running.

1.  **Configure Keys**: Rename `backend/.env.example` to `backend/.env` and add your provider API keys.
2.  **Run**:
    ```bash
    docker compose up --build
    ```

- **Backend**: `http://localhost:8000`
- **Dashboard**: `http://localhost:5173`

### Option B: Local Development 💻

#### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install .
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to access the Dashboard.

## 🔑 Configuration

speCTra manages provider keys via its own settings. You can set them via environment variables or in a `.env` file in the `backend/` directory.

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
```

For the Gateway itself, you generate **Client Keys** via the Dashboard or API.

## �️ Dashboard Guide

The Dashboard is your control center.
1.  **Access**: Open `http://localhost:5173`.
2.  **API Keys**: Go to the **API Keys** tab. Click **"Create New Key"**.
3.  **Copy Key**: Copy the generated `sk-spectra-...` token. You will need this to authenticate your Python/Node.js clients.
4.  **Monitor**: Use the **Home** tab to see how many keys are active.

## �💻 SDK Usage

speCTra is API-compatible with the OpenAI SDK.

```python
from openai import OpenAI

# 1. Initialize Client pointing to speCTra
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="sk-spectra-..." # Create this in your Dashboard
)

# 2. Use any model!
# speCTra automatically routes "claude-*" to Anthropic and "gpt-*" to OpenAI.
response = client.chat.completions.create(
    model="claude-3-sonnet", 
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the Apache 2.0 License. See [LICENSE](LICENSE) for details.
