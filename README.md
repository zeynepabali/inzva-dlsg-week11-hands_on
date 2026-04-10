# 🧠 Week 11 · Deep Learning at Scale: Tools & Ops

**inzva Deep Learning Study Group**

> Build a 100% offline, privacy-first AI microservice from scratch.
> Role: **inzva Engineer**. Project codename: **inzva-AI**.

---

## 🚀 Quick Start

1. **Open in GitHub Codespaces** — Click the green "Code" button → "Codespaces" → "Create codespace on main"
2. Wait for the environment to build (~2 minutes)
3. Open [index.html](index.html) in the browser for the **interactive lab manual**
4. Follow the modules step by step!

## 📋 What You'll Build

| Module | Topic | Tools |
|--------|-------|-------|
| 01 | The Sanctuary Server | Linux CLI, bash, uv, venv |
| 02 | The Hacker's Engine | Docker, docker-compose, Ollama, GGUF |
| 03 | The inzva Router & Telemetry | FastAPI, Pydantic, httpx, MLflow |
| 04 | The Community UI & Handoff | Gradio, Dockerfile, GitHub Actions |

## 📁 Repo Structure

```
inzva-dlsg-week11/
├── .devcontainer/          # Codespace environment config
│   ├── devcontainer.json   # Python 3.11 + Docker-in-Docker
│   └── setup.sh            # Auto-installs uv & htop
├── .github/
│   └── workflows/
│       └── ci.yml          # CI/CD pipeline (Module 4)
├── docker-compose.yml      # Ollama + MLflow services
└── README.md               # This file
```

## 🔧 Environment Details

- **Python**: 3.11 (pre-installed)
- **Package Manager**: [uv](https://github.com/astral-sh/uv) — 10–100× faster than pip
- **Container Runtime**: Docker & Docker Compose v2
- **Ports**: FastAPI (8000), MLflow (5000), Gradio (7860), Ollama (11434)

## 🏗️ Files You'll Create

During the session, you'll create these files inside `inzva-ai-microservice/`:

| File | Module | Description |
|------|--------|-------------|
| `main.py` | 3 | FastAPI backend with system prompt + MLflow telemetry |
| `app.py` | 4 | Gradio chat UI connecting to your API |
| `Dockerfile` | 4 | Container image for the FastAPI service |

## 📚 Resources

- [Lab Manual](index.html) — Follow along during the session
- [Print Version](print.html) — PDF-printable reference

## 📝 License

Built with ❤️ for the [inzva](https://inzva.com) community — Week 11 Deep Learning Study Group.
