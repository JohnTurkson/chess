import json

from chalice import Blueprint

from chalicelib.app_resources import game_statuses_table
from chalicelib.app_utilities import get_event_body, generate_id

matchmaking_functions = Blueprint(__name__)


@matchmaking_functions.lambda_function(name="NotifyMatchFound")
def notify_match_found(event, context):
    return {}


@matchmaking_functions.lambda_function(name="ChallengePlayer")
def challenge_player(event, context):
    return {}


@matchmaking_functions.lambda_function(name="CreateMatch")
def create_match(event, context):
    request = json.loads(get_event_body(event))

    game_id = generate_id()
    game_status = "IN_PROGRESS"
    players = request.get("players")
    last_move_number = 0

    game = {
        "type": "CreateMatchResponse",
        "game": game_id,
        "status": game_status,
        "players": players,
        "lastMoveNumber": last_move_number,
    }

    game_statuses_table.put_item(Item=game)

    return game
