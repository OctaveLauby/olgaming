import pytest

from olgaming import player
from olgaming.gameobj import GameObject


def test_player():

    player1 = player.Player(index=8)
    player2 = player.Player(6, loglvl="DEBUG")

    assert player1.index == 8
    assert player2.index == 6
    assert isinstance(player1, GameObject)
    assert player1.requires_visual is False
    assert player1.name == "Player_1"
    assert player2.name == "Player_2"
    assert player2.get_loglvl() == 10

    with pytest.raises(NotImplementedError):
        player1.action("gstate")

    assert player2.take("consequence") is None

    # Test communication

    assert player1.last_observation is None
    player1.receive({'verb': "observe", 'content': "an_observation"})
    assert player1.last_observation == "an_observation"
    player1.receive({'verb': "observe", 'content': "new_observation"})
    assert player1.last_observation == "new_observation"

    assert player1.last_reward is None
    player1.receive({'verb': "reward", 'content': 1})
    assert player1.last_reward == 1
    player1.receive({'verb': "reward", 'content': 2})
    assert player1.last_reward == 2

    with pytest.raises(TypeError):
        player1.receive(12)

    with pytest.raises(ValueError):
        player1.receive({'verb': "create_a_wormhole"})

    with pytest.raises(KeyError):
        player1.receive({'verb': "reward", 'value': 12})
    assert player1.last_reward == 2
