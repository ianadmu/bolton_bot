import re
from tictactoe import TicTacToe


class TicTacToeManager:

    name = "TicTacToe"
    size_command = "size="
    length_command = "length="
    bolton_command = "comp"
    pvp_command = "pvp"

    help_message = (
        "To talk to the TicTacToe manager type a sentence that starts with "
        "'tictactoe' or 'ttt'\n"
        "To start a game agaisnt bolton, type start as the second word, "
        "followed by the size of the square board, and the length required "
        "to win\n"
        "To play a move, type where you would like to go as the second word\n"
        "To have bolton play himself, type self instead of start")

    def __init__(self, msg_writer, user_manager, game_manager):
        self.game_manager = game_manager
        self.user_manager = user_manager
        self.msg_writer = msg_writer

    def get_message(self, channel, message, user):
        players = self.user_manager.get_users_mentioned(message)
        players.add(user)
        if len(players) > 2:
            self.msg_writer.send_message(
                "You may not have more than two players currently", channel
            )
            return
        tokens = message.split()
        size = 3
        length = 3
        match_type = False
        move = ""
        for token in tokens:
            if TicTacToeManager.size_command in token:
                numbers = re.search(r'\d+', token)
                if numbers:
                    size = int(re.search(r'\d+', token).group())
            elif TicTacToeManager.length_command in token:
                numbers = re.search(r'\d+', token)
                if numbers:
                    length = int(re.search(r'\d+', token).group())
            elif token == TicTacToeManager.bolton_command:
                match_type = TicTacToeManager.bolton_command
            elif token == TicTacToeManager.pvp_command:
                match_type = TicTacToeManager.pvp_command
            else:
                move = token

        if match_type:
            game = TicTacToe(size, length, match_type, players)
            self.game_manager.add_game(
                game, players, channel, TicTacToeManager.name
            )
            self.msg_writer.send_message(game.starting_message(), channel)
        else:
            self.game_manager.process_message(
                players, channel, TicTacToeManager.name, move, user
            )
