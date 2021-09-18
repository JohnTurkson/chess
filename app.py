from chalice import Chalice

from chalicelib.connection_functions import connection_functions
from chalicelib.game_functions import game_functions
from chalicelib.matchmaking_functions import matchmaking_functions
from chalicelib.user_functions import user_functions

app = Chalice(app_name="chess")

app.register_blueprint(connection_functions)
app.register_blueprint(game_functions)
app.register_blueprint(matchmaking_functions)
app.register_blueprint(user_functions)
