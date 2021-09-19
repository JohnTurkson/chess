import json

from chalice import Blueprint

from chalicelib.app_resources import connections, tokens_table, connections_table
from chalicelib.app_utilities import get_event_body

connection_functions = Blueprint(__name__)


@connection_functions.lambda_function(name="AuthenticateUser")
def authenticate_user(event, context):
    connection = event["requestContext"]["connectionId"]
    request = json.loads(get_event_body(event))

    request_user = request.get("user")
    request_token = request.get("token")

    if request_user is None or type(request_user) is not str:
        connections.delete_connection(ConnectionId="connection")
        return {}

    if request_token is None or type(request_token) is not str:
        connections.delete_connection(ConnectionId="connection")
        return {}

    response = tokens_table.get_item(Key={"token": request_token}).get("Item")

    if response is None:
        connections.delete_connection(ConnectionId="connection")
        return {}

    user = response["user"]
    token = response["token"]

    if user != request_user or token != request_token:
        connections_table.delete_item(Key={"connection": connection})
        connections.delete_connection(ConnectionId="connection")
        return {}

    connections_table.put_item(Item={"connection": connection, "user": user})

    response = {
        "type": "AuthenticateUserResponse",
        "user": user,
        "authenticated": True,
    }

    connections.post_to_connection(
        ConnectionId=connection,
        Data=json.dumps(response).encode()
    )

    return {}


@connection_functions.lambda_function(name="DisconnectUser")
def disconnect_user(event, context):
    connection = event["requestContext"]["connectionId"]
    connections.delete_connection(ConnectionId=connection)
    connections_table.delete_item(Key={"connection": connection})
    return {}
