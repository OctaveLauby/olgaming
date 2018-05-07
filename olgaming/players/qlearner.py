"""QLearner player."""
import random

from olgaming.player import Player


class Memory(object):
    def __init__(self, max_size):
        self.content = []
        self.max_size = max_size

    def append(self, item):
        self.content.append(item)
        if len(self.content) > self.max_size:
            self.content = self.content[1:]

    def last(self):
        return self.content[-1]


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
        self.memory = Memory(max_size=1)

    # ---- Overwritten methods

    def action(self, gstate, actions):
        if gstate not in self.qvalue:
            self.qvalue[gstate] = {
                action: 0
                for action in actions
            }
        if random.random() < self.params['exploration_rate']:
            action = self.random_action(actions)
        else:
            action = self.best_action(gstate, actions)
        self.memory.append((gstate, action))
        return action

    def take(self, consequence):
        """"""
        lst_state, lst_action = self.memory.last()
        update = (
            self.params['learning_rate'] * (
                consequence
                + (
                    self.params['discount_rate']
                    * self.qvalues[next_state][next_action]
                )
                - self.qvalues[lst_state][lst_action]
            )
        )
        self.qvalues[lst_state][lst_action] += update

    # ---- Utils

    def best_action(self, gstate, best_action):
        bst_action = None
        bst_qval = - float("inf")
        for action, qval in self.qvalue[gstate].items():
            if bst_qval < qval:
                bst_action = action
                bst_qval = qval
        return bst_action

    def random_action(self, actions):
        return random.choice(actions)
