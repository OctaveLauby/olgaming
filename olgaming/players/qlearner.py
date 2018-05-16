"""QLearner player."""
import random

from olgaming.player import Player


class Qlearner(Player):
    """AI Player using simple qlearning."""

    dft_params = {
        'discount_rate': 0.95,
        'learning_rate': 0.001,
        'exploration_rate': 1,
        'exploration_decay': 0.995,
        'exploration_min': 0.01,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requires_visual = False
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
        self.memory = {
            'stacked_reward': 0,
            'lst_action': None,
            'lst_state': None,
            'new_action': None,
            'new_state': None,
        }

    # ---- Overridden methods

    def action(self, gstate, actions):
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

    def take(self, consequence):
        self.memory['stacked_reward'] += consequence

    # ---- Utils

    def best_action(self, gstate, actions):
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
        if self.memory['lst_action'] is None:
            self.log.debug("No reward to consume")
            return

        lst_state = self.memory['lst_state']
        lst_action = self.memory['lst_action']
        next_action = self.best_action(gstate, actions)

        update = (
            self.params['learning_rate'] * (
                self.memory['stacked_reward']
                + (
                    self.params['discount_rate']
                    * self.qvalue[gstate][next_action]
                )
                - self.qvalue[lst_state][lst_action]
            )
        )
        self.qvalue[lst_state][lst_action] += update

        self.memory['stacked_reward'] = 0

    def init_state(self, gstate, actions):
        self.qvalue[gstate] = {
            action: 0
            for action in actions
        }

    def random_action(self, actions):
        return random.choice(actions)
