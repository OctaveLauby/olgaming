"""Skeleton for player object"""
from olgaming.gameobj import GameObject


class Player(GameObject):
    """Player skeleton.

    Methods to override:
        - action
        - (opt) observe
        - (opt) take
    """
    def __init__(self, index, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.requires_visual = False
        self.last_observation = None
        self.last_reward = None

    def action(self, gstate, actions=None):
        """Return action of players.

        Args:
            gstate  (object):       current game state
            actions (list, opt):    possible actions

        Returns:
            (object) action
        """
        raise NotImplementedError

    def observe(self, game_descr):
        """Remember last game description.

        Args:
            content (dict): game description
                {
                    'status': {
                        'over': <bool>,
                        'player': <int>,
                        'winners': <list>
                    },
                    'state': game_state,
                }
        """
        self.last_observation = game_descr

    def take(self, consequence):
        """Remember last reward."""
        self.last_reward = consequence

    # ----------------------------------------------------------------------- #
    # Communication assets

    def receive(self, msg_dict):
        """Receiving message dictionary (json frmt)."""
        self.log.debug("Receiving message : %s" % msg_dict)

        if not isinstance(msg_dict, dict):
            err_msg = "Message to player must be a dictionary"
            self.log.fatal("Message to player must be a dictionary")
            raise TypeError(err_msg)

        return self.msg_dict_handler(msg_dict)

    def msg_dict_handler(self, msg_dict):
        """Manage incoming message."""

        # Read purpose of message
        try:
            verb = msg_dict['verb']
        except KeyError:
            err_msg = "Expecting 'verb' key in message to player"
            self.log.fatal(err_msg)
            raise KeyError(err_msg)

        # Check if a method exists to accomplish purpose
        try:
            handler = getattr(self, 'verb_' + verb)
        except AttributeError:
            err_msg = "Verb '%s' is not handled by player" % verb
            self.log.fatal(err_msg)
            raise ValueError(err_msg)

        # Gather content to accomplish purpose
        try:
            content = msg_dict['content']
        except KeyError:
            err_msg = "Expecting 'content' key in message to player"
            self.log.fatal(err_msg)
            raise KeyError(err_msg)

        return handler(content)

    def verb_act(self, content):
        """Manage game state to suggest an action.

        Args:
            content (dict): kwargs of self.action method

        Returns:
            Next action
        """
        return self.action(**content)

    def verb_observe(self, content):
        """Manage new observation of game."""
        self.observe(game_descr=content)

    def verb_reward(self, content):
        """Manage reward from game."""
        self.take(content)
