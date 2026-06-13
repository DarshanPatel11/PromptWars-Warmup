# 🍳 DailyCook AI – Personal Cooking To-Do Generator

DailyCook AI is a lightweight, high-performance, and responsive micro-app designed to help users generate structured daily meal plans, grocery shopping lists, and interactive step-by-step cooking to-do lists based on their dietary preferences, daily budget, pantry availability, and time constraints.

---

## 🌟 Key Features

1. **Structured Meal Planning**: Generates breakfast, lunch, and dinner recommendations.
2. **Interactive Cooking To-Do Checklist**: Check off recipe instructions step-by-step as you cook.
3. **Smart Supermarket Grocery List**: Automatically aggregates ingredients and groups them by grocery sections (Produce, Dairy, Pantry, Spices).
4. **Transparent Ingredient Substitutions**: Detects missing pantry items and recommends alternatives dynamically.
5. **Interactive Budget Feasibility Widget**: Provides a colored-coded visual status bar and alert alerts when estimated recipe costs exceed the user-defined budget.
6. **Ultra-Premium Design**: Includes a responsive glassmorphic layout, micro-animations, loading state indicators, and an accessible dark-mode toggle.

---

## 🏗️ Project Architecture

```
├── api/
│   └── generate_plan.py     # Vercel Serverless Function wrapper
├── backend/
│   ├── __init__.py
│   ├── data/
│   │   ├── price_map.json   # Simulated prices
│   │   ├── recipes.json     # Recipe database
│   │   └── substitutions.json # Replacement mapping
│   ├── logic.py             # Business logic (filtering, costing, parsing)
│   ├── main.py              # FastAPI server definition (CORS enabled)
│   └── schemas.py           # Pydantic schemas (typed API contract)
├── index.html               # Main dashboard UI
├── script.js                # Frontend state management & API interaction
├── style.css                # Premium responsive styles
├── vercel.json              # Vercel deployment routing configuration
└── requirements.txt         # Backend dependencies
```

---

## 🚀 How to Run Locally

### 1. Start the Backend Server (FastAPI)
Run the following commands in your terminal from the project root:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server on port 8000
python3 -m uvicorn backend.main:app --reload
```

The backend API documentation will be available locally at `http://127.0.0.1:8000/docs`.

### 2. Run the Frontend
You can launch the frontend in any of the following ways:

* **Direct Open**: Open the root `index.html` file directly in your web browser.
* **Local HTTP Server**: Run a simple local server from the project root:
  ```bash
  python3 -m http.server 3000
  ```
  Then navigate to `http://localhost:3000`.

The frontend is programmed to automatically detect the environment:
* In development, it communicates with the local FastAPI server at `http://127.0.0.1:8000/generate-plan`.
* In staging/production (on Vercel), it makes serverless function requests to `/api/generate-plan`.

---

## ⚡ Deployment on Vercel

The project is pre-configured and ready to be deployed to Vercel instantly.

1. Ensure the Vercel CLI is installed: `npm i -g vercel`
2. Run the deployment command from the project root:
   ```bash
   vercel --prod
   ```

Vercel will build the Python serverless function inside `api/generate_plan.py` and serve the static files (`index.html`, `style.css`, `script.js`) automatically using the configuration defined in `vercel.json`.
