import numpy as np
from market_dcopf import MarketDCOPF

class VREAgent:
    def __init__(self, actions, temperature=0.1, forgetting=0.01):
        self.actions = actions
        self.temperature = temperature
        self.forgetting = forgetting

        self.q =np.ones(len(actions)) # equal propensities initialization

    def softmax_probs(self):
        z = self.q / self.temperature
        z = z - np.max(z) # prevent overflow, numerical stability
        exp_z = np.exp(z)
        return exp_z / np.sum(exp_z)
    
    def select_action(self):
        probs = self.softmax_probs()
        idx = np.random.choice(len(self.actions), p=probs)
        return idx, self.actions[idx], probs
    
    def update(self, action_idx, reward):
        # forgetting
        self.q = (1 - self.forgetting) * self.q
        # normalize reward
        scaled_reward = reward / (1 + abs(reward))
        # reinforce chosen action
        self.q[action_idx] += scaled_reward
        # experimentation bias
        epsilon = 0.05
        self.q += epsilon * np.mean(self.q)

def run_vre_learning(
        n_days=50,
        actions=[1.0, 1.2, 1.4, 1.6],
        temperature=0.2
    ):
        agent = VREAgent(actions=actions, temperature=temperature)
        
        history = {
            "day": [],
            "action": [],
            "profit": [],
            "lmp_bus1": [],
            "lmp_bus2": [],
        }

        for day in range(n_days):
            # agent chooses bid multiplier
            a_idx, multiplier, probs = agent.select_action()

            # building market with chosen bid
            market = MarketDCOPF(line_capacity=0.6)
            market.build_network(reported_cost_multipliers={
                0: multiplier, # learning agent
                1: 1.0})

            dispatch, lmps, profits = market.run()

            reward = profits[0]
            agent.update(a_idx, reward)
            #agent.temperature = max(0.1, agent.temperature * 0.99)

            history["day"].append(day)
            history["action"].append(multiplier)
            history["profit"].append(reward)
            history["lmp_bus1"].append(lmps[0])
            history["lmp_bus2"].append(lmps[1])

            print(
                f"Day {day:02d} | "
                f"Action={multiplier:.2f} | "
                f"Profit={reward:.2f} | "
                f"LMPs=({lmps[0]:.2f}, {lmps[1]:.2f})"
            )

        return history

def run_vre_colearning(
        n_days=60,
        actions=[1.0, 1.2, 1.4, 1.6],
        temperature=1.0
):
        agent0 = VREAgent(actions=actions, temperature=temperature)
        agent1 = VREAgent(actions=actions, temperature=temperature)

        history = { # record history for both agents
            "day": [],
            "action_g0": [],
            "action_g1": [],
            "profit_g0": [],    
            "profit_g1": [],
            "lmp_bus1": [],
            "lmp_bus2": [],
        }

        for day in range(n_days):
            # agents choose bid multipliers
            a0_idx, m0, _ = agent0.select_action()
            a1_idx, m1, _ = agent1.select_action()

            # building market with chosen bids
            market = MarketDCOPF(line_capacity=0.35)
            market.build_network(reported_cost_multipliers={
                0: m0, # learning agent 0
                1: m1  # learning agent 1
            })

            dispatch, lmps, profits = market.run()

            r0 = profits[0]
            r1 = profits[1]
            agent0.update(a0_idx, r0)
            agent1.update(a1_idx, r1)

            history["day"].append(day)
            history["action_g0"].append(m0)
            history["action_g1"].append(m1)
            history["profit_g0"].append(r0)
            history["profit_g1"].append(r1)
            history["lmp_bus1"].append(lmps[0])
            history["lmp_bus2"].append(lmps[1])

            print(
                f"Day {day:02d} | "
                f"Action_G0={m0:.2f} | "
                f"Profit_G0={r0:.2f} | "
                f"Action_G1={m1:.2f} | "
                f"Profit_G1={r1:.2f} | "
                f"LMPs=({lmps[0]:.2f}, {lmps[1]:.2f})"
            )

            agent0.temperature = max(0.1, agent0.temperature * 0.995)
            agent1.temperature = max(0.1, agent1.temperature * 0.995)

        return history