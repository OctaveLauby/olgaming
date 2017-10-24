import os
import pytest
import shutil

from olgaming import game
from olgaming.gameobj import GameObject
from olgaming.players import Bot, Human


# --------------------------------------------------------------------------- #
# Parameters

TMP_DIR = "tmp"


# --------------------------------------------------------------------------- #
# Setup / Teardown

def setup_function(function):
    if os.path.exists(TMP_DIR):
        shutil.rmtree("tmp")


def teardown_function(function):
    if os.path.exists(TMP_DIR):
        shutil.rmtree("tmp")


# --------------------------------------------------------------------------- #
# Tests


def test_game_1():
    """Test Skeleton only."""

    ginstance = game.Game(
        bots=[1],
        p_params={'loglvl': "INFO"},
        loglvl="DEBUG",
    )

    # ---- Players
    assert isinstance(ginstance, GameObject)
    assert ginstance.get_loglvl() == 10
    assert ginstance.players[0].get_loglvl() == 20
    assert ginstance.players[1].get_loglvl() == 20
    assert ginstance.player.name == "Human_1"

    assert isinstance(ginstance.players[0], Human)
    assert isinstance(ginstance.players[1], Bot)

    # ---- Environment
    assert ginstance.status() == {
        'over': False,
        'player': 0,
    }
    assert ginstance.state() == []
    assert ginstance.av_actions() is None
    assert ginstance.is_over() is False

    # ---- Actions on environment
    ginstance.next()
    assert ginstance.player.name == "Bot_1"
    ginstance.next()
    assert ginstance.player.name == "Human_1"

    ginstance.next()
    ginstance.raise_endflag()
    assert ginstance.is_over() is True
    assert ginstance.status() == {
        'over': True,
        'player': 1,
    }

    ginstance.next()
    assert ginstance.status() == {
        'over': True,
        'player': 0,
    }

    with pytest.raises(NotImplementedError):
        ginstance.act("action")

    with pytest.raises(NotImplementedError):
        ginstance.display()

    # ---- Save / Load
    save_dir = os.path.join(TMP_DIR, "test_1_game")

    ginstance.save(save_dir)
    assert os.path.exists(os.path.join(save_dir, game.STATE_FILE))
    assert os.path.exists(os.path.join(save_dir, game.STATUS_FILE))

    ninstance = game.Game()
    ninstance.load(save_dir)
    assert ninstance.status() == ginstance.status()


def test_game_2():
    """Test use of skeleton."""

    class MyGame(game.Game):

        actions = ["a"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.hist = []

        def act(self, action):
            """Add action to history until hist len >= 4."""
            self.hist.append(action)
            if len(self.hist) >= 4:
                self.raise_endflag()
            return [None, None]

        def display(self):
            """Display history."""
            print("Game is on, history is %s" % self.hist)

        def load_state(self, state):
            """Load state."""
            print(state)
            self.hist = state

        def state(self):
            """Return state."""
            return self.hist

    ginstance = MyGame(bots=[0], loglvl="DEBUG")

    # ---- Players
    assert isinstance(ginstance.players[0], Bot)
    assert isinstance(ginstance.players[1], Human)

    # ---- Play
    from olgaming.players import human
    human.input = lambda x: "human"
    ginstance.play()
    assert ginstance.state() == ["a", "human", "a", "human"]
    assert ginstance.status() == {'over': True, 'player': 0}

    # ---- Save / Load
    save_dir = os.path.join(TMP_DIR, "test_2_game")
    ginstance.save(save_dir)
    ninstance = MyGame()
    ninstance.load(save_dir)
    assert ninstance.state() == ["a", "human", "a", "human"]
    assert ninstance.status() == {'over': True, 'player': 0}
