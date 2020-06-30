"""Tic Tac Toe game.

Conversation between the 2 players.
"""
from olgaming.game import Game, InvalidAction


BOARD_FRMT = (
    "+---+---+---+\n"
    "| 0 | 1 | 2 |\n"
    "+---+---+---+\n"
    "| 3 | 4 | 5 |\n"
    "+---+---+---+\n"
    "| 6 | 7 | 8 |\n"
    "+---+---+---+"
)

SYMBOLS = {
    0: "\u26f1",
    1: "\u26c4",
}


class TicTacToe(Game):
    """Tic Tac Toe board game.

    2 players, 3x3 board. Player 1 draws O, player 2 draws X, first player with
    3 successive symbols (line, column or diag) wins.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = [None for _ in range(3*3)]
        self.player_symbols = {
            str(self.players[index]): value
            for index, value in SYMBOLS.items()
        }

    # ----------------------------------------------------------------------- #
    # Utils

    def av_actions(self):
        """Return available actions."""
        return [
            str(i) for i, player in enumerate(self.board) if player is None
        ]

    def refresh(self):
        """Refresh status of game"""
        pass

    def state(self):
        """Return current game state."""
        return tuple(
            None if player is None else player.index
            for player in self.board
        )

    # ----------------------------------------------------------------------- #
    # Gameplay

    def act(self, action):
        """Operate action (as current player).

        Returns:
            (list): consequences for each player
        """
        # Check action
        try:
            position = int(action)
            assert 0 <= position < 3 * 3
        except (AssertionError, ValueError):
            raise InvalidAction(action, "position must be within [0, 8]")

        if self.board[position] is not None:
            raise InvalidAction(action, "position already played")

        # Update board
        self.log.debug(
            "Player %s has played on position %s",
            self.player, position
        )
        self.board[position] = self.player

        # Check if player has won
        for combination in [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]:
            succession = [self.board[index] for index in combination]
            if succession == [self.player for _ in range(3)]:
                self.raise_endflag()
                self.new_winner(self.player)

        if None not in self.board:
            self.raise_endflag()

        return self.dft_consequences()

    # ----------------------------------------------------------------------- #
    # Display

    def board_str(self):
        """Return board string."""
        to_replace = {
            str(position): SYMBOLS[player.index]
            for position, player in enumerate(self.board)
            if player is not None
        }
        self.log.debug("Played positions: %s", str(to_replace))
        board_str = BOARD_FRMT
        for position, player in to_replace.items():
            board_str = board_str.replace(position, player)
        return board_str

    def display(self):
        """Display game."""
        print(self.board_str())
        print(
            "Symbols: %s |" % " | ".join(
                map(
                    lambda item: "%s=%s" % item,
                    self.player_symbols.items()
                )
            )
        )
        print("# Available option are: %s" % ", ".join(self.av_actions()))
