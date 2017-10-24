"""Dummy Game.

Conversation between the 2 players.
"""
from olgaming.game import Game, InvalidAction


class Dummy(Game):
    """Conversation Game.

    Game is over when one of the player says bye.
    """
    actions = {
        "1": "hi",
        "2": "bye",
        "3": "i am a cow",
        "4": "i am a monkey",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg_n = 0

    # ----------------------------------------------------------------------- #
    # Utils

    def av_actions(self):
        """Return available actions."""
        return list(Dummy.actions.keys())

    def refresh(self):
        """Refresh status of game"""
        pass

    def state(self):
        """Return current game state."""
        return {"msg_sent": self.msg_n}

    # ----------------------------------------------------------------------- #
    # Gameplay

    def act(self, action):
        """Operate action (as current player).

        Returns:
            (list): consequences for each player
        """
        # Check action
        try:
            msg = Dummy.actions[action]
        except KeyError:
            raise InvalidAction(action)

        # Display Message
        print("%s : %s" % (self.player, msg))

        # Update environment
        self.msg_n += 1
        if msg == "bye":
            self.raise_endflag()

        # Return consequences
        return [
            "<s>%s</s>" % msg           # Message sent
            if player is self.player
            else "<r>%s</r>" % msg      # Message received

            for player in self.players
        ]

    # ----------------------------------------------------------------------- #
    # Display

    def display(self):
        """Display game."""
        print("# This is a dummy game.")
        print("# Available option are: %s" % ", ".join(Dummy.actions.keys()))
