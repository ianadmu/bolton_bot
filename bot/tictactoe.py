import random
import re


class Line:
    k = 3
    # k is a konstant weighting factor

    def __init__(self, length):
        self.length = length
        self.current_size = 0
        self.owner = 0

    def get_score(self, player):
        if player != -1 and self.length == self.current_size + 1:
            return float("inf")

        if player != self.owner:
            return (self.current_size + 1) ** Line.k

        return (self.current_size + 0.5) ** Line.k

    def play(self, player):
        # returns -1 when the line becomes impossible to win on
        # 1 on a victory
        # 0 on all other normal events
        if self.owner == 0:
            self.owner = player

        if self.owner != player:
            # this means that victory cannot happen on this line and
            # it should be removed
            self.owner = -1
            self.current_size = 0
        else:
            self.current_size += 1
            if self.current_size == self.length:
                return True
        return False

    def __str__(self):
        return ' >' + str(self.owner) + ' ' + str(self.current_size) + '<'


class BoardSpot:

    def __init__(self):
        self.value = 0
        self.lines = set()

    def play(self, player):
        if self.value == 0:
            self.value = player
            for line in self.lines:
                result = line.play(self.value)
                if result is True:
                    return True
        else:
            raise Exception(player + " Tried to override a spot on the board")

        return False

    def update_lines(self):
        self.lines = filter(lambda line: line.owner != -1, self.lines)

    def get_score(self, player):
        score = 0
        for line in self.lines:
            score += line.get_score(player)
        return score

    def get_token(self):
        return TicTacToe.tokens[self.value]

    def get_value(self):
        return self.value

    def change_tokens(self):
        TicTacToe.tokens[1], TicTacToe.tokens[2] = TicTacToe.tokens[2], TicTacToe.tokens[1]

    def __str__(self):
        lines_str = "Lines: "
        for line in self.lines:
            if line.owner != -1:
                lines_str += line.__str__()
        return lines_str + "\n" + self.get_token()

    def add_line(self, line):
        self.lines.add(line)


