from flask import Flask, render_template, redirect, session
import uuid
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

class Player:
    """
    This class is responsible for help storing player information.
    """
    # Player info
    uuid = None
    room = None
    religion = None
    first_card = None
    second_card = None
    coins = None

    def __init__(self, room, religion, first_card, second_card, coins):
        """Game player constructor"""
        self.uuid = str(uuid.uuid4())
        self.room = room
        self.religion = religion
        self.first_card = first_card
        self.second_card = second_card
        self.coins = coins

    def get_uuid(self):
        """Get player uuid"""
        return str(self.uuid)

class Game:
    """
    This class is responsible for the entire game logic. 

    Please read https://www.ultraboardgames.com/coup/reformation.php for more info.
    """
    # Game info
    uuid = None
    players = 0

    # Game cards
    duke = 6
    assassin = 6
    countess = 6
    captain = 6
    ambassador = 6
    inquisitor= 6


    def __init__(self, players):
        """Game room constructor"""
        self.uuid = str(uuid.uuid4())
        self.players = players

    def get_uuid(self):
        """Get room uuid"""
        return str(self.uuid)

    def add_player(self):
        """Add players to the game"""
        return
    

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
        self.running_games[game.get_uuid()] = game
        return game.get_uuid()
    
    def get_room(self, room):
        """Get a game context information (a room)"""
        if room not in self.running_games:
            return None
            
        return True

    def init_player(self, room):
        """Add a new player to the game"""
        self.running_games[room].add_player()

        # lalalala add session variables

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
    
    if session.get('room') == None:
        session['room'] = uuid
        game_server.init_player(uuid)

    return render_template("room.html")

# Setup the game
if __name__ == '__main__':
    # Start the server
    global game_server
    game_server = Server()

    # Start the web server
    app.run(port=5000, debug=True)