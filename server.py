from flask import Flask, render_template, redirect
import uuid

app = Flask(__name__)

class Game:
    """
    This class is responsible for the entire game logic. 

    Please read https://www.ultraboardgames.com/coup/reformation.php for more info.
    """
    # Game identifier
    uuid = None
    players = 0

    # Game cards


    def __init__(self, players):
        self.uuid = str(uuid.uuid4())
        self.players = players

    def get_uuid(self):
        return str(self.uuid)
    

class Server:
    """
    This class will manage different games in the same server.
    """

    # server properties, in the future some of them gonna be environment variables
    max_current_games = 1
    current_games = 0
    max_players = 10
    min_players = 3
    running_games = {}
 
    def is_full(self):
        """Check if the server is full"""

        return self.current_games >= self.max_current_games

    def out_of_players_range(self, n):
        """Check if the game exceeds max number of players"""

        if int(n) <= self.max_players and int(n) >= self.min_players:
            return False
        return True
    
    def init_game(self, players):
        """Create new game for the given number of players, each game is a room"""
        players = int(players)
        game = Game(players)
        self.running_games[game.get_uuid()] = True
        return game.get_uuid()
    
    def get_room(self, room):
        """Get a game context information (a room)"""
        if room not in self.running_games:
            return None
        return True

# Start the server
game_server = None

# This is the main route and must be used to create a new game
@app.route('/', methods=['GET'])
def game_setup():
    global game_server
    if game_server.is_full() == True:
        return render_template("error.html", error_message="Thanks for playing, but this server is already full")
    return render_template("setup.html")

# This route should be used to build new games
@app.route('/init/<players>', methods=['GET'])
def game_init(players):
    global game_server
    if game_server.is_full() == True:
        return render_template("error.html", error_message="Thanks for playing, but this server is already full")
    elif game_server.out_of_players_range(players):
        return render_template("error.html", error_message="This number of players is out of game permitted range")
    
    new_room = game_server.init_game(players)
    return redirect('/room/'+new_room, code=302)

# Each room will be displayed in this endpoint
@app.route('/room/<uuid>', methods=['GET'])
def game_room(uuid):
    global game_server
    if game_server.get_room(uuid) == None:
        return render_template("error.html", error_message="Seems that this room doesn't exists!")

    return render_template("room.html")

# Setup the game
if __name__ == '__main__':
    global game_server

    # Start the game server
    global_server = Server()

    # Start the web server
    app.run(port=5000, debug=True)