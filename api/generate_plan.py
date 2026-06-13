# api/generate_plan.py
"""Vercel Serverless Function exposing the FastAPI app.

Vercel treats any Python file under the `/api` directory as a serverless
function. This thin wrapper imports the full backend package and re‑exports
the FastAPI instance so Vercel can invoke it.
"""

import os
import sys

# Ensure the project root is on the Python path so `backend` can be imported.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Import the FastAPI app defined in backend/main.py.
from backend.main import app

# Vercel expects the callable named `handler` (or `app`). Export both for clarity.
handler = app