class TicTacToe:

    tokens = [' ', 'X', 'O']

    def __init__(self, size, line_size, game_type, players):
        if size < 3:
            size = 3
        elif size > 10:
            size = 10

        self.game_type = game_type
        self.line_size = line_size
        self.winner = False
        self.comp_player = 2
        self.players = dict()
        player_list = list(players)
        for player_num in range(len(player_list)):
            self.players[player_list[player_num]] = player_num + 1
        self.size = size
        self.turn = random.choice([True, False])
        self.board = [[BoardSpot() for x in range(size)] for y in range(size)]
        self.open_spots = self._get_all_spots()
        self.add_lines_to_board()
        if self.turn and self.game_type != "pvp":
            self._self_move(self.comp_player)

    def starting_message(self):
        player_string = ""
        for name in self.players:
            player_string += (
                name + " will be playing as " +
                TicTacToe.tokens[self.players[name]] + '\n'
            )

        player_string += (
            TicTacToe.tokens[2 - self.turn] + " will be going next"
        )
        return player_string

    def _play_self(self):
        end_message = "Cats Game!\n"
        while not self.is_over():
            self.turn = not self.turn
            self._self_move(2 - self.turn)
        if self.winner:
            end_message = TicTacToe.tokens[2 - self.turn] + " Won!\n"
        return(end_message + self.__str__())

    def process_command(self, message, player):
        player_num = self.players[player]
        if self.is_over():
            return "Game is over"
        elif self.game_type == "pvp" and (2 - self.turn) == player_num:
            if self.player_move(message, player_num):
                self.turn = not self.turn
                if self.winner:
                    return "You win!\n" + self.__str__()
                elif self.is_over():
                    return "Cats Game!\n" + self.__str__()
                return self.__str__()
        elif self.game_type == "comp":
            if self.player_move(message, player_num):
                self.turn = not self.turn
                if self.winner:
                    return "You win!\n" + self.__str__()
                elif self.is_over():
                    return "Cats Game!\n" + self.__str__()
                else:
                    self._self_move(self.comp_player)
                    if self.winner:
                        return "bolton wins!\n" + self.__str__()

                if self.is_over():
                    return "Cats Game!\n" + self.__str__()

                return self.__str__()

        return self._get_move_error(message, player_num)

    def is_over(self):
        return not self.open_spots or self.winner

    def add_lines_to_board(self):
        line_directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        # right now the lines are the same length as the board
        for x in range(self.size):
            for y in range(self.size):
                for direction in line_directions:
                    spots_in_line = self.get_spots_for_line(
                        (x, y), direction, self.line_size
                    )
                    line = Line(self.line_size)
                    for spot_to_add in spots_in_line:
                        spot_to_add.add_line(line)

    def get_spots_for_line(self, start, direction, length):
        # if the line would go over the board, an empty list is returned
        x = start[0]
        y = start[1]

        spots = []

        if (x + (direction[0] * length) > self.size or
                x + (direction[0] * length) < -1):
            return spots

        if (y + (direction[1] * length) > self.size or
                y + (direction[1] * length) < -1):
            return spots

        for step in range(length):
            current_x = x + (direction[0] * step)
            current_y = y + (direction[1] * step)
            spots.append(self.board[current_x][current_y])

        return spots

    def _self_move(self, player):
        comp_move = self._find_best_move()
        self.winner = self._move(player, comp_move)
        self._update_lines()

    def _update_lines(self):
        for spot in self.open_spots:
            spot.update_lines()

    def _move_randomly(self):
        return random.choice(self.open_spots)

    def _find_best_move(self):
        self.open_spots = (
            sorted(
                self.open_spots, key=lambda spot: spot.get_score(
                    self.comp_player
                ), reverse=True
            )
        )
        return self.open_spots[0]

    def _get_all_spots(self):
        spots = []
        for row in self.board:
            for spot in row:
                spots.append(spot)
        return spots

    def tokenize(self, spot):
        return spot.get_token()

    def __str__(self):
        middle = " | "
        line = '   ' + ('-' * ((4 * self.size) - 1))
        rows = []
        top_row = '    ' + "   ".join(map(str, range(self.size))) + '\n'
        for row_index in range(self.size):
            result = (
                '\n' + chr(ord('A') + row_index) + '   ' + middle.join(
                    map(self.tokenize, self.board[row_index])
                ) + '\n'
            )
            rows.append(result)

        return "```" + top_row + line.join(rows) + "```"

    def _move(self, player, spot):
        self.open_spots.remove(spot)
        return spot.play(player)

    def _getY(self, move):
        # don't even ask why these seem to be reversed
        # Leon here: whyyyyyyy?????
        numbers = re.sub('[^0-9]', '', move)
        if numbers:
            return int(numbers)
        else:
            return None

    def _getX(self, move):
        char = re.sub('[^A-Z]', '', move.upper())
        if char:
            return ord(char[0]) - ord('A')
        else:
            return None

    def _get_move_error(self, move, player_num):
        x = self._getX(move)
        y = self._getY(move)
        if self.game_type == "pvp" and (2 - self.turn) != player_num:
            return "It's not your turn"
        if x is None:
            return "You must have at least one letter"
        elif y is None:
            return "You must have at least one number"
        elif x > self.size:
            return "You must input a valid Row"
        elif y > self.size:
            return "You must input a valid Column"
        elif self.board[x][y] not in self.open_spots:
            return "You must select an empty spot"
        return "Unknown Error"

    def _parse_move(self, move):
        x = self._getX(move)
        y = self._getY(move)
        ok = (
            (
                x is None or y is None or x > self.size or x < 0 or
                y > self.size or y < 0
            ) or self.board[x][y] not in self.open_spots
        )
        if ok:
            return (None, None)
        return (x, y)

    def player_move(self, move, player):
        coordinates = self._parse_move(move)
        if None in coordinates:
            return False
        winner = self._move(player, self.board[coordinates[0]][coordinates[1]])
        self.winner = winner
        return True
