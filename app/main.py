"""
FastAPI backend for CodeReview Sentinel.
Exposes the Strands Agent as a REST API.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.agent import run_agent, agent, _agent_error
from datetime import datetime

app = FastAPI(
    title="CodeReview Sentinel",
    description="Autonomous code review triage agent powered by Strands Agents SDK",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReviewRequest(BaseModel):
    diff_content: str
    file_paths: str = ""
    language: str = "python"


class HealthResponse(BaseModel):
    status: str
    agent: str
    sdk: str
    tools: int
    timestamp: str


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the main dashboard UI."""
    html_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'index.html')
    if os.path.exists(html_path):
        with open(html_path, 'r') as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>CodeReview Sentinel</h1><p>Dashboard not found.</p>")


@app.get("/api/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        agent="CodeReview Sentinel",
        sdk="Strands Agents SDK v1.51.0",
        tools=6,
        timestamp=datetime.utcnow().isoformat() + "Z",
    )


@app.get("/api/agent/status")
async def agent_status():
    """Get the Strands agent status."""
    return {
        "agent_name": "CodeReview Sentinel",
        "sdk_version": "1.51.0",
        "model": "demo-mode (direct tool orchestration)",
        "tools": [
            {"name": "analyze_diff", "description": "Analyze code diff for complexity metrics"},
            {"name": "classify_severity", "description": "Classify risk level of changes"},
            {"name": "check_style", "description": "Check code style compliance"},
            {"name": "security_scan", "description": "Scan for security vulnerabilities"},
            {"name": "generate_review_comment", "description": "Generate structured review comment"},
            {"name": "draft_pr_summary", "description": "Draft concise PR summary"},
        ],
        "agent_initialized": agent is not None,
        "fallback_mode": agent is None,
        "fallback_reason": _agent_error if agent is None else None,
    }


@app.post("/api/review")
async def review_pr(request: ReviewRequest):
    """
    Run the autonomous code review agent on a PR diff.
    
    The Strands Agent autonomously decides which tools to call
    and synthesizes results into a structured review.
    """
    if not request.diff_content:
        raise HTTPException(status_code=400, detail="diff_content is required")
    
    result = run_agent(
        diff_content=request.diff_content,
        file_paths=request.file_paths,
        language=request.language,
    )
    return JSONResponse(result)


@app.get("/api/demo")
async def demo():
    """
    Run a demo review with a sample PR diff.
    Shows the agent working end-to-end.
    """
    sample_diff = """diff --git a/src/auth/login.py b/src/auth/login.py
index 1234567..abcdefg 100644
--- a/src/auth/login.py
+++ b/src/auth/login.py
@@ -10,6 +10,18 @@ def authenticate(username, password):
     user = db.query(User).filter_by(username=username).first()
     if not user:
         return None
-    if user.password == password:
+    import hashlib
+    password_hash = hashlib.md5(password.encode()).hexdigest()
+    if user.password_hash == password_hash:
+        # Add session token
+        session_token = generate_token(user.id)
+        # Log the attempt
+        print(f"User {username} logged in successfully")
+        return {"token": session_token, "user": user}
-    return {"user": user}
+    return None
diff --git a/src/config/settings.py b/src/config/settings.py
index abc..def 100644
--- a/src/config/settings.py
+++ b/src/config/settings.py
@@ -1,4 +1,7 @@
 DEBUG = True
+API_KEY = "sk-prod-1234567890abcdef"
+DATABASE_URL = "postgresql://admin:password@localhost:5432/prod"
+SECRET_KEY = "super-secret-key-do-not-share"
 ALLOWED_HOSTS = ["*"]
"""
    sample_files = "src/auth/login.py,src/config/settings.py"
    
    result = run_agent(
        diff_content=sample_diff,
        file_paths=sample_files,
        language="python",
    )
    return JSONResponse(result)


@app.post("/api/agent/invoke")
async def invoke_agent(prompt: str):
    """
    Invoke the Strands agent with a natural language prompt.
    
    In production (with a real LLM), the agent reasons about the prompt
    and autonomously calls tools. In demo mode, returns the agent status.
    """
    if agent is not None:
        try:
            response = agent(prompt)
            return {"response": str(response), "agent_mode": "live"}
        except Exception as e:
            return {"response": f"Agent error: {str(e)}", "agent_mode": "error"}
    else:
        return {
            "response": f"Agent in demo mode. Prompt received: '{prompt}'. In production, the Strands Agent would reason about this and call tools autonomously.",
            "agent_mode": "demo",
            "note": "Set up an LLM backend (Bedrock/OpenAI/Ollama) to enable full agent reasoning.",
        }
