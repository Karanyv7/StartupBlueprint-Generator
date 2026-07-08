# 🚀 Blueprint AI — Innovation Blueprint Agent

**AI-powered startup idea → complete innovation blueprint generator**  
Built with **Python Flask** + **IBM watsonx.ai Granite** models

---

## ✨ Features

| Tool | Description |
|------|-------------|
| 💬 **AI Chat** | Generate complete innovation blueprints from rough ideas |
| ✅ **Idea Validator** | Score ideas on innovation, feasibility, scalability & more |
| 🏗️ **System Designer** | Generate full software architecture blueprints |
| 🎨 **UI Planner** | Design pages, flows, color themes & component plans |
| 🎤 **Pitch Builder** | Create 30s / 1-min / 3-min investor pitches + Q&A prep |
| 📊 **Dashboard** | Daily AI insights, inspiration, and quick tool access |

**Additional capabilities:**
- 🌙 Dark / Light mode toggle (persisted)
- 📱 Fully responsive (mobile, tablet, desktop)
- 🔒 Secure API key management via `.env`
- 🤖 Customizable agent personality via `agent_instructions.py`
- 📋 Copy & export all generated content
- ⚡ Powered by IBM Granite 3.3 8B Instruct

---

## 📁 Project Structure

```
innovation-blueprint-agent/
├── app.py                     # Flask backend, routes, watsonx.ai integration
├── agent_instructions.py      # ← CUSTOMIZE AGENT BEHAVIOR HERE
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
├── .env                       # Your credentials (DO NOT COMMIT)
├── templates/
│   ├── base.html              # Base template (sidebar, navbar, dark mode)
│   ├── dashboard.html         # Dashboard with insights & tools
│   ├── chat.html              # AI Chat for blueprint generation
│   ├── validator.html         # Idea Validator
│   ├── designer.html          # System Designer
│   ├── ui_planner.html        # UI/UX Planner
│   ├── pitch_builder.html     # Pitch Builder
│   └── 404.html               # Error page
└── static/
    ├── css/style.css          # Premium design system (730+ lines)
    ├── js/app.js              # Theme, sidebar, toast, utils
    └── images/ibm-logo.svg    # IBM branding asset
```

---

## 🔧 Setup & Installation

### Prerequisites
- Python 3.10+
- IBM Cloud account with watsonx.ai access
- Active watsonx.ai project

### 1. Clone & Enter Directory

```bash
git clone <your-repo-url>
cd innovation-blueprint-agent
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your credentials:

```env
IBM_API_KEY=your_ibm_cloud_api_key_here
WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-3-8b-instruct
FLASK_SECRET_KEY=your-super-secret-random-key-here
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

### 5. Get IBM watsonx.ai Credentials

1. **IBM Cloud API Key:**
   - Go to [IBM Cloud Console](https://cloud.ibm.com)
   - Navigate to **Manage → Access (IAM) → API Keys**
   - Click **Create an IBM Cloud API key**

2. **watsonx.ai Project ID:**
   - Go to [IBM watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home)
   - Open your project
   - Go to **Manage → General**
   - Copy the **Project ID**

3. **watsonx.ai URL** (choose your region):
   - Dallas: `https://us-south.ml.cloud.ibm.com`
   - Frankfurt: `https://eu-de.ml.cloud.ibm.com`
   - Tokyo: `https://jp-tok.ml.cloud.ibm.com`
   - London: `https://eu-gb.ml.cloud.ibm.com`

### 6. Run the Application

```bash
python app.py
```

Open your browser at: **http://localhost:5000**

---

## 🎛️ Customizing Agent Behavior

Edit [`agent_instructions.py`](agent_instructions.py) to customize:

```python
# ── Creativity Level ──────────────────────────────────────────
# Options: "conservative" | "balanced" | "creative" | "visionary"
CREATIVITY_LEVEL = "creative"

# ── Mentoring Style ───────────────────────────────────────────
# Options: "coach" | "consultant" | "professor" | "peer"
MENTORING_STYLE = "coach"

# ── Innovation Focus ──────────────────────────────────────────
# Options: "product" | "process" | "platform" | "social" | "deep-tech"
INNOVATION_FOCUS = "product"

# ── Communication Tone ────────────────────────────────────────
# Options: "professional" | "friendly" | "inspiring" | "concise"
COMMUNICATION_TONE = "inspiring"

# ── Domain Specialization ─────────────────────────────────────
DOMAIN_SPECIALIZATION = ["HealthTech", "EdTech", "FinTech", "SaaS", "AI/ML"]

# ── Safety Rules ──────────────────────────────────────────────
SAFETY_RULES = [
    "Never generate content that promotes illegal activities.",
    # ... add your own rules
]
```

Changes take effect immediately on the next request (no restart needed for most settings).

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Generate innovation blueprint |
| `POST` | `/api/validate` | Validate and score an idea |
| `POST` | `/api/design` | Generate system architecture |
| `POST` | `/api/ui-plan` | Generate UI/UX plan |
| `POST` | `/api/pitch` | Generate investor pitches |
| `GET`  | `/api/daily-content` | Get today's insight & inspiration |
| `GET`  | `/api/health` | Health check & model status |

### Example API Call

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "An app that helps remote teams stay connected through virtual coffee chats"}'
```

---

## 🚀 Deployment

### Option A: Gunicorn (Production)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

### Option B: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
```

```bash
docker build -t blueprint-ai .
docker run -p 5000:5000 --env-file .env blueprint-ai
```

### Option C: IBM Code Engine

```bash
# Install IBM Cloud CLI
# Build and push container image
ibmcloud ce application create \
  --name blueprint-ai \
  --image your-registry/blueprint-ai:latest \
  --env-from-secret blueprint-ai-secrets \
  --port 5000 \
  --min-scale 1
```

### Option D: Railway / Render / Fly.io

1. Push code to GitHub
2. Connect repo to Railway/Render/Fly.io
3. Set environment variables in the platform dashboard
4. Deploy (auto-detected as Python/Flask)

---

## 🔒 Security Notes

- **Never commit** your `.env` file — it's in `.gitignore`
- Use a strong random `FLASK_SECRET_KEY` in production
- Set `FLASK_DEBUG=False` and `FLASK_ENV=production` in production
- Consider rate limiting API endpoints with Flask-Limiter in production
- Use HTTPS in production (reverse proxy with Nginx or platform SSL)

---

## 🛠️ Changing the AI Model

Edit `.env` to use a different Granite model:

```env
# Granite 3.3 8B Instruct (default, fast & capable)
WATSONX_MODEL_ID=ibm/granite-3-3-8b-instruct

# Granite 3 8B Instruct (previous gen)
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct

# Granite 13B Chat
WATSONX_MODEL_ID=ibm/granite-13b-chat-v2
```

---

## 📦 Dependencies

```
flask==3.0.3              # Web framework
python-dotenv==1.0.1      # Environment variable management
ibm-watsonx-ai==1.1.2     # IBM watsonx.ai SDK
requests==2.32.3          # HTTP client
gunicorn==22.0.0          # Production WSGI server
```

**Frontend (CDN, no installation):**
- Bootstrap 5.3.3
- Bootstrap Icons 1.11.3
- Google Fonts (Inter, JetBrains Mono)
- Marked.js (markdown rendering)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

**Built with ❤️ using IBM watsonx.ai Granite**

[IBM watsonx.ai](https://www.ibm.com/watsonx) · [IBM Cloud](https://cloud.ibm.com) · [Granite Models](https://www.ibm.com/granite)

</div>
