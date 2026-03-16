import numpy as np
import torch
print("Using device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")

from electricity_env import ElectricityMarketEnv
from dqn_agent import DQNAgent


env = ElectricityMarketEnv(line_capacity=20)

actions = [1.0, 1.2, 1.4, 1.6]

agent = DQNAgent(state_dim=3, actions=actions)

episodes = 100
steps_per_episode = 50

for ep in range(episodes):

    state = env.reset()

    total_reward = 0

    for t in range(steps_per_episode):

        action_idx, action = agent.choose_action(state)

        # opponent fixed strategy (baseline)
        opponent_action = 1.2

        next_state, r0, r1, done, info = env.step(action, opponent_action)

        agent.store(state, action_idx, r0, next_state)

        agent.train()

        state = next_state

        total_reward += r0

    if ep % 20 == 0:
        agent.update_target()

    print(f"Episode {ep} | Reward {total_reward:.2f} | epsilon {agent.epsilon:.3f}")

state = env.reset()

for _ in range(10):

    idx, action = agent.choose_action(state)

    print("Chosen bid:", action)

    state, r0, r1, done, info = env.step(action, 1.2)