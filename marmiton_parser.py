from bs4 import BeautifulSoup, Tag
from recipe import Recipe
from typing import Optional, Tuple, List
from recipe import Ingredient, Instruction, Recipe
import logging

logger = logging.getLogger(__name__)


class MarmitonParser:
    _soup: BeautifulSoup
    _source_url: str

    def __init__(self, html: str, source_url: str):
        self._soup = BeautifulSoup(html, "html.parser")
        self._source_url = source_url

    def parse_recipe(self) -> Recipe:
        prep_time, cook_time = self.__parse_recipe_time()

        return Recipe(
            title=self.__parse_title(),
            prep_time=prep_time,
            cook_time=cook_time,
            servings=self.__parse_servings(),
            source_url=self._source_url,
            image_url=self.__parse_image_url(),
            ingredients=self.__parse_ingredients(),
            instructions=self.__parse_instructions(),
        )

    def __parse_title(self) -> Optional[str]:
        h1 = self._soup.find("h1")
        return h1.string if h1 else None

    def __parse_recipe_time(self) -> Tuple[Optional[str], Optional[str]]:
        try:
            time_details = self._soup.find("div", class_="time__details")
            prep_time_tag = time_details.div.div.string
            cook_time_tag = time_details.div.find_next_siblings().pop().div.string
            return prep_time_tag, cook_time_tag
        except Exception as e:
            logger.error(f"Failed to parse recipe times: {e}")
            return None, None

    def __parse_servings(self) -> Optional[int]:
        try:
            servings_tag = self._soup.find(
                "div", class_="mrtn-recette_ingredients-counter"
            )
            return int(servings_tag["data-servingsnb"])
        except Exception as e:
            logger.error(f"Failed to parse servings from tag {servings_tag}: {e}")
            return None

    def __parse_image_url(self) -> Optional[str]:
        image_tag = self._soup.find("img", id="recipe-media-viewer-main-picture")
        return image_tag.get("data-src") if image_tag else None

    def __parse_ingredients(self) -> List[Ingredient]:
        ingredients_tag = self._soup.find(
            "div", class_="mrtn-recette_ingredients-items"
        )
        ingredients = []

        for ingredient_tag in ingredients_tag.find_all("div", class_="card-ingredient"):
            ingredient = self.__parse_ingredient(ingredient_tag)
            if ingredient:
                ingredients.append(ingredient)

        return ingredients

    @staticmethod
    def __parse_ingredient(tag: Tag) -> Optional[Ingredient]:
        try:
            name = tag.find("span", class_="ingredient-name")[
                "data-ingredientnamesingular"
            ]
            quantity = float(
                tag.find("span", class_="card-ingredient-quantity")[
                    "data-ingredientquantity"
                ]
            )
            quantity = quantity if quantity > 0 else None
            unit = tag.find("span", class_="unit")["data-unitsingular"]
            unit = unit if len(unit) > 0 else None
            return Ingredient(name, quantity, unit)
        except Exception as e:
            logger.error(f"Failed to parse ingredient from tag {tag}: {e}")
            return None

    def __parse_instructions(self) -> List[Instruction]:
        instructions_tag = self._soup.find("div", class_="recipe-step-list")
        instructions = []

        for step_number, instruction_tag in enumerate(
            instructions_tag.find_all("div", class_="recipe-step-list__container")
        ):
            instruction = self.__parse_instruction(instruction_tag)
            if instruction:
                instructions.append(Instruction(step_number + 1, instruction))

        return instructions

    @staticmethod
    def __parse_instruction(tag: Tag) -> Optional[str]:
        try:
            return tag.p.string
        except Exception as e:
            logger.error(f"Failed to parse instruction from tag {tag}: {e}")
            return None
