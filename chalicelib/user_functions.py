import secrets

from chalice import Blueprint

from chalicelib.app_resources import tokens_table, users_table

user_functions = Blueprint(__name__)


@user_functions.lambda_function(name="create_anonymous_user")
def create_anonymous_user(event, context):
    user_id = secrets.token_urlsafe(32)
    token_value = secrets.token_urlsafe(32)

    user = {
        "user": user_id,
        "anonymous": True,
    }

    token = {
        "token": token_value,
        "user": user_id,
    }

    users_table.put_item(Item=user)

    tokens_table.put_item(Item=token)

    return token
