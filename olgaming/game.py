"""Skeleton for games.

Basically a game is:
    - A list of players playing one after the other
    - Each player perform an action
    - Each action change the state of the game
    - Each action has consequences on every players

Vocabulary:
    - environement: complete description of game (and players)
    - state:    descr of how the game looks like
                e.g. where are the pawns
    - status:   where the game is at
                e.g. who is playing, is it over
"""
import os

from olutils.tools import load, save
from .gameobj import GameObject
from .player import Player
from .players import Bot, Human


STATE_FILE = "state.pickle"
STATUS_FILE = "status.json"


class InvalidAction(Exception):
    """Exception raised when an invalid action is tried."""
    pass


class Game(GameObject):
    """Game Skeleton

    Methods raising NotImplementedError must be implemented.
    """
    actions = None  # Possible actions
    bot = Bot       # Class used to build bots
    human = Human   # Class used to build humans
    players_n = 2   # Number of players in game

    @classmethod
    def set(cls, param, value):
        """Set class attribute to value."""
        if param in ["bot", "human"]:
            if not (isinstance(value, type) and issubclass(value, Player)):
                raise TypeError(
                    "Param %s must be set to Player subclass, got %s"
                    % (param, repr(value))
                )
        else:
            raise ValueError(
                "Parameter %s can't be set" % (param)
            )
        setattr(cls, param, value)

    # ----------------------------------------------------------------------- #
    # Initialisation and properties

    def __init__(self, bots=None, p_params=None, **params):
        """Init a game.

        Args:
            bots        (list): index of players to replace with bots
            load_path   (str):  path where game can be loaded from
            p_params    (dict): key arguments for players
            params      (dict): key arguments for game object

            @see .gameobj.GameObject.params
        """
        super().__init__(**params)

        # Players
        if p_params is None:
            p_params = {}
        if bots is None:
            bots = []
        self._players = [
            self.__class__.bot(index, **p_params)
            if player in bots
            else self.__class__.human(index, **p_params)

            for index, player in enumerate(range(self.__class__.players_n))
        ]

        # Status
        self._player = 0    # Current player
        self._over = False
        self.winner = None

    @property
    def players(self):
        """Return list of players."""
        return self._players

    @property
    def player(self):
        """Return current player."""
        return self.players[self._player]

    def status(self):
        """Return status of game."""
        return {
            'player': self._player,
            'over': self._over,
        }

    # ----------------------------------------------------------------------- #
    # Utils

    def av_actions(self):
        """Return available actions."""
        return self.actions

    def is_over(self):
        """Return whether game is over."""
        return self._over

    def raise_endflag(self):
        """Raise end flag."""
        self._over = True

    def refresh(self):
        """Refresh environement if necessary."""
        pass

    def state(self):
        """Return current game state."""
        self.log.warning("Game has no state")
        return []

    # ----------------------------------------------------------------------- #
    # Gameplay

    def act(self, action):
        """Operate action (as current player).

        Returns:
            (list): consequences for each player
        """
        raise NotImplementedError

    def next(self):
        """Go to next player."""
        self._player += 1
        if self._player >= self.__class__.players_n:
            self._player = 0

    def play(self):
        """Play game until game is over."""
        self.log.debug("Game started")
        while not self.is_over():

            # Current Player
            cplayer = self.player
            self.log.debug("%s turn", cplayer)

            # Display game if player requires it
            if cplayer.requires_visual:
                self.display()

            # Catch and apply player action
            action = self.player.action(
                gstate=self.state(),
                actions=self.av_actions(),
            )
            try:
                consequences = self.act(action)
            except InvalidAction:
                self.log.warning(
                    "%s performed invalid action: %s",
                    cplayer, action
                )
                continue

            # Reverberate consequences on players
            self.log.debug("Apply consequences to players")
            assert len(consequences) == self.__class__.players_n
            for player, consequence in zip(self.players, consequences):
                player.take(consequence)

            # Refresh game and move on
            self.refresh()
            self.next()

        if self.winner is None:
            self.log.info("Tie Game")
        else:
            self.log.info("Winner is %s" % self.winner)

    # ----------------------------------------------------------------------- #
    # Display

    def display(self):
        """Display game."""
        raise NotImplementedError

    # ----------------------------------------------------------------------- #
    # Save / Load

    def load_state(self, state):
        """Load state."""
        self.log.warning("Ignoring state %s", state)

    def load_status(self, status):
        """Load status dictionary."""
        self._over = status['over']
        self._player = status['player']

    def load(self, load_path):
        """Load game environement from file."""
        file_path = os.path.join(load_path, STATE_FILE)
        state = load(file_path)
        self.load_state(state)

        file_path = os.path.join(load_path, STATUS_FILE)
        status = load(file_path)
        self.load_status(status)

    def save(self, save_path):
        """Save game environement."""
        state = self.state()
        file_path = os.path.join(save_path, STATE_FILE)
        save(state, file_path)

        status = self.status()
        file_path = os.path.join(save_path, STATUS_FILE)
        save(status, file_path)
