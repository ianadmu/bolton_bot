class Game:

    def __init__(self, game, players):
        self.game = game

    def process_command(self, message, player):
        return self.game.process_command(message, player)


class GameManager:

    def __init__(self, msg_writer):
        self.games = dict()
        self.msg_writer = msg_writer

    def _make_key(self, players, channel, game_name):
        return channel + game_name + str(sorted(players))

    def add_game(self, game, players, channel, game_name):
        # game should be initialized here
        key = self._make_key(players, channel, game_name)
        self.games[key] = Game(game, players)
        self.msg_writer.send_message(str(game), channel)

    def process_message(
        self, players, channel, game_name, message, current_player
    ):
        # the message needs to be parsed earlier up in the process
        # this is making no assumptions about what information the game needs
        key = self._make_key(players, channel, game_name)
        if key in self.games:
            game = self.games[key]
            result = game.process_command(message, current_player)
            self.msg_writer.send_message(result, channel)
        else:
            error_msg = ("There is currently no game that can be selected "
                         "with the information provided\n")
            self.msg_writer.send_message(error_msg, channel)
