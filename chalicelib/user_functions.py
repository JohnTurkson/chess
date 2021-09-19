from chalice import Blueprint

from chalicelib.app_resources import tokens_table, users_table
from chalicelib.app_utilities import generate_id

user_functions = Blueprint(__name__)


@user_functions.lambda_function(name="CreateAnonymousUser")
def create_anonymous_user(event, context):
    user_id = generate_id()
    token_value = generate_id()

    user = {
        "user": user_id,
        "isAnonymous": True,
    }

    token = {
        "user": user_id,
        "token": token_value,
    }

    response = {"type": "CreateAnonymousUserResponse"} | token

    users_table.put_item(Item=user)

    tokens_table.put_item(Item=token)

    return response
