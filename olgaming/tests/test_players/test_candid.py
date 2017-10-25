from olgaming.player import Player
from olgaming.players import candid


def test_candid():

    player = candid.Candid(index=1)

    assert isinstance(player, Player)
    assert player.action("gstate", actions=[1, 2, 3, 4]) == 1
    assert player.action("gstate", actions=[2, 3, 4]) == 2
    assert player.action("gstate", actions=[4, 3]) == 4

    player.take("food")
    player.take("decision")
    player.take("correction")
    assert player.consequences == ["food", "decision", "correction"]
