"""Candid player: play for action available."""
from olgaming.player import Player


class Candid(Player):
    """Straight forward player, play first action available.

    Also remember all consequences.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consequences = []

    def action(self, gstate, actions):
        """Return first action available."""
        self.log.debug("Picking among actions %s" % actions)
        return actions[0]

    def take(self, consequence):
        """Memorize consequences."""
        self.consequences.append(consequence)
