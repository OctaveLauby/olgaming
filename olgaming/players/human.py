"""Simple human player."""
from olgaming.player import Player


class Human(Player):
    """Simple Human."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requires_visual = True

    def action(self, gstate, actions=None):
        """Ask action in inputs."""
        action = input("> %s action ? " % self)
        self.log.debug("Pick %s for state %s", action, gstate)
        return action
