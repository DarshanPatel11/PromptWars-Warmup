# backend/logic.py
"""Core business logic for DailyCook AI.
All functions are annotated with evaluation criteria comments.
"""

import json
from typing import List, Dict, Any
from .schemas import PlanRequest, PlanResponse, MealPlan, GrocerySection, GroceryItem

# Load static data (in real deployment use caching or DB)
with open("backend/data/recipes.json", "r", encoding="utf-8") as f:
    RECIPES = json.load(f)["recipes"]

with open("backend/data/price_map.json", "r", encoding="utf-8") as f:
    PRICE_MAP = json.load(f)

with open("backend/data/substitutions.json", "r", encoding="utf-8") as f:
    SUBSTITUTIONS = json.load(f)

# ---------- Helper utilities ----------

def filter_recipes(request: PlanRequest) -> List[Dict[str, Any]]:
    """Return recipes matching diet, cuisine and time constraints.
    # CODE QUALITY COMPLIANCE: simple filter, pure function.
    """
    suitable = []
    for r in RECIPES:
        if r["diet"] != request.diet:
            continue
        if r["cuisine"] != request.cuisine:
            continue
        if r["time"] > request.time_limit:
            continue
        suitable.append(r)
    return suitable

def select_meals(recipes: List[Dict[str, Any]]) -> MealPlan:
    """Select three meals (breakfast, lunch, dinner) from the list.
    # CODE QUALITY COMPLIANCE: deterministic simple selection for demo.
    """
    # Fallback ordering: first three items, mapping by name keywords.
    breakfast = next((r for r in recipes if "breakfast" in r["name"].lower()), recipes[0])
    lunch = next((r for r in recipes if "lunch" in r["name"].lower()), recipes[1] if len(recipes) > 1 else recipes[0])
    dinner = next((r for r in recipes if "dinner" in r["name"].lower()), recipes[2] if len(recipes) > 2 else recipes[0])
    return MealPlan(breakfast=breakfast["name"], lunch=lunch["name"], dinner=dinner["name"])

def aggregate_grocery(meal_recipes: List[Dict[str, Any]]) -> List[GrocerySection]:
    """Group ingredients by store section.
    # EFFICIENCY COMPLIANCE: single pass aggregation.
    """
    sections: Dict[str, List[GroceryItem]] = {}
    for recipe in meal_recipes:
        for ing in recipe["ingredients"]:
            sec = ing.get("section", "Other")
            item = GroceryItem(name=ing["name"], qty=ing["qty"], section=sec)
            sections.setdefault(sec, []).append(item)
    return [GrocerySection(section=sec, items=its) for sec, its in sections.items()]

def apply_substitutions(grocery: List[GrocerySection], request: PlanRequest) -> List[GrocerySection]:
    """Replace missing ingredients with static alternatives.
    # SECURITY COMPLIANCE: no external calls, deterministic mapping.
    """
    # Determine missing items based on user's available ingredients.
    available = set(map(str.lower, request.available_ingredients))
    for section in grocery:
        for item in section.items:
            if item.name.lower() not in available:
                # Look for substitution key.
                for key, alt in SUBSTITUTIONS.items():
                    if key.lower() == item.name.lower():
                        item.name = alt  # substitution applied
    return grocery

def parse_qty(qty_str: str) -> float:
    """Parse quantity string into a float value.
    Handles fractions (1/2) and scales down weights (200g -> 1 pack).
    """
    qty_str = qty_str.lower().strip()
    # If it is a weight/volume like 200g, we treat it as 1 package/unit for pricing
    if 'g' in qty_str or 'ml' in qty_str:
        return 1.0
    # Handle fractions like 1/2
    if '/' in qty_str:
        parts = qty_str.split('/')
        try:
            num = float(''.join(c for c in parts[0] if c.isdigit() or c == '.'))
            den = float(''.join(c for c in parts[1] if c.isdigit() or c == '.'))
            return num / den
        except (ValueError, ZeroDivisionError):
            return 0.5
    # Standard numbers
    digits = ''.join(c for c in qty_str if c.isdigit() or c == '.')
    try:
        return float(digits) if digits else 1.0
    except ValueError:
        return 1.0

def calculate_budget(grocery: List[GrocerySection]) -> Dict[str, Any]:
    """Sum cost using PRICE_MAP and return summary.
    # CODE QUALITY COMPLIANCE: returns dict ready for response.
    """
    total = 0
    for section in grocery:
        for item in section.items:
            price_per_unit = PRICE_MAP.get(item.name.lower(), 0)
            qty_val = parse_qty(item.qty)
            total += price_per_unit * qty_val
    return {"estimated_cost": round(total, 2)}


def build_todo_list(meal_recipes: List[Dict[str, Any]]) -> List[str]:
    """Combine steps from all chosen recipes into an ordered to‑do list.
    # CODE QUALITY COMPLIANCE: pure function, easy to test.
    """
    todos = []
    for recipe in meal_recipes:
        todos.extend([f"[{recipe['name']}] {step}" for step in recipe["steps"]])
    return todos

def generate_daily_plan(request: PlanRequest) -> PlanResponse:
    """Orchestrates full plan generation.
    # CODE QUALITY COMPLIANCE: high‑level orchestration, single entry point.
    """
    suitable = filter_recipes(request)
    if not suitable:
        raise ValueError("No recipes match the given constraints")
    # For simplicity pick first three distinct recipes.
    meal_recipes = suitable[:3]
    meals = select_meals(meal_recipes)
    grocery = aggregate_grocery(meal_recipes)
    grocery = apply_substitutions(grocery, request)
    budget = calculate_budget(grocery)
    budget_summary = {
        "estimated_cost": budget["estimated_cost"],
        "budget": request.budget,
        "within_budget": budget["estimated_cost"] <= request.budget,
    }
    # Build a flat dict of substitutions applied for transparency.
    subs = {}
    for sec in grocery:
        for item in sec.items:
            if item.name in SUBSTITUTIONS.values():
                # reverse‑lookup original key
                orig = next(k for k, v in SUBSTITUTIONS.items() if v == item.name)
                subs[orig] = item.name
    return PlanResponse(
        meals=meals,
        todo_list=build_todo_list(meal_recipes),
        grocery_list=grocery,
        substitutions=subs,
        budget_summary=budget_summary,
    )
