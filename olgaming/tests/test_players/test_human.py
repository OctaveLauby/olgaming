from olgaming.player import Player
from olgaming.players import human


# --------------------------------------------------------------------------- #
# Tests

def test_human():

    player = human.Human()

    assert isinstance(player, Player)

    human.input = lambda x: "test"
    assert player.action("gstate") == "test"
    human.input = lambda x: "2"
    assert player.action("gstate") == "2"

    assert player.take("consequence") is None
