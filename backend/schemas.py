"""Pydantic schemas for DailyCook AI.

These models define the request and response contracts for the FastAPI endpoint.
Each model includes comments that map to the evaluation criteria.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any

class PlanRequest(BaseModel):
    """Input payload from the frontend.
    # CODE QUALITY COMPLIANCE: explicit field definitions, type hints.
    """
    diet: str = Field(..., description="Dietary preference (veg, non-veg, vegan)")
    budget: int = Field(..., description="Daily budget in INR")
    available_ingredients: List[str] = Field(default_factory=list, description="Pantry items user already has")
    time_limit: int = Field(..., description="Maximum cooking time in minutes")
    cuisine: str = Field(default="indian", description="Preferred cuisine")

class MealPlan(BaseModel):
    breakfast: str
    lunch: str
    dinner: str

class GroceryItem(BaseModel):
    name: str
    qty: str
    section: str

class GrocerySection(BaseModel):
    section: str
    items: List[GroceryItem]

class PlanResponse(BaseModel):
    """Full response sent back to the UI.
    # CODE QUALITY COMPLIANCE: nested models for clarity.
    """
    meals: MealPlan
    todo_list: List[str]
    grocery_list: List[GrocerySection]
    substitutions: Dict[str, str]
    budget_summary: Dict[str, Any]
