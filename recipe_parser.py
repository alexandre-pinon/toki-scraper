from typing import Protocol
from bs4 import BeautifulSoup
from recipe import Recipe


class RecipeParser(Protocol):
    def parse_recipe(soup: BeautifulSoup) -> Recipe: ...
