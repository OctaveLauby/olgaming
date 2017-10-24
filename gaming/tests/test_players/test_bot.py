from random import seed

from gaming.player import Player
from gaming.players import bot


def test_bot():

    player = bot.Bot()

    assert isinstance(player, Player)

    seed(8)
    assert player.action("gstate", actions=[1, 2, 3, 4]) == 2
    assert player.action("gstate", actions=[1, 2, 3, 4]) == 3
    assert player.action("gstate", actions=[1, 2, 3, 4]) == 4
    assert player.action("gstate", actions=[1, 2, 3, 4]) == 2

    assert player.take("consequence") is None
