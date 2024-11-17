from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Ingredient:
  name: str
  quantity: Optional[float]
  unit: Optional[str]

@dataclass
class Instruction:
  step_number: int
  instruction: str

@dataclass
class Recipe:
  title: Optional[str]
  prep_time: Optional[str]
  cook_time: Optional[str]
  servings: Optional[int]
  source_url: Optional[str]
  image_url: Optional[str]
  ingredients: List[Ingredient]
  instructions: List[Instruction]