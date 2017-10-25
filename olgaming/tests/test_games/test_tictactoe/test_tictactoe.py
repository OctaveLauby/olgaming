from olgaming.players import Candid
from olgaming.games.tictactoe.tictactoe import TicTacToe


def test_tictactoe_candidgame():

    # ---- Change default Bot into straight forward bot

    TicTacToe.set('bot', Candid)

    game = TicTacToe(
        bots=[0, 1],
        rewards={'win': 5, 'lose': -10, 'neutral': 0},
        loglvl="DEBUG",
    )

    assert game.state() == [None] * 9
    assert game.av_actions() == [str(i) for i in range(9)]
    assert game.board_str() == (
        "+---+---+---+\n"
        "| 0 | 1 | 2 |\n"
        "+---+---+---+\n"
        "| 3 | 4 | 5 |\n"
        "+---+---+---+\n"
        "| 6 | 7 | 8 |\n"
        "+---+---+---+"
    )

    game.play()
    assert game.state() == [0, 1, 0, 1, 0, 1, 0, None, None]
    assert game.av_actions() == ["7", "8"]
    assert game.board_str() == (
        "+---+---+---+\n"
        "| O | X | O |\n"
        "+---+---+---+\n"
        "| X | O | X |\n"
        "+---+---+---+\n"
        "| O | 7 | 8 |\n"
        "+---+---+---+"
    )

    player_1, player_2 = game.players
    assert game.status() == {
        'player': 1,
        'over': True,
        'winners': [0],
    }
    assert player_1.consequences == [0, 0, 0, 0, 0, 0, 5]
    assert player_2.consequences == [0, 0, 0, 0, 0, 0, -10]
