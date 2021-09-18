import json
import secrets

from chalice import Blueprint

from chalicelib.app_resources import game_statuses_table
from chalicelib.app_utilities import get_event_body

matchmaking_functions = Blueprint(__name__)


@matchmaking_functions.lambda_function(name="notify_match_found")
def notify_match_found(event, context):
    return {}


@matchmaking_functions.lambda_function(name="challenge_player")
def challenge_player(event, context):
    return {}


@matchmaking_functions.lambda_function(name="create_match")
def create_match(event, context):
    request = json.loads(get_event_body(event))

    game_id = secrets.token_urlsafe(32)
    game_status = "IN_PROGRESS"
    first_player = request.get("firstPlayer")
    second_player = request.get("secondPlayer")

    if first_player is None or type(first_player) is not str:
        return {"error": "Bad Request"}

    if second_player is None or type(second_player) is not str:
        return {"error": "Bad Request"}

    game = {
        "game": game_id,
        "status": game_status,
        "firstPlayer": first_player,
        "secondPlayer": second_player,
    }

    game_statuses_table.put_item(Item=game)

    return game
