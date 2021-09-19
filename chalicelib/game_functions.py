import json

from boto3.dynamodb.conditions import Key
from chalice import Blueprint

from chalicelib.app_resources import connections, game_moves_table, game_statuses_table, connections_table, \
    connections_by_user_index

game_functions = Blueprint(__name__)


@game_functions.lambda_function(name="MakeMove")
def make_move(event, context):
    connection = event["requestContext"]["connectionId"]
    request = json.loads(event["body"])

    game_id = request.get("game")
    move_number = request.get("moveNumber")
    move_value = request.get("move")

    if game_id is None or type(game_id) is not str:
        connections.post_to_connection(
            ConnectionId=connection,
            Data=json.dumps({"error": "Bad Request"}).encode(),
        )
        return {}

    if move_number is None or type(move_number) is not int:
        connections.post_to_connection(
            ConnectionId=connection,
            Data=json.dumps({"error": "Bad Request"}).encode(),
        )
        return {}

    if move_value is None or type(move_value) is not str:
        connections.post_to_connection(
            ConnectionId=connection,
            Data=json.dumps({"error": "Bad Request"}).encode(),
        )
        return {}

    connected_user = connections_table.get_item(Key={"connection": connection}).get("Item")

    if connected_user is None:
        connections.post_to_connection(
            ConnectionId=connection,
            Data=json.dumps({"error": "Not Authenticated"}).encode(),
        )
        return {}

    connected_user_id = connected_user["user"]

    game = game_statuses_table.get_item(Key={"game": game_id}).get("Item")

    if game is None:
        connections.post_to_connection(
            ConnectionId=connection,
            Data=json.dumps({"error": "Bad request"}).encode(),
        )
        return {}

    players = game["players"]
    last_move_number = int(game["lastMoveNumber"])

    if (move_number - 1) != last_move_number:
        connections.post_to_connection(
            ConnectionId=connection,
            Data=json.dumps({"error": "Invalid Move"}).encode(),
        )
        return {}

    if players[last_move_number % len(players)] != connected_user_id:
        connections.post_to_connection(
            ConnectionId=connection,
            Data=json.dumps({"error": "Invalid Move"}).encode(),
        )
        return {}

    move = {
        "game": game_id,
        "moveNumber": move_number,
        "move": move_value,
    }

    status = game | {"lastMoveNumber": move_number}

    game_moves_table.put_item(Item=move)
    game_statuses_table.put_item(Item=status)

    for player in players:
        player_connections = connections_table.query(
            IndexName=connections_by_user_index,
            KeyConditionExpression=Key("user").eq(player),
        ).get("Items")

        for player_connection in player_connections:
            connections.post_to_connection(
                ConnectionId=player_connection["connection"],
                Data=json.dumps(move).encode(),
            )

    return {}
