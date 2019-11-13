import random

_lines = [
    [1, 1, 1,
     0, 0, 0,
     0, 0, 0],
    [1, 0, 0,
     0, 1, 0,
     0, 0, 1],
    [1, 0, 0,
     1, 0, 0,
     1, 0, 0],
    [0, 1, 0,
     0, 1, 0,
     0, 1, 0],
    [0, 0, 1,
     0, 1, 0,
     1, 0, 0],
    [0, 0, 1,
     0, 0, 1,
     0, 0, 1],
    [0, 0, 0,
     1, 1, 1,
     0, 0, 0],
    [0, 0, 0,
     0, 0, 0,
     1, 1, 1]
]

_RED  = 'r'
_BLUE = 'b'

_ROWS    = 6
_COLUMNS = 7

class ConnectFour:

    # Private variables

    @property
    def _reds(self):
        return self._board[:(_ROWS * _COLUMNS)]

    @property
    def _blues(self):
        return self._board[(_ROWS * _COLUMNS):]

    # Constructors

    def __init__(self, turn=None):
        if turn is None:
            self._turn = bool(random.getrandbits(1))
        else:
            self._turn = bool(turn)

        self._player = _RED if self._turn else _BLUE
        self._board = [0.0] * _ROWS * _COLUMNS * 2

    @staticmethod
    def _createFromState(state):
        if len(state) < _ROWS * _COLUMNS * 2 + 1:
            raise ValueError("state array not large enough, expected {}, got {}".format(_ROWS * _COLUMNS * 2 + 1, len(state)))
        ret = ConnectFour()
        ret._board = state[0:(_ROWS * _COLUMNS * 2)]
        ret._turn = True if state[(_ROWS * _COLUMNS * 2) + 1] == 1.0 else False

        return ret

    # Public methods

    def state(self):
        # TODO If we think of changing this to a CNN, then we should use [self._turn] * 9
        #       - AlphaGo does this
        return self._board + [1.0 if self._turn else 0.0]

    def board(self):
        ret = [None] * _ROWS * _COLUMNS

        for index in range(0, _ROWS * _COLUMNS):
            if self._reds[index] == 1.0:
                ret[index] = _RED
            elif self._blues[index] == 1.0:
                ret[index] = _BLUE

        return ret

    def player(self):
        return self._player

    def opponent(self):
        return _RED if self._player == _BLUE else _BLUE

    def isOurTurn(self):
        return self._turn

    def possibleMoves(self):
        if self.isFinished():
            return []

        board = self.board()
        return [column for column in range(0, _COLUMNS) if None in board[(column * _ROWS):((column + 1) * _ROWS)]]

    def playMove(self, column):
        if not self.__isValidMove(column):
            raise IndexError
        if self.isFinished():
            raise Exception("Game finished")

        # Our board is upside down for easiness :)
        board = self.board()
        row = board[(column * _ROWS):((column + 1) * _ROWS)].index(None)

        self._board[(0 if self._turn else _ROWS * _COLUMNS) + (column * _ROWS + row)] = 1.0
        self._turn = not self._turn

    def isFinished(self):
        return self.getWinner() is not None or self.isDraw()

    def isDraw(self):
        return self._board.count(1.0) == _ROWS * _COLUMNS * 2

    def getWinner(self):
        board = self.board()
        for column in range(0, _COLUMNS):
            for row in range(0, _ROWS):
                if board[column * _ROWS + row] is None:
                    continue
                player = board[column * _ROWS + row]
                if column - 3 >= 0 and all([board[index] == player for index in range((column - 3) * _ROWS + row, column * _ROWS + row + 1, _ROWS)]):
                    return player
                if column + 3 < _COLUMNS and all([board[index] == player for index in range(column * _ROWS + row, (column + 3) * _ROWS + row + 1, _ROWS)]):
                    return player
                if row - 3 >= 0 and all([square == player for square in board[(column * _ROWS + (row - 3)):(column * _ROWS + row + 1)]]):
                    return player
                if row + 3 < _ROWS and all([square == player for square in board[(column * _ROWS + row):(column * _ROWS + (row + 3) + 1)]]):
                    return player
                if column - 3 >= 0 and row - 3 >= 0 and all([board[index] == player for index in range(column - 3 * _ROWS + row - 3, column * _ROWS + row + 1, _ROWS + 1)]):
                    return player
                if column - 3 >= 0 and row + 3 < _ROWS and all([board[index] == player for index in range(column - 3 * _ROWS + row, column * _ROWS + row + 3 + 1, _ROWS - 1)]):
                    return player
                if column + 3 < _COLUMNS and row - 3 >= 0 and all([board[index] == player for index in range(column * _ROWS + row - 3, (column + 3) * _ROWS + row + 1, _ROWS - 1)]):
                    return player
                if column + 3 < _COLUMNS and row + 3 < _ROWS and all([board[index] == player for index in range(column * _ROWS + row, (column + 3) * _ROWS + row + 3 + 1, _ROWS + 1)]):
                    return player
        # No winner, either a draw or not finished
        return None

    def score(self):
        if self.isDraw():
            return 0.0

        winner = self.getWinner()

        if winner is None:
            return 0.0

        return 1.0 if winner == self._player else -1.0

    # Private methods

    def __isValidMove(self, column):
        return column >= 0 and column < 9 and self.__isColumnFree(column)

    def __isColumnFree(self, column):
        return None in self.board()[(column * _ROWS):((column + 1) * _ROWS)]

    def _almostWinners(self):
        tempGame = ConnectFour._createFromState(self.state())
        # TODO

    def _possibleForks(self):
        winners = self._almostWinners()
        # TODO

    def __repr__(self):
        return str(self)

    def __str__(self):
        ret = "\n".join([
            "CONNECT FOUR",
            "Our token: {}".format(self._player),
            ""
        ])
        if self.isFinished():
            ret += "Game Over: {} won\n".format(self.getWinner())
        else:
            ret += "Current turn: {}\n".format(_RED if self._turn else _BLUE)

        board = self.board()

        for row in range(_ROWS - 1, -1, -1):
            ret += "+---" * _COLUMNS + "+\n"
            ret += "|   " * _COLUMNS + "|\n"

            for column in range(0, _COLUMNS):
                square = board[column * _ROWS + row]
                ret += "| " + (" " if square is None else square) + " "
            ret += "|\n"

            ret += "|   " * _COLUMNS + "|\n"
        ret += "+---" * _COLUMNS + "+\n"

        return ret
