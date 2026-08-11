"""
Vercel serverless entry point for CodeReview Sentinel.
Handles import paths for both local and Vercel environments.
"""

import sys
import os

# Vercel's working directory is different from local
# Add the parent directory to sys.path so 'app' can be imported
_vercel_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _vercel_root not in sys.path:
    sys.path.insert(0, _vercel_root)

# Also add the current directory structure Vercel uses
for p in ['/var/task', '/var/task/api', os.path.dirname(os.path.dirname(__file__))]:
    if p not in sys.path and os.path.exists(p):
        sys.path.insert(0, p)

from app.main import app

# Vercel uses this as the ASGI handler
handler = app
