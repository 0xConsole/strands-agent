"""
Vercel serverless entry point for CodeReview Sentinel.
"""

from app.main import app

# Vercel uses this as the ASGI handler
handler = app
