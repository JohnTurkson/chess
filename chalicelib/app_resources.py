import boto3

dynamodb = boto3.resource(service_name="dynamodb")
connections = boto3.client(
    service_name="apigatewaymanagementapi",
    region_name="ca-central-1",
    endpoint_url="",
)

connections_table = dynamodb.Table("chess-active-user_connections")
connections_by_user_index = "chess-active-user_connections-by_user"

game_moves_table = dynamodb.Table("chess-active-game_moves")
game_statuses_table = dynamodb.Table("chess-active-game_statuses")

users_table = dynamodb.Table("chess-active-users")

tokens_table = dynamodb.Table("chess-active-user_tokens")
