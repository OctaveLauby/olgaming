import importlib
import os
import pytest
import shutil

from olgaming import game
from olgaming.gameobj import GameObject
from olgaming.player import Player
from olgaming.players import Bot, Human


# --------------------------------------------------------------------------- #
# Parameters

TMP_DIR = "tmp"


# --------------------------------------------------------------------------- #
# Setup / Teardown

def setup_function(function):
    if os.path.exists(TMP_DIR):
        shutil.rmtree("tmp")

    importlib.reload(game)


def teardown_function(function):
    if os.path.exists(TMP_DIR):
        shutil.rmtree("tmp")


# --------------------------------------------------------------------------- #
# Tests


def test_game_cls():
    """Test game class."""

    game.Game.set("bot", Player)
    game.Game.set("human", Bot)
    with pytest.raises(TypeError):
        game.Game.set("bot", 1)

    assert game.Game.bot == Player
    assert game.Game.human == Bot


def test_game_skeleton():
    """Test Skeleton only."""

    ginstance = game.Game(
        bots=[1],
        rewards={'win': 10, 'tie': -3},
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

    # ---- Rewards
    assert ginstance.rewards == {
        'lose': -10,
        'neutral': 0,
        'tie': -3,
        'win': 10,
    }
    assert ginstance.dft_consequences() == [0, 0]

    # ---- Environment
    assert ginstance.status() == {
        'over': False,
        'player': 0,
        'winners': [],
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
        'winners': [],
    }
    assert ginstance.dft_consequences() == [-3, -3]

    ginstance.next()
    ginstance.new_winner(ginstance.players[0])
    assert ginstance.status() == {
        'over': True,
        'player': 0,
        'winners': [0],
    }
    assert ginstance.dft_consequences() == [10, -10]

    ginstance._winners = set()
    ginstance.new_winner(1)
    assert ginstance.dft_consequences() == [-10, 10]

    ginstance.new_winner(0)
    assert ginstance.dft_consequences() == [10, 10]

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

    # ---- Errors

    with pytest.raises(KeyError):
        game.Game(
            rewards={'unexistant case': 3}
        )

    with pytest.raises(ValueError):
        game.Game(
            bots=[2],
        )


def test_game_use():
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
                self.new_winner(0)
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
    assert ginstance.status() == {'over': True, 'player': 0, 'winners': [0]}

    # ---- Save / Load
    save_dir = os.path.join(TMP_DIR, "test_2_game")
    ginstance.save(save_dir)
    ninstance = MyGame()
    ninstance.load(save_dir)
    assert ninstance.state() == ["a", "human", "a", "human"]
    assert ninstance.status() == {'over': True, 'player': 0, 'winners': [0]}
