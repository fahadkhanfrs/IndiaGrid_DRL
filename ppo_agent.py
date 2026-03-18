import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


class ActorCritic(nn.Module):
    def __init__(self, state_dim):
        super().__init__()

        self.shared = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Tanh()
        )

        # actor
        self.mu = nn.Linear(64, 1)
        self.log_std = nn.Parameter(torch.zeros(1))

        # critic
        self.value = nn.Linear(64, 1)

    def forward(self, x):
        x = self.shared(x)

        mu = self.mu(x)
        std = torch.exp(self.log_std)

        value = self.value(x)

        return mu, std, value


class PPOAgent:

    def __init__(self, state_dim):

        self.model = ActorCritic(state_dim)
        self.optimizer = optim.Adam(self.model.parameters(), lr=3e-4)

        self.gamma = 0.99
        self.clip = 0.2

    def select_action(self, state):

        state = torch.FloatTensor(state).unsqueeze(0)

        with torch.no_grad():
            mu, std, _ = self.model(state)

        dist = torch.distributions.Normal(mu, std)

        action = dist.sample()
        log_prob = dist.log_prob(action)

        # clamp to valid bid range
        action = torch.clamp(action, 1.0, 2.0)

        return action.item(), log_prob.item()

    def compute_returns(self, rewards):

        returns = []
        G = 0

        for r in reversed(rewards):
            G = r + self.gamma * G
            returns.insert(0, G)

        return torch.FloatTensor(returns)

    def update(self, states, actions, log_probs, rewards):

        states = torch.FloatTensor(np.array(states))
        actions = torch.FloatTensor(actions).unsqueeze(1)
        old_log_probs = torch.FloatTensor(log_probs).unsqueeze(1)

        returns = self.compute_returns(rewards).unsqueeze(1)

        mu, std, values = self.model(states)

        dist = torch.distributions.Normal(mu, std)
        new_log_probs = dist.log_prob(actions)

        ratio = torch.exp(new_log_probs - old_log_probs)

        advantage = returns - values.detach()

        surr1 = ratio * advantage
        surr2 = torch.clamp(ratio, 1 - self.clip, 1 + self.clip) * advantage

        actor_loss = -torch.min(surr1, surr2).mean()
        critic_loss = nn.MSELoss()(values, returns)

        loss = actor_loss + 0.5 * critic_loss

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()