from olgaming.games.dummy.dummy import Dummy


def test_dummy():

    game = Dummy(bots=[1], loglvl="DEBUG")
    player_1, player_2 = game.players

    assert game.state() == {'msg_sent': 0}
    assert game.players_n == 2
    actions = game.av_actions()
    actions.sort()
    assert actions == ["1", "2", "3", "4"]
    assert game.status() == {
        'player': 0,
        'over': False,
        'winners': [],
    }

    assert game.act("1") == [
        "<s>%s</s>" % "hi",
        "<r>%s</r>" % "hi",
    ]
    game.next()
    assert game.act("3") == [
        "<r>%s</r>" % "i am a cow",
        "<s>%s</s>" % "i am a cow",
    ]
    game.next()
    assert game.act("4") == [
        "<s>%s</s>" % "i am a monkey",
        "<r>%s</r>" % "i am a monkey",
    ]
    game.next()

    assert game.state() == {'msg_sent': 3}
    assert game.status() == {
        'player': 1,
        'over': False,
        'winners': [],
    }

    assert game.act("2") == [
        "<r>%s</r>" % "bye",
        "<s>%s</s>" % "bye",
    ]
    game.next()

    assert game.state() == {'msg_sent': 4}
    assert game.status() == {
        'player': 0,
        'over': True,
        'winners': [1],
    }
