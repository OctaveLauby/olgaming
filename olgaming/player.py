"""Skeleton for player object"""
from olgaming.gameobj import GameObject


class Player(GameObject):
    """Player skeleton."""

    def __init__(self, index, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.requires_visual = False
        self.last_observation = None

    def action(self, gstate, actions=None):
        """Return action of players.

        Args:
            gstate  (object):       current game state
            actions (list, opt):    possible actions

        Returns:
            (object) action
        """
        raise NotImplementedError

    def receive(self, msg_dict):
        """Receiving message dictionary (json frmt)."""
        self.log.debug("Receiving message : %s" % msg_dict)
        self.msg_dict_handler(msg_dict)

    def msg_dict_handler(self, msg_dict):
        """Manage incoming message."""

        # Read purpose of message
        try:
            verb = msg_dict['verb']
        except KeyError:
            err_msg = "Expecting 'verb' key in message to player"
            self.log.error(err_msg)
            raise KeyError(err_msg)

        # Check if a method exists to accomplish purpose
        try:
            handler = getattr(self, 'verb_' + verb)
        except AttributeError:
            err_msg = "Verb '%s' is not handled by player" % verb
            self.log.error(err_msg)
            raise ValueError(err_msg)

        # Gather content to accomplish purpose
        try:
            content = msg_dict['content']
        except KeyError:
            err_msg = "Expecting 'content' key in message to player"
            self.log.error(err_msg)
            raise KeyError(err_msg)

        return handler(content)

    def verb_observe(self, content):
        """Manage new observation of game."""
        self.last_observation = content

    def verb_reward(self, content):
        """Manage reward from game."""
        self.take(content)

    def take(self, consequence):
        """Nothing"""
        self.log.debug("Skip consequence %s", consequence)
