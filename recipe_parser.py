from typing import Protocol
from recipe import Recipe
from typing import Dict, Type
from marmiton_parser import MarmitonParser
from urllib.parse import urlparse


class RecipeParser(Protocol):
    def parse_recipe(self) -> Recipe: ...


class RecipeParserFactory:
    _parsers: Dict[str, Type[RecipeParser]] = {
        "marmiton.org": MarmitonParser,
    }

    @classmethod
    def create_parser(cls, url: str, html: str) -> RecipeParser:
        domain = urlparse(url).netloc.lower()
        domain = domain.replace("www.", "")

        parser_class = cls._parsers.get(domain)
        if not parser_class:
            raise ValueError(f"No parser available for domain: {domain}")

        return parser_class(html=html, source_url=url)
