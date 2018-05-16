"""QLearner player.

Easy run script :

    import olgaming

    player_1 = olgaming.players.Qlearner(index=0)
    player_2 = olgaming.players.Qlearner(index=1)

    player_1.requires_visual = True
    player_2.requires_visual = True

    game = olgaming.games.TicTacToe(players=[player_1, player_2])

    game.play()
"""
import random

from olgaming.player import Player


class Qlearner(Player):
    """AI Player using simple qlearning."""

    dft_params = {
        'discount_factor': 0.95,
        'learning_rate': 0.001,
        'exploration_rate': 1,
        'exploration_decay': 0.995,
        'exploration_min': 0.01,
    }

    def __init__(self, *args, **kwargs):
        """Initialise a qlearner.

        Args:
            *args, **kwargs: arguments for olgaming.Player

        Additionnal kwargs:
            discount_factor       (float) : next qvalue factor in update
                (1 means next action qvalue is fully taken into account)
            learning_rate       (float) : update
                (1 means new value does not take previous one into acount)
            exploration_rate    (float) : exploration vs exploitation trade off
                (1 means full exploration)
            exploration_decay   (float) : decay of exploration rate
            exploration_min     (float) : minimum exploration rate
        """
        given_params = {
            param: kwargs.pop(param, None)
            for param in self.dft_params
        }
        super().__init__(*args, **kwargs)
        self.qvalue = {
            # ...
            # gstate_i : {
            #     ...
            #     action_j : qval_ij,
            #     ...
            # },
            # ...
        }
        self.params = dict(self.dft_params)
        self.params.update({
            param: value for param, value in given_params.items()
            if value is not None
        })
        self.memory = {
            'stacked_reward': 0,
            'lst_action': None,
            'lst_state': None,
            'new_action': None,
            'new_state': None,
        }
        self.log.debug("Player init with following params: %s" % self.params)

    # ---- Overridden methods

    def action(self, gstate, actions):
        """Return action to accomplish given the game state

        Trade off b/w exploration and exploitation.

        Args:
            gstate  (hashable): current game state
            actions (list):     available actions
        """
        self.consume_reward(gstate, actions)

        # If state not explored, create it in qvalue
        if gstate not in self.qvalue:
            self.init_state(gstate, actions)

        # Exploration vs exploitation
        if random.random() < self.params['exploration_rate']:
            action = self.random_action(actions)
        else:
            action = self.best_action(gstate, actions)
        self.memory['lst_action'] = action
        self.memory['lst_state'] = gstate
        return action

    def observe(self, game_descr):
        """Wait for end of game to consume last rewards."""
        if game_descr['status']['over']:
            self.consume_reward(gstate=None, actions=[])

    def take(self, consequence):
        """Stack consequence (= reward) pending the next reward consumption.

        This next reward consumption occurs when player has to play again or
        when game is over.
        """
        self.memory['stacked_reward'] += consequence

    # ---- Utils

    def best_action(self, gstate, actions):
        """Return best action given gstate, av. actions & current qvalue.

        Args:
            gstate  (hashable): current game state
            actions (list):     available actions
        """

        # Case when gstate hasn't been explore yet : random action
        if gstate not in self.qvalue:
            self.init_state(gstate, actions)
            return self.random_action(actions)

        # Otherwise : random action among actions with best qval
        bst_actions = []
        bst_qval = - float("inf")
        for action, qval in self.qvalue[gstate].items():
            if bst_qval < qval:
                bst_actions = [action]
                bst_qval = qval
            elif bst_qval == qval:
                bst_actions.append(action)
        return self.random_action(bst_actions)

    def consume_reward(self, gstate, actions):
        """Consume stacked reward.

        Args:
            gstate  (hashable): current game state
            actions (list):     available actions
        """

        # If not lst_action, no reward to consume
        if self.memory['lst_action'] is None:
            self.log.debug("No reward to consume")
            return

        # Evaluate incoming reward
        # # If gstate is None, it means game is over => no next action
        if gstate is None:
            next_reward = 0
        else:
            next_action = self.best_action(gstate, actions)
            next_reward = self.qvalue[gstate][next_action]

        # Apply formula
        lst_state = self.memory['lst_state']
        lst_action = self.memory['lst_action']
        update = (
            self.params['learning_rate'] * (
                self.memory['stacked_reward']
                + (
                    self.params['discount_factor']
                    * next_reward
                )
                - self.qvalue[lst_state][lst_action]
            )
        )
        self.qvalue[lst_state][lst_action] += update

        # Reset stacked reward
        self.memory['stacked_reward'] = 0

    def init_state(self, gstate, actions):
        """Init gstate with associated actions."""
        self.qvalue[gstate] = {
            action: 0
            for action in actions
        }

    def random_action(self, actions):
        """Return a random action among the available ones."""
        return random.choice(actions)
