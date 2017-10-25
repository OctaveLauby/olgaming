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

from olutils.params import read_params
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

    dft_rewards = {
        "win": 5,
        "tie": 3,
        "lose": -10,
        "neutral": 0,
    }

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

    def __init__(self, rewards=None, bots=None, p_params=None, **params):
        """Init a game.

        Args:
            bots        (list): index of players to replace with bots
            rewards     (dict): dict of rewards (lose, win, tie or neutral)
            load_path   (str):  path where game can be loaded from
            p_params    (dict): key arguments for players
            params      (dict): key arguments for game object

            @see .gameobj.GameObject.params
        """
        super().__init__(**params)

        # Rewards
        rewards = {} if rewards is None else rewards
        self.rewards = read_params(
            rewards,
            self.dft_rewards,
            name="rewards",
        )

        # Players
        if p_params is None:
            p_params = {}
        if bots is None:
            bots = []
        self._bots = bots
        self._players = [
            self.bot(index, **p_params)
            if player in bots
            else self.human(index, **p_params)

            for index, player in enumerate(range(self.players_n))
        ]

        # Status
        self._player = 0        # Current player
        self._over = False
        self._winners = set()   # Index of winner (can be a list of indexes)

        self.check_attributes()

    def check_attributes(self):
        """Raise ValueError if attributes are not consistent."""

        # Bot indexes
        for index in self._bots:
            if not (isinstance(index, int) and index >= 0):
                raise ValueError(
                    "Index of bot must be integer greater than 0, got %s"
                    % index
                )
            if index >= self.players_n:
                raise ValueError(
                    "Index (%s) of bot out of range, must be < %s"
                    % (index, self.players_n)
                )

    @property
    def players(self):
        """Return list of players."""
        return self._players

    @property
    def player(self):
        """Return current player."""
        return self.players[self._player]

    @property
    def winners(self):
        """Return list of winners."""
        return [
            player
            for player in self.players
            if player.index in self._winners
        ]

    def status(self):
        """Return status of game."""
        return {
            'player': self._player,
            'over': self._over,
            'winners': list(self._winners),
        }

    # ----------------------------------------------------------------------- #
    # Utils

    def av_actions(self):
        """Return available actions."""
        return self.actions

    def is_over(self):
        """Return whether game is over."""
        return self._over

    def new_winner(self, player):
        """Add player to list of winners.

        Args:
            player (int or player.Player)
        """
        if isinstance(player, int):
            self._winners.add(player)
        else:
            self._winners.add(player.index)

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

    def dft_consequences(self):
        """Return default consequences given the Game rewards."""
        if not self.is_over():
            return [
                self.rewards['neutral'] for _ in self.players
            ]
        elif not self.winners:
            return [
                self.rewards['tie'] for _ in self.players
            ]
        return [
            self.rewards['win']
            if player in self.winners
            else self.rewards['lose']
            for player in self.players
        ]

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

        if not self.winners:
            self.log.info("Tie Game")
        elif len(self.winners) == 1:
            self.log.info("Winner is %s" % self.winners[0])
        else:
            self.log.info("Winners are %s" % ", ".join(map(str, self.winners)))

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
        self._winners = set(status['winners'])

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
