"""Skeleton for player object"""
from gaming.gameobj import GameObject


class Player(GameObject):
    """Player skeleton."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.requires_visual = False

    def action(self, gstate, actions=None):
        """Return action of players.

        Args:
            gstate  (object):       current game state
            actions (list, opt):    possible actions

        Returns:
            (object) action
        """
        raise NotImplementedError

    def take(self, consequence):
        """Nothing"""
        self.log.debug("Skip consequence %s", consequence)
