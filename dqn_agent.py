import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque


class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )

    def forward(self, x):
        return self.net(x)


class DQNAgent:

    def __init__(self, state_dim, actions):

        self.actions = actions
        self.action_dim = len(actions)
        self.state_dim = state_dim

        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.999

        self.lr = 0.001
        self.batch_size = 32

        self.memory = deque(maxlen=5000)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.q_net = QNetwork(state_dim, self.action_dim).to(self.device)
        self.target_net = QNetwork(state_dim, self.action_dim).to(self.device)

        self.target_net.load_state_dict(self.q_net.state_dict())

        self.optimizer = optim.Adam(self.q_net.parameters(), lr=self.lr)

        self.loss_fn = nn.MSELoss()

    def choose_action(self, state):

        if np.random.rand() < self.epsilon:
            idx = random.randrange(self.action_dim)
            return idx, self.actions[idx]

        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)

        with torch.no_grad():
            q_values = self.q_net(state)

        idx = torch.argmax(q_values).item()

        return idx, self.actions[idx]

    def store(self, state, action_idx, reward, next_state):

        self.memory.append((state, action_idx, reward, next_state))

    def train(self):

        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)

        states = torch.FloatTensor(np.array([b[0] for b in batch])).to(self.device)
        actions = torch.LongTensor([b[1] for b in batch]).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor([b[2] for b in batch]).unsqueeze(1).to(self.device)
        next_states = torch.FloatTensor(np.array([b[3] for b in batch])).to(self.device)

        q_values = self.q_net(states).gather(1, actions)

        with torch.no_grad():
            next_q = self.target_net(next_states).max(1)[0].unsqueeze(1)

        target = rewards + self.gamma * next_q

        loss = self.loss_fn(q_values, target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target(self):
        self.target_net.load_state_dict(self.q_net.state_dict())