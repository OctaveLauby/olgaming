import pytest

from olgaming import player
from olgaming.gameobj import GameObject


def test_player():

    player1 = player.Player()
    player2 = player.Player(loglvl="DEBUG")

    assert isinstance(player1, GameObject)
    assert player1.requires_visual is False
    assert player1.name == "Player_1"
    assert player2.name == "Player_2"
    assert player2.get_loglvl() == 10

    with pytest.raises(NotImplementedError):
        player1.action("gstate")

    assert player2.take("consequence") is None
