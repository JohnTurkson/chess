import json

from chalice import Blueprint

from chalicelib.app_resources import connections, game_moves_table, game_statuses_table

game_functions = Blueprint(__name__)


@game_functions.lambda_function(name="make_move")
def make_move(event, context):
    connection = event["requestContext"]["connectionId"]
    request = json.loads(event["body"])

    game_id = request.get("game")
    move_number = request.get("moveNumber")
    move = request.get("move")

    if game_id is None or type(game_id) is not str:
        connections.post_to_connection(
            Data=json.dumps({"error": "Bad request"}).encode("utf-8"),
            ConnectionId=connection,
        )
        return {}

    if move_number is None or type(move_number) is not int:
        connections.post_to_connection(
            Data=json.dumps({"error": "Bad request"}).encode("utf-8"),
            ConnectionId=connection,
        )
        return {}

    if move is None or type(move) is not str:
        connections.post_to_connection(
            Data=json.dumps({"error": "Bad request"}).encode("utf-8"),
            ConnectionId=connection,
        )
        return {}

    game = game_statuses_table.get_item(Key={"game": game_id}).get("Item")

    if game is None:
        connections.post_to_connection(
            Data=json.dumps({"error": "Bad request"}).encode("utf-8"),
            ConnectionId=connection,
        )
        return {}

    response = {
        "game": game_id,
        "moveNumber": move_number,
        "move": move,
    }

    game_moves_table.put_item(Item=response)

    connections.post_to_connection(
        Data=json.dumps(response).encode("utf-8"),
        ConnectionId=connection,
    )

    return {}
