import numpy as np
from electricity_env import ElectricityMarketEnv
from dqn_agent import DQNAgent


env = ElectricityMarketEnv(line_capacity=20)

actions = [1.0, 1.2, 1.4, 1.6]

agent0 = DQNAgent(state_dim=3, actions=actions)
agent1 = DQNAgent(state_dim=3, actions=actions)

episodes = 100
steps_per_episode = 50


for ep in range(episodes):

    state = env.reset()

    total_r0 = 0
    total_r1 = 0

    for t in range(steps_per_episode):

        idx0, a0 = agent0.choose_action(state)
        idx1, a1 = agent1.choose_action(state)

        next_state, r0, r1, done, info = env.step(a0, a1)

        agent0.store(state, idx0, r0, next_state)
        agent1.store(state, idx1, r1, next_state)

        agent0.train()
        agent1.train()

        state = next_state

        total_r0 += r0
        total_r1 += r1

    if ep % 20 == 0:
        agent0.update_target()
        agent1.update_target()

    if ep % 10 == 0:
     print("Example bids:", a0, a1)

    print(
        f"Episode {ep} | "
        f"G0 reward {total_r0:.2f} | "
        f"G1 reward {total_r1:.2f} | "
        f"eps0 {agent0.epsilon:.3f} | "
        f"eps1 {agent1.epsilon:.3f}"
    )