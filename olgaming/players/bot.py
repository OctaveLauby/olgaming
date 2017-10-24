"""Dummy bot player."""
import random

from gaming.player import Player


class Bot(Player):
    """Dummy Bot."""

    def action(self, gstate, actions=None):
        """Return random action."""
        action = random.choice(actions)
        self.log.debug("Pick %s for state %s", action, gstate)
        return action
