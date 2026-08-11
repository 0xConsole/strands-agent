
# CodeReview Sentinel

> An autonomous AI agent that triages pull requests — powered by **Strands Agents SDK**.

## 🎯 What It Does

CodeReview Sentinel is a **Professional Agents** track entry for the [AWS Agents for Humans Hackathon](https://agentsforhumans.devpost.com/). It makes developers dramatically better at code review by autonomously:

1. **Analyzing** code diffs for complexity metrics
2. **Classifying** the severity/risk level of changes
3. **Checking** code style compliance (Python, JS, TS, Go)
4. **Scanning** for security vulnerabilities (15+ pattern types)
5. **Generating** structured review comments ready to post
6. **Drafting** concise PR summaries for maintainers

The agent uses the **Strands Agents SDK** with 6 callable tools, running an autonomous reasoning loop: *perceive → analyze → decide → report → act*.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CodeReview Sentinel                    │
│                                                           │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  FastAPI     │───▶│ Strands Agent │───▶│  6 Tools     │ │
│  │  Backend     │    │ (SDK v1.51)  │    │              │ │
│  └─────────────┘    └──────────────┘    └──────────────┘ │
│         │                                       │        │
│         ▼                                       ▼        │
│  ┌─────────────┐              ┌──────────────────────┐  │
│  │  Web UI      │              │  analyze_diff         │  │
│  │  (Dashboard) │              │  classify_severity    │  │
│  └─────────────┘              │  check_style          │  │
│                               │  security_scan        │  │
│                               │  generate_review      │  │
│                               │  draft_pr_summary     │  │
│                               └──────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Tech Stack

- **Agent SDK**: Strands Agents SDK v1.51.0 (AWS — mandatory for this hackathon)
- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Vanilla HTML/CSS/JS
- **Deploy**: Vercel (free tier)
- **Repository**: GitHub (public, Apache 2.0)

## 🚀 Quick Start

```bash
# Install dependencies
pip install strands-agents fastapi uvicorn

# Run locally
uvicorn app.main:app --reload --port 8000

# Or use the Vercel deployment
# Live demo: https://code-review-sentinel.vercel.app
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Dashboard UI |
| `/api/health` | GET | Health check |
| `/api/agent/status` | GET | Agent + tools status |
| `/api/review` | POST | Review a PR diff (body: `{diff_content, file_paths, language}`) |
| `/api/demo` | GET | Run demo review with sample diff |
| `/api/agent/invoke` | POST | Invoke agent with natural language prompt |

## 🛠️ Strands Agent Tools

The agent has 6 tools it calls autonomously:

1. **`analyze_diff`** — Complexity metrics (lines added/removed, files changed, complexity score)
2. **`classify_severity`** — Risk classification (low → critical) based on file patterns + dangerous code
3. **`check_style`** — Style compliance checking for Python/JS/TS/Go
4. **`security_scan`** — 15+ vulnerability pattern detection (hardcoded secrets, RCE, XSS, SQLi, etc.)
5. **`generate_review_comment`** — Structured markdown review comment generation
6. **`draft_pr_summary`** — Concise PR summary with categories and recommendation

## 🎪 Demo

Visit `/api/demo` to see the agent review a sample PR containing:
- A login function change with MD5 hashing (weak crypto)
- Hardcoded API keys and secrets in config
- Print statements in production code

The agent will autonomously call all 6 tools and produce a structured review.

## 📁 Project Structure

```
agents-for-humans/
├── api/
│   └── index.py          # Vercel serverless entry point
├── app/
│   ├── agent.py           # Strands Agent + 6 tools
│   └── main.py            # FastAPI backend
├── static/
│   └── index.html         # Dashboard UI
├── requirements.txt
├── vercel.json
├── LICENSE                # Apache 2.0
└── README.md
```

## 🏆 Hackathon Track: Professional Agents

**How this fits the Professional Agents track:**
- Makes developers **dramatically better at code review** — a repetitive, judgment-heavy task
- Runs **autonomously** — given a PR, it decides what to analyze and surfaces only actionable insights
- **Real problem, real audience** — every dev team does code review, and review backlog is a universal bottleneck

## 📝 License

Apache 2.0 — see [LICENSE](LICENSE)

## 🔗 Links

- **Live Demo**: [https://code-review-sentinel.vercel.app](https://code-review-sentinel.vercel.app)
- **GitHub**: [https://github.com/0xConsole/strands-agent](https://github.com/0xConsole/strands-agent)
- **Built with**: Strands Agents SDK, FastAPI, Vercel

---

*Built for the AWS Agents for Humans Hackathon — Sep 14, 2026*
