from flask import Request, abort, jsonify
from flask.typing import ResponseReturnValue
from flask_cors import cross_origin
from dataclasses import asdict
from marmiton_parser import MarmitonParser
import functions_framework
import logging
import requests

# Configure basic logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@functions_framework.http
@cross_origin(methods="POST")
def extract_recipe(request: Request) -> ResponseReturnValue:
    body = request.get_json(silent=True)

    if not body or "url" not in body:
        abort(400, description="url is missing")

    try:
        html = fetch(body["url"])
    except Exception as e:
        logger.error(f"Failed to fetch url: {body["url"]}\nReason: {e}")
        abort(500, description="request failed")

    parser = MarmitonParser(html, body["url"])
    recipe = parser.parse_recipe()

    return asdict(recipe)


@functions_framework.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@functions_framework.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500


def fetch(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    return response.text
