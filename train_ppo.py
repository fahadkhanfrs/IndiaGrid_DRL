from electricity_env import ElectricityMarketEnv
from ppo_agent import PPOAgent


env = ElectricityMarketEnv(line_capacity=20)

agent = PPOAgent(state_dim=3)

episodes = 200
steps_per_episode = 50


for ep in range(episodes):

    state = env.reset()

    states = []
    actions = []
    log_probs = []
    rewards = []

    total_reward = 0

    for t in range(steps_per_episode):

        action, log_prob = agent.select_action(state)

        opponent_action = 1.2   # keep simple first

        next_state, r0, r1, done, info = env.step(action, opponent_action)

        states.append(state)
        actions.append(action)
        log_probs.append(log_prob)
        rewards.append(r0)

        state = next_state
        total_reward += r0

    agent.update(states, actions, log_probs, rewards)

    print(f"Episode {ep} | Reward {total_reward:.2f}")