import json

from chalice import Blueprint

from chalicelib.app_resources import connections, tokens_table, connections_table

connection_functions = Blueprint(__name__)


@connection_functions.lambda_function(name="connect_user")
def connect_user(event, context):
    connection = event["requestContext"]["connectionId"]
    request = json.loads(event["body"])

    request_token = request.get("token")
    request_user = request.get("user")

    if request_token is None or type(request_token) is not str:
        connections.delete_connection(ConnectionId="connection")
        return {}

    if request_user is None or type(request_user) is not str:
        connections.delete_connection(ConnectionId="connection")
        return {}

    response = tokens_table.get_item(Key={"token": request_token}).get("Item")

    if response is None:
        connections.delete_connection(ConnectionId="connection")
        return {}

    token = response["token"]
    user = response["user"]

    if token != request_token or user != request_user:
        connections.delete_connection(ConnectionId="connection")
        return {}

    connections_table.put_item(Item={"connection": connection, "user": user})

    return {}


@connection_functions.lambda_function(name="disconnect_user")
def disconnect_user(event, context):
    connection = event["requestContext"]["connectionId"]
    connections.delete_connection(ConnectionId=connection)
    connections_table.delete_item(Key={"connection": connection})
    return {}
