import numpy as np
from market_ieee5 import MarketIEEE5


class ElectricityMarketEnv:

    def __init__(self, line_capacity=20):

        self.market = MarketIEEE5(line_capacity=line_capacity)

        self.actions = [1.0, 1.2, 1.4, 1.6]

        self.prev_lmp = 0
        self.prev_profit = 0
        self.prev_action = 1.0

    def reset(self):

        self.prev_lmp = 0
        self.prev_profit = 0
        self.prev_action = 1.0

        state = np.array([
            self.prev_lmp,
            self.prev_profit,
            self.prev_action
        ])

        return state

    def step(self, action_g0, action_g1):

        dispatch, lmps, profits = self.market.run({
            0: action_g0,
            1: action_g1
        })

        reward_g0 = profits[0]
        reward_g1 = profits[1]

        avg_lmp = np.mean(lmps)

        next_state = np.array([
            avg_lmp,
            reward_g0,
            action_g0
        ])

        done = False

        info = {
            "dispatch": dispatch,
            "lmps": lmps
        }

        return next_state, reward_g0, reward_g1, done, info