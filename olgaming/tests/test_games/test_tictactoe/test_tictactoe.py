import importlib
import pytest

from olgaming.players import Candid
from olgaming.games.tictactoe import tictactoe


def setup_function(function):
    importlib.reload(tictactoe)


def test_tictactoe_candidgame():

    # ---- Change default Bot into straight forward bot

    tictactoe.TicTacToe.set('bot', Candid)

    game = tictactoe.TicTacToe(
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


def test_tictactoe_playbyplay():

    game = tictactoe.TicTacToe(
        loglvl="DEBUG",
    )

    game.act("4")
    game.next()

    with pytest.raises(tictactoe.InvalidAction):
        game.act("4")

    for action in ["2", "3", "5"]:
        game.act(action)
        game.next()

    assert game.board_str() == (
        "+---+---+---+\n"
        "| 0 | 1 | X |\n"
        "+---+---+---+\n"
        "| O | O | X |\n"
        "+---+---+---+\n"
        "| 6 | 7 | 8 |\n"
        "+---+---+---+"
    )
    assert not game.is_over()

    for action in ["1", "8"]:
        game.act(action)
        game.next()

    assert game.board_str() == (
        "+---+---+---+\n"
        "| 0 | O | X |\n"
        "+---+---+---+\n"
        "| O | O | X |\n"
        "+---+---+---+\n"
        "| 6 | 7 | X |\n"
        "+---+---+---+"
    )
    assert game.status() == {
        'player': 0,
        'over': True,
        'winners': [1],
    }


def test_tictactoe_tie():

    game = tictactoe.TicTacToe(
        loglvl="DEBUG",
    )

    for action in ["0", "1", "3", "4", "2", "6", "5", "8", "7"]:
        game.act(action)
        game.next()

    assert game.is_over()
    assert game.winners == []
